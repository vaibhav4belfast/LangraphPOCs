from dotenv import load_dotenv # used to store secret stuff like API keys or configuration values

load_dotenv()

from langchain_openai import ChatOpenAI
print("Vaibhav")
llm = ChatOpenAI(model="gpt-4o-mini")
response = llm.invoke([{"role": "user", "content": "Hello"}])
print(response.content)