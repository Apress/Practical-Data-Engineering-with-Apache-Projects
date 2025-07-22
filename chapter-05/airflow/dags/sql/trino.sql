CREATE OR REPLACE TABLE iceberg.gold.user_engagement_segments
AS
SELECT
    u.id AS user_id,
    u.email,
    u.full_name,
    COUNT(p.page) AS total_pageviews,
    COUNT(DISTINCT DATE(p.received_at)) AS active_days,
    MAX(DATE(p.received_at)) AS last_active_date,
    DATE_DIFF('day', MAX(DATE(p.received_at)), CURRENT_DATE) AS days_since_last_active,
    CASE
        WHEN COUNT(p.page) >= 50 AND DATE_DIFF('day', MAX(DATE(p.received_at)), CURRENT_DATE) <= 3 THEN 'high_engagement'
        WHEN COUNT(p.page) BETWEEN 10 AND 49 AND DATE_DIFF('day', MAX(DATE(p.received_at)), CURRENT_DATE) <= 7 THEN 'medium_engagement'
        ELSE 'low_engagement'
    END AS engagement_segment
FROM iceberg.silver.users u
LEFT JOIN iceberg.silver.pageviews_by_items p ON u.id = p.user_id
WHERE u.valid_email = TRUE
GROUP BY u.id, u.email, u.full_name