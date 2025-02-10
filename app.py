import streamlit as st
import os

from PIL import Image
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv() # load all the environment variables from .env

genai.configure(api_key=os.getenv(key='GOOGLE_API_KEY'))

model=genai.GenerativeModel('gemini-1.5-pro')

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

#convert image to bytes
def input_image_details(uploaded_file):
    if uploaded_file:
        # read the file into bytes
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]

        return image_parts
    else:
        raise FileNotFoundError('No file uploaded')


# Streamlit app
st.set_page_config(page_title='MultiLanguage Invoice Extractor')
st.header('MultiLanguage Invoice Extractor')

uploaded_file=st.file_uploader(label='Choose an invoice image...',type=['jpg','jpeg','png'])

# Display the image
image=""
if uploaded_file:
    image=Image.open(uploaded_file)
    st.image(image,caption='uploaded image..',use_container_width=True)

input=st.text_input(label='Input Prompt...',key='input')    


# submit=st.button('Tell me about the invoice')
input_prompt="""
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

if input and uploaded_file:
    # convert image to bytes
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input=input_prompt,image=image_data,prompt=input)
    st.subheader('The Response is')
    st.write(response)










