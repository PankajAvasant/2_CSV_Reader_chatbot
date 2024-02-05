import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
import os
from dotenv import load_dotenv
from pandasai import Agent
from pandasai.skills import skill
import streamlit as st




df = pd.read_excel(r"./input_Files/GDP.xls")


load_dotenv()  # take environment variables from .env.

llm = OpenAI(api_token=os.getenv("OPENAI_API_KEY"), model_name="gpt-3.5-turbo-instruct")


#=============================== This is for add some custome skills to the agents ======================
 
# Function doc string to give more context to the model for use this skill
@skill
def plot_USDollarValues(Countries: list[str], US_dollars: list[int]):
    """
    Displays the bar chart  having name on x-axis and salaries on y-axis
    Args:
        names (list[str]): Employees' names
        salaries (list[int]): Salaries
    """
    # plot bars
    import matplotlib.pyplot as plt

    plt.bar(Countries, US_dollars)
    plt.xlabel("Countries Name")
    plt.ylabel("US_Dollars")
    plt.title("GDP of the countries")
    plt.xticks(rotation=45)
    plt.savefig("temp_chart.png")
    fig = plt.gcf()
    st.pyplot(fig)




agent = Agent([df], config={"llm": llm})

agent.add_skills(plot_USDollarValues)

#===================================================================

def get_openai_response(question):
    response = agent.chat(question)
    return response


st.set_page_config(page_title="Q&A chatBot on PAI")

st.header("ChatBOT where You can ask questions based on GDP of Countries")

input=st.text_input("Input: ",key="input")
response=get_openai_response(input)

submit=st.button("get answer")

## If ask button is clicked

if submit:
    st.subheader("The Response is")
    st.write(response)

