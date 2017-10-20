#coding=utf-8
from __future__ import division
import numpy as np

class HuffmanTreeNode():
    def __init__(self,value,possibility):
        # common part of leaf node and tree node
        self.possibility = possibility
        self.left = None #权值较大
        self.right = None #权值较小
        # value of leaf node  will be the word, and be
        # mid vector in tree node
        self.value = value # the value of word
        self.Huffman = "" # store the huffman code

    def __str__(self):
        return 'HuffmanTreeNode object, value: {v}, possibility: {p}, Huffman: {h}'\
            .format(v=self.value,p=self.possibility,h=self.Huffman)

class HuffmanTree():
    def __init__(self, word_dict, vec_len=15000):
        self.vec_len = vec_len      # the length of word vector
        self.root = None

        word_dict_list = list(word_dict.values())
        node_list = [HuffmanTreeNode(x['word'],x['possibility']) for x in word_dict_list]
        self.build_tree(node_list)
        # self.build_CBT(node_list)
        self.generate_huffman_code(self.root, word_dict)

    def build_tree(self,node_list):
        # node_list.sort(key=lambda x:x.possibility,reverse=True)
        # for i in range(node_list.__len__()-1)[::-1]:
        #     top_node = self.merge(node_list[i],node_list[i+1])
        #     node_list.insert(i,top_node)
        # self.root = node_list[0]

        while node_list.__len__()>1:
            i1 = 0  # i1表示概率最小的节点
            i2 = 1  # i2 概率第二小的节点
            if node_list[i2].possibility < node_list[i1].possibility :
                [i1,i2] = [i2,i1]
            for i in range(2,node_list.__len__()): # 找到最小的两个节点
                if node_list[i].possibility<node_list[i2].possibility :
                    i2 = i
                    if node_list[i2].possibility < node_list[i1].possibility :
                        [i1,i2] = [i2,i1]
            top_node = self.merge(node_list[i1],node_list[i2])
            #先删掉大值，防止列表出现溢出
            if i1<i2:
                node_list.pop(i2)
                node_list.pop(i1)
            elif i1>i2:
                node_list.pop(i1)
                node_list.pop(i2)
            else:
                raise RuntimeError('i1 should not be equal to i2')
            node_list.insert(0,top_node)
        self.root = node_list[0]

    #构造一个完全二叉树
    def build_CBT(self,node_list): # build a complete binary tree
        node_list.sort(key=lambda  x:x.possibility,reverse=True)
        node_num = node_list.__len__()
        before_start = 0
        while node_num>1 :
            for i in range(node_num>>1):
                top_node = self.merge(node_list[before_start+i*2],node_list[before_start+i*2+1])
                node_list.append(top_node)
            if node_num%2==1:
                top_node = self.merge(node_list[before_start+i*2+2],node_list[-1])
                node_list[-1] = top_node
            before_start = before_start + node_num
            node_num = node_num>>1
        self.root = node_list[-1]

    def generate_huffman_code(self, node, word_dict):
        # # use recursion in this edition
        # if node.left==None and node.right==None :
        #     word = node.value
        #     code = node.Huffman
        #     print(word,code)
        #     word_dict[word]['Huffman'] = code
        #     return -1
        #
        # code = node.Huffman
        # if code==None:
        #     code = ""
        # node.left.Huffman = code + "1"
        # node.right.Huffman = code + "0"
        # self.generate_huffman_code(node.left, word_dict)
        # self.generate_huffman_code(node.right, word_dict)

        # use stack butnot recursion in this edition
        stack = [self.root]
        while (stack.__len__()>0):
            node = stack.pop()
            # go along left tree
            while node.left or node.right :
                code = node.Huffman
                node.left.Huffman = code + "1"
                node.right.Huffman = code + "0"
                stack.append(node.right)
                node = node.left
            word = node.value
            code = node.Huffman
            # print(word,'\t',code.__len__(),'\t',node.possibility)
            word_dict[word]['Huffman'] = code

    def merge(self,node1,node2):
        top_pos = node1.possibility + node2.possibility
        top_node = HuffmanTreeNode(np.zeros([1,self.vec_len]), top_pos)
        if node1.possibility >= node2.possibility :
            top_node.left = node1
            top_node.right = node2
        else:
            top_node.left = node2
            top_node.right = node1
        return top_node

