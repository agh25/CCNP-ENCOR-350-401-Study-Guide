# CCNP ENCOR 350-401 Automation Lab

**Copyright © 2025 Abdelaziz Ghazal, CCIE #62123. All rights reserved.**  
**Author**: Abdelaziz Ghazal, CCIE #62123

This lab demonstrates network automation for the **Cisco CCNP ENCOR 350-401** exam (automation topics 6.0, 15%), using Python with NETCONF and RESTCONF, and orchestration tools (Chef, Puppet, Ansible) on Cisco CSR 1000v routers and IOSv switches in EVE-NG, managed from a Linux DEVASC VM (Ubuntu 22.04). It includes definitions of NETCONF, RESTCONF, SaltStack, Chef, and Puppet, and aligns with **DEVASC 200-901** programmability concepts.

## Definitions

1. **NETCONF (Network Configuration Protocol)**:
   - **Definition**: NETCONF (RFC 6241) is an IETF protocol for managing network devices, using XML-based data over SSH (port 830). It supports YANG models for structured configuration and operational data retrieval, enabling transaction-based automation (e.g., commit/rollback).
   - **Use**: Configures devices programmatically with tools like `ncclient`. In this lab, NETCONF configures loopback interfaces and VLANs (ENCOR topic 6.3).
   - **Relevance**: Provides model-driven automation for enterprise networks, superior to CLI scripting.

2. **RESTCONF**:
   - **Definition**: RESTCONF (RFC 8040) is an IETF protocol offering a RESTful API for network device management over HTTP/HTTPS (port 443), using JSON/XML with YANG models. It supports CRUD operations (Create, Read, Update, Delete).
   - **Use**: Enables web-based configuration via HTTP methods. Here, RESTCONF configures interface descriptions and VLAN interfaces using `requests` (ENCOR topics 6.2, 6.5).
   - **Relevance**: Simplifies automation with web-compatible APIs, used in platforms like Cisco DNA Center.

3. **SaltStack**:
   - **Definition**: SaltStack is an open-source configuration management and orchestration tool using a client-server model (Salt Minions/Master) with Python/YAML. It supports event-driven automation and remote execution via push/pull architectures.
   - **Use**: Can manage network devices via SSH/APIs, though less common for Cisco compared to Ansible. Not implemented here but relevant for ENCOR topic 6.7 (orchestration tools).
   - **Relevance**: Agent-based, contrasts with agentless tools like Ansible.

4. **Chef**:
   - **Definition**: Chef is an agent-based configuration management tool using Ruby-based recipes/cookbooks to automate infrastructure as code. It operates in client-server (Chef Client/Server) or standalone (Chef Solo) modes, ensuring idempotent configurations.
   - **Use**: In this lab, Chef configures router hostnames via SSH (ENCOR topic 6.7).
   - **Relevance**: Agent-based, supports consistent device states in enterprise automation.

5. **Puppet**:
   - **Definition**: Puppet is an agent-based configuration management tool using a declarative Puppet DSL and client-server model (Puppet Agent/Master). It ensures idempotent configurations via modules.
   - **Use**: Here, Puppet configures VLANs on switches via SSH (ENCOR topic 6.7).
   - **Relevance**: Agent-based, contrasts with agentless tools for enterprise automation.

**Note**: Ansible is used instead of SaltStack for Cisco device automation, as it’s more prevalent in ENCOR labs (topic 6.7) with `cisco.ios` modules. SaltStack is defined but not implemented.

## Lab Overview

**Objective**: Configure and validate network settings on CSR 1000v routers and IOSv switches using NETCONF, RESTCONF, Chef, Puppet, and Ansible, aligning with ENCOR automation topics (6.1–6.3, 6.5, 6.7).

**Components**:
- **EVE-NG**: Virtual topology host.
- **Cisco CSR 1000v**: Routers (IOS-XE 16.09.06) for NETCONF/RESTCONF.
- **Cisco IOSv**: Switches (IOS 15.9) for NETCONF/RESTCONF.
- **Linux DEVASC VM**: Ubuntu 22.04 with Python, `ncclient`, `requests`, Chef, Puppet, Ansible, VSCode.
- **Topology**: Two routers (R1, R2), two switches (SW1, SW2), management network.

