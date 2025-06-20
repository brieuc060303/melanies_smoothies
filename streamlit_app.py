# Import python packages
import streamlit as st

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie !
  """
)

from snowflake.snowpark.functions import col

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on the smoothie will be", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredient_list = st.multiselect('Choose up to 5 ingredients', my_dataframe, max_selections=5)

if ingredient_list:
    
    
    ingredients_string = ''
    
    for fruit in ingredient_list:
        ingredients_string += fruit + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """', '"""+name_on_order+"""')""" 


    time_to_insert = st.button('Submit order')
    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
