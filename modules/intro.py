import streamlit as st
from PIL import Image
def Introduction():
    team_number = "Team 30"
    st.title("Menu Based Python Project")
    st.write("Welcome to the RemoteOps Dashboard. Navigate from the sidebar to explore various modules.")
    st.subheader(f" Team Number: {team_number}")
    name = "Raghav Soni"
    
    image = Image.open("me.jpg")
    st.subheader("Team Member Info")
    st.image(image,width=300)
    st.subheader(f"👤 Name: {name}")
   