import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import os

load_dotenv()   ## initializing/loading all enviroment variable

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt,image[0]])
    return response.text

def input_image_setup(file):
    # Check if a file has been uploaded
    if file is not None:
        # Read the file into bytes
        bytes_data = file.getvalue()

        image_parts = [
            {
                "mime_type": file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
# Initializing streamlit

st.set_page_config(page_title = "Ai NUTRITIONIST APP")

st.header("AI Health Advisor")
upload_file = st.file_uploader("click here to upload the image",type=["jpg","jpeg","png"])
image =""
if upload_file is not None:
    image=Image.open(upload_file)
    st.image(image,caption='Uploaded image',use_column_width=True)

submit = st.button("Is it Healthy..")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----


            finally you can also mention the food is healthy or not and also mention 
            pencentage of carbo hydrate , sugur ,fats,fibers and required things 
            for our diet ,and if it is not healthy suggest a healthy food also


"""

# if sbmit is clicked 
if submit:
    image_data = input_image_setup(upload_file)
    result = get_gemini_response(input_prompt,image_data)
    st.header("The response for you")
    st.write(result)


