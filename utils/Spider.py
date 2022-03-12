import re
import lxml
import requests
from AS_Collect.models import Lin_Fanfiction_And_Section_Data, Lin_Video_Data, DouBan_Article
from bs4 import BeautifulSoup
from lxml import etree


#爬B站专栏
def Get_Lin_fanfiction_and_Section():
    results = []
    model_url = 'https://api.bilibili.com/x/web-interface/search/type?context=&search_type=article' \
                '&page={}&keyword=%E4%B9%83%E7%90%B3'
    cv_url = 'https://www.bilibili.com/read/cv'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56',
    }
    for i in range(1, 51):
        url = model_url.format(str(i))
        print(url)
        res = requests.get(url, headers=header)
        print(res)
        # data_list = res.json()
        res.content.decode('UTF-8')
        x = res.json()
        for article in x['data']['result']:
            if article['title'].find('中之人') != -1 or article['view'] < 10 \
                    or article['like'] < 5 or article['title'].find('报') != -1:
                continue
            tmp = {
                'title': article['title'].replace('<em class="keyword">', '').replace('</em>', ''),
                'like': article['like'],
                'view': article['view'],
                'reply': article['reply'],
                'score': str(round((int(article['like']) / int(article['view'])), 3)),
                'cv': cv_url + str(article['id'])
            }
            results.append(tmp)
    results.sort(reverse=True, key=lambda X: X['score'])
    return results

#爬B站视频
def Get_Lin_Video_Data():
    results = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
    }

    url = 'https://search.bilibili.com/all?keyword=%23%E4%B9%83%E7%90%B3%23&page='

    for i in range(50):
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' + str(i))
        r = requests.get('https://search.bilibili.com/video?keyword=%E4%B9%83%E7%90%B3&page=' + str(i + 1),
                         headers=headers)
        print(r)
        soup = BeautifulSoup(r.text, "lxml")
        print(r.url)
        t = etree.HTML(r.text)
        info_list = t.xpath('//*[@id="video-list"]/ul/li/div/div[1]/a/@href')
        title_list = t.xpath('//*[@id="video-list"]/ul/li/div/div[1]/a/@title')
        info_list = [('https:' + i).replace('from=search', '') for i in info_list]
        print(title_list)
        print(info_list)
        for index, url in enumerate(info_list):
            print('----------------------------')
            print(url)
            r = requests.get(url, headers=headers)
            print(r)
            soup = BeautifulSoup(r.text, "lxml")
            t = etree.HTML(r.text)
            print(index)
            try:
                tmp = {
                    'title': title_list[index],
                    'view': int(re.sub('[\u4e00-\u9fa5]', '',
                                       t.xpath('//*[@id="viewbox_report"]/div/span[1]/@title')[0])),
                    'like': int(re.sub('[\u4e00-\u9fa5]', '',
                                       t.xpath('//*[@id="arc_toolbar_report"]/div[1]/span[1]/@title')[0])),
                    'url': url,
                }

                flag = 0 if t.xpath('//*[@id="arc_toolbar_report"]/div[1]/span[2]/text()')[0].find('万') == -1 \
                    else 1
                tmp_s = re.sub('[\u4e00-\u9fa5]', '',
                               t.xpath('//*[@id="arc_toolbar_report"]/div[1]/span[2]/text()')[0])
                tmp['coin'] = int(float(tmp_s) * 10000) if flag == 1 else int(tmp_s)

                flag = 0 if t.xpath('//*[@id="arc_toolbar_report"]/div[1]/span[3]/text()')[0].find('万') == -1 \
                    else 1
                tmp_s = re.sub('[\u4e00-\u9fa5]', '',
                               t.xpath('//*[@id="arc_toolbar_report"]/div[1]/span[3]/text()')[0])
                tmp['collect'] = int(float(tmp_s) * 10000) if flag == 1 else int(tmp_s)
                tmp['score'] = (tmp['like'] + tmp['coin'] * 2 + tmp['collect'] * 3) / tmp['view']

                ##########
                print('video id:', end='')
                print(len(results) + 1)
                print('title:' + str(tmp['title']))
                print('view:' + str(tmp['view']))
                print('like:' + str(tmp['like']))
                print('coin:' + str(tmp['coin']))
                print('collect:' + str(tmp['collect']))
                print('score:' + str(tmp['score']))
                print('url:' + str(tmp['url']))
                ############

                results.append(tmp)
            except Exception as e:
                print(repr(e))
                print('NetWork Error...')
    results.sort(reverse=True, key=lambda X: X['score'])
    return results

#爬取豆瓣文章
def Get_Douban_Article():
    url_model = 'https://www.douban.com/group/a-soul/discussion?start={}&type=elite'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                      '(KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
    }

    with open(r'static/info/douban.txt', 'r') as f:
        cookie = ''.join(f.readlines())

    print(cookie)
    cookies = {'cookie': cookie}

    cnt = 1

    #爬取的页码68-99:因为豆瓣的强大反爬，一般一个batch只能处理8页左右
    for i in range(68, 99):
        url = url_model.format(i * 25)
        print(url)
        r = requests.get(url, headers=headers)
        print(r, r.url)
        if r.status_code == 403:
            continue
        t = lxml.etree.HTML(r.text)
        url_table = t.xpath('//*[@id="content"]/div/div[1]/div[2]/table')[0]
        tmp = url_table.xpath('//td/a/@href')
        reply_table = url_table.xpath('//td[3]/text()')
        reply_table.pop(0)
        url_list = []
        for index, obj in enumerate(tmp):
            if obj.find('people') == -1:
                url_list.append(obj + '?_dtcc=1')
        for index, per_url in enumerate(url_list):
            print('------------')
            print(f'page:{i},{index}th')
            print(per_url)
            r = requests.get(per_url, cookies=cookies, headers=headers)
            print(r, r.url)
            if r.status_code == 403:
                continue
            try:
                t = lxml.etree.HTML(r.text)
                DouBan_Article.objects.create(
                    title=''.join(t.xpath('//*[@id="content"]/div/div[1]/h1/text()')).strip(),
                    author=t.xpath('//*[@id="topic-content"]/div[2]/h3/span[1]/a/text()')[0],
                    reply=int(t.xpath('//*[@id="sep"]/div[1]/a/span[2]/text()')[0]),
                    like=int(t.xpath('//*[@id="sep"]/div[1]/a/span[2]/text()')[0]),
                    collect=int(t.xpath('//*[@id="sep"]/div[2]/a/span[2]/text()')[0]),
                    score=0,
                    url=per_url
                )
                print(f'Id={cnt}')
                cnt += 1
            except Exception as e:
                print(repr(e))
            print('------------')

#更新专栏
def Update_Lin_fanfiction_and_Section():
    new_data = Get_Lin_fanfiction_and_Section()
    Lin_Fanfiction_And_Section_Data.objects.all().delete()
    for i in new_data:
        Lin_Fanfiction_And_Section_Data.objects.create(
            title=i['title'], view=int(i['view']), like=int(i['like']),
            reply=int(i['reply']), score=i['score'], url=i['cv']
        )

#更新视频
def Update_Lin_Video_Data():
    new_data = Get_Lin_Video_Data()
    Lin_Video_Data.objects.all().delete()
    for i in new_data:
        try:
            Lin_Video_Data.objects.create(
                title=i['title'].strip(), view=int(i['view']), like=int(i['like']),
                coin=int(i['coin']), collect=i['collect'],
                score=i['score'], url=i['url']
            )
        except Exception as e:
            print(repr(e))
            print('Error in store data:')
            print(i)



























