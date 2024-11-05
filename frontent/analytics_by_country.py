import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

from lxml.html import submit_form

url ='http://localhost:8000'

def get_analytics_country_tab():
    st.title("Sales Breakdown by Country")
    with st.form(key='analytics_country_tab'):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime(2018, 8, 1))
        with col2:
            end_date = st.date_input("End Date", datetime(2020, 8, 5))
        submit_button = st.form_submit_button(label='Submit')
    # if st.button('Get Analytics'):
        if submit_button:
            payload = {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
            }
            try:
                response = requests.post(f'{url}/analytics/country', json=payload)
                if response.status_code == 200:
                    analytics_data = response.json()  # Parse the JSON data
                    if isinstance(analytics_data, list):
                        # Create the DataFrame from the response
                        data = {
                            "Country_name": [item['country_name'] for item in analytics_data],
                            "Quantity_total" : [item['total_quantity'] for item in analytics_data],
                            "Sale_total": [item['total_sale'] for item in analytics_data],
                            "Quantity_pct" : [item['total_quantity_pct'] for item in analytics_data],
                            "Sale_pct": [item['total_sale_pct'] for item in analytics_data],
                        }

                        df = pd.DataFrame(data)
                        df_sorted = df.sort_values(by="Sale_total", ascending=False)

                        # st.bar_chart(data=df_sorted.set_index("Product_line")['Sale_total'], use_container_width=True)

                        # Use Plotly for the bar chart, sorting by Sale_total
                        fig = px.bar(df_sorted, x="Country_name", y="Sale_total", title='Sale distribution by Country',
                                     labels={"Country_name": "Country Name", "Sale_total": "Total Sales"})
                        fig.update_layout(xaxis_title="Country Name", yaxis_title="Total Sales", width=800)

                        st.plotly_chart(fig, use_container_width=True)

                        # Use Plotly for the bar chart, sorting by Quantity_total
                        fig = px.bar(df_sorted, x="Country_name", y="Quantity_total",title='Quantity distribution by Country',
                                     labels={"Product_line": "Country Name", "Quantity_total": "Total Quantity"})
                        fig.update_layout(xaxis_title="Product Line", yaxis_title="Total Quantity", width=800)

                        st.plotly_chart(fig, use_container_width=True)

                        # Format and display the table
                        df_sorted["Sale_total"] = df_sorted["Sale_total"].map("{:.2f}".format)
                        st.table(df_sorted)
                    else:
                        st.error("Unexpected response format")
                else:
                    st.error(f"Failed to get analytics data. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
