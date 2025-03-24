import streamlit as st
import google.generativeai as genai
import os
import PIL.Image

# Configure API Key
os.environ['GEMINI_API_KEY'] = "AIzaSyAX3Kj9hUsNz3gxbwvzSgp-1MfY6dNHq-Y"
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# Initialize model
model = genai.GenerativeModel("gemini-2.0-flash")

# Page Config
st.set_page_config(page_title="PromtBot", layout="centered")

# Sidebar Navigation
st.sidebar.title("Options")
option = st.sidebar.radio("Select Mode:", ["Chat", "Image Viewer"])

if option == "Image Viewer":
    st.sidebar.subheader("Upload an Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img = PIL.Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)
        
        # Generate response from image
        model = genai.GenerativeModel('models/gemini-2.0-pro-exp-02-05')
        response = model.generate_content(img)
        
        # Display response
        st.markdown(response.text if hasattr(response, 'text') else "No response generated.")
else:
    # Custom CSS for ChatGPT-like UI
    st.markdown(
        """
        <style>
            .stChatInput textarea {
                background-color: black !important;
                color: white !important;
                border-radius: 8px;
                padding: 10px;
            }
            .stChatInput textarea::placeholder {
                color: #00ccff !important;
            }
            .stChatMessage {
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 10px;
            }
            .user {
                background-color: #0A84FF;
                color: white;
                text-align: right;
                padding: 10px;
                border-radius: 10px;
                margin: 5px;
            }
            .assistant {
                background-color: #4A4B52;
                text-align: left;
                padding: 10px;
                border-radius: 10px;
                margin: 5px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title
    st.markdown(
        "<h1 style='text-align: center; color: #00ccff;'>🤖 Promtbot</h1>", 
        unsafe_allow_html=True
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    question = st.chat_input("Ask me anything...")

    if question:
        # Append user message to history
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Generate response
        try:
            response = model.generate_content(question)
            answer = response.text if hasattr(response, 'text') else "Sorry, I couldn't generate a response."
            
            # Append AI response to history
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)
        
        except Exception as e:
            st.error(f"Error: {e}")
