import subprocess
import tempfile
import os
import streamlit as st
from typing import Tuple, Optional

class CodeExecutor:
    SUPPORTED_LANGUAGES = {
        'Python': {
            'extension': '.py',
            'command': 'python3',  # Changed from 'python' to 'python3'
            'timeout': 10
        },
        'JavaScript': {
            'extension': '.js',
            'command': 'node',
            'timeout': 10
        },
        'HTML': {
            'extension': '.html',
            'type': 'markup',
            'timeout': 5
        },
        'CSS': {
            'extension': '.css',
            'type': 'markup',
            'timeout': 5
        },
        'Ruby': {
            'extension': '.rb',
            'command': 'ruby',
            'timeout': 10
        },
        'PHP': {
            'extension': '.php',
            'command': 'php',
            'timeout': 10
        }
    }

    @staticmethod
    def execute_code(code: str, language: str) -> Tuple[bool, str]:
        """
        Execute code in a safe environment and return the result
        """
        if language not in CodeExecutor.SUPPORTED_LANGUAGES:
            return False, f"Language {language} is not currently supported"

        try:
            lang_config = CodeExecutor.SUPPORTED_LANGUAGES[language]

            # Special handling for HTML/CSS
            if lang_config.get('type') == 'markup':
                return True, code  # Return the markup directly for rendering

            # Create a temporary file
            with tempfile.NamedTemporaryFile(
                suffix=lang_config['extension'],
                mode='w',
                delete=False
            ) as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name

            try:
                # Execute the code with proper error handling
                command = [lang_config['command'], temp_file_path]
                timeout = lang_config['timeout']

                # Add current working directory to PYTHONPATH for Python imports
                env = os.environ.copy()
                if language == 'Python':
                    env['PYTHONPATH'] = os.getcwd()

                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env=env
                )

                # Clean up
                os.unlink(temp_file_path)

                if result.returncode == 0:
                    return True, result.stdout.strip() or "Code executed successfully (no output)"
                else:
                    error_msg = result.stderr.strip()
                    return False, f"Error: {error_msg}"

            except subprocess.TimeoutExpired:
                os.unlink(temp_file_path)
                return False, f"Execution timed out after {timeout} seconds"
            except FileNotFoundError:
                os.unlink(temp_file_path)
                return False, f"Runtime for {language} is not installed. Please install {language} to execute this code."
            except Exception as e:
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                return False, f"Execution error: {str(e)}"

        except Exception as e:
            return False, f"Setup error: {str(e)}"

    @staticmethod
    def render_markup(code: str, language: str) -> str:
        """
        Prepare HTML/CSS code for rendering
        """
        if language == 'HTML':
            return code
        elif language == 'CSS':
            return f"<style>{code}</style>"
        return code