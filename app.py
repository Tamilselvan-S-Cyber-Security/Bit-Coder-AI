import streamlit as st
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from utils.audio_handler import AudioHandler
from utils.gemini_helper import GeminiHelper
from utils.code_executor import CodeExecutor
from assets.programming_info import PROGRAMMING_LANGUAGES, DEVELOPER_BIO

# Page configuration
st.set_page_config(
    page_title="AI Coding Assistant - Bit-Coder Developers",
    page_icon="🤖",
    layout="wide"
)

# Load custom CSS
with open("styles/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if 'audio_handler' not in st.session_state:
    st.session_state.audio_handler = AudioHandler()
if 'gemini_helper' not in st.session_state:
    st.session_state.gemini_helper = GeminiHelper()
if 'current_code' not in st.session_state:
    st.session_state.current_code = ""
if 'execution_result' not in st.session_state:
    st.session_state.execution_result = None

# Main header
st.markdown('<h1 class="main-header">AI Coding Assistant</h1>', unsafe_allow_html=True)

# Sidebar with programming languages
st.sidebar.title("Programming Languages")
for category, languages in PROGRAMMING_LANGUAGES.items():
    st.sidebar.markdown(f"### {category}")
    for lang, desc in languages.items():
        st.sidebar.markdown(f"- **{lang}**: {desc}")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Ask Your Coding Question")

    # Text input for questions
    user_question = st.text_area("Type your question here:", height=100)

    # Voice input button
    if st.button("🎤 Use Voice Input", key="voice_button", help="Click to speak your question"):
        with st.spinner("Listening..."):
            voice_text = st.session_state.audio_handler.listen_to_audio()
            if voice_text:
                user_question = voice_text
                st.text_area("Your voice input:", value=voice_text, height=100)

    # Language selection
    selected_language = st.selectbox(
        "Select Programming Language",
        options=[lang for category in PROGRAMMING_LANGUAGES.values() for lang in category.keys()]
    )

    # Generate response
    if st.button("Get Answer", key="generate_button"):
        if user_question:
            with st.spinner("Generating response..."):
                response = st.session_state.gemini_helper.get_code_response(
                    user_question,
                    selected_language
                )
                if response:
                    st.markdown("### Generated Code:")
                    st.code(response, language=selected_language.lower())
                    st.session_state.current_code = response

    # Code execution section
    if st.session_state.current_code:
        st.markdown("### Code Execution")
        edited_code = st.text_area(
            "Edit code before execution:",
            value=st.session_state.current_code,
            height=200
        )

        # Execute/Preview button
        button_label = "🔍 Preview" if selected_language in ['HTML', 'CSS'] else "▶️ Run Code"
        if st.button(button_label, key="execute_button"):
            with st.spinner("Processing code..."):
                success, result = CodeExecutor.execute_code(edited_code, selected_language)
                st.session_state.execution_result = {
                    'success': success,
                    'output': result
                }

        # Display results
        if st.session_state.execution_result:
            st.markdown("### Result:")
            if selected_language in ['HTML', 'CSS']:
                st.markdown("#### Preview:")
                st.markdown(CodeExecutor.render_markup(
                    st.session_state.execution_result['output'],
                    selected_language
                ), unsafe_allow_html=True)
            else:
                if st.session_state.execution_result['success']:
                    st.code(st.session_state.execution_result['output'])
                else:
                    st.error(st.session_state.execution_result['output'])

with col2:
    st.markdown("### Quick Tips")
    st.info("""
    - Be specific in your questions
    - Include relevant context
    - Use code execution to test solutions
    - Edit code before running if needed
    - For HTML/CSS, use preview to see results
    """)

    # Loading animation for visual feedback
    with st.empty():
        if st.session_state.get('is_generating', False):
            with st.spinner("Generating response..."):
                time.sleep(0.1)

# Developer Bio Section
st.markdown('<div class="bio-section">', unsafe_allow_html=True)
st.markdown(DEVELOPER_BIO)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Made with ❤️ by Bit-Coder Developers</p>
    </div>
    """,
    unsafe_allow_html=True
)