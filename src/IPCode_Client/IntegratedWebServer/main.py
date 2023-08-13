from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse, HTMLResponse, RedirectResponse

app = FastAPI()


@app.get('/get_UsedIPv6', response_class=PlainTextResponse)
def get_UsedIPv6():
    return '::1'


@app.get('/static/', response_class=HTMLResponse)
def entrance_index():
    with open('res/main_page.html', mode='r') as f:
        s = f.read()
    s = s.format(blank_ipv6_address='::1')
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
    uvicorn.run(app, host='127.0.0.1', port=8000)
    pass


if __name__ == "__main__":
    test_main()
