import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set page config (must be at the top before other streamlit functions)
st.set_page_config(page_title="Gemini Health App")

# Function to set up image input
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Function to get Gemini response
def get_gemini_response(input_prompt, image, user_input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input_prompt, image[0], user_input])
    return response.text

# Streamlit UI
st.header("Gemini Calorie Advisor")

input_text = st.text_input("Any specific instruction?", key="input")

uploaded_file = st.file_uploader("Upload an image of food", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

if st.button("Tell me the total calories"):
    input_prompt = """
    You are an expert nutritionist. Based on the uploaded food image, identify the food items and calculate the total calories. 
    Also, provide the details of every item in the following format:

    1. Item 1 - no of calories
    2. Item 2 - no of calories
    ...
    """
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input_text)
    st.subheader("Calorie Details:")
    st.write(response)
