import google.generativeai as genai
import streamlit as st
import os

class GeminiHelper:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY", "your-default-key")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def get_code_response(self, prompt, programming_language=None):
        try:
            context = f"You are an expert {programming_language} developer. " if programming_language else ""
            full_prompt = context + prompt
            
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            st.error(f"Error getting response from Gemini: {str(e)}")
            return None

    def format_code_response(self, response):
        if not response:
            return ""
        
        # Basic formatting for code blocks
        formatted_response = response.replace("```", "")
        return formatted_response
