from ncclient import manager

device = {
    'host': '192.168.1.1',
    'port': 830,
    'username': 'admin',
    'password': 'cisco',
    'hostkey_verify': False
}

with manager.connect(**device) as m:
    config = m.get_config(source='running')
    print(config)
