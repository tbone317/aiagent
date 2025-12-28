from email import parser
import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types

def main():
    load_dotenv()
    print("Hello from aiagent!")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,)
    
    if response.usage_metadata:
        if args.verbose:
            print(f"User prompt: {messages[0].parts[0].text}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print("Response from Gemini API:")
        print(response.text)
    else:
        raise RuntimeError("No usage metadata found in the response.")
if __name__ == "__main__":
    main()
