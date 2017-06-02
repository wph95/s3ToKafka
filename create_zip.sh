#!/bin/bash
virtualenv env && \
	source env/bin/activate && \
	pip install -r requirements.txt && \
	cd env/lib/python2.7/site-packages/ && \
	zip -r9 ~/s3ToKafka/s3ToKafka.zip * && \
	cd ~/s3ToKafka/ && \
	zip -g s3ToKafka.zip s3ToKafka.py
