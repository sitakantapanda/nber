import pandas as pd
import requests
import sys
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, exc
from time import sleep

def get_latest_paper():
    url = 'https://data.nber.org/new.html#latest'
    response = requests.get(url)
    content = BeautifulSoup(response.content, features='html.parser')
    latest = content.find('li', {'class': 'multiline-li'})
    latest = latest.find('a').attrs['href']
    latest = int(latest.replace('https://data.nber.org/papers/w', ''))

    return latest

def get_citation_item(content, item):
    item = content.find('meta', {'name': f'{item}'})
    try:
        item = item.attrs['content']
    except AttributeError:
        item = None

    return item

def get_citation_author(content):
    author = content.find_all('meta', {'name': 'citation_author'})
    author = [x.get('content') for x in author]

    return author

def get_topics(content):
    try:
        bibtop = content.find('p', {'class': 'bibtop'})
        topics = bibtop.find_all('a')
        topics = [x.get_text() for x in topics]
    except AttributeError:
        topics = None

    return topics
    
def get_abstract(content):
    try:
        abstract = content.find('p', {'style': 'margin-left: 40px; margin-right: 40px; text-align: justify'})
        abstract = abstract.contents[0].replace('\n', '')
        if '\x00' in abstract:
            abstract = abstract.replace('\x00', '')
    except AttributeError:
        abstract = None

    return abstract

def get_also_downloaded(content):
    try:
        also_downloaded = content.find('table', {'class': 'also-downloaded'})
        also_downloaded = also_downloaded.find_all('td')
        also_downloaded = [x.find('a') for x in also_downloaded if x.find('a') != None]
        also_downloaded = [x.attrs['href'] for x in also_downloaded]
    except AttributeError:
        also_downloaded = None

    return also_downloaded

def get_paper(
    id,
    citation_title,
    citation_author,
    citation_date,
    citation_publication_date,
    citation_technical_report_institution,
    citation_technical_report_number,
    citation_journal_title,
    citation_journal_issn,
    citation_pdf_url,
    topics,
    abstract,
    also_downloaded
):
    paper = {
        'id': id,
        'citation_title': citation_title,
        'citation_author': citation_author,
        'citation_date': citation_date,
        'citation_publication_date': citation_publication_date,
        'citation_technical_report_institution': citation_technical_report_institution,
        'citation_technical_report_number': citation_technical_report_number,
        'citation_journal_title': citation_journal_title,
        'citation_journal_issn': citation_journal_issn,
        'citation_pdf_url': citation_pdf_url,
        'topics': topics,
        'abstract': abstract,
        'also_downloaded': also_downloaded
    }

    return paper

def main():
    i = int(input("Input initial ID: "))
    latest_paper = get_latest_paper()
    while i <= latest_paper:
        url = 'https://www.nber.org/papers/w' + str(i)
        attempt = 0
        while attempt < 5:
            try:
                response = requests.get(url, timeout=None)
                attempt = 5
            except Exception as error:
                print(error)
                attempt += 1
                sleep(11)
        sleep(11)
        content = BeautifulSoup(response.content, features='html.parser')
        paper = get_paper(
            id = i,
            citation_title = get_citation_item(content, 'citation_title'),
            citation_author = get_citation_author(content),
            citation_date = get_citation_item(content, 'citation_date'),
            citation_publication_date = get_citation_item(content, 'citation_publication_date'),
            citation_technical_report_institution = get_citation_item(content, 'citation_technical_report_institution'),
            citation_technical_report_number = get_citation_item(content, 'citation_technical_report_number'),
            citation_journal_title = get_citation_item(content, 'citation_journal_title'),
            citation_journal_issn = get_citation_item(content, 'citation_journal_issn'),
            citation_pdf_url = get_citation_item(content, 'citation_pdf_url'),
            topics = get_topics(content),
            abstract = get_abstract(content),
            also_downloaded = get_also_downloaded(content)
        )
        df = pd.DataFrame([paper])
        try:
            df.to_sql('paper', con=ENGINE, if_exists='append', index=False)
        except exc.IntegrityError:
            pass
        i += 1

if __name__ == '__main__':
    USER = input("Your PostgreSQL username: ")
    PASSWORD = input("Your PostgreSQL password: ")
    HOST = input("Your PostgreSQL host: ")
    PORT = input("Your PostgreSQL port: ")
    DATABASE = input("Your PostgreSQL database: ")
    ENGINE = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')
    CONNECTION = ENGINE.connect()
    main()
    CONNECTION.close()
