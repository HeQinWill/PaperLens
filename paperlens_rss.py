import feedparser
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime, timezone, timedelta
from pathlib import Path
from tqdm import tqdm
import time
import re
import html
import subprocess
import shutil
import os
from typing import Dict, List, Tuple
import google.generativeai as genai
KEY_GENAI = os.getenv('KEY_GENAI')
genai.configure(api_key=KEY_GENAI, transport='rest')

RSS_FEEDS: Dict[str, str] = {
    "https://iopscience.iop.org/journal/rss/1748-9326": "IOP",  # ERL
    "https://acp.copernicus.org/xml/rss2_0.xml": "Copernicus",
    "https://amt.copernicus.org/xml/rss2_0.xml": "Copernicus",
    "https://essd.copernicus.org/xml/rss2_0.xml": "Copernicus",
    "https://gmd.copernicus.org/xml/rss2_0.xml": "Copernicus",
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=esthag": "ACS",  # ES&T
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=estlcu": "ACS",  # ES&T Letters
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=aeacd5": "ACS",  # ES&T Air
    "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=ehnea2": "ACS",  # ES&T EH
    "https://agupubs.onlinelibrary.wiley.com/feed/2576604x/most-recent": "AGU",  # Advances
    "https://agupubs.onlinelibrary.wiley.com/feed/19448007/most-recent": "AGU",  # GRL
    "https://agupubs.onlinelibrary.wiley.com/feed/21698996/most-recent": "AGU",  # JGR:A
    "https://agupubs.onlinelibrary.wiley.com/feed/23284277/most-recent": "AGU",  # EF
    "https://agupubs.onlinelibrary.wiley.com/feed/24711403/most-recent": "AGU",  # GeoH
    "https://www.nature.com/nature.rss": "Nature",  # Nature
    "https://www.nature.com/ngeo.rss": "Nature",  # NatureGeo
    "https://www.nature.com/ncomms.rss": "Nature",  # NatureComms
}

def fetch_rss_feed(url: str) -> feedparser.FeedParserDict:
    """Fetch and parse an RSS feed."""
    return feedparser.parse(url)

def parse_entry(source: str, entry: feedparser.FeedParserDict, doi_only: bool = False) -> Dict[str, str]:
    """Parse an RSS entry based on its source."""
    if source == "Nature":
        return parse_nature_entry(entry, doi_only)
    elif source == "AGU":
        return parse_agu_entry(entry, doi_only)
    elif source == "ACS":
        return parse_acs_entry(entry, doi_only)
    elif source == "IOP":
        return parse_iop_entry(entry, doi_only)
    elif source == "Copernicus":
        return parse_copernicus_entry(entry, doi_only)
    else:
        raise ValueError(f"Unsupported source: {source}")

def parse_acs_entry(entry: feedparser.FeedParserDict, doi_only: bool = False) -> Dict[str, str]:
    """Parse an ACS RSS entry."""
    doi = entry.get('id', 'DOI not available').split('doi.org/')[-1]
    if doi_only:
        return {'doi': doi}
    return {
        'doi': doi,
        'title': entry.get('title', 'Title not available').split('[ASAP] ')[-1],
        'abstract': get_acs_abstract(doi),
        'authors': entry.get('author', 'Authors not available').replace(', ', ';').replace(';and ', ';'),
        'journal': html.unescape(re.findall(r'<cite>(.*?)</cite>', entry['summary'])[0]),
    }

