#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-16 16:44:38
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import random
import json
import asyncio
import aiohttp
from pyquery import PyQuery as pq

category_dict = {
    '11': 'https://www.meipian.cn/photo',
    '12': 'https://www.meipian.cn/tour',
    '13': 'https://www.meipian.cn/beauty',
    '14': 'https://www.meipian.cn/life',
    '15': 'https://www.meipian.cn/fiction',
    '16': 'https://www.meipian.cn/baby',
    '17': 'https://www.meipian.cn/hobby',
    '18': 'https://www.meipian.cn/food'
}


async def start_category(category_id):
    '''各个分类的起点'''
    async with aiohttp.ClientSession() as session:
        res = await session.get(category_dict[category_id])
        text = await res.text(encoding='utf8')
        max_id = await get_max_category_id(text)
        while True:
            n = await post(category_id, max_id, session)
            max_id = n if n else (max_id - 20)
            print('等待一会')
            await asyncio.sleep(random.randint(1, 5))


async def get_max_category_id(html):
    '''访问分类首页, 取得max_id'''
    doc = pq(html)
    max_id = max([int(i.values()[1]) for i in doc('.item.server-item')])
    return max_id


async def post(category_id, max_id, session):
    '''不断循环 max_id, 抓取 ajax 数据'''
    url = 'https://www.meipian.cn/default/article.php'
    data = {"category_id": "11", "max_id": "100",
            "controller": "category", "action": "list"}
    data['max_id'] = str(max_id)
    data['category_id'] = str(category_id)
    res = await session.post(url, data=json.dumps(data))
    rst = await res.text(encoding='utf8')
    rst = json.loads(rst)
    max_id = None
    if rst['articles']:
        max_id = max([i['id'] for i in rst['articles']])
        for i in rst['articles']:
            await fetch_url(session, i.get('article_id'), i.get('category_name'))
    return max_id


async def fetch_url(session, article_id, category_name):
    '''通过文章 id 拼接对应的 url, 抓取文章对应的页面'''
    url = 'https://www.meipian.cn/{0}'.format(article_id)
    res = await session.get(url)
    html = await res.text(encoding='utf8')
    print('文章链接', url)
    await parse(html, category_name)


async def parse(html, category_name):
    '''解析文章页面, 提取相关数据'''
    doc = pq(html)
    title = doc('.meipian-title').text()
    content = "\n".join([i.text for i in doc('.text').children() if i.text])
    print('分类', category_name)
    print('标题', title)
    print('内容', content)


async def save_to_file():
    '''存储'''
    pass


def main():
    loop = asyncio.get_event_loop()
    tasks = [start_category(i) for i in category_dict.keys()]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

if __name__ == '__main__':
    main()
