import os

class Progress:
    """
        Progressクラス
        ===
        
        Methods:
        ---
        get_progress()
            進捗文を取得
        get_progress_map()
            進捗マップを取得

        Usage:
        ---
        ```python
        >>> progress = Progress()
        >>> print(progress.get_progress())
        >>> print(progress.get_progress_map())

        Requirements(これらのファイルが必要):
        ---
        progress.txt
            進捗文を記述したテキストファイル
        progress_map.txt
            進捗マップを記述したテキストファイル
    """
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.progress_path = os.path.join(self.current_dir, 'progress.txt')
        self.progress_map_path = os.path.join(self.current_dir, 'progress_map.txt')

    def get_progress(self):
        """
            進捗文を取得
        """
        return self._load_text(self.progress_path)
    
    def get_progress_map(self):
        """
            進捗マップを取得
        """
        return self._load_text(self.progress_map_path)
    
    def _load_text(self, path):
        """
            テキストファイルを読み込む
        """
        self.text_list = []
        with open(path, 'r', encoding='UTF-8') as self.f:
            for self.line in self.f:
                self.text_list.append(self.line.split("\n")[0])

        return self.text_list