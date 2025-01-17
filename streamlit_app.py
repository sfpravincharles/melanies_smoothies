# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customise you Smoothie :cup_with_straw:")
st.write(
    """CHOOOSE YOUR FOOD
    """)    

name_on_order =st.text_input("Name on Smoothie")
st.write("Your Name on Order:", name_on_order)

#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select('FRUIT_NAME')
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect('Choose upto 5 ingrediaents', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string =''
    
    for each_fruit in ingredients_list:
        ingredients_string +=each_fruit+' '
        
    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) 
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
    st.write(my_insert_stmt)
    time_to_insert =st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success('Your Smoothie is ordered!', icon="✅")
