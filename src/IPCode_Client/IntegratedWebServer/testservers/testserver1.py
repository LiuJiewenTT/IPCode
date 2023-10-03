# 用终端运行更好，不要用PyCharm的终端，因为输入会被输出打断。
# D:\TT\TTBC-D\python\wksp3-jetbrain\IPCode\venv\Scripts\python.exe D:/TT/TTBC-D/python/wksp3-jetbrain/IPCode/src/IPCode_Client/IntegratedWebServer/testservers/testserver1.py

# import multiprocessing
import sys
# import os
# import subprocess
from threading import Thread
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


app = FastAPI()


@app.get('/', response_class=PlainTextResponse)
def get_UsedIPv6():
    global adapter, usedIP_str
    # usedIP_str = '::1'
    # usedIP_str = '2408:8956:7a80:30de:94a7:e179:b309:fee7'
    # usedIP_str = '2408:8956:7a40:1e2a:94a7:e179:b309:fee7'
    # usedIP_str = ""
    return usedIP_str


def uvi_run():
    import uvicorn
    # sys.stdout = output_pipe
    # sys.stderr = output_pipe
    print('in_uvi_run')
    uvicorn.run(app, host='', port=8001)


if __name__ == '__main__':
    usedIP_str = ''
    p = None
    # conn_send, conn_recv = multiprocessing.Pipe()
    print('Current IP: ' + usedIP_str)
    while True:
        if p is None or p.is_alive() is False:
            p = Thread(target=uvi_run, name='uvi_run', daemon=True)
            p.start()
        s = input('>')
        s = s.strip(' ')
        if s == 'exit' or s == 'quit':
            if p.is_alive():
                # p.kill()
                pass
            sys.exit(0)
        usedIP_str = s
        print('Current IP: ' + usedIP_str)
