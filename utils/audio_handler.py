import speech_recognition as sr
import streamlit as st
from typing import Tuple, Optional, Dict
import re

class AudioHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.command_patterns = {
            'generate': r'(?i)generate|create|write|make',
            'execute': r'(?i)run|execute|start',
            'explain': r'(?i)explain|describe|tell me about',
            'language': r'(?i)in (python|javascript|ruby|php|html|css)',
            'modify': r'(?i)modify|change|update|edit'
        }

    def parse_command(self, text: str) -> Dict[str, str]:
        """Parse voice input into structured command components"""
        command_type = None
        language = None
        query = text

        # Extract programming language if specified
        lang_match = re.search(r'(?i)in (python|javascript|ruby|php|html|css)', text)
        if lang_match:
            language = lang_match.group(1).title()
            query = text.replace(lang_match.group(0), '').strip()

        # Determine command type
        for cmd_type, pattern in self.command_patterns.items():
            if re.search(pattern, text):
                command_type = cmd_type
                break

        return {
            'command_type': command_type,
            'language': language,
            'query': query
        }

    def listen_to_audio(self) -> Optional[Dict[str, str]]:
        """
        Listen and process voice input with improved error handling and feedback
        """
        try:
            with sr.Microphone() as source:
                # Visual feedback
                st.write("🎤 Listening... Speak your command")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)

                st.write("Processing your command...")

                try:
                    # Use Google's speech recognition
                    text = self.recognizer.recognize_google(audio)
                    st.success(f"Recognized: {text}")

                    # Parse the command
                    command = self.parse_command(text)

                    # Provide feedback on command interpretation
                    if command['command_type']:
                        st.info(f"Command type: {command['command_type']}")
                    if command['language']:
                        st.info(f"Language detected: {command['language']}")

                    return command

                except sr.UnknownValueError:
                    st.error("Sorry, I couldn't understand the audio")
                except sr.RequestError:
                    st.error("Sorry, there was an error with the speech recognition service")

        except Exception as e:
            st.error(f"Error accessing microphone: {str(e)}")
            st.info("Please check if your microphone is properly connected and permissions are granted")

        return None

    def get_command_help(self) -> str:
        """Return help text for available voice commands"""
        return """
        Voice Command Examples:
        - "Generate a function to calculate fibonacci in Python"
        - "Run this code"
        - "Explain how this code works"
        - "Change the language to JavaScript"
        - "Create a login form in HTML"
        """