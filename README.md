# 🍳 AI Recipe Generator (End-to-End LLM Project)

An intelligent full-stack application that transforms a list of ingredients into a professional culinary recipe. This project demonstrates how to bridge high-performance AI models with a user-friendly web interface.

## 📺 Live Demo
<div align="center">
  <a href="https://drive.google.com/file/d/1FodCsGDfcUhwlsax5BBJdUiZe_xJKEpQ/view?usp=sharing">
    <img src="https://img.shields.io/badge/🎥_Watch_Video_Demo-Click_Here-red?style=for-the-badge" alt="Watch Demo">
  </a>
</div>


## 📓 Kaggle Notebook
You can find the full backend implementation and model inference logic here:
[![Kaggle](https://img.shields.io/badge/Kaggle-00AFEF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/code/fatmamoataz/test-project)


---

## 🏗️ Technical Architecture
The project uses a distributed architecture to handle the computational load of the LLM:

* **Frontend:** [Streamlit](https://streamlit.io/) - Hosted on Streamlit Cloud for a responsive user interface.
* **AI Engine:** [Mistral-7B-Instruct-v0.2](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2) - Running on NVIDIA T4 GPU.
* **Backend API:** [FastAPI](https://fastapi.tiangolo.com/) - High-performance Python framework serving the model.
* **Secure Tunneling:** [Cloudflare Tunnel](https://www.cloudflare.com/products/tunnel/) - Connects the local Kaggle environment to the public internet securely.

## 🚀 Key Technical Features
- **Prompt Engineering:** Custom-built prompt templates to force the LLM to output strictly valid JSON.
- **Robust Parsing:** Backend logic to extract and auto-repair JSON from LLM stream outputs.
- **Async Execution:** Utilizes `asyncio` and `uvicorn` to handle concurrent API requests.
- **Zero-Cost Deployment:** Leverages Kaggle's GPU and Streamlit Cloud for a completely free hosting solution.

## 🛠️ How to Run

### 1. Backend (Kaggle)
1.  Open the backend notebook and enable **GPU T4** and **Internet**.
2.  Run all cells to download the Mistral model and start the FastAPI server.
3.  Copy the generated `trycloudflare.com` URL.

### 2. Frontend (Streamlit)
1.  Add the URL to your Streamlit secrets or directly into `app.py`.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Launch the app:
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure
```text
├── app.py                # Streamlit UI & Frontend Logic
├── requirements.txt      # Frontend Dependencies
├── backend_notebook.ipynb # FastAPI, Model Loading & Tunneling
└── README.md             # Project Documentation
