import streamlit as st
from message_reflector import message_reflector
import time
import uuid
st.title("Message Reflector")

if "id" not in st.session_state:
    st.session_state["id"] = "1"
if "message" not in st.session_state:
    st.session_state["message"] = "Hello2"

print(st.session_state["id"])
print(st.session_state["message"])

if message:= message_reflector(st.session_state["message"], st.session_state["id"], delay_ms=10000):
    st.write(f"Received message: {message}")
else:
    st.write("No message")  


if st.button("Reflect Message"):
    st.session_state["id"] = str(uuid.uuid4())
    st.session_state["message"] = f"Hello {time.time()}"
    #st.rerun()

st.button("Refresh")


