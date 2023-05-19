import streamlit
import pandas as pd
import snowflake.connector
import requests
from urllib.error import URLError


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
#We want to filter the table data based on the fruits a customer will choose, so we'll pre-populate the list to set an example for the customer. 
# streamlit.multiselect('Pack some fruits:', list(my_fruit_list.index),['Avocado','Strawberries'])

#Display the table on the page
# streamlit.dataframe(my_fruit_list)

#show the selected fruits
fruits_selected = streamlit.multiselect('Pack some fruits:', list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # streamlit.text(fruityvice_response.json())
    #Normalise json data
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

#Display fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.write('The user entered ', fruit_choice)
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()
#Dont run anything past here while we troubleshoot


streamlit.header("The fruit load list contains:")
#snowflake-related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall()
  
# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  
#streamlit.stop()  


def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO fruit_load_list values ('" + new_fruit +"')")
    return "Thanks for adding" + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)



