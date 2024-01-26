import requests

class GetProperties:

    NOTION_MASTER_ID = '222803426c4f441e93afac9ebc2c10e0'

    def __init__(self, db_id:str):
        self.db_id = db_id

    def get_db_info(self):
        self.NOTION_ACCESS_TOKEN = 'secret_LVaQvaBjUP4yoxOChW7st8QRqZqyh5NuAbcLupcgysu' # 共通
        self.NOTION_DATABASE_ID = self.db_id

        self.url = f"https://api.notion.com/v1/databases/{self.NOTION_DATABASE_ID}/query"
        self.headers = {
        'Authorization': 'Bearer ' + self.NOTION_ACCESS_TOKEN,
        'Notion-Version': '2021-05-13',
        'Content-Type': 'application/json',
        }

        self.r = requests.post(self.url, headers=self.headers)
        self.db_json = self.r.json()

        self.mailinfo_dict = self._get_personal_info(self.db_json)

        return self.mailinfo_dict

    def _get_personal_info(self, db_json:str):

        self.name = db_json['results'][0]['properties']['苗字']['title'][0]['plain_text']
        self.grade = db_json['results'][0]['properties']['学年']['rich_text'][0]['plain_text']
        self.email = db_json['results'][0]['properties']['静大メール']['rich_text'][0]['plain_text']
        self.password = db_json['results'][0]['properties']['パスワード']['rich_text'][0]['plain_text']
        self.progress = db_json['results'][0]['properties']['進捗項目']['rich_text'][0]['plain_text']
        self.progress_map = db_json['results'][0]['properties']['進捗マップ']['rich_text'][0]['plain_text']
        self.signature = db_json['results'][0]['properties']['署名']['rich_text'][0]['plain_text']

        self.mailinfo_dict = {'name':self.name, 'grade':self.grade, 'email':self.email, 'password':self.password, 'progress':self.progress, 'progress_map':self.progress_map, 'signature':self.signature}

        return self.mailinfo_dict