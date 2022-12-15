import paramiko
import time
import getpass
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

password = getpass.getpass('Enter password:')

router1 = {'hostname': '10.1.1.10', 'port': '22', 'username':'khoadang', 'password': password}
router2 = {'hostname': '10.1.1.20', 'port': '22', 'username':'khoadang', 'password':password}
router3 = {'hostname': '10.1.1.30', 'port': '22', 'username':'khoadang', 'password':password}


routers = [router1, router2, router3]


for router in routers:
    print(f'Connecting to {router["hostname"]}')
    ssh_client.connect(**router, look_for_keys=False, allow_agent=False)
    shell = ssh_client.invoke_shell()

    shell.send('enable\n')
    shell.send('1234\n')
    shell.send('conf t\n')
    shell.send('router ospf 1\n')
    shell.send('net 0.0.0.0 0.0.0.0 area 0\n')
    shell.send('end\n')
    shell.send('terminal length 0\n')
    shell.send('sh ip protocols\n')
    time.sleep(5)

    output = shell.recv(10000).decode()
    print(output)











if ssh_client.get_transport().is_active() == True:
    print('Closing connection')
    ssh_client.close()