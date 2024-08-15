from typing import List
from dataclasses import dataclass
from loguru import logger
from index import Index
from types import InvertedElemPrint
import jieba
import json


class Searcher:
    def __init__(self, query: str, json_in):
        self.__index = Index()
        words = jieba.cut_for_search(query)
        inverted_lists: List[InvertedElemPrint] = []
        for word in words:
            word = word.lower()
