import webview
import json
import threading
import pandas as pd
class API:
    def __init__(self):
        self.lock = threading.Lock()
        # 示例数据：论文列表
        # self.papers = [
        #     {
        #         'doi': '10.1000/xyz123',
        #         'title': '深度学习在图像识别中的应用',
        #         'authors': '张三, 李四',
        #         'abstract': '本文探讨了深度学习在图像识别中的应用及其效果。',
        #         'explanation': '通过构建卷积神经网络，显著提高了图像分类的准确率。',
        #         'url': 'https://example.com/paper1',
        #         'interested': False
        #     },
        #     {
        #         'doi': '10.1000/xyz456',
        #         'title': '自然语言处理的新进展',
        #         'authors': '王五, 赵六',
        #         'abstract': '本文综述了自然语言处理领域的最新研究进展。',
        #         'explanation': '介绍了Transformer模型及其在机器翻译中的应用。',
        #         'url': 'https://example.com/paper2',
        #         'interested': False
        #     },
        # ]
        self.file_path = 'paper_entries/archive_20240928.csv'
        
        df = pd.read_csv(self.file_path)
        df.dropna(inplace=True)
        df = df[df['is_relevant'] == True]
        self.papers = df.to_dict('records')

    def get_papers(self):
        """
        获取所有论文的信息。
        """
        with self.lock:
            # 返回论文列表的JSON字符串
            return json.dumps(self.papers)

    def mark_interested(self, doi):
        """
        标记某篇论文为感兴趣。
        :param doi: 论文的 DOI
        :return: 标记成功返回 True，已标记返回 False
        """
        with self.lock:
            for paper in self.papers:
                if paper['doi'] == doi:
                    if not paper.get('interested', False):
                        paper['interested'] = True
                        return json.dumps(True)
                    else:
                        return json.dumps(False)
            # 如果未找到对应的DOI，返回False
            return json.dumps(False)

    def get_paper_details(self, doi):
        """
        获取某篇论文的详细信息。
        :param doi: 论文的 DOI
        :return: 论文详细信息的JSON字符串，如果未找到返回空对象
        """
        with self.lock:
            for paper in self.papers:
                if paper['doi'] == doi:
                    return json.dumps(paper)
            # 如果未找到对应的DOI，返回空JSON
            return json.dumps({})

def on_loaded():
    """
    窗口加载完成后调用的函数。
    触发前端的loadPapers函数以加载论文。
    """
    window.evaluate_js('loadPapers()')  # 触发前端的loadPapers函数

if __name__ == '__main__':
    api = API()
    window = webview.create_window(
        'PaperLens',
        url='webview/main.html',
        height=2000,       # 设置窗口高度
        min_size=(500, 900),  # 设置最小窗口大小
        text_select=True,  # 允许文本选择
        js_api=api         # 将API实例传递给js_api参数
    )
    # 订阅 'loaded' 事件，当窗口加载完成后调用on_loaded
    window.events.loaded += on_loaded

    # 启动Webview窗口
    # Setting window icon is supported only on GTK and QT. 
    # For other platforms, icon is set during freezing.
    webview.start(debug=True, icon='webview/icon.png')