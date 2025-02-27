import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv

class GeminiHelper:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Get API key with better error handling
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            st.error("Please set your GEMINI_API_KEY in the .env file")
            raise ValueError("GEMINI_API_KEY environment variable is not properly set")

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
            # Prompt focused on code-only response
            context = f"""As an expert {programming_language} developer, provide ONLY working code example for this question:

            Question: {prompt}

            Rules:
            - Provide ONLY the code solution
            - Include brief comments in the code to explain key parts
            - Wrap the code in appropriate markdown code blocks
            - No explanations or text outside the code block
            """

            # Generate response
            response = self.model.generate_content(context)

            if not response:
                return "Sorry, I couldn't generate code. Please try rephrasing your question."

            # Extract text from response
            if hasattr(response, 'text'):
                return self.extract_code_blocks(response.text)
            elif hasattr(response, 'parts'):
                return self.extract_code_blocks(response.parts[0].text)
            else:
                return "No code could be generated. Please try again."

        except Exception as e:
            error_msg = str(e)
            st.error(f"Error generating response: {error_msg}")
            return "An error occurred while processing your request. Please try again."

    def extract_code_blocks(self, response):
        if not response:
            return "No code received"

        try:
            # Extract only code blocks from the response
            lines = response.split('\n')
            code_blocks = []
            in_code_block = False
            current_block = []

            for line in lines:
                if line.strip().startswith('```'):
                    if in_code_block:
                        current_block.append(line)
                        code_blocks.append('\n'.join(current_block))
                        current_block = []
                        in_code_block = False
                    else:
                        in_code_block = True
                        current_block = [line]
                elif in_code_block:
                    current_block.append(line)

            if current_block:  # Handle any remaining code block
                code_blocks.append('\n'.join(current_block))

            # Return only the code blocks
            return '\n\n'.join(code_blocks) if code_blocks else "No code blocks found in the response"

        except Exception as e:
            st.warning(f"Error extracting code: {str(e)}")
            return response