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
        "top_k": 64,
        "max_output_tokens": 65536,
        "response_mime_type": "application/json",
        }

    model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
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
    and generate a Chinese summary of around 250 words to introduce what this paper is about especially the data and method and its conclusions on the basis of the previous explanation as well as the original title and abstract. 
    Please be specific and concrete and skip the pleasantries. You can bold the key words and warp them into HTML tags <b></b>.
    Finally, as a reviewer for professional academic journals, please rate this article. You need to comprehensively consider its influence, such as the novelty of its research, the writing ability, the imapact factor of the Journal and the popularity of the authors, and rate it on a scale from 0 to 100, with 100 being the highest and 0 being the lowest. 
    Output the above results using the following JSON schema and the number of entries should be the same:
    Return {"summary": str, "tags": list[str], "score": float}"""
    response = chat.send_message(prompt)
    # print(response.text)
    return json.loads(response.text)



# 引入 OpenAI SDK 并配置 SiliconFlow
from openai import OpenAI

API_KEY = os.getenv('SILICONFLOW_API_KEY')

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.siliconflow.cn/v1"
)



def analyze_paper_openai(info_json: str) -> List[Dict]:
    """
    使用类openai接口的模型批量分析论文
    """
    
    # 构建系统指令
    system_instruction = (
        "You are an expert in literature analysis, skilled in qualitative research methods, "
        "literature retrieval, and critical thinking. You excel at interpreting complex texts, "
        "identifying key ideas and methodologies, and conducting comprehensive literature reviews."
    )

    # 构建用户提示词，强调 JSON 列表格式
    prompt = f"""
    You will be provided with a JSON string containing a list of research papers. 
    Analyze the information of each research paper (title, abstract, topic_words, explanation) and generate the following for EACH paper:

    1. **Tags**: Exactly 3 most important topic-tags in Chinese.
    2. **Summary**: A Chinese summary of around 250 words introducing the paper, focusing on data, method, and conclusions. You can bold keywords using HTML tags <b></b>.
    3. **Score**: A rating from 0 to 100 (100 being highest) considering novelty, writing, journal impact, and author popularity.

    Input Data:
    {info_json}

    **CRITICAL OUTPUT FORMAT REQUIREMENTS**:
    - You must return a valid JSON **List** (Array) of Objects.
    - The order of the output list must strictly match the order of the input list.
    - The format for each object in the list must be: {{"summary": "...", "tags": ["tag1", "tag2", "tag3"], "score": 85.5}}
    - Do not output any markdown formatting (like ```json), just the raw JSON string.
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-0528-Qwen3-8B", 
            messages=[
                {'role': 'system', 'content': system_instruction},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.6, # 稍微降低温度以提高 JSON 格式的稳定性
            stream=False     # 数据处理不需要流式
        )
        
        content = response.choices[0].message.content
        
        # 清洗逻辑：防止模型输出 Markdown 代码块
        content = content.replace("```json", "").replace("```", "").strip()
        
        return json.loads(content)

    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}")
        print("模型返回原始内容:", content[:500] + "...") # 打印前500字符用于调试
        # 如果解析失败，返回空列表或者根据业务逻辑处理，这里返回空列表避免 crash
        return []
    except Exception as e:
        print(f"API 调用发生错误: {e}")
        return []



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

BS = 96  # Batch size
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
            <button class="export-button">📤</button>
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
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
</head>
<body>
    <div class="loading-overlay" id="loadingOverlay">
        <div class="spinner"></div>
        <div id="loadingText">正在导出...</div>
    </div>
    
    <div class="preview-modal" id="previewModal">
        <span class="close-preview" id="closePreview">×</span>
        <div class="preview-container">
            <img id="previewImage" class="preview-image" src="" alt="预览">
        </div>
        <button class="download-button" id="downloadButton">下载图片</button>
    </div>
<section class="header">
    <h1>大气环境遥感论文速递</h1>
    <section class="date">{current_date[:4]}/{current_date[4:6]}/{current_date[6:8]}</section>
</section>
<section id="papers-container">'''

template_tail = '''</section>
<div class="export-all-container">
    <button id="exportAllButton" class="export-all-button">📤一键导出所有论文卡片</button>
</div>
<section class="footer">
    论文总结由AI生成，如有失偏颇，敬请指正！<br>关注本公众号，获取更多大气环境遥感科学研究动态
</section>
</body>
<script src="./printcard.js"></script>
</html>'''

html_string = template_head+html_string+template_tail

# Save the HTML string to a file
with open(f'./WeChat/{current_date}.html', 'w', encoding='utf-8') as f:
    f.write(html_string)
