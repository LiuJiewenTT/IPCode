from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.get('/', response_class=PlainTextResponse)
def get_UsedIPv6():
    global adapter
    # usedIP_str = '::1'
    # usedIP_str = '2408:8956:7a80:30de:94a7:e179:b309:fee7'
    # usedIP_str = '2408:8956:7a40:1e2a:94a7:e179:b309:fee7'
    usedIP_str = ""
    return usedIP_str


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='', port=8001)