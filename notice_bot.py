#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import os
import telegram
import ast

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def main() :
    try :
        with open("/home/kwonl/study/latest_list.txt", "r") as f :
            latest_bbs = int(f.readline())
    except :
        latest_bbs = 0
    # Temp for server check..
    # with open("tmp.txt", "r") as f :
    #     res = f.read()

    bot = telegram.Bot(token='776565917:AAF9sbZM_9jxrFYp3DApQFisBcG4AwkGgPQ')
    chat_ids = list()
    user_list = list()
    try :
        with open("/home/kwonl/study/chat_id_list.txt", "r") as f :
            chat_ids = ast.literal_eval(f.read())
        with open("/home/kwonl/study/user_list.txt", "r") as f :
            user_list = ast.literal_eval(f.read())
    except :
        pass

    for chat_list in bot.getUpdates() :
        if chat_list.message.chat.id not in chat_ids :
            chat_ids.append(chat_list.message.chat.id)
        if chat_list.message.chat.first_name not in user_list :
            user_list.append(chat_list.message.chat.first_name)
    
    with open("/home/kwonl/study/chat_id_list.txt", "w+") as f:
        f.write(str(chat_ids))
    with open("/home/kwonl/study/user_list.txt", "w+") as f :
        f.write(str(user_list))

    # For user list
    print(chat_ids)
    print(user_list)

    res = requests.get("https://www.coinbit.co.kr/webbbsmain/noticelists/chno-100/&page=1/&subject=")
    res = res.text
    # Decoding and dict dumping
    decoded_res = res.encode('utf-8').decode("unicode-escape")
    notice_list = ast.literal_eval(decoded_res)
    latest_notice = notice_list[0]

    if latest_bbs == 0 or latest_bbs < int(latest_notice.get("bbs_no", 0)) :
        title = latest_notice.get("subject", "")
        content = latest_notice.get("content", "")
        content = content.replace("<br \\/>", "\n")
        content = remove_html_tags(content)

        for chat_id in chat_ids :
            bot.sendMessage(chat_id=chat_id, text="New notice!\n제목: " + title + "\n\n내용: \n" + content)
            pass
        latest_bbs = latest_notice.get("bbs_no", 0);
        with open("/home/kwonl/study/latest_list.txt", "w+") as f :
            f.write(str(latest_bbs) + "\n")

    return

if __name__ == "__main__" :
    main() 
