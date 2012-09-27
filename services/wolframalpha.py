#!/usr/bin/env python2

from kobunsupport import load_config, handshake, read_line, write_line

from pyquery import PyQuery as pq

import gevent
import urllib

handshake("show stuff from wolfram|alpha")

config = load_config()


def worker(server, target, query):
    p = pq(url="http://api.wolframalpha.com/v2/query?" + urllib.urlencode({
        'input': query,
        'appid': config["wolframalpha.appid"],
        'format': 'plaintext'
    }))

    for line in (p("queryresult[success='true'] > pod[primary='true'] > subpod:first-child > plaintext").text() or "(no result)").split("\n"):
        write_line(server, "PRIVMSG", [target, "\x02Wolfram|Alpha:\x02 {}".format(line.encode("utf-8"))])

def core():
    while True:
        server, prefix, command, args = read_line()

        if command.lower() == "privmsg":
            target, msg = args

            parts = msg.split(" ", 1)
            if parts[0].lower() == "!wa":
                query = parts[1:] and parts[1] or ""
                gevent.spawn(worker, server, target, query)

        gevent.sleep(0)

gevent.spawn(core).join()

