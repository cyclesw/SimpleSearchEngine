from bs4 import BeautifulSoup
from loguru import logger
from typing import List
from scripts.types import DocInfo
import os


class UrlParser:
    """
        用于解析html文件，并将格式化后的文档写入raw.txt文件
    """
    SRC_PATH = 'data/input'
    OUTPUT = 'data/output/raw.txt'
    URL_HEAD = 'https://www.boost.org/doc/libs/1_85_0/doc/html/'
    SEP = '\3'  # 切割的标志符

    def __init__(self):
        self.files_list: List[str] = []
        self.items: List[DocInfo] = []

    def start(self):
        self.enum_file()
        self.parser_html()
        self.save_html()

    def enum_file(self):
        if os.path.exists(self.SRC_PATH) is False:
            logger.error(f'{self.SRC_PATH} not exists')
            return False

        for root, dirs, files in os.walk(self.SRC_PATH):
            for file in files:
                if file.endswith('.html'):
                    self.files_list.append(os.path.join(root, file))
                    print(os.path.join(root, file))

        return True

    def parser_html(self):
        for file in self.files_list:
            doc = DocInfo()
            with open(file) as f:
                soup = BeautifulSoup(f, 'html.parser')
                # fill doc
                if soup.title is None:
                    continue
                else:
                    doc.title = soup.title.string

                for string in soup.stripped_strings:
                    doc.content += string.replace('\n', '')

                doc.url = self.URL_HEAD + file[len(self.SRC_PATH) + 1:]
                self.items.append(doc)

    def save_html(self):
        with open(self.OUTPUT, mode='b+w') as f:
            for item in self.items:
                out = f'{item.title}{self.SEP}{item.content}{self.SEP}{item.url}\n'
                f.write(out.encode('utf-8'))

    def __files_debug(self):
        for file in self.files_list:
            print(file)

if __name__ == '__main__':
    UrlParser().start()