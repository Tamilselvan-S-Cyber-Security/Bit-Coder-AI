import subprocess
import tempfile
import os
import streamlit as st
from typing import Tuple, Optional

class CodeExecutor:
    SUPPORTED_LANGUAGES = {
        'Python': {
            'extension': '.py',
            'command': 'python',
            'timeout': 10
        },
        'JavaScript': {
            'extension': '.js',
            'command': 'node',
            'timeout': 10
        }
    }

    @staticmethod
    def execute_code(code: str, language: str) -> Tuple[bool, str]:
        """
        Execute code in a safe environment and return the result
        """
        if language not in CodeExecutor.SUPPORTED_LANGUAGES:
            return False, f"Language {language} is not supported"

        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(
                suffix=CodeExecutor.SUPPORTED_LANGUAGES[language]['extension'],
                mode='w',
                delete=False
            ) as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name

            # Execute the code
            command = [CodeExecutor.SUPPORTED_LANGUAGES[language]['command'], temp_file_path]
            timeout = CodeExecutor.SUPPORTED_LANGUAGES[language]['timeout']
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            # Clean up
            os.unlink(temp_file_path)

            # Return results
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, f"Error: {result.stderr}"

        except subprocess.TimeoutExpired:
            return False, f"Execution timed out after {timeout} seconds"
        except Exception as e:
            return False, f"Execution error: {str(e)}"
