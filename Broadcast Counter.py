#Developed by Caleb Finigan

import getpass
import paramiko
import logging
import pandas as pd
import time
import re

# setup logging
# log messages will be stored in app.log file
# logging level is set to INFO, so only messages with level INFO and above will be logged
# messages will be logged in the format '%(asctime)s %(message)s'
# date format used is '%m/%d/%Y %I:%M:%S %p'
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Get the host, username and password
host = input("Enter host IP address: ")
username = input("Enter username: ")
password = getpass.getpass(prompt='Enter password: ')
timewait= int(input("Wait time between checks 'seconds': "))

# Connect to the host
try:
    # create a new SSH client
    ssh = paramiko.SSHClient()
    # automatically add the host's RSA key to the known host keys
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # connect to the host
    ssh.connect(host, username=username, password=password)
    # log a message indicating successful connection
    logging.info(f"Connected to {host} successfully.")
except Exception as e:
    # log the error message if connection fails
    logging.error(f"Failed to connect to {host}: {e}")
    # print the error message
    print(f"Failed to connect to {host}: {e}")
    # exit the program
    exit(1)

command = 'show interface'
try:
    # execute the command on the remote host
    stdin, stdout, stderr = ssh.exec_command(command)
except Exception as e:
    # log the error message if command execution fails
    logging.error(f"Failed to execute command: {e}")
    # print the error message
    print(f"Failed to execute command: {e}")

# decode the output from ascii
output = stdout.read().decode('ascii')
print("--------------------------")
# extract relevant information from the output
dataline = output.split("\n\n")    
#breaks up data for each interface
interface = None
count = None
#sets up data frame
df = pd.DataFrame(columns=['interface', 'RX broadcasts', 'RX broadcasts2', 'TX broadcasts', 'TX broadcasts2'])
#creates loop for each interaface
for lines in dataline:
    interface = None
    count = None
    counttx=None
    #creates loop for each line of the individial interface10
    for line in lines.split('\n'):
        if "is up" in line:
            #collects interface name
            interface = re.match(r'^(\S+)\s', line)
            if interface:
                interface = interface.group(1)
        if "Received" in line and "broadcast packets" in line:
            count = re.match(r'     Received (\d+) broadcast', line)
            if count:
                count = int(count.group(1))
        if "Output" in line and "broadcast packets" in line:
            counttx = re.match(r'     Output (\d+) broadcast', line)
            if counttx:
                counttx = int(counttx.group(1))
        if interface is not None and count is not None and (count != 0 or counttx != 0):
            df = df.append({'interface': interface, 'RX broadcasts': count, 'TX broadcasts': counttx}, ignore_index=True)
            interface = None
            count = None
            counttx=None
time.sleep(timewait)
try:
    # create a new SSH client
    ssh = paramiko.SSHClient()
    # automatically add the host's RSA key to the known host keys
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # connect to the host
    ssh.connect(host, username=username, password=password)
    # log a message indicating successful connection
    logging.info(f"Connected to {host} successfully.")
except Exception as e:
    # log the error message if connection fails
    logging.error(f"Failed to connect to {host}: {e}")
    # print the error message
    print(f"Failed to connect to {host}: {e}")
    # exit the program
    exit(1)
try:
    # execute the command on the remote host
    stdin, stdout, stderr = ssh.exec_command(command)
except Exception as e:
    # log the error message if command execution fails
    logging.error(f"Failed to execute command: {e}")
    # print the error message
    print(f"Failed to execute command: {e}")

# decode the output from ascii
output = stdout.read().decode('ascii')
print("--------------------------")
# extract relevant information from the output
dataline = output.split("\n\n")    
#breaks up data for each interface
interface = None
count = None
#creates loop for each interaface
for lines in dataline:
    interface = None
    count = None
    #creates loop for each line of the individial interface10
    for line in lines.split('\n'):
        if "is up" in line:
            #collects interface name
            interface = re.match(r'^(\S+)\s', line)
            if interface:
                interface = interface.group(1)
        if "Received" in line and "broadcast packets" in line:
            count = re.match(r'     Received (\d+) broadcast', line)
            if count:
                count = int(count.group(1))
        if "Output" in line and "broadcast packets" in line:
            counttx = re.match(r'     Output (\d+) broadcast', line)
            if counttx:
                     counttx = int(counttx.group(1))
        if interface is not None and count is not None and (count != 0 or counttx != 0):
                        # check if the interface already exists in the DataFrame
            if interface in df['interface'].values:
                df.loc[df['interface'] == interface, 'RX broadcasts2'] = count
                df.loc[df['interface'] == interface, 'TX broadcasts2'] = counttx
            interface = None
            count = None
            counttx=None
df = df[df['interface'].str.contains("/")]
df['RX Change'] = df['RX broadcasts2'] - df['RX broadcasts']
df['TX Change'] = df['TX broadcasts2'] - df['TX broadcasts']
print(df[['interface', 'RX broadcasts', 'RX broadcasts2', 'TX broadcasts', 'TX broadcasts2', 'RX Change', 'TX Change']])
anything = input("Type anything to close")
# Close the connection
ssh.close()
logging.info(f"Closed the connection to {host}.")
