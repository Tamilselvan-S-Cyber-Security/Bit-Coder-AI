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

            # Initialize with gemini-1.5-flash model
            self.model = genai.GenerativeModel('gemini-1.5-flash')

            # Test the model initialization
            response = self.model.generate_content("Test connection")
            if not response:
                raise ValueError("Failed to initialize Gemini model")

        except Exception as e:
            st.error(f"Failed to initialize Gemini model: {str(e)}")
            self.model = None

    def get_code_response(self, prompt, programming_language=None):
        if not self.model:
            return "The AI model is not properly initialized. Please try again later."

        try:
            # Enhanced prompt formatting
            context = f"""As an expert {programming_language} developer, please help with this question:

            Question: {prompt}

            Format your response with:
            1. Brief explanation
            2. Code example with comments
            3. Key points to remember

            Please use Markdown code blocks for code examples."""

            # Generate response
            response = self.model.generate_content(context)

            if not response:
                return "Sorry, I couldn't generate a response. Please try rephrasing your question."

            # Extract text from response
            if hasattr(response, 'text'):
                return self.format_code_response(response.text)
            elif hasattr(response, 'parts'):
                return self.format_code_response(response.parts[0].text)
            else:
                return "Received an invalid response format. Please try again."

        except Exception as e:
            error_msg = str(e)
            st.error(f"Error generating response: {error_msg}")
            return "An error occurred while processing your request. Please try again."

    def format_code_response(self, response):
        if not response:
            return "No response received"

        try:
            # Format code blocks and preserve markdown
            lines = response.split('\n')
            formatted_lines = []
            in_code_block = False
            code_block_lines = []

            for line in lines:
                if line.strip().startswith('```'):
                    if in_code_block:
                        code_block_lines.append(line)
                        formatted_lines.append('\n'.join(code_block_lines))
                        code_block_lines = []
                        in_code_block = False
                    else:
                        in_code_block = True
                        code_block_lines = [line]
                else:
                    if in_code_block:
                        code_block_lines.append(line)
                    else:
                        formatted_lines.append(line)

            if code_block_lines:  # Handle any remaining code block
                formatted_lines.append('\n'.join(code_block_lines))

            return '\n'.join(formatted_lines)

        except Exception as e:
            st.warning(f"Error formatting response: {str(e)}")
            return response