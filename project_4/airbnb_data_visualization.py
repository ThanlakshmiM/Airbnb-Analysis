import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import base64
import seaborn as sns
import plotly.express as px
from PIL import Image 

pd.set_option('display.max_columns', None)

# page configuration
st.set_page_config(page_title= "Airbnb Data Visualization | By Thana Lakshmi",
                   page_icon= "random",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Thana Lakshmi*!
                                        Data has been gathered from mongodb atlas"""}
                  )

def image_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpeg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
image_local(r'C:\Users\user\Desktop\python\project_4\background_clr.jpeg')    

# title and position
st.markdown(f'<h1 style="text-align: center;">Airbnb Analysis</h1>',
                unsafe_allow_html=True)

option= option_menu(menu_title = None,
                         options = ["Home","Overview","Explore","About"],
                         icons =["image", "pencil-fill", 'exclamation-diamond'],
                         default_index=0,
                         orientation="horizontal",
                         styles={"container": {"padding": "0!important", "background-color": "white","size":"cover", "width": "100%"},
                                "icon": {"color": "black", "font-size": "20px"},
                                "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
                                "nav-link-selected": {"background-color": "#6F36AD"}})


data = pd.read_csv(r'C:\Users\user\Desktop\python\project_4\airbnb.csv')

def get_profile_pic():
     return Image.open(r'C:\Users\user\Desktop\python\project_4\analysis.png')

def main():

  # SIDEBAR

  st.sidebar.image(get_profile_pic(), use_column_width=False, width=250)
  st.sidebar.header("Welcome!")

  st.sidebar.markdown(" ")
  st.sidebar.markdown("*I am a Data Science enthusiast with interest in Python, Machine Learning, Data Analysis.*")
  st.sidebar.markdown("**Author**: Thanalakshmi")
  st.sidebar.markdown("**Mail**: thanalakshmi7558@gmail.com")

  st.sidebar.markdown("- [Linkedin](https://www.linkedin.com/in/thanalakshmi-m-7633ba235/)")
  st.sidebar.markdown("- [Github](https://github.com/ThanlakshmiM)")

  

# HOME PAGE
if option == "Home":
           
    col1,col2=st.columns(2,gap='medium')

    col1.markdown("### :blue[Domain] : 👉Travel Industry, Property Management and Tourism")
    col1.markdown("### :blue[Technologies used] :👉 Python, Pandas, Plotly, Streamlit, MongoDB")
    col1.markdown("### :blue[Overview] : 👉To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
    
    airbnb=Image.open(r'C:\Users\user\Desktop\python\project_4\airbnb1.jfif')
    st.markdown("#   ")
    st.markdown("#   ")
    col2.image(airbnb)

if option == "Overview":
    st.markdown("$\huge🚀 INSIGHTS $")

    
    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country',sorted(data["country"].unique()),sorted(data["country"].unique()))
    prop = st.sidebar.multiselect('Select Property_type',sorted(data["property_type"].unique()),sorted(data["property_type"].unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(data["room_type"].unique()),sorted(data["room_type"].unique()))
    price = st.slider('Select Price',data["price"].min(),data["price"].max(),(data['price'].min(),data['price'].max()))
    


    # CONVERTING THE USER INPUT INTO QUERY
    query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'
        
    # CREATING COLUMNS
    col1,col2 = st.columns(2,gap='medium')
        
    with col1:
            
    # TOP 10 PROPERTY TYPES BAR CHART
        df1 = data.query(query).groupby(["property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
        fig = px.bar(df1,
                    title='Top 10 Property Types',
                         x='Listings',
                         y='property_type',
                         orientation='h',
                         color='property_type',
                         color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True) 

         
         # MOST RATED HOSTS #

        st.header("Most rated hosts")

        st.set_option('deprecation.showPyplotGlobalUse', False)
        ranked = data.query(query).groupby(['host_name'])['number_of_reviews'].count().sort_values(ascending=False).reset_index()
        ranked = ranked.head(5)
        sns.set_style("whitegrid")
        fig = sns.barplot(y='host_name', x='number_of_reviews', data=ranked,palette="Blues_d")
        fig.set_xlabel("Nº de Reviews",fontsize=10)
        fig.set_ylabel("Host",fontsize=10)

        st.pyplot()

        st.write(f"""The host **{ranked.iloc[0].host_name}** is at the top with {ranked.iloc[0].number_of_reviews} reviews.
        **{ranked.iloc[1].host_name}** is second with {ranked.iloc[1].number_of_reviews} reviews. It should also be noted that reviews are not positive or negative reviews, but a count of feedbacks provided for the accommodation.""")


    with col2:
            
            # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
            df1 = data.query(query).groupby(["room_type"]).size().reset_index(name="counts")
            fig = px.pie(df1,
                         title='Total Listings in each Room_types',
                         names='room_type',
                         values='counts',
                         color_discrete_sequence=px.colors.sequential.Rainbow
                        )
            fig.update_traces(textposition='outside', textinfo='value+label')
            st.plotly_chart(fig,use_container_width=True)
            
            # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
            country_df = data.query(query).groupby(['country'],as_index=False)['host_total_listings_count'].count()
            fig = px.choropleth(country_df,
                                title='Total Listings in each Country',
                                locations='country',
                                locationmode='country names',
                                color='host_total_listings_count',
                                color_continuous_scale=px.colors.sequential.Plasma
                               )
            st.plotly_chart(fig,use_container_width=True)


    # EXPLORE PAGE
if option == "Explore":
    st.markdown("## Explore more about the Airbnb data")
    
    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country',sorted(data['country'].unique()),sorted(data['country'].unique()))
    prop = st.sidebar.multiselect('Select Property_type',sorted(data['property_type'].unique()),sorted(data['property_type'].unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(data['room_type'].unique()),sorted(data['room_type'].unique()))
    price = st.slider('Select Price',data['price'].min(),data['price'].max(),(data['price'].min(),data['price'].max()))
    
    # CONVERTING THE USER INPUT INTO QUERY
    query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'
    
    # HEADING 1
    st.markdown("## Price Analysis")
    
    # CREATING COLUMNS
    col1,col2 = st.columns(2,gap='medium')
    
    with col1:
        
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = data.query(query).groupby('room_type',as_index=False)['price'].mean().sort_values(by='price')
        fig = px.bar(data_frame=pr_df,
                     x='room_type',
                     y='price',
                     color='price',
                     title='Avg Price in each Room type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
        # HEADING 2
        st.markdown("## Availability Analysis")
        
        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = px.box(data_frame=data.query(query),
                     x='room_type',
                     y='availability_365',
                     color='room_type',
                     title='availability by room_type'
                    )
        st.plotly_chart(fig,use_container_width=True)

        # REVIEWS ANALYIS #

        st.header("Reviews Analysis")
        st.markdown(" In this scatter plot of show in rooms type based reviews order by host name. ")

        fig = px.scatter(data_frame=data.query(query), x="host_name", y="number_of_reviews", color="room_type")
        fig.update_yaxes(title="Nª Reviews")
        fig.update_xaxes(title="host name")
        st.plotly_chart(fig,use_container_width=True)


        # BLANK SPACE
        st.markdown("#   ")
        st.markdown("#   ")
        st.markdown(" In this scatter plot show in number of revies based on host neighbourhood in oder by host names.")
        fig = px.scatter(data_frame=data.query(query), x="host_name", y="number_of_reviews", color="host_neighbourhood")
        fig.update_yaxes(title="Nª Reviews")
        fig.update_xaxes(title="host name")
        st.plotly_chart(fig,use_container_width=True)

        
    with col2:
        
        # AVG PRICE IN COUNTRIES SCATTERGEO
        country_df = data.query(query).groupby('country',as_index=False)['price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='country',
                                       color= 'price', 
                                       hover_data=['price'],
                                       locationmode='country names',
                                       size='price',
                                       title= 'Avg Price in each Country',
                                       color_continuous_scale='agsunset'
                            )
        col2.plotly_chart(fig,use_container_width=True)
        
        # BLANK SPACE
        st.markdown("#   ")
        st.markdown("#   ")
        
        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = data.query(query).groupby('country',as_index=False)['availability_365'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='country',
                                       color= 'availability_365', 
                                       hover_data=['availability_365'],
                                       locationmode='country names',
                                       size='availability_365',
                                       title= 'Avg Availability in each Country',
                                       color_continuous_scale='agsunset'
                            )
        st.plotly_chart(fig,use_container_width=True)
        
        
        st.header("Most Rated Listings")
        st.markdown("We can slide to filter a range of numbers in the sidebar to view properties whose review count falls in that range.")

        reviews = st.slider('', 0, 12000, (100))

        data.query(f"number_of_reviews<={reviews}").sort_values("number_of_reviews", ascending=False)\
        .head(50)[["number_of_reviews", "price", 'host_neighbourhood', "room_type", "host_name"]]

        st.write("654 is the highest number of reviews and only a single property has it. In general, listings with more than 400 reviews are priced below $ 100,00. Some are between $100,00 and $200,00, and only one is priced above $200,00.")

        fig = px.scatter_geo(data_frame=data.query(query),
                                       locations='country',
                                       color="number_of_reviews" , 
                                       hover_data=["number_of_reviews"],
                                       locationmode='country names',
                                       size="number_of_reviews",
                                       title= 'Reviews in each Country',
                                       color_continuous_scale='agsunset'
                            )
        col2.plotly_chart(fig,use_container_width=True)        
        

if option == "About":
        df = data

        st.title("My Tableau URL Link")
        st.markdown("- [Click & Check to view my Dashboard](https://public.tableau.com/app/profile/thanalakshmi.m1863/viz/MyDashboard1_16990939186760/Dashboard1?publish=yes)")
        st.title("Airbnb listings Data Analysis")
        st.markdown('-----------------------------------------------------')

        st.markdown("*Through Airbnb data we will conduct an exploratory analysis and offer insights into that data. For this we will use the data behind the website **Inside Airbnb** come from publicly available information on the Airbnb website available [here](http://insideairbnb.com/), containing advertisements for accommodation in NY until 2020*")


        st.header("Summary")

        st.markdown("Airbnb is a platform that provides and guides the opportunity to link two groups - the hosts and the guests. Anyone with an open room or free space can provide services on Airbnb to the global community. It is a good way to provide extra income with minimal effort. It is an easy way to advertise space, because the platform has traffic and a global user base to support it. Airbnb offers hosts an easy way to monetize space that would be wasted.")

        st.markdown("On the other hand, we have guests with very specific needs - some may be looking for affordable accommodation close to the city's attractions, while others are a luxury apartment by the sea. They can be groups, families or local and foreign individuals. After each visit, guests have the opportunity to rate and stay with their comments. We will try to find out what contributes to the listing's popularity and predict whether the listing has the potential to become one of the 100 most reviewed accommodations based on its attributes.")

        st.markdown('-----------------------------------------------------')

        st.header("Airbnb Data: Data Analysis")
        st.markdown("Following is presented the first 10 records of Airbnb data. These records are grouped along 50 columns with a variety of informations as host name, price, room type, minimum of nights,reviews and reviews per month.")
        st.markdown("We will start with familiarizing ourselves with the columns in the dataset, to understand what each feature represents. This is important, because a poor understanding of the features could cause us to make mistakes in the data analysis and the modeling process. We will also try to reduce number of columns that either contained elsewhere or do not carry information that can be used to answer our questions.")

        st.dataframe(df.head(10))

        st.markdown("Another point about our data is that it allows sorting the dataframe upon clicking any column header, it a more flexible way to order data to visualize it.")


        st.header("Conclusions")

        st.markdown("Through this exploratory data analysis and visualization project, we gained several interesting insights into the Airbnb rental market. Below we will summarise the answers to the questions that we wished to answer at the beginning of the project:")

        st.markdown("**How do prices of listings vary by location? What localities in Countries are rated highly by guests?** Manhattan has the most expensive rentals compared to the other boroughs. Prices are higher for rentals closer to city hotspots. Rentals that are rated highly on the location by the host also have higher prices")

        
        st.header("Limitations")

        st.markdown(" - We did not have data for past years and hence could not compare current rental trends with past trends. Hence, there was an assumption made, particularly in the demand and supply section of the report to understand the booking trends.")

        # FOOTER

        st.markdown('-----------------------------------------------------')
        st.text('Developed by M.Thanalakshmi - 2023')
        st.text('Mail: thanalakshmi7558@gmail.com')

if __name__ == '__main__':
	      main()
            
                
                
                
        
        
