# import multiprocessing
import sys
import subprocess
# import os

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


app = FastAPI()


@app.get('/', response_class=PlainTextResponse)
def get_UsedIPv6():
    global adapter, usedIP_str
    # usedIP_str = '::1'
    # usedIP_str = '2408:8956:7a80:30de:94a7:e179:b309:fee7'
    # usedIP_str = '2408:8956:7a40:1e2a:94a7:e179:b309:fee7'
    usedIP_str = ""
    return usedIP_str


if __name__ == '__main__':
    is_parent = True
    if sys.argv.__len__() >= 2:
        if sys.argv[-1] == '-child':
            is_parent = False
    if not is_parent:
        import uvicorn
        uvicorn.run(app, host='', port=8001)
    else:
        child_argv = sys.argv.copy() + ['-child']
        if sys.argv[0][-3:] == '.py':
            child_argv = ['python.exe'] + child_argv
        print(child_argv)
        # p = multiprocessing.Process(name=sys.argv[0], args=tuple(child_argv))
        # sp = subprocess.Popen(child_argv)
        sp = subprocess.Popen(child_argv, stdout=subprocess.PIPE)
        # pm_list = []
        while True:
            if sp.poll() is not None:
                sp = subprocess.Popen(child_argv, stdout=subprocess.PIPE)
                # pm_list = multiprocessing.active_children()
            print(sp.stdout)
            s = input()
            if s == 'exit' or s == "quit":
                if sp.poll() is not None:
                    sp.kill()
                sys.exit(0)
            else:
                usedIP_str = s
