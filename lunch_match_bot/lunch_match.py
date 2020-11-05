from slacker import Slacker
import random
from private.tokens import slack as slack_token

slack = Slacker(slack_token)

def lunch_ask_bot():
    attachments_dict = {}

    attachments_dict['pretext'] = "오늘의 점심조 참여 여부를 확인해주세요 :mememe:"
    attachments_dict['text'] = "특히 제외해야한다면 꼭! 댓글로 알려주세요 :)"
    attachments = [attachments_dict]

    # slack bot으로 알림을 보냅니다.
    slack.chat.post_message(channel='# 81_일반_업무', attachments=attachments, as_user=True)


def lunch_match_bot(add_no_lunch):

    lunch_people = [
        '조엘', '이본', '루씨', '제나', '센스', '안젤라', '영',
        '린다', '하니', '피터',
        '엘로이', '테드', '써니', '데니스', '에이제이',
        '존', '앤디',
    ]

    attachments_dict = {}

    for i in add_no_lunch:
        lunch_people.remove(i)


    def make_matches(lunch_people, match_count):
        lunch_dict = {}
        num = 0

        for i in range(match_count):
            lunch_dict['%s조' % str(i + 1)] = []

        random.shuffle(lunch_people)
        print(lunch_people)

        while num < len(lunch_people):
            for j in lunch_dict.keys():
                try:
                    lunch_dict[j].append(lunch_people[num])
                    num += 1
                except:
                    break

        return lunch_dict


    if len(lunch_people) // 4 == 0:
        attachments_dict['pretext'] = "오늘의 점심조입니다 :mememe:"
        attachments_dict['text'] = "오늘은 점심조가 없습니다. 점심 맛있게 드세요 :wink:"
        attachments = [attachments_dict]

    else:
        match_count = (len(lunch_people) // 5) +1
        lunch_dict = make_matches(lunch_people, match_count)

        lunch_dict['열외'] = add_no_lunch

        keys = lunch_dict.keys()
        slack_bot_text = ''

        for key in keys:
            slack_bot_text += '*%s* (%s명)   ' % (key, str(len(lunch_dict[key])))

            text = ''
            for people in lunch_dict[key]:
                text += people + ' '

            slack_bot_text += '%s\n' % text

        # slack bot setting
        attachments_dict['pretext'] = "오늘의 점심조입니다 :mememe:"
        attachments_dict['text'] = slack_bot_text
        attachments_dict['mrkdwn_in'] = ["text", "pretext"]
        attachments = [attachments_dict]

    # slack bot으로 알림을 보냅니다.
    slack.chat.post_message(channel='# 81_일반_업무', attachments=attachments, as_user=True)

    print('lunch_bot Done')
