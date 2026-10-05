import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import sys

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
    
    for _ in range(20):
        
        response = client.chat.completions.create(
            model = "openrouter/free",
            messages = messages,
            temperature = 0,
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
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call , args.verbose)
                messages.append(result_message)
                
                if result_message["content"] == "":
                    print("Error: content is empty")
                    sys.exit(1)
   
                if args.verbose:
                    print(f"-> {result_message['content']}")
                                     
        else:
            print("Response:")  
            print(message.content)
            return 
            
    print("Error: maximum iterations reached")
    sys.exit(1)
            
    


if __name__ == "__main__":
    main()

