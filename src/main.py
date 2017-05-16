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

def parse(html):
    doc = pq(html)
    title = doc('.meipian-title').text()
    print(doc('.text').text())
    print()
    for i in doc('.text').children():
        print(i.text)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()

if __name__ == '__main__':
    main()
