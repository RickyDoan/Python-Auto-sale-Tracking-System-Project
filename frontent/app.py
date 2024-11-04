import streamlit as st
from add_update_ui import get_update_tab
from analytics_by_productline import get_analytics_productline_tab
from analytics_by_country import get_analytics_country_tab
url ='http://localhost:8000'

st.title("Auto Sales Tracking System")

tab1, tab2, tab3 = st.tabs(['Add/Update', 'Analytics by Product Line', 'Analytics by Country'])
with tab1:
    get_update_tab()
with tab2:
    get_analytics_productline_tab()
with tab3:
    get_analytics_country_tab()
    pass
