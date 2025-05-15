from netmiko import ConnectHandler

device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'cisco'
}

connection = ConnectHandler(**device)
output = connection.send_command('show run')
print(output)
connection.disconnect()
