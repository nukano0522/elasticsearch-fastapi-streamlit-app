import streamlit as st
import requests
import pandas as pd

def keyword_search():
    # フォームの作成
    with st.form(key='my_form'):
        text_input = st.text_input(label='検索キーワードを入力してください')
        submit_button = st.form_submit_button(label='Submit')
        
    # サブミットボタンが押されたときの処理
    if submit_button:
        # ここでバックエンドのデータ処理を行う
        res = requests.get(f"http://backend:8002/search/kaigo_swem_01/{text_input}")
        # st.write(res.json())
        data = res.json()
        df = pd.json_normalize(data)
        st.table(df)
        

def main():
    keyword_search()

if __name__ == "__main__":
    main()