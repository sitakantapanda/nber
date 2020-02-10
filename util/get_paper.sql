CREATE TABLE paper (
    id SERIAL PRIMARY KEY,
    citation_title VARCHAR,
    citation_author VARCHAR[],
    citation_date DATE,
    citation_publication_date DATE,
    citation_technical_report_institution VARCHAR,
    citation_technical_report_number VARCHAR UNIQUE,
    citation_journal_title VARCHAR,
    citation_journal_issn VARCHAR,
    citation_pdf_url VARCHAR,
    topics VARCHAR[],
    abstract VARCHAR
);