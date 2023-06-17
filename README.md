# IOS-BroadcastCheck
Displays Broadcast packet change for time input for IOS and IOS-XR, assisting with interface troubleshooting



This is a Python script that connects to a remote host using SSH and retrieves information about network interfaces.
It uses the paramiko library for SSH communication and the pandas library for data manipulation.

Prerequisites

    Python 3.x
    paramiko library (pip install paramiko)
    pandas library (pip install pandas)

Usage

    Clone the repository or download the script.
    Install the required libraries mentioned in the prerequisites.
    Open the script in a Python IDE or text editor.
    Replace the placeholder values in the script with your actual remote host IP address, username, and password.
    Adjust the timewait variable if desired. This determines the wait time between checks in seconds.
    Run the script.

The script will establish an SSH connection to the remote host, execute the show interface command, and retrieve information about network interfaces. It will then print the relevant information, including received and transmitted broadcast packets, and calculate the change in values between two consecutive checks. The results will be displayed in a tabular format.

Please note that the script logs information to the app.log file, including successful connections and any errors encountered during execution.

After running the script, you will be prompted to enter anything to close the program.
