from dataclasses import dataclass, field
from typing import List


@dataclass
class DocInfo:
    title: str = ''
    content: str = ''
    url: str  = ''

@dataclass
class InvertedElem:
    id: int = 0
    word: str = ''
    weight: int = 0

@dataclass
class InvertedElemPrint:
    id: int = 0
    weight: int = 0
    words: List[str] = field(default_factory=list)

# only use for index
@dataclass
class word_cnt:
    title_cnt: int = 0
    content_cnt: int = 0

