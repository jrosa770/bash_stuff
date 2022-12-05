import napalm
from tabulate import tabulate
from jinja2 import Environment, FileSystemLoader
import yaml
import inspect
import json

def main():
    #Call for Mainline Cisco CLI Drivers
    driver_ios = napalm.get_network_driver("ios")
    driver_iosxr = napalm.get_network_driver("iosxr")
    driver_nxos = napalm.get_network_driver("nxos")
    device_list = [["csr1", "ios", "router"],["csr2", "ios", "router"],["csr3", "ios", "router"]]
    network_devices = []
    for device in device_list:
        if device[1] == "ios":
            network_devices.append(
                            driver_ios(
                            hostname = device[0],
                            username = "ntc",
                            password = "ntc123"
                            )
            )
        elif device[1] == "iosxr":
            network_devices.append(
                            driver_iosxr(
                            hostname = device[0],
                            username = "ntc",
                            password = "ntc123"
                            )
            )
    devices_table = [["hostname", "vendor", "model"]]
    for device in network_devices:
        print("Connecting to {} ...".format(device.hostname))
        device.open()
        print("Getting device facts")
        device_facts = device.get_facts()
        devices_table.append([device_facts["hostname"],
                            device_facts["vendor"],
                            device_facts["model"]
                            ]
        )
        #Configure and Check
        ##Tabulation Credit Cisco DevNet Learning Labs
        device.load_merge_candidate(filename=None, config=get_template_config(device_facts["hostname"]))
        print ("Pre Commit Check")
        print("\nDiff:")
        print(device.compare_config())
        device.commit_config()
        device.close()
        print("Done.")
    # BGP Peering Verification
    for device in network_devices:
        print("Connecting to {} ...".format(device.hostname))
        device.open()
        print("Getting Peering Information")
        bgp_neighbors = device.get_bgp_neighbors()
        print (json.dumps(bgp_neighbors,indent=4))
        device.close()
        print("Done.")
    print(tabulate(devices_table, headers="firstrow"))
def get_template_config(hostname):
    config_data = yaml.load(open('{}_vars.yml'.format(hostname)), Loader=yaml.FullLoader)
    env = Environment(loader = FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('CSR1000V_build.j2')
    print(template.render(config_data))
    return(template.render(config_data))
if __name__ == '__main__':
    main()