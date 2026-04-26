# Frontend Streamlit
import streamlit as st
import requests

st.title("👨‍🍳 AI Recipe Generator")

ingredients = st.text_input("Enter your ingredients (e.g., Chicken, Lemon):")

if st.button("Generate Recipe"):
    #  Cloudflare
    API_URL = "https://bigger-historic-trained-version.trycloudflare.com/generate"
    
    response = requests.post(API_URL, json={"ingredients": ingredients})
    
    if response.status_code == 200:
        recipe = response.json()
        st.header(recipe['recipe_name'])
        st.subheader("Ingredients")
        st.write(recipe['ingredients'])
        st.subheader("Instructions")
        st.write(recipe['instructions'])
    else:
        st.error("Failed to connect to the AI model.")
