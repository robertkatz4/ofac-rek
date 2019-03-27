import os
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection, TransportError

host = os.environ["HOST"]
region = 'us-east-1'
headers={'Content-Type': 'application/json'}
awsauth = AWS4Auth(os.environ["ACCESS_KEY"], os.environ["SECRET_KEY"], region, 'es')
es_connect = Elasticsearch(
    hosts=[{'host': host,
             'port': 443
    }],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    headers=headers#, sniff_on_start=True, sniffer_timeout=10
)
