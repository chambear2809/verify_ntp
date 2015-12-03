'''
Python 2.7.x only
show_ntp


Copyright (C) 2015 Cisco Systems Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''
#!/usr/bin/env python

import sys
import paramiko as pm
sys.stderr = sys.__stderr__
import os

forHtmlString = ""
#HtmldomainInfo = []

class AllowAllKeys(pm.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return

def ssh_leaf(hostIP, userID, pw):
    forHtmlString = ""

    client = pm.SSHClient()
    client.load_system_host_keys()
    client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    client.set_missing_host_key_policy(AllowAllKeys())
    client.connect(hostIP, username=userID, password=pw)

    channel = client.invoke_shell()
    stdin = channel.makefile('wb')
    stdout = channel.makefile('rb')

    stdin.write('''
show ntp peers
show ntp peer-status
exit
''')
    lines = stdout.readlines()
    for line in lines:
        print line.strip('\n')
        linez = line.strip('\n')
        forHtmlString += linez #+"<br>"

    print
    stdout.close()
    stdin.close()
    client.close()

    return forHtmlString

def ssh_apic(hostIP, userID, pw):
    forHtmlString = ""

    client = pm.SSHClient()
    client.load_system_host_keys()
    client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    client.set_missing_host_key_policy(AllowAllKeys())
    client.connect(hostIP, username=userID, password=pw)
    channel = client.invoke_shell()
    stdin = channel.makefile('wb')
    stdout = channel.makefile('rb')

    stdin.write('''
cat /etc/ntp.conf
ntpstat
exit
''')
    lines = stdout.readlines()
    for line in lines:
        print line.strip('\n')
        linez = line.strip('\n')
        forHtmlString += linez #+"<br>"

    print
    stdout.close()
    stdin.close()
    client.close()

    return forHtmlString

###-----------------------------------------------------------------------------------###
def main(hostIP, userID, pw):
    HtmldomainInfo = []

    forHtmlString = ""
    forHtmlString += '<pre>'
    forHtmlString += '<!DOCTYPE>'
    forHtmlString += '<html>'
    forHtmlString += '<head>'
    forHtmlString += '</head>'
    forHtmlString += '<body>'
    print '\n APIC OOB IP : ' + hostIP
    linez = '<b> APIC OOB IP : ' + hostIP
    forHtmlString += "<br>"+"<br>"+linez+"<br>"
    print   '\n              Check NTP in ACI Fabric Solution'
    linez = '              Check NTP in ACI Fabric Solution'
    forHtmlString += linez+"<br>"
    print   '\n======================================================================================================\n'
    linez = '======================================================================================================'
    forHtmlString += linez+"<br>"
    HtmldomainInfo.append(forHtmlString)
    forHtmlString = ""

### leaf
    print '*************************** Leaf ******************************************** '
    linez = '*************************** Leaf ******************************************** '
    forHtmlString += "<br>"+"<br>"+linez+"<br>"
    HtmldomainInfo.append(forHtmlString)

    hostIP, userID, pw = '172.16.65.8', 'admin', 'ins3965!'
    forHtmlString = ssh_leaf(hostIP, userID, pw)
    HtmldomainInfo.append(forHtmlString)
    forHtmlString = ""

### APIC
    print '*************************** APIC ******************************************** '
    linez = '*************************** APIC ******************************************** '
    forHtmlString += "<br>"+"<br>"+linez+"<br>"
    HtmldomainInfo.append(forHtmlString)

    hostIP, userID, pw = '172.16.65.5', 'admin', 'ins3965!'
    forHtmlString = ssh_apic(hostIP, userID, pw)
    HtmldomainInfo.append(forHtmlString)
    forHtmlString = ""

    forHtmlString += '</body>'
    forHtmlString += '</html>'
    forHtmlString += '</pre>'
    HtmldomainInfo.append(forHtmlString)

    return HtmldomainInfo

###------------------------------------------------------------------------------------------------------------------------###
if __name__ == "__main__":
    apicIP, userID, pw = '', '',''
    main(sys.argv[1],sys.argv[2],sys.argv[3])

