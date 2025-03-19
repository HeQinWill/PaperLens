import os
import shutil
import subprocess
import pandas as pd
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from tqdm import tqdm
from typing import Dict, List, Tuple
import feedparser
import requests

import re
import json
import html
import yaml
from bs4 import BeautifulSoup

import google.generativeai as genai
KEY_GENAI = os.getenv('KEY_GENAI')

genai.configure(api_key=KEY_GENAI, transport='rest')

def analyze_paper(info_json: str) -> Tuple[bool, str]:
    # print(info_json)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
        }

    model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
            system_instruction="You are an expert in literature analysis, skilled in qualitative research methods, literature retrieval, and critical thinking. You excel at interpreting complex texts, identifying key ideas and methodologies, and conducting comprehensive literature reviews to identify research trends and gaps.",
            )

    chat = model.start_chat(
            history=[{
                "role": "user",
                "parts": [info_json]
                }]
            )
    prompt = """Analyze the information of each research paper and summarize the most important topic-tags in Chinese (exactly 3), 
    and generate a Chinese summary of around 200 words to introduce what this paper is about especially the data and method and its conclusions on the basis of the previous explanation as well as the original title and abstract. 
    Please be specific and concrete and skip the pleasantries. You can bold the key words and warp them into HTML tags <b></b>.
    Finally, as a reviewer for professional academic journals, please rate this article. You need to comprehensively consider its influence, such as the novelty of its research, the writing ability, the imapact factor of the Journal and the popularity of the authors, and rate it on a scale from 0 to 100, with 100 being the highest and 0 being the lowest. 
    Output the above results using the following JSON schema and the number of entries should be the same:
    Return {"summary": str, "tags": list[str], "score": float}"""
    response = chat.send_message(prompt)
    # print(response.text)
    return json.loads(response.text)



# Get the current year and month
current_date = datetime.now().strftime("%Y%m%d")

# Path to the paper_entries directory
paper_entries_dir = Path('./paper_entries')

# Get all CSV files in this period
csv_files = sorted(paper_entries_dir.glob(f'{current_date}*.csv'))
print('Number of CSV files:', len(csv_files))

# List to store dataframes
dfs = []

# Read each CSV file
for file in csv_files:
    df = pd.read_csv(file)
    dfs.append(df)

# Concatenate all dataframes
merged_df = pd.concat(dfs, ignore_index=True)

# Remove the entries with no 'doi'
merged_df = merged_df.dropna(subset=['doi'])

# Get the relevant papers
relevant_true = merged_df[merged_df['is_relevant'] == True]
relevant_true.reset_index(inplace=True)
print(len(relevant_true))

# Send the information to GPT
info = relevant_true[['title', 'abstract', 'topic_words', 'explanation','authors']]

BS = 10  # Batch size
DFS = []
for i in range(len(info)//BS +1):
    print(i, i*BS, i*BS+BS)
    info_json = info[i*BS:i*BS+BS].to_json(orient='records', force_ascii=False)
    response = analyze_paper(info_json)
    DFS.append(pd.DataFrame(response))

tmp = pd.concat(DFS, ignore_index=True)
relevant_true = pd.concat([relevant_true, tmp], axis=1)
relevant_true.dropna(inplace=True)
print(len(relevant_true))

# Sort it by score although it is not necessary
# the score is not scientifically correct
# here is only for a random effect
relevant_true = relevant_true.sort_values(by='score', ascending=False)

# relevant_true.to_csv('relevant_true.csv', index=None)
# relevant_true = pd.read_csv('relevant_true.csv')

#%%
HTMLs = []
for i, row in relevant_true.iterrows():
    tag1, tag2, tag3 = row['tags']  # eval(tags_str)  if read it from csv
    HTML = f'''<section class="paper-card">
            <section class="paper-title">{row['title']}</section>
            <section class="paper-authors">{row['authors'].replace(';', ', ')}</section>
            <div class="paper-info-container">
                <div class="paper-info-left">
                    <section class="paper-journal">{row['journal']}</section>
                    <section class="paper-doi"><a href="https://doi.org/{row['doi']}" target="_blank">https://doi.org/{row['doi']}</a></section>
                    <section class="topic-tags">
                        <span class="topic-tag">{tag1}</span>
                        <span class="topic-tag">{tag2}</span>
                        <span class="topic-tag">{tag3}</span>
                    </section>
                </div>
                <div class="paper-info-right">
                    <img class="qr-code" src="https://api.qrserver.com/v1/create-qr-code/?size=96x96&data=https://doi.org/{row['doi']}" alt="QR Code" />
                </div>
            </div>
            <section class="abstract-content">{row['summary']}</section>
            </section>
            '''
    HTMLs.append(HTML)
# Concatenate all strings in the list
html_string = ''.join(HTMLs)

template_head = f'''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" type="text/css" href="wechat.css">
</head>
<body>
<section class="header">
    <h1>大气环境遥感论文速递</h1>
    <section class="date">{current_date[:4]}/{current_date[4:6]}/{current_date[6:8]}</section>
</section>
<section id="papers-container">'''

template_tail = '''</section>
<section class="footer">
    论文总结由AI生成，如有失偏颇，敬请指正！<br>关注本公众号，获取更多大气环境遥感科学研究动态
</section>
</body>
</html>'''

html_string = template_head+html_string+template_tail

# Save the HTML string to a file
with open(f'./WeChat/{current_date}.html', 'w', encoding='utf-8') as f:
    f.write(html_string)