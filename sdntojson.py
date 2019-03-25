import xmltodict, json, boto3, os
from requests_aws4auth import AWS4Auth
import requests


def put_json(data):
    host = 'https://search-movies-lhd34cp5ng4kxk6uxfmvacymte.us-east-1.es.amazonaws.com/'
    path = 'my-index/_doc'
    region = 'us-east-1'

    credentials = boto3.Session(
                            aws_access_key_id=os.environ["ACCESS_KEY"],
                            aws_secret_access_key=os.environ["SECRET_KEY"],
                            # aws_session_token=None,
                            region_name=region,
                            # botocore_session=None,
                            profile_name='rkatz-sandbox'
                    ).get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es')

    url = host + path

    # The JSON body to accompany the request (if necessary)
    payload = {
        "settings" : {
            "number_of_shards" : 7,
            "number_of_replicas" : 2
        }
    }

    headers={'Content-Type': 'application/json'}
    r = requests.post(
                    url,
                    json=data,
                    headers=headers
    )
    print(r.text)


with open('sdn.xml') as fd:
    doc = xmltodict.parse(fd.read())
    sample = doc['sdnList']['sdnEntry']
    count = 0
    while (count < 2):
        data = json.dumps(sample[count]) + '\n'
        # print ('######', data)
        print (data)
        put_json(data)
        count = count + 1
