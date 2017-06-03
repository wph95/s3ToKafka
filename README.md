## S3 file to kafka by aws lambda

### How to usage

 ### 1.press create lambda 



### 2.select blueprint 

- select runtime -> python 2.7
- filter -> s3-get-objetct-python



### 3.configure triggers

- Bucket: {select your bucket}
- Event Type: Object Created ALL


- enable trigger: True



### 4.configure function

- Name: {your lambda name}
- Runtime: python2.7
- Code entry type: zip
- Environment variables
  - KAFKA_HOST => {your kafka host name}
  - KAFKA_TOPIC => {your kafka topic name}
- Handler (!important) : s3ToKafka.handler




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



