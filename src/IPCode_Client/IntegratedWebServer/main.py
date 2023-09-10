from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse, HTMLResponse, RedirectResponse

from IPCode_Client.utils.network_toolkit1 import AdapterAndIP_Used

adapter: AdapterAndIP_Used

app = FastAPI()


@app.get('/get_UsedIPv6', response_class=PlainTextResponse)
def get_UsedIPv6():
    global adapter
    usedIP_str = '::1'
    usedIP = adapter.getUsedIP_v6()
    usedIP_str = usedIP.ip[0]
    return usedIP_str


@app.get('/get_UsedIPv6Prefix', response_class=PlainTextResponse)
def get_UsedIPv6():
    global adapter
    usedIP_str = '::1'
    # usedPrefix = adapter.getUsedPrefixFromAdapterWithIP()
    # usedPrefix = adapter.cache.usedPrefix
    usedPrefix = adapter.getUsedPrefix()
    usedPrefix_str = str(usedPrefix)
    return usedPrefix_str


@app.get('/static/', response_class=HTMLResponse)
def entrance_index():
    with open('res/main_page.html', mode='r', encoding='utf-8') as f:
        s = f.read()
    s = s.format(blank_ipv6_address=get_UsedIPv6())
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

    # uvicorn.run(app, host='127.0.0.1', port=8000)
    # uvicorn.run(app, host='0.0.0.0', port=8000)
    # uvicorn.run(app, host='localhost', port=8000)
    # uvicorn.run(app, host='', port=8000)
    uvicorn.run(app, host=host_str, port=host_port)
    pass


if __name__ == "__main__":
    adapter = AdapterAndIP_Used()
    adapter.cache_enabled = True
    test_main()
