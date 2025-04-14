import streamlit as st
from dotenv import load_dotenv
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(model_name="llama-3.3-70b-versatile")

# Define system role for chatbot
message = """
You are an advanced legal chatbot designed specifically for Indian law, equipped with comprehensive knowledge of legal principles, procedures, and statutes relevant to the Indian legal system. Your primary goal is to assist users in understanding legal concepts, providing accurate information, and guiding them through legal queries in a user-friendly manner.
Your task is to generate informative responses to user inquiries regarding Indian law. This includes answering questions about legal rights, processes, and relevant laws affecting individuals and businesses in India.
Please keep in mind the following details while responding: 

Ensure that all information provided is accurate and up-to-date according to the latest Indian laws and regulations.
Offer clear explanations and avoid using overly complex legal jargon, making the information accessible to users without a legal background.
Provide relevant examples or case references when necessary to illustrate legal concepts.

For instance, if a user asks about the process of filing a complaint in a consumer court, you might explain the steps involved, relevant laws, and any important deadlines or requirements they should be aware of.
"""

system_message = SystemMessage(
    content=message)

# Initialize session state for chat history & input management
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [system_message]
if "latest_query" not in st.session_state:
    st.session_state.latest_query = ""


# Function to get legal advice
def get_legal_advice(query):
    # Append user message to chat history
    st.session_state.chat_history.append(HumanMessage(content=query))

    # Get AI response
    response = llm.invoke(st.session_state.chat_history)

    # Append AI response to chat history
    st.session_state.chat_history.append(AIMessage(content=response.content))

    return response.content


# Streamlit UI
st.set_page_config(page_title="AI Legal Assistance", page_icon="⚖️")

st.title("⚖️ AI Legal Assistance")
st.write("Ask any legal question, and I'll try to help!")

# Display chat history
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        st.markdown(f"👤 **You:** {msg.content}")
    elif isinstance(msg, AIMessage):
        st.markdown(f"🤖 **AI Lawyer:** {msg.content}")

# Input form to prevent auto-refresh issues
with st.form(key="user_input_form"):
    query = st.text_input("Enter your legal question here:", value=st.session_state.latest_query)
    submit_button = st.form_submit_button("Ask")

if submit_button and query:
    st.session_state.latest_query = query  # Store query temporarily
    with st.spinner("Thinking..."):
        response = get_legal_advice(query)
    st.session_state.latest_query = ""  # Clear input after response
    st.rerun()  # Rerun after processing input (but only once)

# Clear chat button
if st.button("🗑 Clear Chat"):
    st.session_state.chat_history = [system_message]
    st.session_state.latest_query = ""
    st.rerun()
