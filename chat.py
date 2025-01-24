# This python script is used to chat with the chatbot
# It have interactive chat with the chatbot, allow user to input text and get response from the chatbot continuously

import os
import typer
from dotenv import dotenv_values
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

config = dotenv_values(".env")

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]


app = typer.Typer()

@app.command()
def dialog():
    """
    TODO: this is just a test, it may not work in an actual conversational context
    """
    model = ChatOpenAI(model="gpt-4o-mini")

    while True:
        user_input = input("You: ")
        if user_input == "bye":
            print("Bot: Goodbye!")
            break
        prompt = ChatPromptTemplate.from_template(user_input)
        chain = prompt | model | StrOutputParser()
        response = chain.invoke({})
        print(f"Bot: {response}")


@app.command()
def fact(topic: str):
    model = ChatOpenAI(model="gpt-4o-mini")
    prompt = ChatPromptTemplate.from_template("Tell me a fact about {topic}")
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"topic": topic})
    print(response)


if __name__ == "__main__":
    app()
