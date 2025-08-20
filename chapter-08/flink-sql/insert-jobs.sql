-- Enrichment + classification job
INSERT INTO login_events_enriched
SELECT
  user_id,
  `timestamp`,
  ip,
  platform,
  CASE
    WHEN LOWER(device) LIKE '%iphone%' OR LOWER(device) LIKE '%android%' THEN 'mobile'
    ELSE 'desktop'
  END AS device_type,
  g.country,
  g.city
FROM login_events
LEFT JOIN ip_geo AS g ON ip LIKE CONCAT(g.ip_prefix, '%');

-- Anomaly detection job: new country in past 7 days
INSERT INTO login_anomalies
SELECT
  e.user_id,
  e.`timestamp`,
  'Login from new country' AS reason,
  e.country
FROM login_events_enriched e
LEFT JOIN (
  SELECT DISTINCT user_id, country
  FROM login_events_enriched
  WHERE `timestamp` > '2025-08-13'
) AS recent
ON e.user_id = recent.user_id AND e.country = recent.country
WHERE recent.country IS NULL;