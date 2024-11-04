from datetime import datetime
import streamlit as st
from holoviews.operation import collapse
import requests


# url ='http://localhost:8000'
url = 'https://your-public-backend-url.com'

def get_update_tab():
    select_date = st.date_input('Enter date', datetime(2018, 1, 5), label_visibility="collapsed")
    select_date_str = select_date.strftime('%Y-%m-%d')
    response = requests.get(f"{url}/sales/{select_date_str}")

    if response.status_code == 200:
        data = response.json()
            # if isinstance(response.json(), list) else []
    else:
        st.error("Failed to retrieve expense data")
        data = []
    # date_time, ORDERNUMBER, PRODUCTLINE, DEALSIZE, STATUS, COUNTRY, QUANTITYORDERED, PRICEEACH, SALES
    # Declare category to get list  collapsed
    PRODUCTLINE = ['Classic Cars' , 'Motorcycles', 'Planes', 'Ships', 'Trains', 'Trucks and Buses', 'Vintage Cars']
    STATUS = ['Disputed', 'In Process', 'Cancelled', 'On Hold', 'Resolved', 'Shipped']
    with st.form(key="sales_form"):
        # Add header
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.text("PRODUCTLINE")
        with col2:
            st.text("STATUS")
        with col3:
            st.text("COUNTRY")
        with col4:
            st.text("QUANTITYORDERED")
        with col5:
            st.text("SALES")

        #add number of row in table
        sales = []
        for i in range(9):
            # Check if customer choose date will not over than the last date
            if i < len(data):
                productline = data[i]['PRODUCTLINE']
                status = data[i]['STATUS']
                country = data[i]['COUNTRY']
                quantity = data[i]['QUANTITYORDERED']
                sale = data[i]['SALES']

            else:
                productline = "Ships"
                status = "Disputed"
                country = ""
                quantity = 0.0
                sale = 0.0

            # ordernumber:int(ordernumber)
            # quantity : float(quantity)
            # price : float(price)
            # sale : float(sale)
            # ordernumber = int(ordernumber)
            # quantity = float(quantity)
            # price = float(price)
            # sale = float(sale)
            # Create full table
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                productline_input = st.selectbox(label="Product_line", options=PRODUCTLINE, index=PRODUCTLINE.index(productline),
                                            key=f"productline_{i}", label_visibility="collapsed")
            with col2:
                status_input = st.selectbox(label="Status", options=STATUS, index=STATUS.index(status),
                                              key=f"status_{i}", label_visibility="collapsed")
            with col3:
                country_input = st.text_input(label="Country", value=country, key=f"country_{i}", label_visibility="collapsed")
            with col4:
                quantity_input = st.number_input(label="Quantity_order", min_value=0.0, step=1.0, value=quantity,
                                             key=f"quantity_{i}",label_visibility="collapsed")
            with col5:
                sale_input = st.number_input(label="Sale", min_value=0.0, step=1.0, value=sale,
                                             key=f"sale_{i}",label_visibility="collapsed")

            # with col3:
            #     notes_input = st.text_input(label="Notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")

            sales.append({
                'DATE_TIME' :select_date_str,
                'PRODUCTLINE': productline_input,
                'STATUS': status_input,
                'COUNTRY': country_input,
                'QUANTITYORDERED': quantity_input,
                'SALES': sale_input,

                # 'expense_date': select_date_str,
            })
        # Should have submit button to finish table
        submit_button = st.form_submit_button()
        if submit_button:
            filter_sales = [sale for sale in sales if sale['PRICEEACH'] > 0]
            response = requests.post(f"{url}/sales/{select_date_str}", json=filter_sales)
            if response.status_code == 200:
                st.success("update successful")
            else:
                st.error("failed to update sales data")

