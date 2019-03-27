import xmltodict, json, os
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection, TransportError
from elasticsearch.client import CatClient

host = os.environ["HOST"]
region = 'us-east-1'
headers={'Content-Type': 'application/json'}
awsauth = AWS4Auth(os.environ["ACCESS_KEY"], os.environ["SECRET_KEY"], region, 'es')
es = Elasticsearch(
    hosts=[{'host': host,
             'port': 443
    }],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    headers=headers#, sniff_on_start=True, sniffer_timeout=10
)

def iterate_xml(xml_file, state='dev'):

    with open(xml_file) as fd:
        doc = xmltodict.parse(fd.read())
        sdn_xml = doc['sdnList']['sdnEntry']
        count = 0
        while (count < len(sdn_xml)):
            data = json.dumps(sdn_xml[count]) + '\n'
            try:
                if state='dev':
                    pass
                if state='prod':
                    es.index('ofac', '_doc', body=data, id=count) # how you index your document here
            except TransportError as e:
                print(e.info)
            if count % 100 == 0:
                print ('# ', count)
                print (data)
            count = count + 1
    catES = CatClient(es)
    o = catES.indices(['ofac'
                        ],bytes = 'b', v=True)
    print ('current state... \n', o)


def ofac_search(search_dict):
    for key, value in search_dict.items():
        for v in value:
            if key == 'all':
                search_json = "{\"query\":{\"query_string\":{\"query\":\"" + str(v) + "\"}}}"
            else:
                search_json = "{\"query\": {\"bool\": {\"must\": [{ \"match\": { \"" + str(key) + "\" : \"" + str(v) +  "\" }}]}}}"
            print ('###', search_json)
            results = es.search(index='ofac', body=search_json, _source = True)
            _len = results['hits']['total']
            print (_len, 'hits....')
            count = 0
            while (count < _len):
                print ('#', results['hits']['hits'][count]['_source'])
                count += 1

this_search_dict = {
 'lastName' : ['cuba'], 'uid': ['200'], 'all' : ['Nihombashi']
}

iterate_xml(os.environ["XML_FILE"])
ofac_search(this_search_dict)
