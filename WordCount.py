#coding=utf-8

from collections import Counter
from operator import itemgetter as _itemgetter
import jieba
import File_Interface as FI
import pickle

class WordCounter():
    # can calculate the freq of words in a text list
    # for example
    # >>> data = ['Merge multiple sorted inputs into a single sorted output',
    #           'The API below differs from textbook heap algorithms in two aspects']
    # >>> wc = WordCounter(data)
    # >>> print(wc.count_res)
    # >>> MulCounter({' ': 18, 'sorted': 2, 'single': 1, 'below': 1, 'inputs': 1, 'The': 1, 'into': 1, 'textbook': 1,
    #                'API': 1, 'algorithms': 1, 'in': 1, 'output': 1, 'heap': 1, 'differs': 1, 'two': 1, 'from': 1,
    #                'aspects': 1, 'multiple': 1, 'a': 1, 'Merge': 1})

    def __init__(self, text_list):
        self.text_list = text_list
        self.stop_word = self.Get_Stop_Words()
        self.count_res = None
        self.Word_Count(self.text_list)

    def Get_Stop_Words(self):
        ret = []
        ret = FI.load_pickle('./static/stop_words.pkl')
        return ret

    def Word_Count(self,text_list,cut_all=False):
        filtered_word_list = []
        count = 0
        for line in text_list:
            res = jieba.cut(line,cut_all=cut_all)
            res = list(res)
            text_list[count] = res
            count += 1
            filtered_word_list += res

        self.count_res = MulCounter(filtered_word_list)
        #去掉停用词
        for word in self.stop_word:
            try:
                self.count_res.pop(word)
            except:
                pass

class MulCounter(Counter):
    # a class extends from collections.Counter
    # eg: Counter(["a","class","extends","from","collections","Counter"])
    # add some methods, larger_than and less_than
    #github上没注释掉此代码
    """
    def __init__(self,element_list):
        super().__init__(element_list)
    """
    def larger_than(self,minvalue,ret='list'):
        temp = sorted(self.items(),key=_itemgetter(1),reverse=True)
        low = 0
        high = temp.__len__()
        while(high - low > 1):
            mid = (low+high) >> 1
            if temp[mid][1] >= minvalue:
                low = mid
            else:
                high = mid
        if temp[low][1]<minvalue:
            if ret=='dict':
                return {}
            else:
                return []
        if ret=='dict':
            ret_data = {}
            for ele,count in temp[:high]:
                ret_data[ele]=count
            return ret_data
        else:
            return temp[:high]

    def less_than(self,maxvalue,ret='list'):
        temp = sorted(self.items(),key=_itemgetter(1))
        low = 0
        high = temp.__len__()
        while ((high-low) > 1):
            mid = (low+high) >> 1#/
            if temp[mid][1] <= maxvalue:
                low = mid
            else:
                high = mid
        if temp[low][1]>maxvalue:
            if ret=='dict':
                return {}
            else:
                return []
        if ret=='dict':
            ret_data = {}
            for ele,count in temp[:high]:
                ret_data[ele]=count
            return ret_data
        else:
            return temp[:high]

if __name__ == '__main__':
    """
    stop_words = open(u"./static/中文停用词表（比较全面，有1208个停用词）.txt")
    list1 = []
    for line in stop_words:
        list1.append(line.strip())
    print len(list1)
    pickle.dump(list1,open("./static/stop_words.pkl","wb"),protocol = 2)
    """
    text = FI.load_pickle("./static/stop_words.pkl") #list
    for x in text:
        print x.decode("gbk")
        break

    data = ['Merge multiple sorted inputs into a single sorted output','The API below differs from textbook heap algorithms in two aspects']
    wc = WordCounter(data)
    print(wc.count_res.larger_than(16))
    """
    c=MulCounter('abcdeabcdaffbcabag')
    print(sorted(c.items(),key=_itemgetter(1),reverse=True))#operator.itemgetter(1)
    print(c.larger_than(3))
    """
    pass