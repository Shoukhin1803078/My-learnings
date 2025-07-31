import os

def secret_key_extraction():
    secret_key = os.getenv("GEMINI_API_KEY")
    return secret_key



if __name__== "__main__":
#   x=secret_key_extraction()
    secret_key = os.getenv("GEMINI_API_KEY")
    print(secret_key)