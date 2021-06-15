# -*- coding: utf-8 -*-
import time
import os.path
import asyncio
import logging
import argparse
import websockets
from collections import deque
from urllib.parse import urlparse, parse_qs
import os

NUM_LINES = 1000
HEARTBEAT_INTERVAL = 15 # seconds
serverInfo= {'host':'0.0.0.0', 'port':8765, 'prefix':'/app/log/'}

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

@asyncio.coroutine
def view_log(websocket, path):
    logging.info('Connected, remote={}, path={}'.format(websocket.remote_address, path))

    try:
        try:
            parse_result = urlparse(path)
        except Exception:
            raise ValueError('URL不正确')

        file_path= serverInfo.get('prefix')

        file_list={}
        for count,file_name in enumerate(os.listdir(file_path)):
            file_ab_name= os.path.join(file_path,file_name)
            if not os.path.isfile(file_ab_name):
                raise ValueError('NOT FILE')
            else:
                file_list[file_ab_name]=0
        tail=True

        for fController in file_list.keys():
            f = open(fController)
            content = ''.join(deque(f, NUM_LINES))
            file_list[fController]=f.tell()
            f.close()
            if content:
                yield from websocket.send(content)
        if tail:
            last_heartbeat = time.time()
            while True:
                for fController in file_list.keys():
                    f=open(fController)
                    f.seek(file_list.get(fController))
                    content = f.read()
                    file_list[fController]=f.tell()
                    f.close()
                    if content:
                        yield from websocket.send(content)
                yield from asyncio.sleep(1)
                if time.time() - last_heartbeat > HEARTBEAT_INTERVAL:
                    try:
                        yield from websocket.send("ping")
                        pong = yield from asyncio.wait_for(websocket.recv(), 5)
                        if (pong != "pong"):
                            raise Exception()
                    except Exception as e:
                        raise Exception('Ping error')
                    else:
                        last_heartbeat = time.time()

        else:
            yield from websocket.close()

    except ValueError as e:
        try:
            yield from websocket.send('<font color="red"><strong>{}</strong></font>'.format(e))
            yield from websocket.close()
        except Exception:
            pass

        log_close(websocket, path, e)

    except Exception as e:
        log_close(websocket, path, e)

    else:
        log_close(websocket, path)

def log_close(websocket, path, exception=None):
    message = 'Closed, remote={}, path={}'.format(websocket.remote_address, path)
    if exception is not None:
        message += ', exception={}'.format(exception)
    logging.info(message)

def main():
    start_server = websockets.serve(view_log, serverInfo.get('host'), serverInfo.get('port'))
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
main()
