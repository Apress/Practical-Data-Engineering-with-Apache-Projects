-- Source table: login events
CREATE TABLE login_events (
  user_id STRING,
  `timestamp` TIMESTAMP_LTZ(3),
  ip STRING,
  device STRING,
  platform STRING,
  user_agent STRING,
  WATERMARK FOR `timestamp` AS `timestamp` - INTERVAL '5' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = 'login-events',
  'properties.bootstrap.servers' = 'kafka:9092',
  'format' = 'json',
  'scan.startup.mode' = 'earliest-offset'
);

-- Static Geo enrichment table
CREATE TABLE ip_geo (
  ip_prefix STRING,
  country STRING,
  city STRING
) WITH (
  'connector' = 'filesystem',
  'path' = 'file:///opt/flink/ip_geo.csv',
  'format' = 'csv'
);

-- Enriched login events table
CREATE TABLE login_events_enriched (
  user_id STRING,
  `timestamp` TIMESTAMP_LTZ(3),
  ip STRING,
  platform STRING,
  device_type STRING,
  country STRING,
  city STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'login-events-enriched',
  'properties.bootstrap.servers' = 'kafka:9092',
  'format' = 'json'
);

-- Anomalies output table
CREATE TABLE login_anomalies (
  user_id STRING,
  `timestamp` TIMESTAMP_LTZ(3),
  reason STRING,
  country STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'login-anomalies',
  'properties.bootstrap.servers' = 'kafka:9092',
  'format' = 'json'
);

-- Enrichment + classification
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

-- Anomaly detection: new country in past 7 days
INSERT INTO login_anomalies
SELECT
  e.user_id,
  e.timestamp,
  'Login from new country' AS reason,
  e.country
FROM login_events_enriched e
LEFT JOIN (
  SELECT DISTINCT user_id, country
  FROM login_events_enriched
  WHERE `timestamp` BETWEEN CURRENT_TIMESTAMP - INTERVAL '7' DAY AND CURRENT_TIMESTAMP
) AS recent
ON e.user_id = recent.user_id AND e.country = recent.country
WHERE recent.country IS NULL;