**Tasks**:
1. NETCONF: Configure loopback interfaces (routers) and VLANs (switches), validate YANG models.
2. RESTCONF: Set interface descriptions (routers) and VLAN interfaces (switches), handle JSON/response codes.
3. Chef: Configure router hostnames.
4. Puppet: Configure switch VLANs.
5. Ansible: Configure interface settings on routers/switches.
6. Validate JSON outputs.

**Skills Covered**:
- **ENCOR 350-401**: Python (6.1), JSON (6.2), YANG (6.3), REST API (6.5), orchestration (6.7).
- **DEVASC 200-901**: Network automation, APIs, configuration management.

**Prerequisites**:
- EVE-NG (16GB RAM, 4 vCPUs).
- CSR 1000v (`csr1000v-universalk9.16.09.06.iso`), IOSv (`vios_l2-adventerprisek9-m.vmdk.SPA.159-3.M2`).
- Ubuntu 22.04 VM (2 vCPUs, 4GB RAM, 20GB disk).
- Cisco IOS-XE 16.3+ for RESTCONF.

## Lab Setup

### 1. EVE-NG Installation
1. **Install EVE-NG**:
   - Download Community Edition from [eve-ng.net](https://www.eve-ng.net/).
   - Install on VMware ESXi/VirtualBox (16GB RAM, 100GB disk).
   - Follow [EVE-NG documentation](https://www.eve-ng.net/index.php/documentation/).

2. **Add Images**:
   - **CSR 1000v**: Upload to `/opt/unetlab/addons/qemu/csr1000vng-universalk9.16.09.06/`.
   - **IOSv**: Upload to `/opt/unetlab/addons/qemu/viosl2-adventerprisek9-m.vmdk.SPA.159-3.M2/`.
   - Fix permissions:
     ```bash
     /opt/unetlab/wrappers/unl_wrapper -a fixpermissions
     ```

3. **Create Topology**:
   - In EVE-NG GUI, create lab “ENCOR-Automation-Lab”.
   - Add nodes:
     - 2 CSR 1000v routers (R1, R2).
     - 2 IOSv switches (SW1, SW2).
     - 1 Management Cloud (Cloud0).
   - Connect:
     - R1 (GigabitEthernet1) → SW1 (Eth0/0).
     - R2 (GigabitEthernet1) → SW2 (Eth0/0).
     - SW1 (Eth0/1) ↔ SW2 (Eth0/1).
     - SW1 (Eth0/2) → Cloud0.
   - **Topology Diagram**:
     ```
     R1(G1)---SW1(E0/0)---(E0/1)---SW2(E0/0)---R2(G1)
                  |
                 E0/2
                  |
               Cloud0 (Management)
     ```

### 2. DEVASC VM Setup
1. **Install Ubuntu 22.04**:
   - Download Ubuntu Server 22.04 from [ubuntu.com](https://ubuntu.com/download/server).
   - Create VM (2 vCPUs, 4GB RAM, 20GB disk, Bridged Network: 192.168.56.0/24).
   - Update:
     ```bash
     sudo apt-get update && sudo apt-get upgrade -y
     ```

2. **Install Tools**:
   - **Python**:
     ```bash
     sudo apt-get install -y python3 python3-venv python3-pip
     pip3 install ncclient requests ansible
     ```
   - **Chef Workstation**:
     ```bash
     wget https://packages.chef.io/files/stable/chef-workstation/22.10.1013/ubuntu/20.04/chef-workstation_22.10.1013-1_amd64.deb
     sudo dpkg -i chef-workstation_22.10.1013-1_amd64.deb
     ```
   - **Puppet Agent**:
     ```bash
     wget https://apt.puppet.com/puppet7-release-focal.deb
     sudo dpkg -i puppet7-release-focal.deb
     sudo apt-get update
     sudo apt-get install -y puppet-agent
     ```
   - **VSCode**:
     ```bash
     sudo snap install code --classic
     ```

3. **Configure Network**:
   - Set IP (192.168.56.104):
     ```bash
     sudo nano /etc/netplan/00-installer-config.yaml
     ```
     ```yaml
     network:
       ethernets:
         enp0s3:
           addresses: [192.168.56.104/24]
           gateway4: 192.168.56.1
           nameservers:
             addresses: [8.8.8.8]
       version: 2
     ```
     ```bash
     sudo netplan apply
     ```

### 3. Configure Devices
1. **Start Devices**:
   - Power on R1, R2, SW1, SW2, and Cloud0 in EVE-NG.

2. **Router Configuration (R1, R2)**:
   - Enable NETCONF, RESTCONF, SSH.
   - **R1 Configuration** (`r1_config.txt`):
     ```text
     enable
     configure terminal
     hostname R1
     ip domain-name lab.local
     crypto key generate rsa modulus 2048
     ip ssh version 2
     username cisco privilege 15 secret cisco
     line vty 0 4
      login local
      transport input ssh
     netconf-yang
     restconf
     ip http secure-server
     interface GigabitEthernet1
      ip address 192.168.56.101 255.255.255.0
      no shutdown
     ip route 0.0.0.0 0.0.0.0 192.168.56.1
     end
     write memory
     ```
   - **R2 Configuration**: IP `192.168.56.102`, hostname `R2`.

3. **Switch Configuration (SW1, SW2)**:
   - **SW1 Configuration** (`sw1_config.txt`):
     ```text
     enable
     configure terminal
     hostname SW1
     ip domain-name lab.local
     crypto key generate rsa modulus 2048
     ip ssh version 2
     username cisco privilege 15 secret cisco
     line vty 0 4
      login local
      transport input ssh
     netconf-yang
     restconf
     ip http secure-server
     interface Ethernet0/0
      switchport mode access
      no shutdown
     interface Ethernet0/1
      switchport mode trunk
      no shutdown
     interface Ethernet0/2
      switchport mode access
      no shutdown
     vlan 10
      name MANAGEMENT
     interface vlan 10
      ip address 192.168.56.201 255.255.255.0
      no shutdown
     ip default-gateway 192.168.56.1
     end
     write memory
     ```
   - **SW2 Configuration**: IP `192.168.56.202`, hostname `SW2`.

4. **Verify Connectivity**:
   - From DEVASC VM:
     ```bash
     ping 192.168.56.101  # R1
     ping 192.168.56.102  # R2
     ping 192.168.56.201  # SW1
     ping 192.168.56.202  # SW2
     ```
   - Test SSH:
     ```bash
     ssh cisco@192.168.56.101
     ```
     - Fix SSH if needed:
       ```bash
       echo "PubkeyAcceptedAlgorithms +ssh-rsa" | sudo tee -a /etc/ssh/ssh_config
       sudo service sshd restart
       ```

## Automation Scripts and Configurations

### 1. NETCONF Script (Topics 6.1, 6.3)
Configures loopback interfaces (routers: Loopback1, 1.1.1.1/32) and VLAN 20 (switches) using NETCONF with YANG models.

**`netconf_config.py`**:
```python
# Import required libraries for NETCONF, XML parsing, logging, and JSON handling
from ncclient import manager
import xmltodict
import logging
import json

# Configure logging to track script execution and errors
logging.basicConfig(filename='netconf_config.log', level=logging.INFO)
logger = logging.getLogger("netconf")

# Define devices with their IP, hostname, and type (router/switch)
devices = [
    {"host": "192.168.56.101", "hostname": "R1", "type": "router"},
    {"host": "192.168.56.102", "hostname": "R2", "type": "router"},
    {"host": "192.168.56.201", "hostname": "SW1", "type": "switch"},
    {"host": "192.168.56.202", "hostname": "SW2", "type": "switch"}
]

# Define NETCONF XML configuration for routers (Loopback1 with IP 1.1.1.1/32)
router_config = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>1</name>
        <ip>
          <address>
            <primary>
              <address>1.1.1.1</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

# Define NETCONF XML configuration for switches (VLAN 20, name DATA)
switch_config = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <vlan>
      <vlan-list>
        <id>20</id>
        <name>DATA</name>
      </vlan-list>
    </vlan>
  </native>
</config>
"""

# Prompt for credentials (username and password)
username = input("Enter username: ")
password = input("Enter password: ")

# Initialize dictionary to store configuration results
results = {}

# Iterate through devices to apply configurations
for device in devices:
    host = device["host"]
    try:
        print(f"\nConnecting to {host} ({device['hostname']})...")
        logger.info(f"Attempting NETCONF connection to {host}")
        
        # Establish NETCONF connection (ENCOR 6.1: Python components)
        conn = manager.connect(
            host=host,
            port=830,
            username=username,
            password=password,
            device_params={'name': 'iosxe'},
            hostkey_verify=False
        )
        logger.info(f"Connected to {host}")
        
        # Select and apply configuration based on device type (ENCOR 6.3: YANG)
        config_xml = router_config if device["type"] == "router" else switch_config
        conn.edit_config(target="running", config=config_xml)
        
        # Define XML filter to retrieve configuration (Loopback or VLAN)
        filter_xml = """
        <filter>
          <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface><Loopback><name>1</name></Loopback></interface>
            <vlan><vlan-list><id>20</id></vlan-list></vlan>
          </native>
        </filter>
        """
        # Retrieve and parse configuration
        result = conn.get_config(source="running", filter=filter_xml)
        results[host] = xmltodict.parse(result.data_xml)
        print(f"Configuration applied on {host}:\n{json.dumps(results[host], indent=4)}\n{'-'*50}")
        
        # Close NETCONF session
        conn.close_session()
        logger.info(f"Disconnected from {host}")
        
    except Exception as e:
        # Log and display errors
        logger.error(f"Error on {host}: {str(e)}")
        print(f"Error on {host}: {str(e)}")

# Save results to JSON file (ENCOR 6.2: JSON handling)
with open('netconf_results.json', 'w') as f:
    json.dump(results, f, indent=4)
print("Results saved to netconf_results.json")
```

**Exam Alignment**:
- **6.1**: Python loops, dictionaries, error handling.
- **6.3**: Cisco IOS-XE YANG models.
- **6.2**: JSON output.

### 2. RESTCONF Script (Topics 6.1, 6.2, 6.5)
Configures interface descriptions (routers: GigabitEthernet1) and VLAN interfaces (switches: Vlan20, 192.168.20.0/24) using RESTCONF.

**`restconf_config.py`**:
```python
# Import libraries for HTTP requests, JSON, logging, and authentication
import requests
import json
import logging
from requests.auth import HTTPBasicAuth

# Disable SSL warnings for self-signed certificates
requests.packages.urllib3.disable_warnings()

# Configure logging to track RESTCONF operations
logging.basicConfig(filename='restconf_config.log', level=logging.INFO)
logger = logging.getLogger("restconf")

# Define devices with their IP, hostname, and type
devices = [
    {"host": "192.168.56.101", "hostname": "R1", "type": "router"},
    {"host": "192.168.56.102", "hostname": "R2", "type": "router"},
    {"host": "192.168.56.201", "hostname": "SW1", "type": "switch"},
    {"host": "192.168.56.202", "hostname": "SW2", "type": "switch"}
]

# Define RESTCONF JSON payload for routers (GigabitEthernet1 description)
router_payload = {
    "ietf-interfaces:interface": {
        "name": "GigabitEthernet1",
        "description": "RESTCONF Configured Interface",
        "type": "iana-if-type:ethernetCsmacd",
        "enabled": True
    }
}

# Define RESTCONF JSON payload for switches (Vlan20 with IP)
switch_payload = {
    "ietf-interfaces:interface": {
        "name": "Vlan20",
        "type": "iana-if-type:l2vlan",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [{"ip": "192.168.20.201", "netmask": "255.255.255.0"}]
        }
    }
}

# Prompt for credentials
username = input("Enter username: ")
password = input("Enter password: ")

# Initialize dictionary to store results
results = {}

# Iterate through devices to apply configurations
for device in devices:
    host = device["host"]
    try:
        print(f"\nConnecting to {host} ({device['hostname']})...")
        logger.info(f"Attempting RESTCONF connection to {host}")
        
        # Define RESTCONF base URL for interface configuration
        base_url = f"https://{host}:443/restconf/data/ietf-interfaces:interfaces/interface"
        headers = {"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}
        
        # Select payload and adjust for switches (set unique VLAN IP)
        payload = router_payload if device["type"] == "router" else switch_payload
        if device["type"] == "switch":
            payload["ietf-interfaces:interface"]["name"] = "Vlan20"
            payload["ietf-ip:ipv4"]["address"][0]["ip"] = "192.168.20.201" if host == "192.168.56.201" else "192.168.20.202"
        
        # Send PUT request to apply configuration (ENCOR 6.5: REST API)
        response = requests.put(
            f"{base_url}={payload['ietf-interfaces:interface']['name']}",
            json=payload,
            auth=HTTPBasicAuth(username, password),
            headers=headers,
            verify=False
        )
        # Store response status and text
        results[host] = {"status_code": response.status_code, "response": response.text}
        print(f"Status Code for {host}: {response.status_code}")
        if response.status_code == 204:
            print("Configuration successful (No Content)")
        elif response.status_code >= 400:
            print(f"Error: {response.text}")
        
        # Retrieve applied configuration via GET request
        get_response = requests.get(
            f"{base_url}={payload['ietf-interfaces:interface']['name']}",
            auth=HTTPBasicAuth(username, password),
            headers=headers,
            verify=False
        )
        results[host]["config"] = get_response.json()
        print(f"Configuration retrieved for {host}:\n{json.dumps(results[host]['config'], indent=4)}\n{'-'*50}")
        
    except Exception as e:
        # Log and display errors
        logger.error(f"Error on {host}: {str(e)}")
        print(f"Error on {host}: {str(e)}")

# Save results to JSON file (ENCOR 6.2: JSON handling)
with open('restconf_results.json', 'w') as f:
    json.dump(results, f, indent=4)
print("Results saved to restconf_results.json")
```

**Exam Alignment**:
- **6.1**: Python HTTP requests, JSON handling.
- **6.2**: JSON payloads.
- **6.5**: REST API response codes (204, 400).

### 3. Chef Configuration (Topic 6.7)
Configures router hostnames using Chef (agent-based).

1. **Setup Chef**:
   ```bash
   chef generate repo network-automation
   cd network-automation
   chef generate cookbook cookbooks/cisco_config
   ```

2. **Chef Recipe** (`cisco_config/recipes/default.rb`):
   ```ruby
   # Require net/ssh for SSH connections to devices
   require 'net/ssh'

   # Define devices and their target hostnames
   node.default['cisco_config']['devices'] = [
     { 'host' => '192.168.56.101', 'hostname' => 'R1-Auto' },
     { 'host' => '192.168.56.102', 'hostname' => 'R2-Auto' }
   ]

   # Iterate through devices to apply hostname configurations
   node['cisco_config']['devices'].each do |device|
     # Execute SSH command to configure hostname (ENCOR 6.7: Chef orchestration)
     execute "configure_hostname_#{device['host']}" do
       command <<~CMD
         ssh -o StrictHostKeyChecking=no cisco@#{device['host']} << 'EOF'
         enable
         cisco
         configure terminal
         hostname #{device['hostname']}
         end
         write memory
         EOF
       CMD
       action :run
       sensitive true # Hide sensitive output (e.g., passwords)
     end
   end
   ```

3. **Run Chef**:
   ```bash
   chef-client --local-mode --runlist 'recipe[cisco_config]'
   ```

**Exam Alignment**:
- **6.7**: Chef as an agent-based tool.

### 4. Puppet Configuration (Topic 6.7)
Configures VLAN 30 on switches using Puppet (agent-based).

1. **Setup Puppet**:
   ```bash
   mkdir -p /etc/puppetlabs/code/environments/production/modules/cisco_vlan
   ```

2. **Puppet Manifest**_BYTES: 16384
