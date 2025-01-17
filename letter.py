# This python script generates cover letter from your resume

import os
import typer
from rich import print
from dotenv import dotenv_values
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

config = dotenv_values(".env")
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]

app = typer.Typer()

@app.command()
def cover_letter(your_name: str = typer.Option(...,prompt=True),
                 job_title: str = typer.Option(...,prompt=True)):
    print(f"This python script generates cover letter from your resume: {your_name}")

    model = ChatOpenAI(model="gpt-4o-mini")

    print("[bold blue]Highlight your skills[/bold blue]")
    print("Enter 'done' when you are finished")

    skills = []
    while (skill := input("> Enter your skill: ")) != "done":
        skills.append(skill)

    prompt = ChatPromptTemplate.from_template("""
        generate cover letter for {your_name} for the position of {job_title}.
        Try to hightlight the skills: {skills}
        Show that you are the best candidate for the job.
        Give basic format of the cover letter as new line for each paragraph, etc.
    """)
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"your_name": your_name, "job_title": job_title, "skills": skills})
    print(f"[bold green]Cover Letter for {your_name}[/bold green]")
    print(response)

if __name__ == "__main__":
    app().cover_letter()
