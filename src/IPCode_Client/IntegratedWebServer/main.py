from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse, HTMLResponse, RedirectResponse
from typing import List, Dict, Any

from IPCode_Client.utils.network_toolkit1 import AdapterAndIP_Used

adapter: AdapterAndIP_Used

config_pages: dict

app = FastAPI()


@app.get('/get_UsedIPv6', response_class=PlainTextResponse)
def get_UsedIPv6():
    global adapter
    usedIP_str = '::1'
    usedIP = adapter.getUsedIP_v6()
    usedIP_str = usedIP.ip[0]
    return usedIP_str


@app.get('/get_UsedIPv6Prefix', response_class=PlainTextResponse)
def get_UsedIPv6Prefix():
    global adapter
    usedIP_str = '::1'
    # usedPrefix = adapter.getUsedPrefixFromAdapterWithIP()
    # usedPrefix = adapter.cache.usedPrefix
    usedPrefix = adapter.getUsedPrefix()
    usedPrefix_str = str(usedPrefix)
    return usedPrefix_str


def page_homepage_config_keymap(display_keys: List[str]) -> Dict[str, Any]:
    keymap = {}
    # if 'IPv6' in display_keys:
    #     keymap['blank_ipv6_address'] = get_UsedIPv6()
    if 'IPv6_Prefix' in display_keys:
        keymap['blank_ipv6_prefix'] = get_UsedIPv6Prefix()
    return keymap


@app.get('/static/', response_class=HTMLResponse)
def entrance_index():
    # page: "homepage"
    page_config = config_pages.get('homepage')
    keymap = page_homepage_config_keymap(page_config['display_keys'])
    with open('res/main_page.html', mode='r', encoding='utf-8') as f:
        s_lines = f.readlines()
    s_lines2 = []
    for line in s_lines:
        line2 = line
        try:
            line2 = line2.format_map(keymap)
        except KeyError as ke:
            pass
        else:
            s_lines2.append(line2)
    s = ''
    for line2 in s_lines2:
        s += line2
    return HTMLResponse(content=s)


@app.get('/')
def entrance():
    # return entrance_index()
    return RedirectResponse('/static/')

# @app.get('/', response_class=HTMLResponse)
# def entrance():
#     with open('res/main_page.html', mode='r') as f:
#         s = f.read()
#     s = s.format(blank_ipv6_address='::1')
#     return s


app.mount("/static", StaticFiles(directory="res"), name="res")


def test_main():
    import uvicorn, orjson, os

    adapter.cache_enabled = True

    host_str = ''
    host_port = 8000

    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config_str = f.read()
            print(config_str)
            config = orjson.loads(config_str)
            config: dict

            config_host: dict = config.get('host_info')
            host_str = config_host.get('host_str')
            host_port = int(config_host['host_port'])

            config_ifconfig: dict = config.get('ifconfig')
            ifconfig_url = config_ifconfig.get('url')
            ifconfig_options: list = config_ifconfig.get('options')
            ifconfig_cache_validtime: str = config_ifconfig.get('cache_validtime')
            if ifconfig_url is not None: adapter.ifconfig_url = ifconfig_url
            if ifconfig_options is not None: adapter.ifconfig_options = ifconfig_options
            if ifconfig_cache_validtime is not None: adapter.cache.validtime = ifconfig_cache_validtime

            global config_pages
            config_pages = config.get('pages')


    # uvicorn.run(app, host='127.0.0.1', port=8000)
    # uvicorn.run(app, host='0.0.0.0', port=8000)
    # uvicorn.run(app, host='localhost', port=8000)
    # uvicorn.run(app, host='', port=8000)
    uvicorn.run(app, host=host_str, port=host_port)
    pass


if __name__ == "__main__":
    adapter = AdapterAndIP_Used()
    test_main()
