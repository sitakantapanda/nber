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

SELECT abstract
FROM paper
WHERE LOWER(abstract) ILIKE '%poverty%';