
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


if __name__ == '__main__':
    ofac_search(this_search_dict)
