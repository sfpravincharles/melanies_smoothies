# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import when_matched
#from snowflake.snowpark.functions import filter


# Write directly to the app
st.title(":cup_with_straw: Customise you Smoothie :cup_with_straw:")
#st.write( """CHOOOSE YOUR FOOD """)    

#name_on_order =st.text_input("Name on Smoothie")
#st.write("Your Name on Order:", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    if submitted:
        try:
            
            og_dataset = session.table("smoothies.public.orders")
            edited_dataset = session.create_dataframe(editable_df)
            og_dataset.merge(edited_dataset
                         , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
            st.success('Someone clicked the button', icon = '👍')
        except:
            st.write("Something failed", icon = '👍')
else:
    st.write("There is no records",icon = '👍')
#st.write(my_dataframe)
