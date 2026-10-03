import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions
import json


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    if api_key is None:
        raise RuntimeError("Api key not found")
    
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )   
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model = "openrouter/free",
        messages = messages,
        # temperature = 0,
        tools = available_functions,
    )
    
    if response.usage is not None:
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        
        if args.verbose:  
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {completion_tokens}")
    else:
        raise RuntimeError("Response usage is not found")
    
    
    message = response.choices[0].message
    print("Response:")        
    
    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
    else:
        print(response.choices[0].message.content)
    


if __name__ == "__main__":
    main()

