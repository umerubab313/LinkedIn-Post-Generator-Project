#this is a file we made to use llama model through groq cloud service

from dotenv import load_dotenv  #loading function used to load environmental variable in .env file
from langchain_groq import ChatGroq #importing object that is a specific LangChain wrapper to access LLM models through GROQ service

import os # os lib is used to access env variables and other stuff

load_dotenv()

llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"),model_name="meta-llama/llama-4-scout-17b-16e-instruct")

if __name__ == "__main__":
    response = llm.invoke("What are the steps to make coffee")
    print(response.content)
