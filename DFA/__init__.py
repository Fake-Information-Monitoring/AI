# -*- coding:utf-8 -*-

import time

import jieba

from config import *
from loadingData.DFAFilter import DFAFilter


def getFilter(path: str,type:int):
    model = DFAFilter(type)
    model.parse(path)
    return model


if __name__ == "__main__":
    models = []
    for key,value in path_list.items():
        models.append(getFilter(value,key))
    text = "新疆骚乱法轮大法雞八是法轮功吧卧槽"
    text =jieba.cut(text,use_paddle=True)
    text = ','.join(text)  # 对语料进行分词
    respones = {}
    for model in models:
        text, words = model.filter(text)
        respones[model.type] = words
    print(text.replace(',', ''))
    print(respones)
