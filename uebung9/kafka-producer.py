from kafka import KafkaProducer
import logging

logging.basicConfig(level=logging.WARN)

producer = KafkaProducer(
    bootstrap_servers=["infbdt06.fh-trier.de:6667"],
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism="GSSAPI")

response = producer.send("schmi-1", b"testmessage")
result = response.get(timeout=50)
print(result)
