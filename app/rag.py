from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

prompt = PromptTemplate.from_template("""
You are a helpful assistant.

Answer ONLY using the context below.

If the answer is not present,
say:

"I couldn't find that in the document."

Context:
{context}

Question:
{question}

Answer:
""")

parser = StrOutputParser()

chain = prompt | llm | parser