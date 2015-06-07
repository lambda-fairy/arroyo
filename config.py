import os

host = os.environ.get('HOST', '')
port = os.environ.get('PORT', 8144)

config_root = os.path.dirname(os.path.realpath(__file__))
script_root = os.path.join(config_root, 'scripts')

max_request_size = 10 ** 6
max_queue_size = 5

secrets_path = os.path.join(config_root, 'secrets')
check_signatures = True
