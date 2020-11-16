
indexes = [{
    'name': 'audits',
    'mappings': {
        'properties': {
            'id': {'type': 'keyword'},
            'timestamp': {'type': 'date'},
            'user.uuid': {'type': 'keyword'},
            'user.name': {'type': 'keyword'},
            'source_entity.uuid': {'type': 'keyword'},
            'source_entity.name': {'type': 'text'},
            'source_entity.type': {'type': 'keyword'},
            'affected_entities.uuid': {'type': 'keyword'},
            'affected_entities.name': {'type': 'text'},
            'affected_entities.type': {'type': 'keyword'},
            'operation_type': {'type': 'keyword'},
            'message': {'type': 'text'},
        }
    }
}]
