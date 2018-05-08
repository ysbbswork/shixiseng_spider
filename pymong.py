import pymongo
from shixiseng_spider import get_url
from shixiseng_spider import get_detail

client = pymongo.MongoClient('localhost', 27017)
ceshi = client['shixiseng']
url_list = ceshi['url_list']
job_info = ceshi['job_info']

givenurl = "https://www.shixiseng.com/interns/st-None_c-440300_?k=IT%E4%BA%92%E8%81%94%E7%BD%91&p=1"

urllist = get_url(givenurl)  # 先获取所有要爬的链接
for url in urllist:  # 再一个个去爬取内容
    title, money, time, week, text = get_detail(url)
    job_info.insert_one({'title': title, 'money': money, 'time': time, 'week': week, 'text': text})
    print(title, money, time, week)
    for t in text:
        print(t)

