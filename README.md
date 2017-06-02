[![CircleCI](https://circleci.com/gh/dashbase/s3ToKafka/tree/master.svg?style=svg)](https://circleci.com/gh/dashbase/s3ToKafka/tree/master)

## S3 file to kafka by aws lambda

### 1. usage

1. upload zip 
2. setting ENV ["KAFKA_HOST", "KAFKA_TOPIC"]



### 2. Build aws lambda package

```
# create python virtual env
pip install virtualenv
cd /path/to/project
virtualenv env
source env/bin/activate

# install libary
pip install -r requirements.txt

# add libary to lambda package
cd env/lib/python2.7/site-packages/
zip -r9 /path/to/project/s3ToKafka.zip *

# add source code to lambda package
cd /path/to/project
zip -g s3ToKafka.zip s3ToKafka.py
```



