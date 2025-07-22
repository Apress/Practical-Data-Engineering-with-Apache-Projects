-- Gold Layer: Aggregated and Analytical Data
USE iceberg.gold;

-- top_selling_items
CREATE TABLE gold.top_selling_items AS
SELECT
    item_id,
    item_name,
    item_category,
    SUM(total_price) AS total_revenue
FROM
    silver.purchases_enriched
GROUP BY
    item_id, item_name, item_category
ORDER BY
    total_revenue DESC
LIMIT 10;

-- Last 24h sales
CREATE TABLE gold.sales_performance_24h AS
SELECT
    p.purchase_hour AS purchase_hour,
    SUM(p.total_price) AS total_revenue
FROM
    silver.purchases_enriched p
WHERE
    p.created_at >= CURRENT_TIMESTAMP - INTERVAL '24' HOUR
GROUP BY
    purchase_hour
ORDER BY
    purchase_hour ASC;

-- Top converting items
CREATE TABLE gold.top_converting_items AS
SELECT
    pvi.item_id,
    pvi.item_name,
    pvi.item_category,
    COUNT(DISTINCT pvi.user_id) AS unique_pageview_users,
    COUNT(DISTINCT pe.user_id) AS unique_purchase_users,
    COUNT(pe.id) AS total_purchases,
    COUNT(pvi.user_id) AS total_pageviews,
    CASE 
        WHEN COUNT(pvi.user_id) = 0 THEN 0
        ELSE CAST(COUNT(pe.id) AS DOUBLE) / COUNT(pvi.user_id)
    END AS conversion_rate
FROM
    silver.pageviews_by_items pvi
LEFT JOIN
    silver.purchases_enriched pe
    ON pvi.item_id = pe.item_id
    AND pvi.user_id = pe.user_id
    AND date(pvi.received_at) = pe.purchase_date
GROUP BY
    pvi.item_id,
    pvi.item_name,
    pvi.item_category
ORDER BY
    conversion_rate DESC
LIMIT 10;

-- Pageviews by channel
CREATE TABLE gold.pageviews_by_channel AS
SELECT
    channel,
    COUNT(*) AS total_pageviews
FROM
    silver.pageviews_by_items
GROUP BY
    channel
ORDER BY
    total_pageviews DESC;



