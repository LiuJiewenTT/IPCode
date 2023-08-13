import ifaddr
import subprocess
import ipaddress
from typing import Dict, Union


class NetworkTools:

    def getPrefixFromIPWithLength_Int(self, ip: ipaddress.IPv6Address, length: int):
        suffix_length = ipaddress.IPV6LENGTH - length
        prefix = (int(ip) >> suffix_length) << suffix_length
        return prefix

    def getPrefixFromIPWithLength(self, ip: ipaddress.IPv6Address, length: int):
        return ipaddress.IPv6Address(self.getPrefixFromIPWithLength_Int(ip, length))

    def getPrefixFromAdapterWithIP(self, adapter: ifaddr.Adapter, ip: ifaddr.IP):
        if not ip.is_IPv6:
            print('[Debug]: Function getPrefixFromAdapterWithIP() only supports IPv6.')
            return None
        usedPrefix = None
        ip2 = ipaddress.IPv6Address(ip.ip[0])
        ips2 = [{'ip': ipaddress.IPv6Address(x.ip[0]), 'network_prefix_length': x.network_prefix}
                for x in adapter.ips if x.is_IPv6]
        for x in ips2:
            # suffix_length = ipaddress.IPV6LENGTH - x['network_prefix_length']
            # x['prefix'] = ipaddress.IPv6Address((int(x['ip']) >> suffix_length) << suffix_length)
            x['prefix'] = self.getPrefixFromIPWithLength(x['ip'], x['network_prefix_length'])
        ip_list = [x['ip'] for x in ips2]
        ip_list_str = [x.compressed for x in ip_list]
        # print(ip_list_str)
        ip_exploded_list_str = [x.exploded for x in ip_list]
        # print(ip_exploded_list_str)
        # for x in ips2:
        #     print(x['prefix'])

        # In[33]: a2._ip - a2_s._ip == a2_p._ip
        # Out[33]: True
        for x in ips2:
            if x['ip'] != ip2:
                temp = int(x['prefix']) & int(ip2)
                # print(ipaddress.IPv6Address(temp))
                if temp == int(x['prefix']):
                    print(f'[Debug]: Recognized Prefix: {x["prefix"]}')
                    usedPrefix = x['prefix']
                    break
        # self.usedPrefix = usedPrefix
        return usedPrefix


class AdapterAndIP_Used(NetworkTools):
    usedNetworkAdapter: ifaddr.Adapter
    usedIP: ifaddr.IP
    usedPrefix: ipaddress.IPv6Address

    def getUsedNetworkAdapterRaw(self, opt='') -> Dict[str, Union[None, ifaddr.Adapter, ifaddr.IP]]:
        adapters = ifaddr.get_adapters()
        p = subprocess.Popen(f'curl --silent {opt} ifconfig.co', text=True, stdout=subprocess.PIPE)
        ip_used = p.stdout.readline()
        ip_used = ip_used.strip(' \r\n')
        print(f'[Debug]: IP: "{ip_used}".')
        usedNetworkAdapter = usedIP = None
        for adapter in adapters:
            for ip in adapter.ips:
                if ip_used in str(ip.ip):
                    usedNetworkAdapter = adapter
                    usedIP = ip
                    break
        self.usedNetworkAdapter = usedNetworkAdapter
        self.usedIP = usedIP
        return {'adapter': usedNetworkAdapter, 'ip': usedIP}

    def getUsedNetworkAdapterRaw_v6(self):
        return self.getUsedNetworkAdapterRaw(opt='-6')

    def getUsedNetworkAdapterRaw_v4(self):
        return self.getUsedNetworkAdapterRaw(opt='-4')

    def getUsedNetworkAdapter_v6(self) -> ifaddr.Adapter:
        return self.getUsedNetworkAdapterRaw_v6()['adapter']

    def getUsedNetworkAdapter_v4(self) -> ifaddr.Adapter:
        return self.getUsedNetworkAdapterRaw_v4()['adapter']

    def getUsedIP_v6(self) -> ifaddr.IP:
        return self.getUsedNetworkAdapterRaw_v6()['ip']

    def getUsedIP_v4(self) -> ifaddr.IP:
        return self.getUsedNetworkAdapterRaw_v4()['ip']

    def getUsedPrefixFromAdapterWithIP(self):
        self.usedPrefix = self.getPrefixFromAdapterWithIP(self.usedNetworkAdapter, self.usedIP)
        return self.usedPrefix


def example_test_main():
    used_AdapterAndIP = AdapterAndIP_Used()
    usedNetworkAdapterRaw = used_AdapterAndIP.getUsedNetworkAdapterRaw_v6()
    usedNetworkAdapter = usedNetworkAdapterRaw['adapter']
    usedIP = usedNetworkAdapterRaw['ip']
    print(usedNetworkAdapter, usedIP, sep='\n')
    # print(used_AdapterAndIP.getUsedNetworkAdapter_v6())
    # print(used_AdapterAndIP.getUsedIP_v6())
    print('-' * 20)
    print(used_AdapterAndIP.getUsedPrefixFromAdapterWithIP())

if __name__ == '__main__':
    example_test_main()
