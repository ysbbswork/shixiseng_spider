import urllib.request
from bs4 import BeautifulSoup
def get_url(shorturl):
    urllist=[]
    for index in range(500):
        url=shorturl[:-1]+str(index+1)
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

    url = "https://www.shixiseng.com/interns/st-None_c-440300_?k=IT%E4%BA%92%E8%81%94%E7%BD%91&p=1"
    urllist=get_url(url)
    print(urllist)
