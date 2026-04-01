# main.py
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

# 1️⃣ Load environment variables from .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# 2️⃣ Initialize the AI client
client = ChatGroq(
    model="llama-3.1-8",
    api_key=api_key
)

# 3️⃣ Simple chat loop
print("🤖 Chatbot is ready! Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    try:
        # Get AI response
        response = client.chat(user_input)
        print(f"🤖 AI: {response}")
    except Exception as e:
        print(f"🤖 AI Error: {e}")