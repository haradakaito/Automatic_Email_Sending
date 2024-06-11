class Database:
    """
        データベースの情報を取得するクラス

        Parameters
        ----------
        None
        
        Methods
        -------
        db_info_parse(db_json:str) -> dict
            db_jsonをパースし，ユーザ情報を取得する
    """
    # db_infoのパーサー
    def db_info_parse(self, db_json:str) -> dict:
        """
            db_jsonをパースし，ユーザ情報を取得する

            Parameters
            ----------
            db_json : str
                データベースの情報

            Returns
            -------
            mailinfo_dict : dict
                ユーザ情報
        """
        parent_node = db_json['results'][len(db_json['results'])-1]['properties']
        properties  = ['学年', '静大メール', 'パスワード', '進捗項目', '進捗マップ', '署名', '自由記入欄']
        # すべてのプロパティが存在する場合
        if all([len(parent_node[p]['rich_text'])!=0 for p in properties]):
            mailinfo_dict = {
                'name':         parent_node['苗字']['title'][0]['plain_text'],
                'grade':        parent_node['学年']['rich_text'][0]['plain_text'],
                'email':        parent_node['静大メール']['rich_text'][0]['plain_text'],
                'password':     parent_node['パスワード']['rich_text'][0]['plain_text'],
                'progress':     parent_node['進捗項目']['rich_text'][0]['plain_text'],
                'progress_map': parent_node['進捗マップ']['rich_text'][0]['plain_text'],
                'signature':    parent_node['署名']['rich_text'][0]['plain_text'],
                'other':        parent_node['自由記入欄']['rich_text'][0]['plain_text'],
                'flag':         True
                }
            return mailinfo_dict
        # 名前は存在するが，それ以外のプロパティが存在しない場合
        else:
            try:
                mailinfo_dict = {
                    'name':parent_node['苗字']['title'][0]['plain_text'],
                    'flag':False
                    }
                return mailinfo_dict
            except:
                return None