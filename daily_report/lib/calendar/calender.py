import datetime as dt
import os
from pathlib import Path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# requirements.txt

class Calendar:
    """
    Calendar
    ===
    Google Calendar APIを使用して、峰野研究室予定表からイベントを取得します。

    Parameters
    ---
    None
    
    Methods
    ---
    get_today_events()
        本日のイベントを取得

    Usage
    ---
    ```python
    >>> calendar_api = Calendar()
    >>> calendar_api.get_today_events()
    [('2021-09-02T10:00:00+09:00', 'イベント1'), ('2021-09-02T12:00:00+09:00', 'イベント2')]
    >>> calendar_api.get_next_plan_list('ユーザ名')
    [('2021-09-03T10:00:00+09:00', '予定1'), ('2021-09-03T12:00:00+09:00', '予定2')]
    ```

    Requirements(これらのファイルが必要):
    ---
    credentials.json
        Google Calendar APIの認証情報
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    def __init__(self):
        self.creds = None
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.token_path = os.path.join(self.current_dir, 'token.json')
        self.credentials_path = os.path.join(self.current_dir, 'credentials.json')
        # アクセスとリフレッシュトークンを保存するファイルであるtoken.jsonが存在する場合、それを使用
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        # 利用可能な認証情報がない場合、ユーザーにログイン
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # 次回の実行のために認証情報を保存
            with open(self.token_path, 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_today_events(self):
        """
            本日のイベントを取得
            
            Returns
            ---
            list
                本日のイベントの開始時間とタイトルのリスト
        """
        # 日本時間に変換して、本日の0時から23時59分59秒までのイベントを取得
        start_of_today = dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + '+09:00'
        end_of_today = dt.datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999).isoformat() + '+09:00'
        events = self.service.events().list(
            calendarId='minelab.jp_8ssb6bcklf9il488gdf8diknb0@group.calendar.google.com',
            timeMin=start_of_today,
            timeMax=end_of_today,
            singleEvents=True,
            orderBy='startTime'
        ).execute().get('items', [])
        # イベントの開始時間とタイトルを取得
        start = [event['start'].get('dateTime', event['start'].get('date')) for event in events]
        summary = [event['summary'] for event in events]
        schedules = list(zip(start, summary))
        return schedules
    
    def get_next_plan_list(self, user_name):
        """
            明日以降1週間の予定を取得
            
            Parameters
            ---
            user_name : str
                ユーザー名
            
            Returns
            ---
            list
                [ユーザ名] 明日以降1週間の予定(予定の開始時間, 予定のタイトル)のリスト
        """
        # 予定の取得
        start_of_tomorrow = (dt.datetime.now() + dt.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + '+09:00'
        end_of_week = (dt.datetime.now() + dt.timedelta(days=7)).replace(hour=23, minute=59, second=59, microsecond=999999).isoformat() + '+09:00'
        events = self.service.events().list(
            calendarId='minelab.jp_8ssb6bcklf9il488gdf8diknb0@group.calendar.google.com',
            timeMin=start_of_tomorrow,
            timeMax=end_of_week,
            singleEvents=True,
            orderBy='startTime'
        ).execute().get('items', [])
        # ユーザ名かWRを含むイベントのみを抽出
        events = [event for event in events if (user_name in event['summary']) or ('WR' in event['summary'])]
        # イベントの開始時間とタイトルを取得
        start = [event['start'].get('dateTime', event['start'].get('date')) for event in events]
        summary = [event['summary'] for event in events]
        schedules = list(zip(start, summary))
        return schedules