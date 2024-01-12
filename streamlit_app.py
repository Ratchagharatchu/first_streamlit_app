import streamlit
#import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My parents new healthy dinner')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣Omega 3 & blueberry oatmeal')
streamlit.text('🥗Kale 3 & spinach & Rocket Smoothie')
streamlit.text('🐔Hard-boiled free range Egg')
streamlit.text('🥑🍞Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected  = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#create a repetable code block(called a function)
def get_fruityvice_data(this_fruit_choice):
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
     return fruityvice_normalized

#new section to display  fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("please select a fruit get the information")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
        
except URLError as e:
    streamlit.error()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("The fruit_load_list contains:")
streamlit.dataframe(my_data_row)

# Section to allow the user to add a fruit to the list
streamlit.header("Add a New Fruit to the List")
new_fruit = streamlit.text_input('Enter a new fruit:')
if streamlit.button('Add Fruit'):
    # Add the new fruit to the Snowflake database
    try:
        my_cur.execute("INSERT INTO fruit_load_list (fruit_name) VALUES (%s)", (new_fruit,))
        my_cnx.commit()
        streamlit.success(f'{new_fruit} has been added to the list!')
    except Exception as e:
        streamlit.error(f'Error adding {new_fruit} to the list: {str(e)}')

# Display the fruit list
streamlit.header("View our Fruit List - Add Your Favorites!")
if streamlit.button("Get Fruit List"):
    fruit_list_data = get_fruit_list()
    if not fruit_list_data:
        streamlit.warning("The fruit list is empty.")
    else:
        fruit_df = pd.DataFrame(fruit_list_data, columns=["Fruit ID", "Fruit Name"])
        streamlit.dataframe(fruit_df)

#Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
     with my_cnx.cursor() as my_cur:
          my_cur.execute("insert into fruit_load_list values('from streamlit')")
          return "Thanks for adding"+new_fruit

add_my_fruit =  streamlit.text_input('what fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     back_from_function = insert_row_snowflake(add_my_fruit)
     streamlit.text(back_from_function)
     



