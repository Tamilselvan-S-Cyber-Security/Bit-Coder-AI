import speech_recognition as sr
import streamlit as st

class AudioHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen_to_audio(self):
        try:
            with sr.Microphone() as source:
                st.write("🎤 Listening... Speak your question")
                audio = self.recognizer.listen(source, timeout=5)
                st.write("Processing your speech...")
                
                try:
                    text = self.recognizer.recognize_google(audio)
                    return text
                except sr.UnknownValueError:
                    st.error("Sorry, I couldn't understand the audio")
                except sr.RequestError:
                    st.error("Sorry, there was an error with the speech recognition service")
                
        except Exception as e:
            st.error(f"Error accessing microphone: {str(e)}")
        
        return None
