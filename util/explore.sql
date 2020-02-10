SELECT
    published_year, 
    topics, 
    COUNT(*)
FROM (
	SELECT 
        DATE_PART('YEAR', citation_date) AS published_year, 
        UNNEST(topics) AS topics
	FROM paper
) AS paper
WHERE topics != ''
GROUP BY published_year, topics
ORDER BY published_year DESC
LIMIT 5;

SELECT
    citation_title,
    abstract
FROM paper
WHERE 
    LOWER(abstract) ILIKE '%indonesia%'
    OR LOWER(citation_title) ILIKE '%indonesia%';

SELECT 
	DATE_PART('YEAR', citation_date) citation_year,
	COUNT(*)
FROM paper
GROUP BY citation_year
ORDER BY citation_year ASC
LIMIT 10;

SELECT 
	'Numbers of papers on NBER where the abstract starts with "This paper": ' AS description,
	COUNT(*)
FROM paper
WHERE abstract ILIKE 'this paper%'
UNION ALL 
SELECT
	'Total numbers of papers on NBER: ' AS description,
	COUNT(*)
FROM paper;

SELECT topics, COUNT(*)
FROM (
	SELECT UNNEST(topics) AS topics
	FROM paper
) AS paper
WHERE topics != ''
GROUP BY topics
ORDER BY topics ASC;

SELECT * 
FROM (
	SELECT citation_date, citation_title, abstract, UNNEST(topics) topics
	FROM paper
) AS paper
WHERE topics = 'Economics of Education Program';