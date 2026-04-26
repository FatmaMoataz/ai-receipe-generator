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
    
    st.header(f"🍴 {recipe.get('recipe_name', 'Delicious Recipe')}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⏱ Time", recipe.get('time', 'N/A'))
    with col2:
        st.metric("🔥 Calories", recipe.get('calories', 'N/A'))
    with col3:
        st.metric("💰 Cost", recipe.get('cost', 'Low'))

    st.divider()

    st.subheader("🛒 Ingredients")
    ingredients_list = recipe.get('ingredients', [])
    for item in ingredients_list:
        # هنا بنعرض الـ name والـ quantity بشكل نظيف
        st.write(f"✅ **{item.get('quantity')}** {item.get('name')}")

    st.divider()

    st.subheader("👨‍🍳 Instructions")
    instructions_list = recipe.get('instructions', [])
    for i, step in enumerate(instructions_list, 1):
        st.write(f"{i}. {step}")