#自定义,below for test
if __name__ == "__main__":
    from WordCount import WordCounter
    data = ['Merge multiple sorted inputs into a single sorted output',
            'The API below differs from textbook heap algorithms in two aspects']
    wc = WordCounter(data)
    word_freq = wc.count_res.larger_than(1)
    word_dict = {}
    if isinstance(word_freq, dict):
        # if word_freq is in type of dictionary
        sum_count = sum(word_freq.values())
        for word in word_freq:
            temp_dict = dict(
                word=word,
                freq=word_freq[word],
                possibility=word_freq[word] / sum_count,
                vector=np.random.random([1, 100]),#100位词向量的长度
                Huffman=None
            )
            word_dict[word] = temp_dict
    else:
        # if word_freq is in type of list
        freq_list = [x[1] for x in word_freq]
        sum_count = sum(freq_list)
        for item in word_freq:
            temp_dict = dict(
                word=item[0],
                freq=item[1],
                possibility=item[1] / sum_count,
                vector=np.random.random([1, 100]),
                Huffman=None
            )
            word_dict[item[0]] = temp_dict
    cutted_text_list = wc.text_list
    #tree = HuffmanTree(word_dict)
    #print tree.root.left.left.Huffman

    word_dict_list = list(word_dict.values())
    node_list = [HuffmanTreeNode(x['word'], x['possibility']) for x in word_dict_list]

    # 自底向上构建一颗哈夫曼树
    def merge(node1,node2):
        top_pos = node1.possibility + node2.possibility
        top_node = HuffmanTreeNode(np.zeros([1,100]), top_pos)
        if node1.possibility >= node2.possibility :
            top_node.left = node1
            top_node.right = node2
        else:
            top_node.left = node2
            top_node.right = node1
        return top_node

    print "*" * 36 + "build tree" + "*" * 36
    #node_list.sort(key = lambda x:x.possibility,reverse = False)
    root = None
    while node_list.__len__() > 1:
        i1 = 0 #最小概率值对应的点
        i2 = 1 #第二小概率值对应的点
        if node_list[i2].possibility < node_list[i1].possibility:
            [i1,i2] = [i2,i1]
        for i in range(2,node_list.__len__()):
            if node_list[i].possibility < node_list[i2].possibility:
                i2 = i
                if node_list[i2].possibility < node_list[i1].possibility:
                    [i1,i2] = [i2,i1]
        top_node = merge(node_list[i1],node_list[i2])
        if i1 < i2:
            node_list.pop(i2)
            node_list.pop(i1)
        elif i2 < i1:
            node_list.pop(i1)
            node_list.pop(i2)
        else:
            raise RuntimeError('i1 should not be equal to i2')
        node_list.insert(0,top_node)
    root = node_list[0]
    print "*" * 36 + "building huffman code" + "*" * 36
    stack = [root]
    while stack.__len__() > 0:
        node = stack.pop()
        while node.left or node.right:
            code = node.Huffman
            node.left.Huffman = code + "1"#此处编码为1的设置为负类
            node.right.Huffman = code + "0"#编码为0的设置为正类
            stack.append(node.right)
            node = node.left
        word = node.value
        code = node.Huffman
        word_dict[word]["Huffman"] = code

    l = [node_list[0]]
    while l.__len__() > 0:
        node = l.pop()
        while node.left or node.right:
            #print node.Huffman,node.possibility
            l.append(node.right)
            node = node.left

    print len(word_dict)
    for key in word_dict:
        print key,word_dict[key]["Huffman"],word_dict[key]["possibility"]