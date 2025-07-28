from modules.aws import create_aws
from modules.intro import Introduction
from modules.myblogs import myblogs
from modules.startup import *
from modules.linux import linux_operations
from modules.python import python_tasks
from modules.bms import Bms
from modules.docker import docker_operations
from modules.machineLearning import ml
from modules.Genai import genai_sql_generator
from modules.js import javascript_tasks
import streamlit as st
st.set_page_config(page_title="RemoteOps Dashboard", layout="wide")
st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        h1, h2, h3, h4 {
            font-family: 'Segoe UI', sans-serif;
            color: #1f1f1f;
        }
        .stButton>button {
            background-color: #0E1117;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
        .stTextInput>div>input, .stTextArea>div>textarea {
            border-radius: 6px;
            padding: 0.4rem;
        }
    </style>
""", unsafe_allow_html=True)
def main_menu():
    st.sidebar.markdown("### Module Selection")
    menu = st.sidebar.radio(
        "Select Module",
        [
            "Introduction",
            "Linux Shell",
            "Docker Manager",
            "GenAI SQL Generator",
            "Machine Learning",
            "Bank Management System",
            "Python",
            "JavaScript",
            "AWS",
            "Startup Builder",
            "MyBlogs"
        ]
    )
    if "Introduction" in menu:
        Introduction()
    elif "Linux Shell" in menu:
        linux_operations()
    elif "Docker Manager" in menu:
        docker_operations()
    elif "GenAI SQL Generator" in menu:
        genai_sql_generator()
    elif "Machine Learning" in menu:
        ml()
    elif "Bank Management System" in menu:
        Bms()
    elif "Python" in menu:
        python_tasks()
    elif "JavaScript" in menu:
        javascript_tasks()
    elif "AWS" in menu:
        create_aws()
    elif "Startup Builder" in menu:
        startup_builder()
    elif "MyBlogs" in menu:
        myblogs()
main_menu()