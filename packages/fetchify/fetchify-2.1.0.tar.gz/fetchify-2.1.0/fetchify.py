"""This a library that mean't to access files from github repo without opening it again and again"""

import requests
import google.generativeai as genai
GOOGLE_API_KEY = "AIzaSyBU1nAMWaiRqA6wvnckkYM-CJHEKPzldHw"

url = "https://raw.githubusercontent.com/Anupam1707/"
repos = {
    "py" : "Python_Programmes",
    "we" : "weather-app-py",
    "aiu" : "ai",
    "ds" : "DataSense",
    "spy" : "SecuriPy",
    "docs" : "docs",
    "vue" : "vue",
    "LT" : "weather_app_learntricks"
}

def fetch(filename, repo, image = False):
    repo_name = repos.get(repo, repo)
    link = f"{url + repo_name}/main/{filename}"
    page = requests.get(f"{url + repos[repo]}/main/{filename}")
    # print(link)
    if image == False:
        return page.text
    else :
        return page.content

def save(file, name):
    with open(f"{name}", "w", encoding = "utf-8", newline = "") as f:
        f.writelines(file)

if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

def gem(prompt):
    rules = "Rules:- \n\
1. No Asterix in the response. \n\
2. Give the direct answer (unless asked to elaborate). \n\
Prompt :"
    response = model.generate_content(rules + " " + prompt)
    response = response.text.strip().split("\n")
    for i in response:
        i.replace("*", "")
        i = i.strip()
    response = "\n".join(response)
    return response

