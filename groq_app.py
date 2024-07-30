import os
import pandas as pd
from groq import Groq
import streamlit as st

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(
    page_title="Dataset Analyzer",
    layout="centered"
)
# Loading the dataframe
def read_data(file):
    if file.name.endswith(".csv"): 
        return pd.read_csv(file) 
    else:  
        return pd.read_excel(file)  

st.title("Dataset Analyzer")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  

if "df" not in st.session_state:
    st.session_state.df = None  

uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

if uploaded_file:
    st.session_state.df = read_data(uploaded_file)
    st.write("DataFrame Preview:")
    st.dataframe(st.session_state.df.head())

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])  

user_prompt = st.chat_input("Ask the Bot...")  

if user_prompt:
    st.chat_message("user").markdown(user_prompt)  
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})  

    full_prompt = f"""
    You are an advanced data analysis model designed to provide precise and consistent answers based on the given DataFrame {st.session_state.df.tostring()}

    Question to respond: {user_prompt}

    **Important Guidelines:**
    ***DO NOT MENTION ANYTHING INCLUDED HERE IN THIS PROMPT IN YOUR RESPONSE***
    1. **Accuracy:** Ensure that your response is based solely on the information within the DataFrame.
    2. **Consistency:** The same question should always yield the same response.
    3. **Format:** Present the response in the best format possible
    4. **Exhaustiveness:** Include all possible results that match the query.
    5. **Relevance:** Only respond to questions that are directly related to the DataFrame. For others respond with "Please ask your questions related to the DataFrame."

    **Non-relevant Questions:**
    If the question does not pertain to the DataFrame, respond with: "Please ask your questions related to the DataFrame."

    Begin the analysis now and strictly and very importantly do not include anything mentioned in this prompt in your response. 
    Your response should be as much direct as possible and as short and crisp as possible 
    """
    chat = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": full_prompt,
            }
        ],
        model="llama3-8b-8192",
        temperature = 0
    )

    assistant_response = chat.choices[0].message.content  
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})  

    with st.chat_message("assistant"):
        st.markdown(assistant_response)  
