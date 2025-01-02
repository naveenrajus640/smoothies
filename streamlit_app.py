# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie"""
)

title = st.text_input("Name on Smoothie")
st.write("The Name on Smoothie is", title)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.FRUIT_OPTIONs").select(col("fruit_name"),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect('Choose up to 5 ingredients:',my_dataframe, max_selections = 5)


if ingredients_list:
    ingredients_string = ''
    
    for fruits_chosen in ingredients_list:
        ingredients_string +=  fruits_chosen + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruits_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruits_chosen,' is ', search_on, '.')

        st.subheader(fruits_chosen + " Nutrition Information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruits_chosen)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+title + """')"""

    st.write(my_insert_stmt)


    time_to_insert = st.button("Submit order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!'+ title , icon="✅")

