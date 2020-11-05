import requests
from bs4 import BeautifulSoup

#제목 확인을 위한 파서
req = requests.get('http://www.bizinfo.go.kr/see/seea/selectSEEA100.do')
req.encoding = 'utf-8'

html = req.text
soup = BeautifulSoup(html, 'html.parser')
posts = soup.select('td.txtAgL')

post_list = []
post_title_list = []
before_title_list = []
posts_detail = []

for i in posts:
    post_title_list.append(i.text)

with open('latest2.txt', 'w', encoding='utf-8') as f_write:
    # 내용을 깨끗하게 확인하기 위해 공백을 제거
    for i in range(0, 20):
        post = str(post_title_list[i])
        post = post.replace('\n', '')
        post = post.replace('\r', '')
        post = post.replace('\t', '')
        post_list.append(post)

    for i in range(0,20):
        f_write.write(post_list[i])
        f_write.write('\n')