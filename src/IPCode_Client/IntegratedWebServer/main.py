from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse, HTMLResponse, RedirectResponse

from IPCode_Client.utils.network_toolkit1 import AdapterAndIP_Used

app = FastAPI()


@app.get('/get_UsedIPv6', response_class=PlainTextResponse)
def get_UsedIPv6():
    usedIP_str = '::1'
    adapter = AdapterAndIP_Used()
    usedIP = adapter.getUsedIP_v6()
    usedIP_str = usedIP.ip[0]
    return usedIP_str


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
    import uvicorn
    # uvicorn.run(app, host='127.0.0.1', port=8000)
    # uvicorn.run(app, host='0.0.0.0', port=8000)
    # uvicorn.run(app, host='localhost', port=8000)
    uvicorn.run(app, host='', port=8000)
    pass


if __name__ == "__main__":
    test_main()
