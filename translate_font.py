from fontTools.ttLib import TTFont     # 导包
import re

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
def translate(onestr):

    file = r'C:\Users\dell\Downloads\sss'
    numberlist = analysis_font(file, 'sss')

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

if __name__ == '__main__':

    str1 = '&#xe528&#xf316&#xf316-&#xe528&#xf450&#xf316／天</span><span title="北京" class="job_position">北京</span><span class="job_academic">不限</span><span class="job_week cutom_font">&#xf450天／周</span><span class="job_time cutom_font">实习&#xf4bf个月</span></div>'

    print(translate(str1))