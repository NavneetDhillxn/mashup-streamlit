import streamlit as st
from youtubepy import Video
import os
import smtplib
from youtube_search import YoutubeSearch
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from moviepy.editor import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()
# email_main=os.getenv("EMAIL_MAIN")
# pass_key = os.getenv("PASS_KEY")
email_main="nsingh2_be20@thapar.edu"
pass_key ="inztevbxnieinayc"


def send_email_with_attachment(email, password, to, subject, body, file_path):
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(body))

    with open(file_path, "rb") as f:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(f.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', "attachment; filename= %s" % file_path)
    msg.attach(attachment)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, to, msg.as_string())
    server.quit()

def createmash(Singer,num,dur):
    filedir=os.getcwd()
    files=os.listdir(filedir)

    print(files)
    mp3_files = [file for file in files if file.endswith('.mp3')]

    for i in mp3_files:
        os.remove(i)

    results = YoutubeSearch(Singer, max_results=int(num)).to_dict()

    for i in results:
        try:
            video = YouTube('http://youtube.com/watch?v='+i['id']).streams.filter(only_audio=True).first().download()
        
        except VideoUnavailable:
            pass  # Skip videos that can't be loaded
        else:
            base, ext = os.path.splitext(video)
            new_file = base + '.mp3'
            os.rename(video, new_file)

    filedir=os.getcwd()
    files=os.listdir(filedir)

    print(files)
    mp3_files = [file for file in files if file.endswith('.mp3')]

    ad = AudioFileClip(mp3_files[0])
    merged_audio=ad.subclip(0,0)

    time=int(dur)
    for i in range(0,len(mp3_files)):
        audio = AudioFileClip(mp3_files[i])
        trimmed_audio = audio.subclip(10, time+10)
        merged_audio = concatenate_audioclips([merged_audio, trimmed_audio])

    merged_audio.write_audiofile("output.mp3")
    return os.getcwd()+"/output.mp3"


st.set_page_config(page_title="MASHIT")
st.subheader("MASHUP CREATOR")

st.write("Enter details: ")

with st.form("my_form"):
   Singer = st.text_input("Singer Name")
   num = st.text_input("Number of songs")
   dur = st.text_input("Audio duration")
   rec_email = st.text_input("Enter Email")
   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       output=createmash(Singer,num,dur)
       email = email_main
       password = pass_key
       to = rec_email
       subject = "Email with Attachment from Streamlit app"
       body = "This is a test email with attachment sent from a Streamlit app."
       file_path = os.getcwd()+"/output.mp3"
       send_email_with_attachment(email, password, to, subject, body, file_path)
       st.subheader("MAIL sent")

