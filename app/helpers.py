
def flatten_resource(resources):
    flat_result = {'uuid': [], 'name': [], 'type': []}
    for resource in resources:
        flat_result['uuid'].append(resource['uuid'])
        flat_result['name'].append(resource['name'])
        flat_result['type'].append(resource['type'])

    return flat_result


def parse_log_message(message, parameters):
    for parameter in parameters:
        message = message.replace('{'+parameter['name']+'}', str(list(parameter['value'].values())[0]))
    return message


