# LLM test/test_groq_api.py

import os
from dotenv import load_dotenv
from groq import Groq, GroqError

# Instructions:
# 1. Make sure you have the 'groq' and 'python-dotenv' libraries installed:
#    pip install groq python-dotenv
# 2. Create a .env file in the same directory as this script (or in your project root).
# 3. Add your Groq API key to the .env file like this:
#    GROQ_API_KEY=your_actual_api_key_here

def test_groq_api_key():
    """
    Tests the Groq API key by making a simple API call.
    """
    try:
        # Load environment variables from .env file
        # Ensure .env is in the same directory as this script, or specify path
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if not os.path.exists(dotenv_path):
            # Fallback to checking project root if .env not next to script
            project_root_dotenv_path = os.path.join(os.getcwd(), '.env')
            if os.path.exists(project_root_dotenv_path):
                load_dotenv(project_root_dotenv_path)
            else:
                print(f"Warning: .env file not found at {dotenv_path} or {project_root_dotenv_path}")
        else:
            load_dotenv(dotenv_path)

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            print("Error: GROQ_API_KEY not found in environment variables.")
            print("Please ensure it's set in your .env file (e.g., in the LLM test/ directory or project root) or system environment.")
            return

        # Print partial key for verification, ensuring key is long enough
        if len(api_key) > 10:
            print(f"Found GROQ_API_KEY: {api_key[:5]}...{api_key[-5:]}")
        else:
            print("Found GROQ_API_KEY (key is too short to abbreviate).")


        client = Groq(api_key=api_key)

        print("Attempting to create a chat completion with Groq...")
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Explain briefly what Groq is.",
                }
            ],
            model="llama3-8b-8192", # Using a common small model
            temperature=0.7,
            max_tokens=100,
        )

        response_content = chat_completion.choices[0].message.content
        print("\nGroq API call successful!")
        print("Response:")
        print(response_content)

    except GroqError as e:
        print(f"\nGroq API Error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Status Code: {e.response.status_code}")
            try:
                error_details = e.response.json()
                print(f"Error Details: {error_details}")
            except Exception: # If parsing JSON fails
                print(f"Raw Error Response: {e.response.text}")
        elif hasattr(e, 'status_code'): # For errors that might not have a full response object
             print(f"Status Code: {e.status_code}")
        # Add more specific error handling if needed
        if "authentication" in str(e).lower():
            print("Hint: This might be an issue with your API key. Double-check it.")


    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    test_groq_api_key()
