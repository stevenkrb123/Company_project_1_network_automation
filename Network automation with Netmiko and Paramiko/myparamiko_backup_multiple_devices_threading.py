import myparamiko
import threading
import getpass


# this function backups the config of a router
# this is the target function which gets executed by each thread
def backup(router):
    client = myparamiko.connect(**router)
    shell = myparamiko.get_shell(client)

    myparamiko.send_command(shell, 'terminal length 0')
    myparamiko.send_command(shell, 'enable')
    myparamiko.send_command(shell, '1234')  # this is the enable command
    myparamiko.send_command(shell, 'show run')

    output = myparamiko.show(shell)
    # print(output)
    output_list = output.splitlines()
    output_list = output_list[11:-1]
    # print(output_list)
    output = '\n'.join(output_list)
    # print(output)

    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

    file_name = f'{router["server_ip"]}_{year}-{month}-{day}.txt'
    with open(file_name, 'w') as f:
        f.write(output)

    myparamiko.close(client)
password = getpass.getpass('Enter password:')
router1 = {'server_ip':'10.1.1.10', 'server_port': '22', 'user': 'khoadang', 'passwd': password}
router2 = {'server_ip':'10.1.1.20', 'server_port': '22', 'user': 'khoadang', 'passwd': password}
router3 = {'server_ip':'10.1.1.30', 'server_port': '22', 'user': 'khoadang', 'passwd': password}

# creating a list of dictionaries (of devices)
routers = [router1, router2, router3]

# creating an empty list (it will store the threads)
threads = list()
for router in routers:
    # creating a thread for each router that executes the backup function
    th = threading.Thread(target=backup, args=(router,))
    threads.append(th)  # appending the thread to the list

# starting the threads
for th in threads:
    th.start()

# waiting for the threads to finish
for th in threads:
    th.join()