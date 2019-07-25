
'''
获取自己所有学期成绩 导出csv文件
导出的csv文件将放在export/下(没有会新建)
'''
import requests
from chd_portal_login.login import *
from bs4 import BeautifulSoup as BS
import csv
import os
import re

def format_str(string: str):  # 格式化成绩 注意replace并非改变了原串
    return string.replace(' ', '').replace('\t','').replace('\r\n','').replace('\n', '')


if __name__ == '__main__':
    login_url = 'http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F'
    home_page_url = 'http://portal.chd.edu.cn/index.portal?.pn=p167'
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
    }
    cookies = login(login_url, headers, home_page_url)  #此函数最终返回一个cookies
    #print(type(cookies))
    #print(cookies['JSESSIONID'])
    #print(cookies)
    session = requests.session()  # 此方法可以保存服务器发来的cookies
    url = 'http://bkjw.chd.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR'
    session.headers = headers
    session.cookies = cookies  # 手动加载返回的cookies
    res = session.get(url)

    soup = BS(res.text, 'html.parser') # 在 Android 上未能安装lxml，就换用html.parser了
    text1 = soup.findAll(class_=re.compile('griddata'))
    if not os.path.exists('./export'):
        os.makedirs('./export')
    f = open('./export/test.csv','w',newline='')
    file = csv.writer(f)
    st0 = ['学年度', '学期', '门数', '总学分', '平均绩点']
    for i in text1:
        if len(i.contents) == 3:
            print(i.get_text())
            continue
        elif len(i.contents) == 9:
            st = text1[4].get_text().split('\n')[1:5]
            print(st[0] + ":")
            print(st0[2] + ": " + st[1])
            print(st0[3] + ": " + st[2])
            print(st0[4] + ": " + st[3])
            continue
        st = i.get_text().split('\n')[1:6]
        for j in range(5):
            print(st0[j] + ": " + st[j])
        print(' ')

    sc0 = [
        '学年学期', '课程代码', '课程序号', '课程名称', '课程情况', '课程类别', '学分', '期中成绩', '期末成绩',
        '平时成绩', '总评成绩', '实验成绩', '最终', '绩点'
    ]
    
    file.writerow(sc0)
    sc = soup.findAll('td', text=re.compile(r'[\w|\d]{2}\d{5}[\w|\d]\.\d\d'))  # 匹配课程号

    for i in sc:
        result = []
        sc1 = i.parent.get_text('%').split('%')[1:]
        for j in range(3):
            del sc1[j + 1]
        sc1[3] = format_str(sc1[3])
        if sc1[4] != '\n':
            del sc1[5]
            sc1[4] = sc1[4][1:-1]
        else:
            sc1[4] = '正常'
        del sc1[6]
        del sc1[7]
        for j in range(7):
            result.append(sc1[j])
        del sc1
        scr = i.parent.findAll('td', style=True) # 搜索含有style属性的td元素
        for j in range(6):
            if scr[j].text == '':
                result.append('N/A')
            else:
                result.append(format_str(scr[j].text))
        result.append(format_str(i.parent.findAll('td')[-1].text))
        '''
        for j in range(14):
            print(sc0[j] + ': ' + result[j])
        print(' ')'''
        file.writerow(result)
    #print(res.text)
    f.close()
    print('每科成绩保存在 export/test.csv 中')
    print('正在打开export文件夹...')
    os.system('start export')
    input('任意键退出')