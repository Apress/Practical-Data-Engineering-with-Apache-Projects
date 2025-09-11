-- Source table: login events
CREATE TABLE login_events (
  user_id STRING,
  `timestamp` STRING,
  ip STRING,
  device STRING,
  platform STRING,
  user_agent STRING
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
  'format' = 'csv',
  'csv.ignore-parse-errors' = 'true',
  'csv.allow-comments' = 'true'
);

-- Enriched login events table
CREATE TABLE login_events_enriched (
  user_id STRING,
  `timestamp` STRING,
  ip STRING,
  platform STRING,
  device_type STRING,
  country STRING,
  city STRING,
  PRIMARY KEY (user_id, `timestamp`) NOT ENFORCED
) WITH (
  'connector' = 'upsert-kafka',
  'topic' = 'login-events-enriched',
  'properties.bootstrap.servers' = 'kafka:9092',
  'key.format' = 'json',
  'value.format' = 'json'
);

-- Anomalies output table
CREATE TABLE login_anomalies (
  user_id STRING,
  `timestamp` STRING,
  reason STRING,
  country STRING,
  PRIMARY KEY (user_id, `timestamp`) NOT ENFORCED
) WITH (
  'connector' = 'upsert-kafka',
  'topic' = 'login-anomalies',
  'properties.bootstrap.servers' = 'kafka:9092',
  'key.format' = 'json',
  'value.format' = 'json'
);
