import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.callbacks import get_openai_callback
import os

import os
from dotenv import load_dotenv
load_dotenv()

## Langsmith Tracking
# os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
# os.environ["LANGCHAIN_TRACING_V2"]="true"
# os.environ["LANGCHAIN_PROJECT"]="Simple Q&A Chatbot With OPENAI"

## Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a {profession}. Please interpret the given statement from the perspective of a {profession} and generate text in the tone of a {profession}. The generated text should not exceed {max_words} words."),
        ("user","Statement:{question}")
    ]
)

def generate_response(question,profession,max_words,api_key,engine,temperature,max_tokens):
    if api_key=="kindnessiscosteffective":
        api_key = "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"
        
    #openai.api_key=api_key

    llm=ChatOpenAI(model=engine,temperature=temperature,max_tokens=max_tokens, openai_api_key=api_key)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    cbl = []
    with get_openai_callback() as cb:
        answer=chain.invoke({'question':question, 'profession': profession, 'max_words': max_words})
        cbl.append(cb)
    return answer, cbl

## #Title of the app
st.title("Interpretor for HEOR")



## Sidebar for settings
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your Open AI API Key:",type="password")

## Select the OpenAI model
engine=st.sidebar.selectbox("Select Open AI model",["gpt-4-turbo","gpt-4", "gpt-4o"])

## Adjust response parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.1)
max_words = st.sidebar.slider("Max Words", min_value=50, max_value=300, value=150)

profession = st.radio("I am a: ", ('HEOR modeler', 'Clinician', 'Health policy maker', 'Market access professional', 'Naive math guy'))

## MAin interface for user input
st.write("Interpret this statement for me: ")
user_input=st.text_input("You:")

max_tokens = max_words * 2.5

if st.button("Generate"):
    if user_input and api_key:
        response, cbl=generate_response(user_input,
                                        profession,
                                        max_words,
                                        api_key,
                                        engine,
                                        temperature,
                                        max_tokens
                                        )
        st.write(response, cbl[0])

    elif user_input:
        st.warning("Please enter the OPENAI API Key in the sider bar")
    else:
        st.write("Please provide the user input")


