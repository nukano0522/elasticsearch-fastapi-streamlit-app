import streamlit as st
from streamlit.logger import get_logger
import requests
import pandas as pd

def run():
    st.set_page_config(
        page_title="elasticsearch_demo_app",
        page_icon="👋",
    )
    
    st.markdown("""
                ### インデックス一覧
                """)    
    res = requests.get('http://backend:8002/es/index/info')
    data = res.json()
    df = pd.json_normalize(data)
    st.table(df)

    
if __name__ == "__main__":
    run()
