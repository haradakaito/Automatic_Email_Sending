import json

from pathlib       import Path
from notion_client import Client

class Notiontools:

    # 設定ファイルの読み込み
    current_dir = Path(__file__).resolve().parent
    conf_path   = current_dir / "../config/config.json"
    conf        = json.load(open(conf_path, "r", encoding="utf-8"))
    # クラス変数
    NOTION_ACCESS_TOKEN = conf["master"]["NOTION_ACCESS_TOKEN"]
    NOTION_MASTER_ID    = conf["master"]["NOTION_MASTER_ID"]

    def __init__(self):
        self.client = Client(auth=self.NOTION_ACCESS_TOKEN)

    def check_all_user(self) -> dict:
        all_dbid = self._get_all_dbid()
        checked_user = {} # {name: bool}
        for dbid in all_dbid:
            name = self.get_property(dbid, "苗字")
            # データベースの内容をチェック（-> bool）
            if self._check_db(dbid=dbid):
                checked_user[name] = True
            else:
                checked_user[name] = False
        return checked_user
    
    def check_all_dbid(self) -> list:
        all_dbid = self._get_all_dbid()
        checked_dbid = {} # {dbid: bool}
        for dbid in all_dbid:
            # データベースの内容をチェック（-> bool）
            if self._check_db(dbid=dbid):
                checked_dbid[dbid] = True
            else:
                checked_dbid[dbid] = False
        return checked_dbid

    def _get_all_dbid(self) -> list:
        db_json  = self.client.databases.query(self.NOTION_MASTER_ID)
        all_dbid = [tmp["properties"]["データベースID"]["title"][0]["plain_text"] for tmp in db_json["results"]]
        return all_dbid
    
    def _check_db(self, dbid:str) -> bool:
        db_json = self.client.databases.query(dbid)
        if db_json["results"][len(db_json["results"])-1]["properties"]["苗字"]["title"][0]["plain_text"] == "":
            return False
        else:
            properties = ["学年", "静大メール", "パスワード", "進捗項目", "進捗マップ", "署名", "自由記入欄"]
            if any([len(db_json["results"][len(db_json["results"])-1]["properties"][p]["rich_text"]) == 0 for p in properties]):
                return False
            else:
                return True
    
    def get_property(self, dbid:str, property:str) -> str:
        db_json = self.client.databases.query(dbid)
        if property == '苗字':
            return db_json["results"][len(db_json["results"])-1]["properties"][property]["title"][0]["plain_text"]
        else:
            return db_json["results"][len(db_json["results"])-1]["properties"][property]["rich_text"][0]["plain_text"]