# -*- coding:utf-8 -*-
import private.DB as DB
import os
from openpyxl import load_workbook
from private.aws_emailsender import mail_sender


def WEEK1(company_name, month_no, employees, email_date, thismonth):

    f1 = open('./raw/Week1_JOINDATE.html', 'r', encoding='utf-8')
    f2 = open('./html/%s_WEEK1/%s.html' % (email_date, company_name), 'w', encoding='utf-8')

    for line in f1:
        for r in (
                ("{M}", month_no), ("{employees}", employees), ("{thismonth}", thismonth)):
            line = line.replace(*r)
        f2.write(line)
    f1.close()
    f2.close()

    f = open('./html/%s_WEEK1/%s.html' % (email_date, company_name), "r", encoding='utf-8')
    html = f.read()
    f.close()

    return html

def WEEK2_3(company_name, month_no, employees, email_date, thismonth, duedate):

    if employees != '없음':

        status = 'NEWBIE'

        f1 = open('./raw/Week2-3_NEWBIE.html', 'r', encoding='utf-8')
        f2 = open('./html/%s_WEEK2-3/%s_%s.html' % (email_date, status, company_name), 'w', encoding='utf-8')

        for line in f1:
            for r in (
                    ("{M}", month_no), ("{employee}", employees), ("{thismonth}", thismonth), ("{duedate}", duedate)):
                line = line.replace(*r)
            f2.write(line)
        f1.close()
        f2.close()
    else:

        status = 'NO_NEWBIE'

        f1 = open('./raw/Week2-3_NO_NEWBIE.html', 'r', encoding='utf-8')
        f2 = open('./html/%s_WEEK2-3/%s_%s.html' % (email_date, status, company_name), 'w', encoding='utf-8')

        for line in f1:
            for r in (
                    ("{M}", month_no), ("{thismonth}", thismonth), ("{duedate}", duedate)):
                line = line.replace(*r)
            f2.write(line)
        f1.close()
        f2.close()

    f = open('./html/%s_WEEK2-3/%s_%s.html' % (email_date, status, company_name), "r", encoding='utf-8')
    html = f.read()
    f.close()

    return html


def WEEK4(status, company_name, month_no, employees, post_no, email_date):

    f1 = open('./raw/Week4_%s.html' % status, 'r', encoding='utf-8')
    f2 = open('./html/%s_WEEK4/%s_%s.html' % (email_date, status, company_name), 'w', encoding='utf-8')

    if status == 'NONE' or status == 'NEXT_APPLY':
        line = f1.read().replace("{M}", month_no)
        f2.write(line)
    elif status == 'RECEIVING':
        for line in f1:
            for r in (
                    ("{M}", month_no), ("{employee}", employees)):
                line = line.replace(*r)
            f2.write(line)
    elif status == 'REVIEWING':
        for line in f1:
            for r in (
                    ("{M}", month_no), ("{employee}", employees), ("{post}", post_no)):
                line = line.replace(*r)
            f2.write(line)
    f1.close()
    f2.close()

    f = open('./html/%s_WEEK4/%s_%s.html' % (email_date, status, company_name), "r", encoding='utf-8')
    html = f.read()
    f.close()

    return html


def find_userlist(company_id):
    SQL = ''
    cur.execute(SQL)
    infos = cur.fetchall().pop()
    includes = infos['includes']
    includes = includes.split(';')

    return includes


conn = DB.get_connection_real()
cur = DB.get_cursor(conn)

week_no = input('몇주차의 메일을 보내나요?(1~4): ')
month_no = input('몇월달에 대한 신청인가요?: ')
if week_no == '1':
    thismonth = input('몇월달, 몇일까지 제출해야 하나요?(M월 D일): ')
elif week_no == '2-3':
    thismonth = input('몇월의 마지막 신청월인가요?: ')
    duedate = input('언제까지 제출해야하나요?(M월 D일): ')
is_test = input('테스트로 발송합니까?(예:1,아니오:0): ')
email_date = input('오늘은 몇일인가요?: ')

try:
    path = os.path.join('./html', '%s_WEEK%s' % (email_date, week_no))
    os.mkdir(path)

except:
    print('============  %s 폴더가 이미 생성되어있습니다.  ============' % email_date)

# HTML생성기
excel_document = load_workbook(filename='./mail_list.xlsx')
sheet = excel_document['Sheet1']
all_rows = sheet.rows

row_count = len(sheet['A'])
for num in range(2, row_count+1):
    company_id = str(sheet['A%s' % num].value)  # 회사id
    company_name = str(sheet['B%s' % num].value)  # 회사이름
    status = str(sheet['C%s' % num].value)  # 상태값
    employees = str(sheet['D%s' % num].value)  # 대상 이름
    if employees == 'None' or employees == '':
        employees = '없음'
    amount = str(sheet['E%s' % num].value)  # 신청금액
    post_no = str(sheet['F%s' % num].value)  # 게시글 번호
    if post_no == 'None':
        post_no = ''

    title = '20년 %s월 %주차 진행을 시작합니다.' % (month_no, week_no)

    if week_no == '1':
        html = WEEK1(company_name, month_no, employees, email_date, thismonth)

    elif week_no == '2-3':

        html= WEEK2_3(company_name, month_no, employees, email_date, thismonth, duedate)

    elif week_no == '4':

        html = WEEK4(status, company_name, month_no, employees, post_no, email_date)

    if is_test == '1':
        result = mail_sender(title, html, 'sparrow_hh@naver.com', 'contact')

        if result is not None:
            print(company_name + ' 테스트 발송 성공')

    else:
        user_list = find_userlist(company_id)
        for userID in user_list:
            if userID != '':
                SQL = ""
                cur.execute(SQL)
                user = cur.fetchall().pop()

                if user['email'] is not None:
                    result = mail_sender(title, html, user['email'], 'contact')

                    if result is not None:
                        print(company_name + user['email'] + ' 성공')
                else:
                    print(company_name + userID + ' 메일주소없음')

title_txt = open('./html/%s_WEEK%s/00_메일제목_%s.txt' % (email_date, week_no, title), 'w', encoding='utf-8')
title_txt.close()