# coding: utf-8

from collections import defaultdict
from typing import List
from scripts.index import Index
from scripts.types import InvertedElemPrint
import jieba


class Searcher:
    """
        根据关键词在本地raw文件中搜索文档，并返回所需要的文档。
    """
    def __init__(self):
        self.__index = Index()

    def init_searcher(self, msg):
        self.__index.build_index(msg)

    def search(self, query: str):
        words = jieba.cut_for_search(query)
        inverted_list_all: List[InvertedElemPrint] = []
        token_map = defaultdict(InvertedElemPrint)

        for word in words:
            inverted_list = self.__index.get_inverted_index(word)
            if not inverted_list:
                continue

            for elem in inverted_list:
                item = token_map[elem.id]
                item.id = elem.id
                item.weight += elem.weight
                item.words.append(word)

        for item in token_map.values():
            inverted_list_all.append(item)

        # 降序排序，将权重高的排在前面，用于网页显示。
        inverted_list_all.sort(key=lambda x: x.weight, reverse=True)
        elems = []
        for item in inverted_list_all:
            doc = self.__index.get_forward_index(item.id)   # 正排
            elem = {
                'title': doc.title,
                'desc': self.get_desc(doc.content, query),
                'url': doc.url,
                'id': item.id,
                'weight': item.weight,
            }
            elems.append(elem)
        return elems

    def get_desc(self, content: str, word: str) -> str:
        prev_step = 50
        next_step = 100

        pos = content.find(word)

        start = 0
        end = len(content) - 1
        if pos > start + prev_step:
            start = pos + prev_step
        if pos < end - next_step:
            end = pos + next_step

        return content[start:end] + '...'
