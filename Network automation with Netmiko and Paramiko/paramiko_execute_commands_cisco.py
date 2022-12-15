import paramiko
import time
import getpass

ssh_client = paramiko.SSHClient()
password = getpass.getpass('Enter Password:')
router = {'hostname': '10.1.1.10', 'port': '22', 'username':'khoadang', 'password': password}
print(f'Connecting to {router["hostname"]}')
ssh_client.connect(**router, look_for_keys=False, allow_agent=False)

shell = ssh_client.invoke_shell()



shell.send('enable\n')
shell.send('1234\n')
shell.send('configure terminal\n')
shell.send('int e0/1\n')
shell.send('ip address 192.168.1.3 255.255.255.0\n')
shell.send('do show ip int brief\n')
time.sleep(5)


output = shell.recv(10000)



output = output.decode('utf-8')
print(output)


if ssh_client.get_transport().is_active() == True:
    print('Closing connection')
    ssh_client.close()