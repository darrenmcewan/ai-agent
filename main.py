import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    
    if len(sys.argv) > 1:
        contents = sys.argv[1]    
        model = 'gemini-2.0-flash-001'

        messages = [types.Content(role="user", parts=[types.Part(text=contents)]),]

        response = client.models.generate_content(model=model, contents=messages)
        
        if sys.argv[2] == '--verbose':
            print(f"User prompt: {sys.argv[1]}")
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        else:
            print(response.text)
    else: 
        print("No argument provided. Using default content")
        sys.exit(1)

if __name__ == "__main__":
    main()
