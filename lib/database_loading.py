import requests
import json
from pathlib import Path

class GetProperties:
    current_dir = Path(__file__).resolve().parent
    conf_path = current_dir / '../config/config.json'
    conf = json.load(open(conf_path, 'r', encoding='utf-8'))

    NOTION_MASTER_ID = conf['database_loading']['NOTION_MASTER_ID']

    def get_db_info(self, db_id:str):
        self.db_id = db_id
        self.NOTION_ACCESS_TOKEN = self.conf['database_loading']['NOTION_ACCESS_TOKEN']
        self.NOTION_DATABASE_ID = self.db_id

        self.url = f"https://api.notion.com/v1/databases/{self.NOTION_DATABASE_ID}/query"
        self.headers = {
        'Authorization': 'Bearer ' + self.NOTION_ACCESS_TOKEN,
        'Notion-Version': '2021-05-13',
        'Content-Type': 'application/json',
        }

        self.r = requests.post(self.url, headers=self.headers)
        self.db_json = self.r.json()

        self.mailinfo_dict, _ = self._get_personal_info(self.db_json)

        return self.mailinfo_dict, self.flag

    def get_dbid_list(self):
        NOTION_ACCESS_TOKEN = self.conf['master']['NOTION_ACCESS_TOKEN']
        NOTION_MASTER_ID = self.conf['master']['NOTION_MASTER_ID']

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

    def get_user_name_list(self, db_id_list:list):
        user_name_list, flag_list = [], []
        for db_id in db_id_list:
            user_info, flag = self.get_db_info(db_id)
            user_name_list.append(user_info['name'])
            flag_list.append(flag)
        return user_name_list, flag_list

    def _get_personal_info(self, db_json:str):

        self.flag = True
        self.name = db_json['results'][0]['properties']['苗字']['title'][0]['plain_text']

        property_list = ['学年', '静大メール', 'パスワード', '進捗項目', '進捗マップ', '署名', '自由記入欄']
        if not any([len(db_json['results'][0]['properties'][p]['rich_text'])==0 for p in property_list]): # 全プロパティが空でない
            self.grade = db_json['results'][0]['properties']['学年']['rich_text'][0]['plain_text']
            self.email = db_json['results'][0]['properties']['静大メール']['rich_text'][0]['plain_text']
            self.password = db_json['results'][0]['properties']['パスワード']['rich_text'][0]['plain_text']
            self.progress = db_json['results'][0]['properties']['進捗項目']['rich_text'][0]['plain_text']
            self.progress_map = db_json['results'][0]['properties']['進捗マップ']['rich_text'][0]['plain_text']
            self.signature = db_json['results'][0]['properties']['署名']['rich_text'][0]['plain_text']
            self.other = db_json['results'][0]['properties']['自由記入欄']['rich_text'][0]['plain_text']
        else:
            self.grade = ''
            self.email = ''
            self.password = ''
            self.progress = ''
            self.progress_map = ''
            self.signature = ''
            self.other = ''
            self.flag = False

        self.mailinfo_dict = {'name':self.name, 'grade':self.grade, 'email':self.email, 'password':self.password, 'progress':self.progress, 'progress_map':self.progress_map, 'signature':self.signature, 'other':self.other}
        return self.mailinfo_dict, self.flag