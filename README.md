# About

Hello world :earth_asia:! Are you an economist, or economics student, or just a random person like me who is interested in economics? Do you want to write a paper, a thesis, or just ramble on some stuffs but don't have any fresh ideas on what should be the topic? Worry no more! Because, this repository is for you!

Before jumping in, consider this:

```
As of this writing, there are more than 20,000 working papers on NBER. If getting one paper takes around 30 seconds (including the required time interval imposed by NBER in its crawler policy, it takes more than a week to finish the program.
```

If you are okay with above caution, you may want to use [Heroku](https://elements.heroku.com/addons/heroku-postgresql) or other cloud service so that the program won't run on your local machine. If yes, you may need to spare $9/month to maintain the PostgreSQL database because its free edition only covers up to 10,000 rows. If you are okay with this, you may go on. However, I won't get into setting up database on Heroku since in this repository I only run on my local machine.

# Clone

If you think this is going to be useful for your purpose, don't hesitate to clone this repository:

```
cd ~
git clone https://github.com/ledwindra/nber.git
cd nber
```

To get the latest updates, run `git pull origin master`

# Permission

Check its [robots.txt](http://data.nber.org/robots.txt)

Following is the snippet:

```
User-agent: *
Crawl-delay: 10

User-agent: *
Disallow: /fda/
Disallow: /contact/
Disallow: /confer/
Disallow: /~confer/
Disallow: /conf_papers/
Disallow: /c/
Disallow: /wpsubmit/
Disallow: /custom
Disallow: /confsubmit/
Disallow: /family/
Disallow: /1050/
Disallow: /cal/
Disallow: /cgi-bin/
Disallow: /nberhistory/historicalarchives/
Disallow: /xming*
Disallow: /taxex/
Disallow: /papers/mail
Disallow: /tmp/
Disallow: /server-status/
Disallow: /mrtg/
Disallow: /bb/
Disallow: /img/
Disallow: /pics
Disallow: /*.ris$
Disallow: /*.marc$
Disallow: /*.bib$
Disallow: /*palm*$
Disallow: /taxsim-calc*/
Disallow: /medicare/
Disallow: /*.pl/
Disallow: /arfpub/
Disallow: /pscp*
Disallow: /jobs/stateforms/
Disallow: /hcris/
```

Everybody is not disallowed to get `/papers/` tag. However, please scrape ethically by setting time interval between each request for 10 seconds (see `Crawl-delay: 10`).

# Virtual environment

It's not an obligation to use a virtual environment, but using it is better (I think) for a good reason. This project has dependencies on third-party modules such as `pandas`, `requests`. Some of these modules may be updated and have consequences to the project. Or maybe you have another project with the same modules but different versions. Using virtual environment will tackle all of the issues. Just run the following on terminal:

```
python3 -m venv .venv-nber
source .venv-nber/bin/activate
```

# Install requirements

As mentioned above, this project depends on third-party modules. Run the following on terminal to install them on your machine:

```
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

# PostgreSQL

Install: [link](https://www.postgresql.org/download/)

Connect to localhost:

```
psql -h localhost -p 5432 -d postgres
```

Then input your password when it prompts something like this:

```
Password for user postgres: 
```

However, it may be different if you have different configurations.

To create table, run the SQL query in `util/get_paper.sql`

# Run

Run the Python script on terminal:

```
python3 src/get_paper.py
```

It will prompt you questions:

```
Your PostgreSQL username: [YOUR POSTGRESQL USERNAME]
Your PostgreSQL password: [YOUR POSTGRESQL PASSWORD]
Your PostgreSQL host: [YOUR POSTGRESQL HOST]
Your PostgreSQL port: [YOUR POSTGRESQL PORT]
Your PostgreSQL database: [YOUR POSTGRESQL DATABASE]
Input initial ID: [PRESS 0 IF YOU WANT TO START FROM https://www.nber.org/papers/w0000] 
```

# Test

Run unit tests to ensure the data quality is good.

```
pytest test -s
```

It then will prompt you to input your PostgreSQL password:

```
collecting ... Your PostgreSQL password: 
```

# Columns

|column_name|data_type|description|
|-|-|-|
|id|int4|A unique ID for each paper|
|citation_title|varchar|Paper title|
|citation_author|varchar|Paper author(s). Can be more than one. Hence it is stored as an array|
|citation_date|date|Date of paper (not clear)|
|citation_publication_date|date|Date of paper being published|
|citation_technical_report_institution|varchar|Institution which publishes the report|
|citation_technical_report_number|varchar|Paper ID as in the website|
|citation_journal_title|varchar|Journal title|
|citation_journal_issn|varchar|ISSN number|
|citation_pdf_url|varchar|Paper URL for PDF version|
|topics|varchar|Paper topic(s). Can be more tan one. Hence it is stored as an array|
|abstract|varchar|Paper abstract|
|also_downloaded|varchar|Users who downloaded this paper also downloaded* these. Can be more than one. Hence it is stored as an array. The reason I use the URL because otherwise it won't catch other than the working papers. Users may also download something from `/chapters/`, which may be useful for analysis|

# Explore

Play around with the SQL queries inside `util/explore.sql`, for example:

```
SELECT topics, COUNT(*)
FROM (
	SELECT UNNEST(topics) AS topics
	FROM paper
) AS paper
WHERE topics != ''
GROUP BY topics
ORDER BY topics ASC;
```

...and the output will be:


```
                         topics                         | count 
--------------------------------------------------------+-------
 Asset Pricing Program                                  |  2417
 Corporate Finance Program                              |  2049
 Development Economics Program                          |  1017
 Economic Fluctuations and Growth Program               |  5218
 Economics of Education Program                         |  1429
 Environment and Energy Program                         |  1101
 Health Care Program                                    |  1472
 Health Economics Program                               |  2067
 Industrial Organization Program                        |  1538
 International Finance and Macroeconomics Program       |  3841
 International Trade and Investment Program             |  3323
 Labor Studies Program                                  |  5288
 Law and Economics Program                              |  1030
 Monetary Economics Program                             |  3004
 Political Economy Program                              |  1138
 Productivity, Innovation, and Entrepreneurship Program |  2191
 Program on Children                                    |  1522
 Program on the Development of the American Economy     |  1410
 Program on the Economics of Aging                      |  1505
 Public Economics Program                               |  5273
 Technical Working Papers                               |   246
(21 rows)
```

# Contribute

If you'd like to contribute, here's what you can do:

1. Clone the repo
2. Create new branch by running `git checkout -b [YOUR-BRANCH-NAME]`
3. Always pull from `master` before push
4. Make `pull request`

The other way would be just contact me personally. I'm just a regular person.

# Closing

If you have read up to this line, thank you for bearing with me. Hope this is useful for your purpose! :sunglasses:
