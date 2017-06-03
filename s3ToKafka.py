from __future__ import print_function
from kafka import KafkaProducer
import boto3
import zlib
import os
import time

s3 = boto3.client('s3')
producer = KafkaProducer(bootstrap_servers=os.environ.get('KAFKA_HOST', 'localhost:9092'))
topic = os.environ.get('KAFKA_TOPIC', 'DASHBASE')
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
        start_time = time.time()
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            body = response['Body']
            data = body.read()
        except Exception as e:
            print(e)
            print('Error getting object {} from bucket {}. '.format(key, bucket))
            raise e

        print("=>   download usage time: {}s".format(time.time() - start_time))
        if key.endswith(".gz"):
            try:
                data = zlib.decompress(data, 16 + zlib.MAX_WBITS)
                print("Detected gzipped content")
                print("=>   gzip decompress usage time: {}s".format(time.time() - start_time))
            except zlib.error:
                print("Content couldn't be ungzipped, assuming plain text")
        lines = data.splitlines()
        try:
            for line in lines:
                producer.send(topic, line)
            producer.flush()
            print("=>   send usage time: {}s".format(time.time() - start_time))
            print("s3 file:{} transfer to kafka successful ".format(key))

            return key
        except Exception as e:
            raise e