def get_acs_abstract(doi: str) -> str:
    """Attempt to fetch and extract the full text of an article."""
    try:
        url = 'https://pubs.acs.org/doi/' + doi

        command = [
            "./curl_chrome116",  # from https://github.com/lwthiker/curl-impersonate
            url,
            "-H", "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "-H", "accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "-H", "cache-control: max-age=0",
            "-H", "priority: u=0, i",
            "-H", 'sec-ch-ua: "Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
            "-H", 'sec-ch-ua-arch: "arm"',
            "-H", 'sec-ch-ua-bitness: "64"',
            "-H", 'sec-ch-ua-full-version: "128.0.2739.42"',
            "-H", 'sec-ch-ua-full-version-list: "Chromium";v="128.0.6613.85", "Not;A=Brand";v="24.0.0.0", "Microsoft Edge";v="128.0.2739.42"',
            "-H", 'sec-ch-ua-mobile: ?0',
            "-H", 'sec-ch-ua-model: ""',
            "-H", 'sec-ch-ua-platform: "macOS"',
            "-H", 'sec-ch-ua-platform-version: "14.6.1"',
            "-H", 'sec-fetch-dest: document',
            "-H", 'sec-fetch-mode: navigate',
            "-H", 'sec-fetch-site: none',
            "-H", 'sec-fetch-user: ?1',
            "-H", 'upgrade-insecure-requests: 1',
            "-H", 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        ]
        # 使用 subprocess 来执行命令并捕获输出
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            response = result.stdout
        except subprocess.CalledProcessError as e:
            print("Error executing command:", e)

        soup = BeautifulSoup(response, 'html.parser')

        # Find the script tag containing the abstract
        script_tag = soup.find('meta', attrs={'property': 'og:description'})

        if script_tag:
            abstract = script_tag['content']
            return abstract
        else:
            print("Full text not available. Please check the original article.")
            return ''
    except Exception as e:
        print(f"Error fetching full text from {url}: {str(e)}")
        return ''

def parse_copernicus_entry(entry: feedparser.FeedParserDict, doi_only: bool = False) -> Dict[str, str]:
    """Parse a Copernicus RSS entry."""
    doi = entry.get('id').replace('https://doi.org/', '')
    if doi_only:
        return {'doi': doi}
    abstract, journal = get_copernicus_abstract(entry.get('id'))
    short_summary = entry['summary'].split('\n')[-1].strip()
    return {
        'doi': doi,
        'title': entry.get('title', 'Title not available'),
        'abstract': short_summary + ' \n ' + abstract,
        'authors': entry['summary'].split('\n')[1].strip().replace(', ', ';').replace(';and ', ';').split('<br')[0].replace(' and ', ';'),
        'journal': journal,
    }

def get_copernicus_abstract(url: str):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
    abstract = soup.find('div', class_='abstract-content show-no-js')
    if abstract:
        abstract = abstract.text
    else:
        abstract = soup.find('div', class_='abstract').find('p').text.replace('Abstract. ','')
    abstract = abstract.replace('\u2009',' ').replace('\xa0',' ').replace('\u200b','')  # 处理特殊空格
    journal = soup.find('meta', attrs={'name': 'citation_journal_title'})['content']
    return abstract, journal

def parse_nature_entry(entry: feedparser.FeedParserDict, doi_only: bool = False) -> Dict[str, str]:
    """Parse a Nature RSS entry."""
    doi = entry.get('prism_doi', 'DOI not available')
    if doi_only:
        return {'doi': doi}
    abstract = get_nature_abstract(doi)
    short_summary = entry.get('content', '')[0].value.split('</a></p>')[-1]
    return {
        'doi': doi,
        'title': entry.get('title', 'Title not available'),
        'abstract': short_summary + ' \n ' + abstract,
        'authors': ';'.join(author['name'] for author in entry.get('authors', [])),
        'journal': entry.get('prism_publicationname', 'Journal not available'),
    }

def get_nature_abstract(doi: str) -> str:
    """Attempt to fetch and extract the full text of an article."""
    try:
        url = 'https://doi.org/' + doi
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the script tag containing the JSON data
        script_tag = soup.find('script', type='application/ld+json')

        if script_tag:
            # Parse the JSON data
            json_data = json.loads(script_tag.string)
            # Extract the abstract (description) from the JSON data
            abstract = json_data['mainEntity']['description']
            return abstract
        else:
            print("Full text not available. Please check the original article.")
            return ''
    except Exception as e:
        print(f"Error fetching full text from {url}: {str(e)}")
        return ''

def parse_agu_entry(entry: feedparser.FeedParserDict, doi_only: bool = False) -> Dict[str, str]:
    """Parse an AGU RSS entry."""
    doi = entry.get('prism_doi', 'DOI not available')
    if doi_only:
        return {'doi': doi}
    return {
        'doi': doi,
        'title': entry.get('title', 'Title not available'),
        'abstract': entry.get('content', '')[0].value.replace('Abstract\n', '', 1),
        'authors': entry.get('author', 'Authors not available').replace(', \n', ';'),
        'journal': entry.get('prism_publicationname', 'Journal not available'),
    }

