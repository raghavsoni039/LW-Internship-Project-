import streamlit as st
from googlesearch import search
from credentials import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pywhatkit
from instagrapi import Client
import tweepy
import requests
from bs4 import BeautifulSoup
import datetime

def python_tasks():

# ----------------------- GOOGLE SEARCH -----------------------
    def search_on_google(query):
        st.subheader("Top 5 Google Search Results:")
        for url in search(query, num_results=5):
            st.write(url)

    # ----------------------- EMAIL SENDING -----------------------
    def send_mail(receiver_mail, subject, body):
        sender_email = "raghavsoni28115@gmail.com"
        password = mail_pass
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_mail
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_mail, msg.as_string())
            st.success("Email sent successfully!")
        except Exception as e:
            st.error(f"Error sending email: {e}")
        finally:
            server.quit()

    # ----------------------- WHATSAPP MESSAGE -----------------------
    def send_whatsapp(phone, msg, hour, minute):
        try:
            pywhatkit.sendwhatmsg(phone, msg, hour, minute)
            st.success("Message scheduled successfully!")
        except Exception as e:
            st.error(f"Error sending message: {e}")

    # ----------------------- INSTAGRAM POST -----------------------
    def post_on_instagram(image_path, caption):
        try:
            c1 = Client()
            c1.login("_.raghavsoni", insta_pass)
            c1.photo_upload(path=image_path, caption=caption)
            st.success("Image posted to Instagram!")
        except Exception as e:
            st.error(f"Instagram upload failed: {e}")

    # ----------------------- TWEET -----------------------
    def tweet_on_twitter(tweet_texts):
        try:
            client = tweepy.Client(
                consumer_key=twitter_api_key,
                consumer_secret=twitter_apikey_secret,
                access_token=twitter_access_token,
                access_token_secret=twitter_access__token_secret
            )
            for i, text in enumerate(tweet_texts):
                client.create_tweet(text=text)
                st.success(f"Tweet #{i+1} posted: {text}")
        except Exception as e:
            st.error(f"Twitter Error: {e}")

    # ----------------------- WEB SCRAPING -----------------------
    def web_scraping(url):
        url =url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        st.subheader("Title:")
        st.write(soup.title.string)

        paragraphs = soup.find_all('p')
        full_text = "\n".join(p.get_text() for p in paragraphs)
        st.subheader("Page Content:")
        st.write(full_text[:1000])

        links = [a['href'] for a in soup.find_all('a', href=True)]
        st.subheader("Sample Links:")
        st.write(links[:10])


    # ----------------------- STREAMLIT UI -----------------------
    st.title("Automation Hub: Mail, WhatsApp, Twitter, Instagram, Google Search, Web Scraping")

    option = st.sidebar.selectbox(
        "Choose Task",
        ("Search on Google", "Send Email", "Send WhatsApp Message", "Post on Instagram", "Tweet", "Web Scraping")
    )

    if option == "Search on Google":
        query = st.text_input("Enter your search query:")
        if st.button("Search"):
            search_on_google(query)

    elif option == "Send Email":
        to = st.text_input("Receiver Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message")
        if st.button("Send Email"):
            send_mail(to, subject, message)

    elif option == "Send WhatsApp Message":
        phone = st.text_input("Phone Number (e.g., +911234567890)")
        msg = st.text_area("Message")
        now = datetime.datetime.now()
        hour = st.number_input("Hour (24-hr format)", min_value=0, max_value=23, value=now.hour)
        minute = st.number_input("Minute", min_value=0, max_value=59, value=now.minute + 2)
        if st.button("Schedule Message"):
            send_whatsapp(phone, msg, hour, minute)

    elif option == "Post on Instagram":
        image = st.file_uploader("Upload Image", type=["jpg", "png"])
        caption = st.text_input("Caption")
        if st.button("Post to Instagram"):
            if image is not None:
                with open("temp_img.jpg", "wb") as f:
                    f.write(image.read())
                post_on_instagram("temp_img.jpg", caption)
            else:
                st.warning("Please upload an image.")

    elif option == "Tweet":
        num = st.number_input("How many tweets?", min_value=1, max_value=5, value=1)
        tweet_list = [st.text_input(f"Tweet #{i+1}") for i in range(num)]
        if st.button("Post Tweets"):
            tweet_on_twitter(tweet_list)

    elif option == "Web Scraping":
        url =  st.text_input("Enter a URL to scrap",value="https://en.wikipedia.org/wiki/Web_scraping")
        if st.button("Scrape Wikipedia Page"):
            web_scraping(url)
