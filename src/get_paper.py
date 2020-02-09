import pandas as pd
import requests
import sys
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, exc
from time import sleep

ENGINE = create_engine('postgresql://localhost:5432/postgres')

def get_citation_item(content, item):
    item = content.find('meta', {'name': f'{item}'})
    try:
        item = item.attrs['content']
    except AttributeError:
        item = None

    return item

def get_topics(content):
    bibtop = content.find('p', {'class': 'bibtop'})
    topics = bibtop.find_all('a')
    topics = [x.get_text() for x in topics]

    return topics


def get_abstract(content):
    abstract = content.find('p', {'style': 'margin-left: 40px; margin-right: 40px; text-align: justify'})
    abstract = abstract.contents[0].replace('\n', '')

    return abstract

def get_paper(
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
    abstract
):
    paper = {
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
        'abstract': abstract
    }

    return paper

def main():

    i = 0
    while i >= 0:
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
        status_code = response.status_code
        if status_code != 200:
            assert status_code == 200, "Status code must be 200."
            sys.exit(1)
        sleep(11)
        content = BeautifulSoup(response.content, features='html.parser')
        citation_title = get_citation_item(content, 'citation_title')
        citation_author = get_citation_item(content, 'citation_author')
        citation_date = get_citation_item(content, 'citation_date')
        citation_publication_date = get_citation_item(content, 'citation_publication_date')
        citation_technical_report_institution = get_citation_item(content, 'citation_technical_report_institution')
        citation_technical_report_number = get_citation_item(content, 'citation_technical_report_number')
        citation_journal_title = get_citation_item(content, 'citation_journal_title')
        citation_journal_issn = get_citation_item(content, 'citation_journal_issn')
        citation_pdf_url = get_citation_item(content, 'citation_pdf_url')
        topics = get_topics(content)
        abstract = get_abstract(content)
        paper = get_paper(
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
            abstract
        )
        df = pd.DataFrame([paper])
        try:
            df.to_sql('paper', con=ENGINE, if_exists='append', index=False)
        except exc.IntegrityError:
            pass
        i += 1

if __name__ == '__main__':
    main()
