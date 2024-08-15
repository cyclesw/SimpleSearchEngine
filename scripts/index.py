# coding: utf-8
import os
import jieba
from threading import Lock
from typing import List
from dataclasses import dataclass
from loguru import logger
from collections import defaultdict
from types import InvertedElem


@dataclass
class DocInfo:
    title: str = ''
    content: str = ''
    url: str = ''
    id: int = 0

@dataclass
class word_cnt:
    title_cnt: int = 0
    content_cnt: int = 0


class Index:
    instance = None
    lock = Lock()

    X = 10  # 标题权重
    Y = 1  # 内容权重

    # TODO 检查是否必要
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            with cls.lock:
                if cls.instance is None:
                    cls.instance = super().__new__(cls)
        else:
            return cls.instance

    def __init__(self):
        self.__forward_index: List[DocInfo] = []
        self.__inverted_index: defaultdict[str, List[InvertedElem]] = defaultdict(list)

    def get_forward_index(self, doc_id: int):
        if doc_id > len(self.__forward_index):
            logger.error('doc_id is out of range')
            return None
        return self.__forward_index[doc_id]

    def get_inverted_index(self, word: str):
        if word not in self.__inverted_index:
            logger.error('word not in inverted_index')
            return None

        return self.__inverted_index[word]

    """
        @brief 建立搜索引擎所需的前后排索引
    """
    def build_index(self, string: str):
        with open(string, mode='b+r') as f:
            while f.tell() != os.fstat(f.fileno()).st_size:
                line = f.readline()
                doc = self.__build_forward_index(line.decode('utf-8'))
                if doc is None:
                    logger.error(f'build {line} error')
                    continue

                self.__build_inverted_index(doc)

    """
        @:brief: 前排索引
    """
    def __build_forward_index(self, line: str):
        sep = '\3'
        words = line.split(sep)
        if len(words) != 3:
            return None

        doc = DocInfo()
        doc.title = words[0]
        doc.content = words[1]
        doc.url = words[2]
        doc.id = len(self.__forward_index)
        self.__forward_index.append(doc)

        return self.__forward_index[-1]  #todo 检查是否为引用

    """
        @:brief: 构建倒排索引
    """
    def __build_inverted_index(self, doc: DocInfo):
        word_map = defaultdict(word_cnt)

        title_words = jieba.cut_for_search(sentence=doc.title)
        for s in title_words:
            word_map[s.lower()].title_cnt += 1

        content_words = jieba.cut_for_search(sentence=doc.content)
        for s in content_words:
            word_map[s.lower()].content_cnt += 1

        for key, value in word_map.items():
            item = InvertedElem()
            item.id = doc.id
            item.word = key
            item.weight = value.title_cnt * self.X + value.content_cnt * self.Y
            inverted_list = self.__inverted_index[key]
            inverted_list.append(item)

