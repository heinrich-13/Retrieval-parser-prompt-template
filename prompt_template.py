from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

#instantiate Model
openai_client = ChatOpenAI(
  model="gpt-3.5-turbo",
  temperature=0.9,
  max_tokens=1000,
  verbose=True
)

# prompt = ChatPromptTemplate.from_template("Tell me a joke about a {subject}")

prompt = ChatPromptTemplate.from_messages(
  [
    ("system", "You are an AI comedian. Generate a list of knock knock jokes. Return the results as a comma seperated list."),
    ("human", "{input}")
  ]
)

chain = prompt | openai_client

response = chain.invoke("{input: 'dog'}")

print(response)