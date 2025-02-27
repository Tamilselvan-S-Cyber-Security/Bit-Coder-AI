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
    page_title="Bit-Coder-AI  ",
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
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = None
if 'execute_code' not in st.session_state:
    st.session_state.execute_code = False


# Main header
st.markdown('<h1 class="main-header">🧠Bit-Coder-AI 🤖</h1>', unsafe_allow_html=True)

# Sidebar with programming languages
st.sidebar.title("Programming Languages")
for category, languages in PROGRAMMING_LANGUAGES.items():
    st.sidebar.markdown(f"### {category}")
    for lang, desc in languages.items():
        st.sidebar.markdown(f"- **{lang}**: {desc}")

# Voice commands help section in sidebar
st.sidebar.markdown("### Voice Commands")
st.sidebar.info(st.session_state.audio_handler.get_command_help())

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Ask Your Coding Question")

    # Text input for questions
    user_question = st.text_area("Type your question here:", height=100)

    # Voice input section with enhanced feedback
    voice_col1, voice_col2 = st.columns([1, 2])
    with voice_col1:
        if st.button("🎤 Use Voice Input", key="voice_button", help="Click to speak your command"):
            with st.spinner("Listening..."):
                command_result = st.session_state.audio_handler.listen_to_audio()
                if command_result:
                    # Update language if specified in voice command
                    if command_result['language']:
                        st.session_state.selected_language = command_result['language']

                    # Update question field with the voice input
                    user_question = command_result['query']

                    # Handle specific command types
                    if command_result['command_type'] == 'execute' and st.session_state.current_code:
                        st.session_state.execute_code = True

    with voice_col2:
        st.info("🎙️ Click the button and speak your command")

    # Language selection
    selected_language = st.selectbox(
        "Select Programming Language",
        options=[lang for category in PROGRAMMING_LANGUAGES.values() for lang in category.keys()],
        index=list(PROGRAMMING_LANGUAGES['Backend Languages'].keys()).index('Python') if 'Backend Languages' in PROGRAMMING_LANGUAGES and 'Python' in PROGRAMMING_LANGUAGES['Backend Languages'] else 0,
        key='language_selector'
    )
    st.session_state.selected_language = selected_language

    # Generate response
    if st.button("Get Answer", key="generate_button") or user_question:
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

        # Execute/Preview button with appropriate label
        button_label = "🔍 Preview" if selected_language in ['HTML', 'CSS'] else "▶️ Run Code"
        if st.button(button_label, key="execute_button") or st.session_state.get('execute_code', False):
            with st.spinner("Processing code..."):
                success, result = CodeExecutor.execute_code(edited_code, selected_language)
                st.session_state.execution_result = {
                    'success': success,
                    'output': result
                }
                st.session_state.execute_code = False

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
    - Use voice commands for quick actions
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
