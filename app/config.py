import os
import logging
from datetime import timezone, timedelta


# prism config
prism_ip = os.environ.get('PRISM_IP', '10.38.2.9')
prism_port = os.environ.get('PRISM_PORT', '9440')
verify_ssl = os.environ.get('VERIFY_SSL', False)
username = os.environ.get('PRISM_USERNAME', 'admin')
password = os.environ.get('PRISM_PASSWORD', 'nx2Tech911!')
prism_timezone = os.environ.get('PRISM_TIMEZONE', timezone(timedelta(hours=int(-8))))

# elastic config
ec_host = os.environ.get('EC_HOST', 'localhost')
ec_port = os.environ.get('EC_PORT', '9200')

# other config
log_level = os.environ.get('LOG_LEVEL', 'INFO')
audit_index = 'audits'


prism_config = dict(((k, eval(k)) for k in ('prism_ip', 'prism_port', 'verify_ssl', 'username', 'password',
                                            'prism_timezone')))
ec_config = dict(((k, eval(k)) for k in ('ec_host', 'ec_port')))
# create logger
log = logging.getLogger()
log.setLevel(log_level)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(log_level)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
log.addHandler(ch)