import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

# Initialize model
model = ChatGroq(model_name="llama-3.1-8b-instant")

code_string = """
def calculate_sum(a, b):
    result = a + b
    if result > 10:
        print("Greater than 10")
    else:
        print("Less than or equal to 10")
    return result
"""

# Prompt template
prompt_template = PromptTemplate(
    input_variables=["code_string"],
    template="""
You are an experienced coding teacher. Generate suggestions for the following code:

{code_string}

Explain:
1. Possible improvements
2. Errors if any
3. Time complexity
4. Space complexity
"""
)

# Function to get AI suggestion
def get_ai_suggestion(code_string):
    formatted_prompt = prompt_template.format(code_string=code_string)
    result = model.invoke(formatted_prompt)

    print("\n--- AI Review Report ---")
    print(result.content)

# Call function
get_ai_suggestion(code_string)