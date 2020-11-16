import urllib3
from prsim import PrismClient
from elastic import ElasticClient
from config import prism_config, ec_config, audit_index, log

urllib3.disable_warnings()

log.info('initializing elastic client and prism client')
ec_client = ElasticClient(**ec_config)
prism_client = PrismClient(**prism_config)


def main():
    last_audit_time = ec_client.last_record_time(audit_index)
    log.info(f'Last recorded time in index {audit_index} is: {last_audit_time}')

    audit_logs = prism_client.get_audit_logs(starting_time=last_audit_time, default_length=200)
    log.info(f'total logs from {audit_index} is: {len(audit_logs)}')

    if len(audit_logs):
        log.info(f'inserting logs to elastic index {audit_index}')
        for audit_log in audit_logs:
            ec_client.index(index=audit_index, id=audit_log['id'], body=audit_log)


if __name__ == '__main__':
    main()






