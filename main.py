from email import parser
import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

def main():
    load_dotenv()

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
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt,
                                            tools=[available_functions]),
        )
    
    if response.usage_metadata:
        if args.verbose:
            print(f"User prompt: {messages[0].parts[0].text}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print("Response from Gemini API:")
        
        if response.function_calls:
            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
        if response.text:
            print(response.text)
        
    else:
        raise RuntimeError("No usage metadata found in the response.")
if __name__ == "__main__":
    main()
