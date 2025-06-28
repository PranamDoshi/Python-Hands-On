import streamlit as st
import pandas as pd
from datetime import datetime
import os, pdfkit

import streamlit.components.v1 as components

from main import main, get_available_tickers, get_period_values, get_benchmark_indices
# Streamlit application layout
st.title("Compare your Portfolio performance with the Nifty Benchmark!")

# Take reference benchmark index from user
benchmark = st.selectbox('Select the benchmark index:', list(get_benchmark_indices().keys()))

# Dropdown for multiple values
tickers = st.multiselect('Select all the Stocks from your Portfolio:', get_available_tickers())

# Take mutual fund input from user
# mutual_fund = st.text_input("Enter a Mutual Fund Name:", value=None)

# Optional date fields
start_date = st.date_input('Start date', value=None)
end_date = st.date_input('End date', value=None)

# Optional Comparison Period
period = st.selectbox('Select a Time Period:', get_period_values())

# Submit button
if st.button('Submit'):
    try:
        # Call the function to generate HTML
        html_content = main(get_benchmark_indices()[benchmark], [f"{ticker}.NS" for ticker in tickers], 0.0615, mutual_fund=get_benchmark_indices()[benchmark], start_date=start_date, end_date=end_date, period=period)

        # st.markdown(html_content, unsafe_allow_html=True)
        # with open("C:/Users/Pranam/Desktop/output.html", 'wb') as f:
        #     f.write(html_content.encode('utf-8', errors='ignore'))
        # pdfkit.from_file("C:/Users/Pranam/Desktop/output.html", "C:/Users/Pranam/Desktop/output.pdf")
        pdfkit.from_string(html_content.encode('utf-8', errors='ignore').decode(), 'C:/Users/Pranam/Desktop/output.pdf')

        components.html(html_content, width=1400, height=1080, scrolling=True)

    except Exception as e:
        st.error(f"An error occured while comparing your Portfolio: {str(e)}")
