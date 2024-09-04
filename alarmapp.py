from datetime import datetime, time as dt_time, timedelta
import time
from gtts import gTTS
import pygame
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from threading import Thread, Event

GEMINI_API_KEY = "YOUR_API_KEY"  # Replace with your Gemini API key

# Global event to control alarm stopping
stop_alarm_event = Event()

# Hard-coded track path
TRACK_PATH = "/home/durga/Desktop/alarm alert/WhatsApp Audio 2024-09-03 at 12.26.10.mpga"  # Replace with the path to your track

def initialize_pygame():
    pygame.mixer.init()

def play_audio(file_path):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
    except Exception as e:
        st.error(f"Error playing audio: {e}")

def stop_alarm():
    stop_alarm_event.set()
    pygame.mixer.music.stop()
    st.session_state.stop_alarm_requested = False
    st.success("Alarm stopped by user.")

def listen_for_stop():
    while True:
        if stop_alarm_event.is_set():
            break
        time.sleep(1)  # Check every second

def schedule_alarm(alarm_time):
    initialize_pygame()
    
    # Start a separate thread to listen for user input to stop the alarm
    stop_listener_thread = Thread(target=listen_for_stop, daemon=True)
    stop_listener_thread.start()
    
    while not stop_alarm_event.is_set():
        current_time = datetime.now()
        if current_time >= alarm_time:
            st.write("Alarm! Playing the specified track.")
            
            # Play the alarm track
            try:
                if TRACK_PATH:
                    play_audio(TRACK_PATH)
                else:
                    tts = gTTS(text="No track provided. Default message.", lang='en')
                    tts.save("default_alarm.mp3")
                    play_audio("default_alarm.mp3")
            except Exception as e:
                st.error("Error during alarm setup. Playing default message.")
                tts = gTTS(text="Error playing track. Default message.", lang='en')
                tts.save("default_alarm.mp3")
                play_audio("default_alarm.mp3")
            
            # Wait for the alarm duration or until stopped
            while pygame.mixer.music.get_busy() and not stop_alarm_event.is_set():
                time.sleep(1)  # Check every second
            break
        time.sleep(60)  # Check every minute

def get_generated_message(prompt):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        google_api_key=GEMINI_API_KEY,
    )
    try:
        # Correctly pass a list of HumanMessage objects
        messages = [HumanMessage(content=prompt)]  # Ensure this is a list
        response = llm.generate(messages=messages)  # Pass the correct parameter name

        # Check if generations exist to avoid NoneType errors
        if response and response.generations:
            return response.generations[0].text
        else:
            return "Error generating message"
    except ValueError as e:
        return "Error generating message"
    except Exception as e:
        return "Error generating message"

def main():
    st.title("Alarm Application")

    # Initialize session state for stop alarm request
    if 'stop_alarm_requested' not in st.session_state:
        st.session_state.stop_alarm_requested = False

    # Input fields for user to enter details
    alarm_date = st.date_input("Enter the date for the alarm:")
    alarm_time = st.time_input("Enter the time for the alarm:", value=dt_time(0, 0), step=60)  # Set step to 60 seconds

    # Layout for buttons side by side
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Set Alarm"):
            if alarm_date and alarm_time:
                try:
                    alarm_datetime = datetime.combine(alarm_date, alarm_time)
                    
                    generated_message = get_generated_message(
                        f"Create an alert message for setting an alarm to play this track: {TRACK_PATH}"
                    )
                    
                    if generated_message != "Error generating message":
                        st.write(f"Generated alert message: {generated_message}")
                    else:
                        st.write("")
                        
                    # Reset the stop_alarm_event
                    stop_alarm_event.clear()
                    
                    alarm_thread = Thread(target=schedule_alarm, args=(alarm_datetime,))
                    alarm_thread.start()
                    st.success(f"Alarm set for {alarm_datetime}.")
                except ValueError:
                    st.error("Invalid date or time format. Please ensure the inputs are correct.")

    with col2:
        if st.button("Stop Alarm"):
            st.session_state.stop_alarm_requested = True
            stop_alarm()

if __name__ == "__main__":
    main()
