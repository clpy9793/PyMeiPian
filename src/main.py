#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-16 16:44:38
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import asyncio
import aiohttp
from pyquery import PyQuery as pq

async def run():
    async with aiohttp.ClientSession() as session:
        res = await session.get('https://www.meipian.cn/jkwjtk5')
        print(res.status)
        with open('tmp.html', 'w') as f:
            text = await res.text(encoding='utf8')
            parse(text)
    print(1)

async def fetch_url(session, url):
    res = await session.get(url)
    html = await res.text()
    parse(html)


def parse(html):
    doc = pq(html)
    path = doc('.box').children()[3].text.strip()
    title = doc('.meipian-title').text()
    content = "\n".join([i.text for i in doc('.text').children()])
    print(path)
    print(title)
    print(content)
    pass


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()

if __name__ == '__main__':
    main()
