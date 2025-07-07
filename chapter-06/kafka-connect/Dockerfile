# Dockerfile
FROM debezium/connect:2.5

# Download OpenSearch sink connector
RUN curl -L https://github.com/Aiven-Open/opensearch-connector-for-apache-kafka/releases/download/v3.1.1/opensearch-connector-for-apache-kafka-3.1.1.zip -o /tmp/opensearch-connector-for-kafka.zip && \
    unzip /tmp/opensearch-connector-for-kafka.zip -d /kafka/connect && \
    rm -f /tmp/opensearch-connector-for-kafka.zip
