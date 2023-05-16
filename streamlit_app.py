import streamlit
import pandas as pd

streamlit.title('My parents Healthy Diner')
  
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('Build your own Fruit Smoothie')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#Make Fruit column as index column
my_fruit_list = my_fruit_list.set_index('Fruit')

# Add multiselect option to pic the fruits for smoothie
streamlit.multiselect('Pack some fruits:', list(my_fruit_list.index))

#Display the table on the page
streamlit.dataframe(my_fruit_list)
