#!/usr/bin/env python3

from collections import namedtuple
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from queue import Queue, Full
import re
import subprocess
from threading import Thread

import config


SCRIPT_RE = re.compile(r'^[A-Za-z0-9_-]+$', re.ASCII)

QUEUE = Queue(maxsize=config.max_queue_size)


class Task(namedtuple('Task', 'name path')):
    @classmethod
    def find(cls, name):
        if not SCRIPT_RE.match(name):
            raise ValueError('Invalid script')
        path = os.path.join(config.script_root, name)
        if not os.path.exists(path):
            raise ValueError('Script does not exist')
        return cls(name, path)

    def run(self):
        # TODO: add logging
        subprocess.check_call(self.path, cwd='/', stdin=subprocess.DEVNULL)

    def __str__(self):
        return self.name


def worker():
    print('Started worker thread')
    while True:
        task = QUEUE.get()
        print('Working on', task)
        task.run()
        print('Finished', task)
        QUEUE.task_done()


class Liana(BaseHTTPRequestHandler):
    server_version = 'Liana/0'

    def do_GET(self):
        self.send_simple(200, self.version_string())

    def do_POST(self):
        # Grab the script path
        name = self.path.strip('/')
        try:
            task = Task.find(name)
        except ValueError as e:
            self.send_simple(404, str(e))
            return

        # Extract JSON data
        length = int(self.headers['Content-Length'])
        if length > config.max_request_size:
            self.send_simple(413, 'Too much data!')
            return
        else:
            data = self.rfile.read(length)

        # Enqueue
        try:
            QUEUE.put_nowait(task)
        except Full:
            self.send_simple(503, 'Server is overloaded right now')
        else:
            print('Queued {}'.format(task))
            self.send_simple(200, 'Task "{}" queued'.format(name))

    def send_simple(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))



def main():
    thread = Thread(target=worker, daemon=True)
    thread.start()
    server = HTTPServer((config.host, config.port), Liana)
    print('Started server on {}:{}'.format(config.host, config.port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print('Waiting for tasks to finish')
    QUEUE.join()
    print('Au revoir')


if __name__ == '__main__':
    main()
