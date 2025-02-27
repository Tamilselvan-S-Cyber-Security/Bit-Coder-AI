import google.generativeai as genai
import streamlit as st
import os

class GeminiHelper:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        # Configure the Google Generative AI
        try:
            genai.configure(api_key=api_key)

            # List available models to verify configuration
            model_list = genai.list_models()
            self.model = None

            # Find and select the correct model
            for model in model_list:
                if 'gemini-pro' in model.name:
                    self.model = genai.GenerativeModel(model.name)
                    break

            if not self.model:
                raise ValueError("Gemini Pro model not found in available models")

        except Exception as e:
            st.error(f"Failed to initialize Gemini model: {str(e)}")
            raise

    def get_code_response(self, prompt, programming_language=None):
        try:
            # Enhanced prompt formatting
            context = f"""You are an expert {programming_language} developer. 
            Please help with the following question:

            Question: {prompt}

            Please format your response as follows:
            1. Brief explanation
            2. Code example with comments
            3. Key points to remember

            Use markdown code blocks for any code."""

            # Generate response with proper error handling
            response = self.model.generate_content(context)

            if hasattr(response, 'text'):
                return self.format_code_response(response.text)
            elif hasattr(response, 'parts'):
                return self.format_code_response(response.parts[0].text)
            else:
                return "I apologize, but I couldn't generate a response. Please try rephrasing your question."

        except Exception as e:
            error_msg = str(e)
            st.error(f"Error generating response: {error_msg}")
            return f"I encountered an error while processing your request: {error_msg}. Please try again."

    def format_code_response(self, response):
        if not response:
            return ""

        try:
            # Split response into sections
            formatted_lines = []
            current_block = []
            in_code_block = False

            for line in response.split('\n'):
                if line.strip().startswith('```'):
                    if in_code_block:
                        current_block.append(line)
                        formatted_lines.append('\n'.join(current_block))
                        current_block = []
                        in_code_block = False
                    else:
                        in_code_block = True
                        current_block = [line]
                else:
                    if in_code_block:
                        current_block.append(line)
                    else:
                        formatted_lines.append(line)

            # Handle any remaining code block
            if current_block:
                formatted_lines.append('\n'.join(current_block))

            return '\n'.join(formatted_lines)

        except Exception as e:
            st.warning(f"Error formatting response: {str(e)}")
            return response