def parse_iop_entry(entry: feedparser.FeedParserDict, doi_only: bool = False) -> Dict[str, str]:
    """Parse an IOP RSS entry."""
    doi = entry.get('prism_doi', 'DOI not available')
    if doi_only:
        return {'doi': doi}
    return {
        'doi': doi,
        'title': entry.get('title', 'Title not available'),
        'abstract': entry.get('summary', 'Abstract not available'),
        'authors': entry.get('author', 'Authors not available').replace(', ', ';').replace(' and ', ';'),
        'journal': entry.get('prism_publicationname', 'Journal not available'),
    }

def analyze_relevance(title: str, abstract: str) -> Tuple[bool, str]:
    """Analyze the relevance of a paper to atmospheric environmental remote sensing."""
    title = 'Title: '+title
    abstract = 'Abstract: '+abstract
    # print(title, abstract)

    generation_config = {
        "temperature": 0.42,
        "top_p": 0.98,
        "top_k": 64,
        "max_output_tokens": 256,
        "response_mime_type": "application/json",
        }

    model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-exp-0827",  # gemini-1.5-flash
            generation_config=generation_config,
            system_instruction="You are an expert in literature analysis, skilled in qualitative research methods, literature retrieval, and critical thinking. You excel at interpreting complex texts, identifying key ideas and methodologies, and conducting comprehensive literature reviews to identify research trends and gaps.",
            )

    chat = model.start_chat(
            history=[{
                "role": "user",
                "parts": [title, abstract]
                }]
            )
    prompt = """Analyze the title and abstract of the research paper. Determine if it's strongly related to atmospheric environmental remote sensing technology like air quality monitoring, satellite observations, and atmospheric composition analysis.
    Respond with 'True' or 'False', give topic words in English (which kind of atmospheric composition, which kind of satellite/sensor, which kind of application， etc.) and then provide a brief explanation about the paper itself in Chinese using this JSON schema:
    Return {"is_relevant": bool, "topic_words": list[str], "explanation": str}"""
    response = chat.send_message(prompt)
    # print(response.text)
    return json.loads(response.text)


#%% Main function to process RSS feeds and generate a report
# Create a directory for storing CSV files if it doesn't exist
csv_dir = Path('./paper_entries')
csv_dir.mkdir(exist_ok=True)

# Load existing data from all CSV files in the directory
existing_dois = set()
for file in csv_dir.glob('*.csv'):
    existing_df = pd.read_csv(file)
    existing_dois.update(existing_df['doi'])
print(len(existing_dois))

# Parse all entries from all feeds
relevant_entries = []
for feed_url, source in RSS_FEEDS.items():
    feed = fetch_rss_feed(feed_url)
    for entry in tqdm(feed.entries):
        try:
            # First, only get the DOI
            parsed_entry = parse_entry(source, entry, doi_only=True)
            if parsed_entry['doi'] not in existing_dois:
                # If DOI is new, then get full entry details
                full_entry = parse_entry(source, entry, doi_only=False)
                analysis = analyze_relevance(full_entry['title'], full_entry['abstract'])
                full_entry.update(analysis)  # combine the analysis into the full entry
                relevant_entries.append(full_entry)
                time.sleep(1.42)
            else:
                print(f"Skipping entry with DOI {parsed_entry['doi']} as it already exists.")
        except Exception as e:
            bad_entry = full_entry
            print(f"Error processing entry from {bad_entry}: {str(e)}")

# Generate a timestamp for the new file
utc_now = datetime.now(timezone.utc)
utc_plus_8 = utc_now + timedelta(hours=8)
timestamp = utc_plus_8.strftime("%Y%m%d_%H%M%S")
new_csv_file = csv_dir / f'{timestamp}.csv'

# Save the updated data to the new CSV file
if len(relevant_entries)>0:
    df = pd.DataFrame(relevant_entries)
    df.to_csv(new_csv_file, index=False)
    print(f"Data saved to {new_csv_file}")
