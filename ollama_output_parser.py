from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

ollama_klient = ChatOllama(
  model="llama3.2:3b",
  temperature=0.8,
  verbose=True
)

def call_string_output_parser():
    user_input = input("What kind of knock knock joke do you want to hear? ")

    if not user_input:
        return None  # If the user presses enter without typing anything, exit the loop.

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an AI comedian. Tell me a joke about the following subject"),
            ("human", "{input}")
        ]
    )

    parser = StrOutputParser()
    chain = prompt | ollama_klient | parser

    return chain.invoke({
        "input": user_input
    })

while True:
    result = call_string_output_parser()
    if result is None:  # If the result is None, it means the user pressed enter without typing anything.
        print("Goodbye!")
        break
    else:
        print(result + "Press enter to exit")  # Print the joke output

