from notion_client import Client
import json
import datetime as dt
from pathlib import Path

class GetProperties:
    current_dir = Path(__file__).resolve().parent
    conf_path = current_dir / '../config/config.json'
    conf = json.load(open(conf_path, 'r', encoding='utf-8'))

    NOTION_MASTER_ID = conf['database_loading']['NOTION_MASTER_ID']

    # 全登録ユーザーのデータベースIDリストを取得
    def get_dbid_list(self):
        NOTION_ACCESS_TOKEN = self.conf['master']['NOTION_ACCESS_TOKEN']
        NOTION_MASTER_ID = self.conf['master']['NOTION_MASTER_ID']
        client = Client(auth=NOTION_ACCESS_TOKEN)
        self.r = client.databases.query(NOTION_MASTER_ID)

        # パース部
        self.dbid_list = []
        for i in range(len(self.r['results'])):
            self.id = self.r['results'][i]['properties']['データベースID']['title'][0]['plain_text']
            self.dbid_list.append(self.id)
        return self.dbid_list
    
    # ユーザー名リストを取得
    def get_user_name_list(self, db_id_list:list):
        self.user_name_list, self.flag_list = [], []
        for db_id in db_id_list:
            self.user_info, self.flag = self.get_db_info(db_id)
            self.user_name_list.append(self.user_info['name'])
            self.flag_list.append(self.flag)
        return self.user_name_list, self.flag_list
    
    # 指定したDBIDに対応したDBを参照し、情報を取得
    def get_db_info(self, db_id:str):
        NOTION_ACCESS_TOKEN = self.conf['database_loading']['NOTION_ACCESS_TOKEN']
        NOTION_DATABASE_ID = db_id
        self.client = Client(auth=NOTION_ACCESS_TOKEN)
        self.r = self.client.databases.query(NOTION_DATABASE_ID)

        # パース部
        self.mailinfo_dict, self.flag = self._get_personal_info(self.r)
        return self.mailinfo_dict, self.flag
    
    # db_infoのjsonパーサー
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
    
    # 指定したプロパティを更新
    def update_property(self, db_id:str, property_name:str, new_contents:str):
        NOTION_ACCESS_TOKEN = self.conf['master']['NOTION_ACCESS_TOKEN']
        client = Client(auth=NOTION_ACCESS_TOKEN)
        r = client.databases.query(db_id)
        try:
            client.pages.update(page_id=r['results'][0]['id'], properties={property_name: {'rich_text': [{'type':'text', 'text':{'content':{new_contents}}}]}})
        except:
            error_time = dt.datetime.now().strftime('[%Y/%m/%d] %H:%M')
            print(f'{error_time} NOTION_ERROR')
        