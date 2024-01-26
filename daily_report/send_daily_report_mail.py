import requests
import schedule
import time
import random
from lib.mail.contents import Contents
from lib.mail.sender import Sender
from lib.database_loading import GetProperties

def get_dbid_list():
    NOTION_ACCESS_TOKEN = 'secret_LVaQvaBjUP4yoxOChW7st8QRqZqyh5NuAbcLupcgysu' # 共通
    NOTION_MASTER_ID = '222803426c4f441e93afac9ebc2c10e0'

    url = f"https://api.notion.com/v1/databases/{NOTION_MASTER_ID}/query"
    headers = {
    'Authorization': 'Bearer ' + NOTION_ACCESS_TOKEN,
    'Notion-Version': '2021-05-13',
    'Content-Type': 'application/json',
    }

    r = requests.post(url, headers=headers)
    db_json = r.json()

    dbid_list = []
    for i in range(len(db_json['results'])):
        id = db_json['results'][i]['properties']['データベースID']['title'][0]['plain_text']
        dbid_list.append(id)

    return dbid_list

def send_daily_report():
    db_id_list = get_dbid_list()

    # db_idからメールを送信
    for db_id in db_id_list:
        time.sleep(random.randint(1, 60*20))
        user_info = GetProperties(db_id=db_id).get_db_info()
        mail_contents = Contents(**user_info)
        subject = mail_contents.create_subject() # 件名
        body = mail_contents.create_body() # 本文
        to_email = 'progress@minelab.jp'
        # to_email = 'shimada.takuto.21@shizuoka.ac.jp'

        # 送信
        sender = Sender(from_email=user_info['email'], to_email=to_email, user_name=user_info['email'], password=user_info['password'], subject=subject, body=body)
        sender.send()

def main():
    schedule.every(1).day.at('20:00').do(send_daily_report)
    while(True):
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()