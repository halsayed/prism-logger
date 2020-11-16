from elasticsearch import Elasticsearch
from datetime import datetime
from datetime import timezone


class ElasticClient(Elasticsearch):
    def __init__(self, ec_host='127.0.01', ec_port='9200'):
        hosts = [{'host': ec_host, 'port': ec_port}]
        super().__init__(hosts)

    def get_last_record(self, index):
        search_last_record = {
            'size': 1,
            'sort': {'timestamp': 'desc'},
            'query': {'match_all': {}}
        }
        return self.search(index=index, body=search_last_record)

    def last_record_time(self, index):
        record = self.get_last_record(index)
        if record['hits']['total']['value']:
            # get latest record in es
            return datetime.fromisoformat(record['hits']['hits'][0]['_source']['timestamp'])
        else:
            # audits log is empty, insert all records
            return datetime(year=2010, month=1, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc)