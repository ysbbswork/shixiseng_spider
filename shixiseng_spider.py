import requests
import hashlib
import urllib.request
from fontTools.ttLib import TTFont     # 导包
import re
import os
from bs4 import BeautifulSoup

def to_md5(onestr):
    md5=hashlib.md5(onestr.encode("utf8")).hexdigest()
    return md5

def download(url, md5):
    new_file = urllib.request.urlopen(url)
    with open(md5, 'wb') as f:
        f.write(new_file.read())


#已有font文件后解析font文件函数
#每个网站的font文件不相同，需要分析文件后改写
def analysis_font(font_url,filename):

    font = TTFont(font_url)    # 打开文件
    font.saveXML('./{}.xml'.format(filename))     # 转换成 xml 文件并保存
    font_map = font.getBestCmap()    #查看font文件里面的单元，并提取关键值
    map = {v:k for k,v in font_map.items()}
    # print(font_map)
    # print(map)
    temp_list=font.getGlyphOrder()[2:12]
    # print(temp_list)
    numberlist=[]
    for temp in temp_list:
        numberlist.append(hex(int(map[temp])))
    return numberlist


#转换函数，将字符串中的编码按解析出来的数字一一对应的替换
def translate(onestr,filename):
    fontfile = filename

    # fontfile = r'C:\Users\dell\Downloads\sss'
    numberlist = analysis_font(fontfile, filename)

    def _fontmatch(matched):#匹配函数
        tempstr = matched.group()
        shortstr=tempstr[2:]
        newstr = 9999
        for i in range(10):
            if shortstr == numberlist[i][1:]:
                newstr=str(i)
        return newstr

    replacedStr = re.sub("&#x....", _fontmatch, onestr)#这里用了re.sub加入匹配函数
    return replacedStr


def get_font_name(font_url):

    font_md5=to_md5(font_url)
    file_list = os.listdir()
    if font_md5 not in file_list:
        print('不在字体库中, 下载:', font_md5)
        download(font_url,font_md5)
    return font_md5


#用正则解析网页
def get_data(url):
    data = requests.get(url)
    pattern = re.compile(r'<div class="job_msg">.+</div>')
    result = re.search(pattern, data.text)
    job_money = re.findall(r'<span class="job_money cutom_font">(.+?)</span>', result.group())
    job_week = re.findall(r'<span class="job_week cutom_font">(.+?)</span>', result.group())
    job_time = re.findall(r'<span class="job_time cutom_font">(.+?)</span>', result.group())
    title_pattern = re.compile(r'<div class="new_job_name" title="(.+?)">.+</div>')
    titles = re.findall(title_pattern, data.text)
    font_url_pattern = re.compile('@font-face \{font-family:myFont; src: url\("(.+)"\)\}')
    font_url=re.findall(font_url_pattern,data.text)
    font_md5=get_font_name(font_url[0])

    title=titles[0]
    money=translate(job_money[0],font_md5)
    time=translate(job_time[0],font_md5)
    week=translate(job_week[0],font_md5)
    return title,money,time,week

def get_detail(url):
    html=urllib.request.urlopen(url)
    soup=BeautifulSoup(html.read(),'lxml')
    detail=soup.select('body > div.wrap > div.job-box > div.job-content > div.content_left > div.con-job.job_introduce > div.job_part > div > p')
    text=[]
    for d in detail:
        text.append(d.text)
    title, money, time, week = get_data(url)
    return title, money, time, week,text

def get_url(givenurl):
    urllist=[]
    for index in range(500):
        url=givenurl[:-1]+str(index+1)
        html=urllib.request.urlopen(url)
        soup=BeautifulSoup(html.read(),'lxml')
        singleurl=soup.select('a.name')
        if singleurl ==[]:
            break
        else:
            for i in singleurl:
                urllist.append('https://www.shixiseng.com'+i.get('href'))
    return urllist


if __name__ == '__main__':
    #指定搜索类目
    givenurl="https://www.shixiseng.com/interns/st-None_c-440300_?k=IT%E4%BA%92%E8%81%94%E7%BD%91&p=1"

    urllist=get_url(givenurl)#先获取所有要爬的链接


    for url in urllist:#再一个个去爬取内容
        title, money, time, week,text=get_detail(url)
        print(title,money,time,week)
        for t in text:
            print(t)

