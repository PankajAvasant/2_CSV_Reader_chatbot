from llama_index.indices.struct_store import GPTPandasIndex
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

import os
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
 

df = pd.read_excel(r"./input_Files/GDP.xls")

index = GPTPandasIndex(df=df)

query_engine = index.as_query_engine(
    verbose=True
)

def get_openai_response(question):
    response = query_engine.query(question)
    return response
  

st.set_page_config(page_title="Q&A chatBot on PI")

st.header("ChatBOT where You can ask questions based on GDP of Countries")

input=st.text_input("Input: ",key="input")
response=get_openai_response(input)

submit=st.button("get answer")

## If ask button is clicked

if submit:
    st.subheader("The Response is")
    st.write(response.response)

