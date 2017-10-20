# word2vec
code中./static目录下的文件中文停用词表（比较全面，有1208个停用词），其余两个*.pkl文件为生成的文件
code主要实现了以下功能：
1分词 / 词干提取和词形还原
2构造词典，统计词频
3构造哈夫曼树
4生成节点所在的二进制编码
5初始化各非叶节点的中间向量和叶节点中的词向量
6训练中间向量和词向量

PS:word2vec数学原理可以参考大神peghoty关于word2vec数学原理的一系列博客
