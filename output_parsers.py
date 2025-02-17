from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser, JsonOutputParser

load_dotenv()

#instantiate Model
openai_client = ChatOpenAI(
  model="gpt-3.5-turbo",
  temperature=0.9,
  max_tokens=1000,
  verbose=True
)

def call_string_output_parser():
  user_input = input("What kind of knock knock joke do you want to hear? Type any subject and press enter: ")
  prompt = ChatPromptTemplate.from_messages(
    [
      ("system", "You are an AI comedian. Tell me a joke aboyt the following subject"),
      ("human", "{input}")
    ]
  )

  parser = StrOutputParser()

  chain = prompt | openai_client | parser

  return chain.invoke({
    "input": user_input
  })

def call_list_output_parser():
  prompt = ChatPromptTemplate.from_messages(
    [
      ("system", "You are an AI comedian. Generate a list of knock knock jokes with the input as the subject. Return the results as a comma seperated list."),
      ("human", "{input}")
    ]
  )

  parser = CommaSeparatedListOutputParser()

  chain = prompt | openai_client | parser

  return chain.invoke({
    "input": "dog"
  })

def all_json_output_parser():
  prompt = ChatPromptTemplate.from_messages(
    [
      ("system", "Extract information from the folllowing phrase. \nFormatting Instruction: {format_instructions}"),
      ("human", "{phrase}")
    ]
  )

  class Person(BaseModel):
    recipe: str = Field(description="the name of the recipe")
    ingredients: list = Field(description="ingresients")


  parser = JsonOutputParser(pydantic_object=Person)

  chain = prompt | openai_client | parser

  return chain.invoke({
    "phrase": "Braai brooidjies are made of bread, cheese, tomato, onion and cheese. Put somme salt and pepper on and grill it on the fire.",
    "format_instructions": parser.get_format_instructions()
  })

print(call_string_output_parser())