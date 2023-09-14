# -*- coding: UTF-8 –*-
import sys

import jiagu
import pandas as pd
from snownlp import SnowNLP
from wordcloud import WordCloud
from pprint import pprint  # 美观打印
import jieba.analyse
from PIL import Image
import numpy as np


# jiagu.init() # 可手动初始化，也可以动态初始化

# text = '厦门明天会不会下雨'

# 情感分析打标
def sentiment_analyse(v_cmt_list):
    score_list = []
    tag_list = []
    pos_count = 0
    neg_count = 0
    for comment in v_cmt_list:
        tag = ''
        sentiments_score = SnowNLP(comment).sentiments
        if sentiments_score < 0.3:
            tag = '消极'
            neg_count += 1
        else:
            tag = '积极'
            pos_count += 1
        score_list.append(sentiments_score)  # 得分值
        tag_list.append(tag)  # 判定结果
    print('积极评价占比：', round(pos_count / (pos_count + neg_count), 4))
    print('消极评价占比：', round(neg_count / (pos_count + neg_count), 4))
    df['情感得分'] = score_list
    df['分析结果'] = tag_list
    # 把情感分析结果保存到excel文件
    df.to_excel('老番茄弹幕.xlsx', index=None)
    print('情感分析结果已生成')


def make_wordcloud(v_str, v_stopwords, v_outfile):
    print('开始生成词云图：{}'.format(v_outfile))
    try:
        stopwords = v_stopwords  # 停用词
        background_Image = np.array(Image.open('老番茄.png'))  # 读取背景图片
        wc = WordCloud(
            background_color="white",
            width=531,
            height=500,
            max_words=1000,
            font_path='STCAIYUN.TTF',
            stopwords=stopwords,
            mask=background_Image,
        )
        jieba_text = " ".join(jieba.lcut(v_str))
        wc.generate_from_text(jieba_text)
        wc.to_file(v_outfile)
        print('词云文件保存成功：{}'.format(v_outfile))
    except Exception as e:
        print('make_wordcloud except:{}'.format(str(e)))


if __name__ == '__main__':
    # with open('test.csv', 'rb') as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         print(line.decode('utf-8'),end='')
    # f.close()
    # sys.exit(0)
    df = pd.read_excel('老番茄弹幕.xlsx')  # 读取excel
    # print(df)
    # sys.exit(0)
    v_cmt_list = df['弹幕内容'].values.tolist()  # 评论内容列表
    print('length of v_cmt_list is:{}'.format(len(v_cmt_list)))
    v_cmt_list = [str(i) for i in v_cmt_list]
    v_cmt_str = ' '.join(str(i) for i in v_cmt_list)

    f = open('stop_words.txt', encoding='utf-8')
    v_stopwords_tmp = f.read()
    v_stopwords = list(v_stopword for v_stopword in v_stopwords_tmp.split('\n'))
    f.close()

    # 1、情感分析打分
    sentiment_analyse(v_cmt_list=v_cmt_list)
    # 2、用jieba统计弹幕中的top10高频词
    keywords_top10 = jieba.analyse.extract_tags(v_cmt_str, withWeight=True, topK=20)
    print("top10关键词及权重：")
    pprint(keywords_top10)
    # 3、画词云图
    make_wordcloud(v_str=v_cmt_str,
                   v_stopwords = v_stopwords,
                   v_outfile='老番茄弹幕_词云图.jpg'
                   )

# f = open('stop_words.txt', encoding='utf-8')
# v_stopwords = f.read()


# words = jiagu.seg(text)
# print(words)

# jiagu.load_userdict('dict/user.dict') # 加载自定义字典，支持字典路径、字典列表形式。
# jiagu.load_userdict(['汉服和服装'])

# words = jiagu.seg(text) # 自定义分词，字典分词模式有效
# print(words)

# sentiment = jiagu.sentiment(text)
# print(sentiment)
