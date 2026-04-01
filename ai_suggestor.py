import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# ---------- LOAD ENV (FIXED PATH) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "..", ".env"))

# Debug (remove later if you want)
api_key = os.getenv("GROQ_API_KEY")
print("DEBUG GROQ KEY:", api_key)


# ---------- AI MODEL ----------
def get_model():
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Check your .env file.")

    return ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=api_key
    )


# ---------- CODE ANALYZER AI ----------
prompt_template = PromptTemplate(
    input_variables=["code_string"],
    template="""
You are an experienced coding teacher. Analyze the following code:

{code_string}

Explain:
1. Possible improvements
2. Errors (if any)
3. Time complexity
4. Space complexity
"""
)


def get_ai_suggestion(code_string):
    try:
        model = get_model()

        formatted_prompt = prompt_template.format(
            code_string=code_string
        )

        response = model.invoke(formatted_prompt)

        return response.content

    except Exception as e:
        return f"AI Error: {str(e)}"


# ---------- CHATBOT ----------
def chat_with_ai_bot(user_input):
    try:
        model = get_model()

        prompt = f"""
You are a helpful AI coding assistant.
Give clear, short, and helpful answers.

User: {user_input}
"""

        response = model.invoke(prompt)

        return response.content

    except Exception as e:
        return f"AI Error: {str(e)}"