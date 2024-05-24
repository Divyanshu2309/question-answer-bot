import openai
import time
import hashlib
import json

openai.api_key = "sk-proj-yCMzaixDSxiPpRB3Bb3gT3BlbkFJqJGbKYIt8dhvCHmdXpHb"

# Simple cache dictionary
cache = {}

def get_cache_key(prompt):
    return hashlib.sha256(prompt.encode()).hexdigest()

def chat_with_gpt(prompt):
    cache_key = get_cache_key(prompt)
    
    # Check if response is in cache
    if cache_key in cache:
        return cache[cache_key]
    
    retries = 5
    for i in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            response_content = response.choices[0].message["content"].strip()
            
            # Store response in cache
            cache[cache_key] = response_content
            return response_content
        except openai.error.RateLimitError:
            wait_time = min(2 ** i, 32)  # Exponential backoff with a max wait time of 32 seconds
            print(f"Rate limit exceeded. Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
        except openai.error.OpenAIError as e:
            print(f"An error occurred: {e}")
            break
    return "Sorry, I'm currently unable to process your request due to rate limits."

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        response = chat_with_gpt(user_input)
        print("Chatbot: ", response)
