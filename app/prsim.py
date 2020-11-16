import requests
from urllib.parse import urljoin
from config import log
import datetime
from datetime import datetime,timezone


from helpers import flatten_resource, parse_log_message


class PrismClient(requests.Session):

    def __init__(self, prism_ip, prism_port, username, password, prism_timezone=timezone.utc, verify_ssl=False):
        self.base_url = f'https://{prism_ip}:{prism_port}/api/nutanix/v3/'
        self.timezone = prism_timezone
        super().__init__()
        self.auth = (username, password)
        self.verify = verify_ssl

    def get_audit_logs(self, starting_time=None, default_length=100):
        # check the total number of records for paginated download
        result = self._api_audit_logs(length=default_length)
        filtered_logs = []
        if not starting_time:
            starting_time = datetime(year=2010, month=1, day=1, hour=0, minute=0, second=0, tzinfo=self.timezone)

        for x in range(0, result['total']//default_length+1):
            for entry in result['logs']:
                if entry['timestamp'] >= starting_time:
                    filtered_logs.append(entry)
                else:
                    return filtered_logs
            offset = result['offset'] + result['length']
            if offset < result['total']:
                result = self._api_audit_logs(offset=offset, length=default_length)

        return filtered_logs

    def _api_audit_logs(self, offset=0, length=100):
        payload = {'kind': 'audit', 'sort_order': 'DESCENDING', 'offset': offset,
                   'sort_attribute': 'op_end_timestamp_usecs', 'length': length}

        url = urljoin(self.base_url, 'audits/list')
        resp = self.post(url, json=payload)
        if resp.status_code == 200:
            json_result = resp.json()
            result = {
                'total': int(json_result['metadata']['total_matches']),
                'length': int(json_result['metadata']['length']),
                'offset': int(json_result['metadata']['offset']),
                'logs': []
            }
            log.info(f'API call for audit call successful, '
                     f'total records: {result["total"]}, offset: {result["offset"]}, length: {result["length"]}')

            for entity in json_result['entities']:
                if entity['status'].get('operation_complete_time'):
                    affected_resources = flatten_resource(entity['status'].get('affected_entity_reference_list', []))
                    parsed_message = parse_log_message(entity['status'].get('audit_message', ''),
                                                       entity['status'].get('operation_parameter_list', []))

                    parsed_entity = {
                        'id': entity['metadata']['uuid'],
                        'timestamp': datetime.fromisoformat(entity['status']['operation_complete_time'])
                        .replace(tzinfo=self.timezone),
                        'user.uuid': entity['status']['initiated_user'].get('uuid'),
                        'user.name': entity['status']['initiated_user'].get('name'),
                        'source_entity.uuid': entity['status']['source_entity_reference']['uuid'],
                        'source_entity.name': entity['status']['source_entity_reference']['name'],
                        'source_entity.type': entity['status']['source_entity_reference']['type'],
                        'affected_entities.uuid': affected_resources['uuid'],
                        'affected_entities.name': affected_resources['name'],
                        'affected_entities.type': affected_resources['type'],
                        'operation_type': entity['status']['operation_type'],
                        'message': parsed_message
                    }
                    result['logs'].append(parsed_entity)

            return result
        else:
            # TODO: Better connection error handling
            log.error(f'Error in API call, status code: {resp.status_code}, message: {resp.content}')
