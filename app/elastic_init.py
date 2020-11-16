from elasticsearch import Elasticsearch
from config import *
from model import indexes


def main():
    es_hosts = [{'host': ec_host, 'port': ec_port}]
    es = Elasticsearch(es_hosts)

    for index in indexes:
        resp = es.indices.create(index=index['name'], body={'mappings': index['mappings']}, ignore=400)
        log.info(f'result for creating index: {index["name"]}: {resp}')


if __name__ == '__main__':
    main()
