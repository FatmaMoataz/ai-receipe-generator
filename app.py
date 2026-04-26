import streamlit as st
import requests

st.set_page_config(page_title="AI Chef", page_icon="🍳")

st.title("👨‍🍳 AI Recipe Generator")

API_URL = "https://helping-pubmed-charles-invalid.trycloudflare.com/generate"

ingredients = st.text_input("Enter your ingredients (e.g., Chicken, Lemon):")

if st.button("Generate Recipe"):
    if ingredients:
        with st.spinner("Chef is thinking..."):
            try:
                response = requests.post(API_URL, json={"ingredients": ingredients}, timeout=60)
                
                if response.status_code == 200:
                    recipe = response.json()
                    
                    st.header(f"🍴 {recipe.get('recipe_name')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("⏱ Time", recipe.get('time'))
                    with col2:
                        st.metric("🔥 Calories", recipe.get('calories'))
                    
                    st.subheader("🛒 Ingredients")
                    for item in recipe.get('ingredients', []):
                        st.write(f"✅ **{item.get('quantity')}** {item.get('name')}")
                        
                    st.subheader("👨‍🍳 Instructions")
                    for i, step in enumerate(recipe.get('instructions', []), 1):
                        st.write(f"{i}. {step}")
                        
                    st.balloons()
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
    else:
        st.warning("Please enter ingredients first!")
