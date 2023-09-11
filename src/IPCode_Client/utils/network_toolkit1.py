import ifaddr
import subprocess
import ipaddress
from IPCode_Client.utils.cache_toolkit1 import timelimtited_cache
from IPCode_Client.utils import cache_toolkit2
from IPCode_Client.utils.cache_toolkit1 import cls_getvalidvalue_autorefresh
from typing import Dict, Union, List, Callable, Any
from ast import literal_eval
import time


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
        # ip_list = [x['ip'] for x in ips2]
        # ip_list_str = [x.compressed for x in ip_list]
        # print(ip_list_str)
        # ip_exploded_list_str = [x.exploded for x in ip_list]
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

    class CacheUnit(timelimtited_cache):
        auto_refresh: bool = True
        refresh_context: [4, 6, None] = None

        _usedNetworkAdapter: ifaddr.Adapter
        _usedIP: ifaddr.IP
        _usedPrefix: ipaddress.IPv6Address

        # Refresh Callbacks
        _usedNetworkAdapter_refresh_callback: Callable[[], ifaddr.Adapter]
        _usedIP_refresh_callback: Callable[[], ifaddr.IP]
        _usedPrefix_refresh_callback: Callable[[], ipaddress.IPv6Address]

        _usedNetworkAdapter_refresh_callback_v4: Callable[[], ifaddr.Adapter]
        _usedNetworkAdapter_refresh_callback_v6: Callable[[], ifaddr.Adapter]
        _usedIP_refresh_callback_v4: Callable[[], ifaddr.IP]
        _usedIP_refresh_callback_v6: Callable[[], ifaddr.IP]

        def __init__(self):
            self.refresh_context_applywork(None)

        def refresh_context_applywork(self, contextid: [4, 6]):
            self.refresh_context = contextid
            if contextid == 4:
                self._usedIP_refresh_callback = self._usedIP_refresh_callback_v4
                self._usedNetworkAdapter_refresh_callback = self._usedNetworkAdapter_refresh_callback_v4
            elif contextid == 6:
                self._usedIP_refresh_callback = self._usedIP_refresh_callback_v6
                self._usedNetworkAdapter_refresh_callback = self._usedNetworkAdapter_refresh_callback_v6
            else:
                pass  # keep

        @property
        @cls_getvalidvalue_autorefresh(refresh_callback_function_name='_usedNetworkAdapter_refresh_callback')
        def usedNetworkAdapter(self) -> Union[ifaddr.Adapter, None]:
            return self._usedNetworkAdapter

        # @property
        # def usedNetworkAdapter(self) -> Union[ifaddr.Adapter, None]:
        #     if self.valid is True:
        #         return self._usedNetworkAdapter
        #     elif self.auto_refresh is True:
        #         self._usedNetworkAdapter = self._usedNetworkAdapter_refresh_callback.__call__()
        #         return self._usedNetworkAdapter
        #     return None

        @usedNetworkAdapter.setter
        def usedNetworkAdapter(self, data):
            self._usedNetworkAdapter = data

        @property
        @cls_getvalidvalue_autorefresh(refresh_callback_function_name='_usedIP_refresh_callback')
        def usedIP(self) -> Union[ifaddr.IP, None]:
            return self._usedIP

        # @property
        # def usedIP(self):
        #     if self.valid is True:
        #         return self._usedIP
        #     elif self.auto_refresh is True:
        #         self._usedIP = self._usedIP_refresh_callback.__call__()
        #         return self._usedIP
        #     return None

        @usedIP.setter
        def usedIP(self, data):
            # print(f'usedIP.setter self: {self}')
            self._usedIP = data

        @property
        @cls_getvalidvalue_autorefresh(refresh_callback_function_name='_usedPrefix_refresh_callback')
        def usedPrefix(self) -> Union[ipaddress.IPv6Address, None]:
            return self._usedPrefix

        # @property
        # def usedPrefix(self):
        #     if self.valid is True:
        #         return self._usedPrefix
        #     elif self.auto_refresh is True:
        #         self._usedPrefix = self._usedPrefix_refresh_callback.__call__()
        #         return self._usedPrefix
        #     return None

        @usedPrefix.setter
        def usedPrefix(self, data):
            self._usedPrefix = data

    class CacheBlock(cache_toolkit2.CacheBlock):
        cache_units: List[Any]

        def __init__(self):
            self.cache_unit1 = AdapterAndIP_Used.CacheUnit()    # Adapter, IP
            self.cache_unit2 = AdapterAndIP_Used.CacheUnit()    # Prefix
            self.cache_units: List[AdapterAndIP_Used.CacheUnit] = [self.cache_unit1, self.cache_unit2]

        @property
        def validtime(self):
            v1 = self.cache_unit1.validtime
            v2 = self.cache_unit2.validtime
            try:
                v1_d = literal_eval(v1)
                v2_d = literal_eval(v2)
                if v1_d is None or v2_d is None:
                    raise AssertionError()
            except:
                v = v1
                pass
            else:
                v = min(v1_d, v2_d)
            # v = min(v1, v2)
            return v

        @validtime.setter
        def validtime(self, data):
            self.cache_unit1.validtime = data
            self.cache_unit2.validtime = data

        @property
        def usedNetworkAdapter(self):
            return self.cache_unit1.usedNetworkAdapter

        @usedNetworkAdapter.setter
        def usedNetworkAdapter(self, data):
            self.cache_unit1.usedNetworkAdapter = data

        @property
        def usedIP(self):
            return self.cache_unit1.usedIP

        @usedIP.setter
        def usedIP(self, data):
            self.cache_unit1.usedIP = data

        @property
        def usedPrefix(self):
            return self.cache_unit2.usedPrefix

        @usedPrefix.setter
        def usedPrefix(self, data):
            self.cache_unit2.usedPrefix = data

        @property
        def _usedNetworkAdapter_refresh_callback_v4(self):
            return self.cache_unit1._usedNetworkAdapter_refresh_callback_v4

        @_usedNetworkAdapter_refresh_callback_v4.setter
        def _usedNetworkAdapter_refresh_callback_v4(self, data):
            self.cache_unit1._usedNetworkAdapter_refresh_callback_v4 = data

        @property
        def _usedNetworkAdapter_refresh_callback_v6(self):
            return self.cache_unit1._usedNetworkAdapter_refresh_callback_v6

        @_usedNetworkAdapter_refresh_callback_v6.setter
        def _usedNetworkAdapter_refresh_callback_v6(self, data):
            self.cache_unit1._usedNetworkAdapter_refresh_callback_v6 = data

        @property
        def _usedIP_refresh_callback_v4(self):
            return self.cache_unit1._usedIP_refresh_callback_v4

        @_usedIP_refresh_callback_v4.setter
        def _usedIP_refresh_callback_v4(self, data):
            self.cache_unit1._usedIP_refresh_callback_v4 = data

        @property
        def _usedIP_refresh_callback_v6(self):
            return self.cache_unit1._usedIP_refresh_callback_v6

        @_usedIP_refresh_callback_v6.setter
        def _usedIP_refresh_callback_v6(self, data):
            self.cache_unit1._usedIP_refresh_callback_v6 = data

        @property
        def _usedPrefix_refresh_callback(self):
            return self.cache_unit2._usedPrefix_refresh_callback

        @_usedPrefix_refresh_callback.setter
        def _usedPrefix_refresh_callback(self, data):
            self.cache_unit2._usedPrefix_refresh_callback = data

        def refresh_context_applywork(self, contextid: [4, 6]):
            self.cache_unit1.refresh_context_applywork(contextid)
            # self.cache_unit2.refresh_context_applywork(contextid)

    cache_enabled: bool = False
    cache: CacheBlock
    getUsedPrefix: Callable

    # config section
    ifconfig_url: str = 'ifconfig.co'
    ifconfig_options: Union[str, List[str], None] = None

    def __init__(self):
        self.cache = AdapterAndIP_Used.CacheBlock()
        self.cache._usedNetworkAdapter_refresh_callback_v4 = self.getUsedNetworkAdapter_v4
        self.cache._usedNetworkAdapter_refresh_callback_v6 = self.getUsedNetworkAdapter_v6
        self.cache._usedIP_refresh_callback_v4 = self.getUsedIP_v4
        self.cache._usedIP_refresh_callback_v6 = self.getUsedIP_v6
        self.cache._usedPrefix_refresh_callback = self.getUsedPrefixFromAdapterWithIP
        # 默认设置为IPv6
        # self.cache.refresh_context = 6
        self.cache.refresh_context_applywork(6)
        self.getUsedPrefix: Callable = self.getUsedPrefixFromAdapterWithIP

    def getUsedNetworkAdapterRaw(self, opt='') -> Dict[str, Union[None, ifaddr.Adapter, ifaddr.IP]]:
        if self.cache_enabled is True and self.cache.cache_unit1.valid is True:
            return {'adapter': self.cache.usedNetworkAdapter, 'ip': self.cache.usedIP}

        if self.ifconfig_options is str:
            opt += f' {self.ifconfig_options}'
        elif self.ifconfig_options is List[str]:
            for i in self.ifconfig_options:
                opt += f' {i}'

        adapters = ifaddr.get_adapters()
        curl_command_str = f'curl --silent {opt} {self.ifconfig_url}'
        print(f'[Debug]: curl_command_str: {curl_command_str}')
        p = subprocess.Popen(curl_command_str, text=True, stdout=subprocess.PIPE)
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
        self.cache.usedNetworkAdapter = usedNetworkAdapter
        self.cache.usedIP = usedIP
        self.cache.cache_unit1._lasttime = time.time()
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
        if self.cache_enabled is True and self.cache.cache_unit2.valid is True:
            return self.cache.usedPrefix

        # if self.cache.valid is not True:  # 仅当没有使用自动刷新修饰器时使用
        #     self.getUsedIP_v6()
        # if self.cache.usedIP is None:     # 仅当没有使用自动刷新修饰器时使用
        #     self.getUsedIP_v6()
        self.cache.usedPrefix = usedPrefix = self.getPrefixFromAdapterWithIP(self.cache.usedNetworkAdapter, self.cache.usedIP)
        self.cache.cache_unit2._lasttime = time.time()
        return usedPrefix


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