# from datetime import datetime
# import streamlit as st
# from holoviews.operation import collapse
# import requests
#
# url = 'http://localhost:8000'
#
#
# def get_update_tab():
#     # Format date input for API
#     select_date = st.date_input('Enter date', datetime(2018, 1, 5), label_visibility="collapsed")
#     select_date_str = select_date.strftime('%Y-%m-%d')  # Convert date to string format
#
#     # Fetch data for the selected date
#     response = requests.get(f"{url}/sales/{select_date_str}")
#     if response.status_code == 200:
#         data = response.json()
#     else:
#         st.error("Failed to retrieve expense data")
#         data = []
#
#     PRODUCTLINE = ['Classic Cars', 'Motorcycles', 'Planes', 'Ships', 'Trains', 'Trucks and Buses', 'Vintage Cars']
#     STATUS = ['Disputed', 'In Process', 'Cancelled', 'On Hold', 'Resolved', 'Shipped']
#     DEALSIZE = ['Small', 'Medium', 'Large']
#
#     with st.form(key="sales_form"):
#         # Add header
#         col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
#         for col, text in zip([col1, col2, col3, col4, col5, col6, col7, col8],
#                              ["ORDERNUMBER", "PRODUCTLINE", "DEALSIZE", "STATUS", "COUNTRY", "QUANTITYORDERED",
#                               "PRICEEACH", "SALES"]):
#             col.text(text)
#
#         # Add rows for each entry in data or empty default rows
#         sales = []
#         for i in range(9):
#             # Pre-fill with data from the server or default values
#             if i < len(data):
#                 ordernumber = data[i].get('ORDERNUMBER', 0.0)
#                 productline = data[i].get('PRODUCTLINE', 'Motorcycles')
#                 size = data[i].get('DEALSIZE', 'Medium')
#                 status = data[i].get('STATUS', 'Disputed')
#                 country = data[i].get('COUNTRY', ' ')
#                 quantity = data[i].get('QUANTITYORDERED', 0.0)
#                 price = data[i].get('PRICEEACH', 0.0)
#                 sale = data[i].get('SALES', 0.0)
#             else:
#                 ordernumber = 0.0
#                 productline = "Motorcycles"
#                 size = "Medium"
#                 status = "Disputed"
#                 country = " "
#                 quantity = 0.0
#                 price = 0.0
#                 sale = 0.0
#
#             ordernumber = float(ordernumber)
#             quantity = float(quantity)
#             price = float(price)
#             sale = float(sale)
#
#             # Populate form fields
#             with col1:
#                 ordernumber_input = st.number_input(label="Order_Number", min_value=0.0, step=1.0, value=ordernumber,
#                                                     key=f"ordernumber_{i}", label_visibility="collapsed")
#             with col2:
#                 productline_input = st.selectbox(label="Product_line", options=PRODUCTLINE,
#                                                  index=PRODUCTLINE.index(productline),
#                                                  key=f"productline_{i}", label_visibility="collapsed")
#             with col3:
#                 dealsize_input = st.selectbox(label="Deal_Size", options=DEALSIZE, index=DEALSIZE.index(size),
#                                               key=f"size_{i}", label_visibility="collapsed")
#             with col4:
#                 status_input = st.selectbox(label="Status", options=STATUS, index=STATUS.index(status),
#                                             key=f"status_{i}", label_visibility="collapsed")
#             with col5:
#                 country_input = st.text_input(label="Country", value=country, key=f"country_{i}",
#                                               label_visibility="collapsed")
#             with col6:
#                 quantity_input = st.number_input(label="Quantity_order", min_value=0.0, step=1.0, value=quantity,
#                                                  key=f"quantity_{i}", label_visibility="collapsed")
#             with col7:
#                 price_input = st.number_input(label="Price", min_value=0.0, step=1.0, value=price, key=f"price_{i}",
#                                               label_visibility="collapsed")
#             with col8:
#                 sale_input = st.number_input(label="Sale", min_value=0.0, step=1.0, value=sale, key=f"sale_{i}",
#                                              label_visibility="collapsed")
#
#             # Append to sales list
#             sales.append({
#                 "DATE_TIME" : select_date.strftime('%Y-%m-%d'),
#                 'ORDERNUMBER': ordernumber_input,
#                 'PRODUCTLINE': productline_input,
#                 'DEALSIZE': dealsize_input,
#                 'STATUS': status_input,
#                 'COUNTRY': country_input,
#                 'QUANTITYORDERED': quantity_input,
#                 'PRICEEACH': price_input,
#                 'SALES': sale_input
#             })
#
#         # Submit button
#         submit_button = st.form_submit_button()
#         if submit_button:
#             # Filter sales for valid entries
#             filter_sales = [sale for sale in sales if sale['PRICEEACH'] > 0]
#             response = requests.post(f"{url}/sales/{select_date_str}", json=filter_sales)
#
#             if response.status_code == 200:
#                 st.success("Update successful")
#             else:
#                 st.error(f"Failed to update sales data: {response.text}")
#                 st.write("Data sent:", filter_sales)  # Optional: print data sent to API
