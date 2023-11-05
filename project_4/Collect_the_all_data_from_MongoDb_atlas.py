#import libraries
import pymongo
import pandas as pd

# connect to the mongo client -->db--->col
client=pymongo.MongoClient("mongodb+srv://thanalakshmi:thanam@cluster0.5jj0you.mongodb.net/?retryWrites=true&w=majority")
db=client['sample_airbnb']
col=db['listingsAndReviews']

# collect the data of primary 
def airbnb():
        data = []
        for i in col.find({}, {'_id': 1, 'listing_url': 1, 'name': 1, 'property_type': 1, 'room_type': 1, 'bed_type': 1,
                                               'minimum_nights': 1, 'maximum_nights': 1, 'cancellation_policy': 1, 'accommodates': 1,
                                               'bedrooms': 1, 'beds': 1, 'number_of_reviews': 1, 'bathrooms': 1, 'price': 1,
                                               'cleaning_fee': 1, 'extra_people': 1, 'guests_included': 1, 'images.picture_url': 1,
                                               'review_scores.review_scores_rating': 1}):
            data.append(i)
            df= pd.DataFrame(data)

            # data cleaning
            df['images'] = df['images'].apply(lambda x: x['picture_url'])
            df['review_scores'] = df['review_scores'].apply( lambda x:x.get('review_scores_rating'))
            df['review_scores'].fillna(0,inplace=True)
            df['bedrooms'].fillna(0, inplace=True)
            df['beds'].fillna(0, inplace=True)
            df['bathrooms'].fillna(0, inplace=True)
            df['cleaning_fee'].fillna('Not Specified', inplace=True)

             # type conversion
            df['minimum_nights'] = df['minimum_nights'].astype(int)
            df['maximum_nights'] = df['maximum_nights'].astype(int)
            df['bedrooms'] = df['bedrooms'].astype(int)
            df['beds'] = df['beds'].astype(int)
            df['bathrooms'] = df['bathrooms'].astype(str).astype(float)
            df['price'] = df['price'].astype(str).astype(float).astype(int)
            df['cleaning_fee'] = df['cleaning_fee'].apply(lambda x: int(float(str(x))) if x != 'Not Specified' else 'Not Specified')
            df['extra_people'] = df['extra_people'].astype(str).astype(float).astype(int)
            df['guests_included'] = df['guests_included'].astype(str).astype(int)
        return df

# collect the data of host
def host():
        host = []
        for i in col.find({}, {'_id': 1, 'host': 1}):
            host.append(i)

        df_host = pd.DataFrame(host)
        host_keys = list(df_host.iloc[0, 1].keys())    # _id : 0 index , host : 1 index---->get keys
        host_keys.remove('host_about')

        # make nested dictionary to separate columns
        for i in host_keys:
            if i == 'host_response_time':
                df_host['host_response_time'] = df_host['host'].apply(
                    lambda x: x['host_response_time'] if 'host_response_time' in x else 'Not Specified')
            else:
                df_host[i] = df_host['host'].apply(
                    lambda x: x[i] if i in x and x[i] != '' else 'Not Specified')

        df_host.drop(columns=['host'], inplace=True)

        # data type conversion
        df_host['host_is_superhost'] = df_host['host_is_superhost'].map(
            {False: 'No', True: 'Yes'})
        df_host['host_has_profile_pic'] = df_host['host_has_profile_pic'].map(
            {False: 'No', True: 'Yes'})
        df_host['host_identity_verified'] = df_host['host_identity_verified'].map(
            {False: 'No', True: 'Yes'})

        return df_host

# collect the data of address
def address():
        address = []
        for i in col.find({}, {'_id': 1, 'address': 1}):
            address.append(i)

        df_address = pd.DataFrame(address)
        address_keys = list(df_address.iloc[0, 1].keys())

        # nested dicionary to separate columns
        for i in address_keys:
            if i == 'location':
                df_address['location_type'] = df_address['address'].apply(
                    lambda x: x['location']['type'])
                df_address['longitude'] = df_address['address'].apply(
                    lambda x: x['location']['coordinates'][0])
                df_address['latitude'] = df_address['address'].apply(
                    lambda x: x['location']['coordinates'][1])
                df_address['is_location_exact'] = df_address['address'].apply(
                    lambda x: x['location']['is_location_exact'])
            else:
                df_address[i] = df_address['address'].apply(
                    lambda x: x[i] if x[i] != '' else 'Not Specified')

        df_address.drop(columns=['address'], inplace=True)

        # bool data conversion to string
        df_address['is_location_exact'] = df_address['is_location_exact'].map(
            {False: 'No', True: 'Yes'})
        return df_address

# collect the data of availability
def availability():
        availability = []
        for i in col.find({}, {'_id': 1, 'availability': 1}):
            availability.append(i)

        df_availability = pd.DataFrame(availability)
        availability_keys = list(df_availability.iloc[0, 1].keys())

        # nested dicionary to separate columns
        for i in availability_keys:
            df_availability['availability_30'] = df_availability['availability'].apply(
                lambda x: x['availability_30'])
            df_availability['availability_60'] = df_availability['availability'].apply(
                lambda x: x['availability_60'])
            df_availability['availability_90'] = df_availability['availability'].apply(
                lambda x: x['availability_90'])
            df_availability['availability_365'] = df_availability['availability'].apply(
                lambda x: x['availability_365'])

        df_availability.drop(columns=['availability'], inplace=True)
        return df_availability

# sort the amenities
def amenities_sort(x):
        a = x
        a.sort(reverse=False)
        return a

# collect the data of amenities
def amenities():
        amenities = []
        for i in col.find({}, {'_id': 1, 'amenities': 1}):
            amenities.append(i)

        df_amenities = pd.DataFrame(amenities)

        # sort the list of amenities
        df_amenities['amenities'] = df_amenities['amenities'].apply(
            lambda x:amenities_sort(x))
        return df_amenities

# merge the all dataframe
def merge_dataframe():
        df_1 =airbnb()
        df_host =host()
        df_address =address()
        df_availability =availability()
        df_amenities = amenities()

        df = pd.merge(df_1, df_host, on='_id')
        df = pd.merge(df, df_address, on='_id')
        df = pd.merge(df, df_availability, on='_id')
        df = pd.merge(df, df_amenities, on='_id')

        return df

m_df=merge_dataframe()

# csv file save 
m_df.to_csv('airbnb.csv', index=False, header=True)




