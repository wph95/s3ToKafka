from __future__ import print_function
from kafka import KafkaProducer
import boto3
import os
import smart_open

producer = KafkaProducer(bootstrap_servers=os.environ.get('KAFKA_HOST', 'localhost:9092'))
topic = os.environ.get('KAFKA_TOPIC', 'DASHBASE')
s3 = boto3.client('s3')
print('Loading function host:{} topic:{}', producer, topic)


class ReadOnce(object):
    def __init__(self, k):
        self.key = k
        self.has_read_once = False


def read(self, size=0):
    if self.has_read_once:
        return b''
    data = self.key.read(size)
    if not data:
        self.has_read_once = True
    return data


def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        try:
            key = s3.get_bucket("my_bucket").get_key("my_key")
            #   smart_open supports gzipped content
            #   as long as the key is obviously a gzipped file (e.g. ends with ".gz").
            with smart_open.smart_open(key) as f:
                for message in f:
                    producer.send(topic, message)
            producer.flush()

            print("s3 file:{} transfer to kafka successful ".format(key))
            return key
        except Exception as e:
            print(e)
            print('Error getting object {} from bucket {}. '.format(key, bucket))
            raise e
