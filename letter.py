# This python script generates cover letter from your resume

import os
import typer
import json

from typing_extensions import Annotated, TypedDict
from rich import print
from dotenv import dotenv_values
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import Html2TextTransformer


config = dotenv_values(".env")
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]

app = typer.Typer()

class Job(TypedDict):
    """
    Job data from a web page content
    """
    job_title: Annotated[str, ...,"Job Title in the content"]
    job_description: Annotated[str, ..., "Job Description in the content"]


@app.command()
def cover_letter(your_name: Annotated[str, typer.Argument()],
                 resume_file_path: Annotated[str, typer.Option("--resume","-r")],
                 job_url: Annotated[str, typer.Option("--url", "-u")]):
    print(f":email: >>>[green] Generating cover letter from your resume: {your_name}[/green]")

    job = getJobDescription(loadHtmlContent(job_url))
    pdfPages = readPdf(resume_file_path)
    print("> Resume loaded successfully. Pages {len(pdfPages)}")
    resume_content = format("\n".join([page.page_content for page in pdfPages]))

    print("[bold blue]Need to impress on something?[/bold blue]")
    print("What in the resume do you want to highlight in your cover letter?")
    print("Enter 'done' when you are finished.")

    notes = []
    while (skill := input("> Enter your notes: ")) != "done":
        notes.append(skill)

    model = ChatOpenAI(model="gpt-4o-mini")
    prompt = ChatPromptTemplate.from_template("""
        {your_name} is applying for the position of {job_title}.
        Help {your_name} to write a cover letter that highlight the skills and experiences to make it a strong fit for the {job_title}. The cover letter should write up to content of the resume:
```{resume_content}```.
        And the cover letter also should consider the job description below: ```{job_description}```.

        May or may not include the following notes: {notes}

        Give basic format of the cover letter as new line for each paragraph, etc.
    """)
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"your_name": your_name, "job_title": job['job_title'], "job_description": job['job_description'], "resume_content": resume_content, "notes": notes})
    print(f"[bold green]Cover Letter for {your_name}[/bold green]")
    print(response)


def readPdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = []
    for page in loader.load():
        pages.append(page)
    return pages

def loadHtmlContent(url):
    loader = AsyncChromiumLoader([url], user_agent=config.get("USER_AGENT"))
    html = loader.load()
    html2text = Html2TextTransformer()
    text = html2text.transform_documents(html)
    return text

def getJobDescription(text):
    model = ChatOpenAI(model="gpt-4o-mini")
    prompt = ChatPromptTemplate.from_template("""
        Extract job title and job description from the content below:
```{text}```
Job Description should include all the details and sections, for example: summary, responsibilities, requirements, etc.
""")
    chain = prompt | model.with_structured_output(Job)
    response = chain.invoke({"text": text})
    return response

if __name__ == "__main__":
    app().cover_letter()
