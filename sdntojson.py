import xmltodict, json, boto3, os
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection, TransportError
import requests

host = 'search-movies-lhd34cp5ng4kxk6uxfmvacymte.us-east-1.es.amazonaws.com'
path = '/my-index/_doc'
url = host + path
region = 'us-east-1'
headers={'Content-Type': 'application/json'}


def put_json(data):


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

    r = requests.post(
                    url,
                    json=data,
                    headers=headers
    )
    print(r.text)



awsauth = AWS4Auth(os.environ["ACCESS_KEY"], os.environ["SECRET_KEY"], region, 'es')
print ('0')
es = Elasticsearch(
    hosts=[{'host': host,
             'port': 443
    }],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    headers=headers
)
s_data= '{"uid": "36", "lastName": "SUCCESS AIRLINES", "sdnType": "Entity", "programList": {"program": "CUBA"}, "akaList": {"aka": {"uid": "12", "type": "a.k.a.", "category": "strong", "lastName": "AERO-CARIBBEAN"}}, "addressList": {"address": {"uid": "25", "city": "Havana", "country": "Cuba"}}}'
print ('curl -XPOST search-movies-lhd34cp5ng4kxk6uxfmvacymte.us-east-1.es.amazonaws.com/movies/_doc/1 -d ')
try:
    es.index('movies', '_doc', s_data) # how you index your document here
except TransportError as e:
    print(e.info)
# print(es.info())

# curl -XPOST search-movies-lhd34cp5ng4kxk6uxfmvacymte.us-east-1.es.amazonaws.com/movies/_doc/1 -d '{"uid": "173",
#"lastName": "ANGLO-CARIBBEAN CO., LTD.", "sdnType": "Entity", "programList": {"program": "CUBA"}, "akaList": {"aka": {"uid": "57", "type": "a.k.a.", "category": "strong", "lastName": "AVIA IMPORT"}}, "addressList": {"address": {"uid": "129", "address1": "Ibex House, The Minories", "city": "London", "postalCode": "EC3N 1DY", "country": "United Kingdom"}}}' -H 'Content-Type: application/json'

# with open('sdn.xml') as fd:
#     doc = xmltodict.parse(fd.read())
#     sample = doc['sdnList']['sdnEntry']
#     count = 0
#     while (count < 2):
#         data = json.dumps(sample[count]) + '\n'
#         # print ('######', data)
#         print (data)
#         put_json(data)
#         count = count + 1
