import requests
from bs4 import BeautifulSoup
from slacker import Slacker
from private.tokens import slack as slack_token


def post_bot1():
    # 고용노동부
    # 제목 확인을 위한 파서
    req = requests.get('http://www.moel.go.kr/news/notice/noticeList.do')
    req.encoding = 'utf-8'

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    posts = soup.select('a.b_tit')

    post_list = []
    post_title_list = []
    before_title_list = []

    # 슬랙 토큰
    slack = Slacker(slack_token)
    attachments_dict = dict()

    # 내용을 깨끗하게 확인하기 위해 공백을 제거
    for i in range(0,10):
        post = str(posts[i])
        post = post.replace('\n', '')
        post = post.replace('\r', '')
        post = post.replace('\t', '')
        post_list.append(post)

    # 기존의 10개 리스트를 불러옴
    with open('latest.txt', 'r', encoding='utf-8') as f_read:
        befores = f_read.readlines()

    # 기존의 10개와 실행당시의 10개를 비교할 수 있도록 타이틀 분류
    for i in range(0,10):
        post_title = post_list[i][251:-12]
        post_title = post_title.strip('\n')
        post_title = post_title.strip('</a>')
        post_title_list.append(post_title)
        before_title = befores[i][251:-13]
        before_title = before_title.strip('\n')
        before_title = before_title.strip('</a>')
        before_title_list.append(before_title)

    # 중복 게시글 확인 후 중복되지 않는 것은 슬랙으로 알림을 보냅니다.
    for i in range(0,10):
        if before_title_list[0] != post_title_list[i] and before_title_list[1] != post_title_list[i] \
                and before_title_list[2] != post_title_list[i] and before_title_list[3] != post_title_list[i] \
                and before_title_list[4] != post_title_list[i] and before_title_list[5] != post_title_list[i] \
                and before_title_list[6] != post_title_list[i] and before_title_list[7] != post_title_list[i] \
                and before_title_list[8] != post_title_list[i] and before_title_list[9] != post_title_list[i] :

            URL = post_list[i][23:175]
            TITLE = post_list[i][251:-12]

            # slack bot setting
            attachments_dict['pretext'] = "고용노동부 사이트에 새로운 공지사항이 등록되었습니다. :mememe:"
            attachments_dict['title'] = TITLE
            attachments_dict['title_link'] = "http://www.moel.go.kr"+URL

            # slack bot에서 내용도 확인할 수 있도록 한번 더 parser합니다.
            req2 = requests.get("http://www.moel.go.kr"+URL)
            req2.encoding = 'utf-8'

            html2 = req2.text
            soup2 = BeautifulSoup(html2, 'html.parser')
            post_detail = soup2.select('div.b_content')
            post_detail = str(post_detail.pop(0))

            post_detail = post_detail.strip('<div class="b_content">\n')

            # 신규 내용을 new_post.txt에 저장합니다.
            with open('new_post.txt', 'w', encoding='utf-8') as f_write2:
                f_write2.write(post_detail)

            # new_post.txt에 들어있는 내용을 표현하기 예쁘게 가공합니다.(공백제거, 태그제거 등)
            post_detail_inrow =[]
            post_datail_toslack = ''
            with open('new_post.txt', 'r', encoding='utf-8') as f_read2:
                rows = f_read2.readlines()
                for row in rows :
                    row = row.strip()
                    row = row.strip('<br/>')
                    row = row.strip('<div style="text-align: center;">')
                    row = row.strip('<div style="text-align: right;">')
                    row = row.strip('<div>')
                    row = row.strip('</div>')
                    row = row.strip('</')
                    row = row.strip('<strong>')
                    row = row.strip('</strong>')
                    row = row.strip('ong>')
                    row = row.strip('</stro')
                    if row != '':
                        post_detail_inrow.append(row)

            # 해당 내용이 마지막줄이 아니면 개행하고, 마지막줄이면 넘어갑니다.
            count_inrow = len(post_detail_inrow)
            for idx, row in enumerate(post_detail_inrow) :
                post_datail_toslack = post_datail_toslack+str(row)
                if idx < count_inrow-1 :
                    post_datail_toslack = post_datail_toslack+'\n'

            attachments_dict['fallback'] = "for_ government new post_to_ slack bot"
            attachments_dict['text'] = post_datail_toslack
            attachments_dict['mrkdwn_in'] = ["text", "pretext"]
            attachments = [attachments_dict]

            # slack bot으로 알림을 보냅니다.
            slack.chat.post_message(channel='# 98_알림_정부정책', attachments=attachments, as_user=True)
            print(TITLE)

    # 이번에 가져온 새로운 10개의 내용을 저장합니다.
    with open('latest.txt', 'w', encoding='utf-8') as f_write:
        for i in range(0,10):
            f_write.write(post_list[i])
            f_write.write('\n')

    print('new_post_bot Done')


def post_bot2():
    # 기업마당당
    # 제목 확인을 위한 파서
    req = requests.get('http://www.bizinfo.go.kr/see/seea/selectSEEA100.do')
    req.encoding = 'utf-8'

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    posts = soup.select('td.txtAgL')

    post_list = []
    post_title_list = []
    before_list = []

    for i in posts:
        post_title_list.append(i.text)

    # 슬랙 토큰
    slack = Slacker(slack_token)
    attachments_dict = dict()

    # 내용을 깨끗하게 확인하기 위해 공백을 제거
    for i in range(0,20):
        post = str(post_title_list[i])
        post = post.replace('\n', '')
        post = post.replace('\r', '')
        post = post.replace('\t', '')
        post = post.rstrip()
        post_list.append(post)

    # 기존의 20개 리스트를 불러옴
    with open('latest2.txt', 'r', encoding='utf-8') as f_read:
        befores = f_read.readlines()

    for i in range(0,20):
        before = str(befores[i])
        before = before.replace(' \n', '')
        before_list.append(before)

    # 중복 게시글 확인 후 중복되지 않는 것은 슬랙으로 알림을 보냅니다.
    for i in range(0,20):
        if before_list[0] != post_list[i] and before_list[1] != post_list[i] \
                and before_list[2] != post_list[i] and before_list[3] != post_list[i] \
                and before_list[4] != post_list[i] and before_list[5] != post_list[i] \
                and before_list[6] != post_list[i] and before_list[7] != post_list[i] \
                and before_list[8] != post_list[i] and before_list[9] != post_list[i] \
                and before_list[10] != post_list[i] and before_list[11] != post_list[i] \
                and before_list[12] != post_list[i] and before_list[13] != post_list[i] \
                and before_list[14] != post_list[i] and before_list[15] != post_list[i] \
                and before_list[16] != post_list[i] and before_list[17] != post_list[i] \
                and before_list[18] != post_list[i] and before_list[19] != post_list[i]:

            # slack bot setting
            attachments_dict['pretext'] = "기업마당 사이트에 새로운 공지사항이 등록되었습니다. :mememe:"
            attachments_dict['title'] = post_list[i]
            attachments_dict['title_link'] = "http://www.bizinfo.go.kr/see/seea/selectSEEA100.do"
            attachments = [attachments_dict]

            # slack bot으로 알림을 보냅니다.
            slack.chat.post_message(channel='# 98_알림_정부정책', attachments=attachments, as_user=True)
            print(post_list[i])

    # 이번에 가져온 새로운 20개의 내용을 저장합니다.
    with open('latest2.txt', 'w', encoding='utf-8') as f_write:
        for i in range(0,20):
            f_write.write(post_list[i])
            f_write.write('\n')

    print('new_post_bot2 Done')