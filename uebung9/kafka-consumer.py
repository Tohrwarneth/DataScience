from kafka import KafkaConsumer
import logging

logging.basicConfig(level=logging.WARN)

consumer = KafkaConsumer("schmi-1",
    group_id="schmi",
    bootstrap_servers=["infbdt06.fh-trier.de:6667"],
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism="GSSAPI")

for msg in consumer:
    print(msg)
