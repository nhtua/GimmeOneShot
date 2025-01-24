GimmeOneShot
============
This tool automates some steps when you are preparing and looking for jobs.
It will help you to write a cover letter. However, the accuracy is depending on your resume. So please make sure your resume is well written, cover all the important information of your skills and experience, and keep it up to date.


## Requirements
- Python 3.10+
- Poetry 2.0.0+ (Install [poetry](https://python-poetry.org/docs/#installation) if you haven't)
- Job boards website which is not protected by CAPTCHA
- Resume in PDF format

## Installation
```bash
git clone https://github.com/nhtua/GimmeOneShot.git
cd GimmeOneShot
poetry install
```

You also need to create a file `.env`, fill it with content
```
OPENAI_API_KEY=sk-proj-gNhxxxxxxxxxx
USER_AGENT="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
```
Create OpenAI API Key at [platform.openai.com](https://platform.openai.com/)

## Usage
```bash
alias gimme="poetry run python"
gimme letter.py "Your Name" -r path/to/your/resume.pdf -u "https://examplejobboard.com/view/123456"
```

Review and copy the content to document editor of your choice. Don't forget to review and update the text's placeholder. 

Good luck, bruh!

