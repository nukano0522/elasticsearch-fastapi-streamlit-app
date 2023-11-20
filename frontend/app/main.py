import streamlit as st
from streamlit.logger import get_logger
import requests

def run():
    st.set_page_config(
        page_title="elasticsearch_demo_app",
        page_icon="👋",
    )
    
    st.markdown("""
                ### インデックス情報
                """)    
    res = requests.get('http://elasticsearch_pg_backend_1:8002/es/index/info/my_index')
    st.write(res.json())
    
    st.markdown("""
                ## 検索結果
                """)    
    res = requests.get('http://elasticsearch_pg_backend_1:8002/search/kaigo_swem_01/認知症')
    st.write(res.json())

    
if __name__ == "__main__":
    run()
