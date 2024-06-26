from notion_client import Client
import json
from datetime import datetime
from pathlib import Path

class GetProperties:
    """
        GetProperties
        ===
        NotionAPIを用いてデータベースの情報を取得する
        
        Parameters
        ---
        None
        
        Methods
        ---
        get_dbid_list()
            全登録ユーザーのデータベースIDリストを取得
        get_user_name_list(db_id_list:list)
            ユーザー名リストを取得
        get_db_info(db_id:str)
            指定したDBIDに対応したDBを参照し、情報を取得
        update_property(db_id:str, property_name:str, new_contents:str)
            指定したプロパティを更新
    """
    
    current_dir = Path(__file__).resolve().parent
    conf_path = current_dir / '../config/config.json'
    conf = json.load(open(conf_path, 'r', encoding='utf-8'))

    def get_dbid_list(self) -> list:
        """
        全登録ユーザーのデータベースIDリストを取得

        Parameters
        ---
        None

        Returns
        ---
        dbid_list : list
            全登録ユーザーのデータベースIDリスト
        """

        NOTION_ACCESS_TOKEN = self.conf['master']['NOTION_ACCESS_TOKEN']
        NOTION_MASTER_ID = self.conf['master']['NOTION_MASTER_ID']
        client = Client(auth=NOTION_ACCESS_TOKEN)
        self.r = client.databases.query(NOTION_MASTER_ID)

        # パース部
        try:
            self.dbid_list = []
            for i in range(len(self.r['results'])):
                self.id = self.r['results'][i]['properties']['データベースID']['title'][0]['plain_text']
                self.dbid_list.append(self.id)
        except:
            error_time = datetime.now().strftime('[%Y/%m/%d] %H:%M')
            print(f'{error_time} NOTION_ERROR_001')
        return self.dbid_list
    
    # ユーザー名リストを取得
    def get_user_name_list(self, db_id_list:list) -> list:
        """
        ユーザー名リストを取得

        Parameters
        ---
        db_id_list : list
            データベースIDリスト
        
        Returns
        ---
        user_name_list : list
            ユーザー名リスト
        """

        self.user_name_list, self.flag_list = [], []
        for db_id in db_id_list:
            self.user_info, self.flag = self.get_db_info(db_id)
            self.user_name_list.append(self.user_info['name'])
            self.flag_list.append(self.flag)
        return self.user_name_list, self.flag_list
    
    # 指定したDBIDに対応したDBを参照し、情報を取得
    def get_db_info(self, db_id:str) -> dict:
        """
        指定したDBIDに対応したDBを参照し、情報を取得

        Parameters
        ---
        db_id : str
            データベースID
        
        Returns
        ---
        mailinfo_dict : dict
            メール構成要素情報
        """

        NOTION_ACCESS_TOKEN = self.conf['database_loading']['NOTION_ACCESS_TOKEN']
        NOTION_DATABASE_ID = db_id
        self.client = Client(auth=NOTION_ACCESS_TOKEN)
        self.r = self.client.databases.query(NOTION_DATABASE_ID)
        # パース部
        try:
            self.mailinfo_dict, self.flag = self._get_personal_info(self.r)
        except:
            error_time = datetime.now().strftime('[%Y/%m/%d] %H:%M')
            print(f'{error_time} NOTION_ERROR_002')
        return self.mailinfo_dict, self.flag
    
    # db_infoのjsonパーサー
    def _get_personal_info(self, db_json:str):
        self.parent_node = db_json['results'][len(db_json['results'])-1]['properties']
        self.name = self.parent_node['苗字']['title'][0]['plain_text']
        property_list = ['学年', '静大メール', 'パスワード', '進捗項目', '進捗マップ', '署名', '自由記入欄']
        if not any([len(self.parent_node[p]['rich_text'])==0 for p in property_list]): # 全プロパティが空でない
            self.grade = self.parent_node['学年']['rich_text'][0]['plain_text']
            self.email = self.parent_node['静大メール']['rich_text'][0]['plain_text']
            self.password = self.parent_node['パスワード']['rich_text'][0]['plain_text']
            self.progress = self.parent_node['進捗項目']['rich_text'][0]['plain_text']
            self.progress_map = self.parent_node['進捗マップ']['rich_text'][0]['plain_text']
            self.signature = self.parent_node['署名']['rich_text'][0]['plain_text']
            self.other = self.parent_node['自由記入欄']['rich_text'][0]['plain_text']
            self.mailinfo_dict = {'name':self.name,'grade':self.grade,'email':self.email,'password':self.password,'progress':self.progress,'progress_map':self.progress_map,'signature':self.signature,'other':self.other}
            self.flag = True
        else:
            self.mailinfo_dict = {'name':'','grade':'','email':'','password':'','progress':'','progress_map':'','signature':'','other':''}
            self.flag = False
                
        return self.mailinfo_dict, self.flag
    
    # 指定したプロパティを更新
    def update_property(self, db_id:str, property_name:str, new_contents:str):
        """
        指定したプロパティを更新

        Parameters
        ---
        db_id : str
            データベースID
        property_name : str
            プロパティ名
        new_contents : str
            更新内容

        Returns
        ---
        None
        """

        NOTION_ACCESS_TOKEN = self.conf['master']['NOTION_ACCESS_TOKEN']
        client = Client(auth=NOTION_ACCESS_TOKEN)
        r = client.databases.query(db_id)
        try:
            client.pages.update(page_id=r['results'][0]['id'], properties={property_name: {'rich_text': [{'type':'text', 'text':{'content':{new_contents}}}]}})
        except:
            error_time = datetime.now().strftime('[%Y/%m/%d] %H:%M')
            print(f'{error_time} NOTION_ERROR_003')