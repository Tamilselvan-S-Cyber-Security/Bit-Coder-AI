import google.generativeai as genai
import streamlit as st
import os

class GeminiHelper:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def get_code_response(self, prompt, programming_language=None):
        try:
            # Enhanced prompt formatting
            context = f"""You are an expert {programming_language} developer providing clear, practical code examples.
            Please provide a solution for the following question:
            {prompt}

            Format your response with:
            1. A brief explanation
            2. Code example
            3. Key points to remember
            """

            response = self.model.generate_content(context)

            if not response or not response.text:
                return "I apologize, but I couldn't generate a response. Please try rephrasing your question."

            return self.format_code_response(response.text)

        except Exception as e:
            st.error(f"Error: {str(e)}")
            return f"I encountered an error while processing your request. Please try again."

    def format_code_response(self, response):
        if not response:
            return ""

        # Preserve code blocks and formatting
        formatted_response = response
        if "```" not in formatted_response:
            # If no code blocks are present, try to format any code-like content
            lines = formatted_response.split('\n')
            formatted_lines = []
            in_code_block = False

            for line in lines:
                if line.strip().startswith('def ') or line.strip().startswith('class ') or line.strip().startswith('import '):
                    if not in_code_block:
                        formatted_lines.append('```python')
                        in_code_block = True
                elif in_code_block and not line.strip():
                    formatted_lines.append('```')
                    in_code_block = False
                formatted_lines.append(line)

            if in_code_block:
                formatted_lines.append('```')
            formatted_response = '\n'.join(formatted_lines)

        return formatted_response