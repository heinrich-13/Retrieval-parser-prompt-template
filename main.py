from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

load_dotenv()

# Create an instance of the OpenAI class
openai_client = ChatOpenAI(
  model="gpt-3.5-turbo",
  temperature=0.1,
  max_tokens=1000,
  verbose=True
)

llm = openai_client

result = llm.stream("Tell me a joke?")

# print(result)
for chunk in result:
  print(chunk.content, end="", flush=True)