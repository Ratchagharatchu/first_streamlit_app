import streamlit
streamlit.title('My parents new healthy dinner')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣Omega 3 & blueberry oatmeal')
streamlit.text('🥗Kale 3 & spinach & Rocket Smoothie')
streamlit.text('🐔Hard-boiled free range Egg')
streamlit.text('🥑🍞Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
