import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
url = os.getenv("BACKEND_URL", "http://localhost:8000")

# url ='http://localhost:8000'
# url = 'https://your-public-backend-url.com'

def get_analytics_productline_tab():
    st.title("Sales Breakdown by Product Line")
    payload = {
            'start_date': "2018-01-05",
            'end_date': "2020-01-05"
        }

    try:
        response = requests.post(f'{url}/analytics/productline', json=payload)
        if response.status_code == 200:
            analytics_data = response.json()  # Parse the JSON data
            if isinstance(analytics_data, list):
                # Create the DataFrame from the response
                data = {
                    "Product_line": [item['name_productline'] for item in analytics_data],
                    "Quantity_total" : [item['total_quantity'] for item in analytics_data],
                    "Sale_total": [item['total_sale'] for item in analytics_data],
                    "Quantity_pct" : [item['total_quantity_pct'] for item in analytics_data],
                    "Sale_pct": [item['total_sale_pct'] for item in analytics_data],
                }

                df = pd.DataFrame(data)
                df_sorted = df.sort_values(by="Sale_total", ascending=False)

                # st.bar_chart(data=df_sorted.set_index("Product_line")['Sale_total'], use_container_width=True)

                # Use Plotly for the bar chart, sorting by Sale_total
                fig = px.bar(df_sorted, x="Product_line", y="Sale_total", title='Sale distribution by product line',
                             labels={"Product_line": "Product Line", "Sale_total": "Total Sales"})
                fig.update_layout(xaxis_title="Product Line", yaxis_title="Total Sales", width=800)

                st.plotly_chart(fig, use_container_width=True)

                # Use Plotly for the bar chart, sorting by Quantity_total
                fig = px.bar(df_sorted, x="Product_line", y="Quantity_total",title='Quantity distribution by product line',
                             labels={"Product_line": "Product Line", "Quantity_total": "Total Quantity"})
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
