# -*- coding:utf-8 -*-
import util
import sys

'''
π是初始状态概率分布，就是说，对于语料库每个词，初始状态的发生概率
（实际上词中词尾的初始概率就是0）
'''
A_dic = {}  # 转移概率 
B_dic = {}  # 发射概率
Count_dic = {}  # Count(Ci)
state_list = ['B', 'M', 'E', 'S']  # 状态集

line_num = -1
word_set = set()
# INPUT_DATA = '../data/corpu.txt'
INPUT_DATA = '../data/corpus_POS.txt'
PROB_TRANS = "matrix\prob_trans.txt"  # 保存转移概率
PROB_EMIT = "matrix\prob_emit.txt"  # 保存发射概率


# 初始化字典
def init():
	for state in state_list:
		A_dic[state] = {}
		for state1 in state_list:
			A_dic[state][state1] = 0.0
	for state in state_list:
		B_dic[state] = {}
		Count_dic[state] = 0


# 输入词语，输出状态
def getList(input_str):
	outpout_str = []
	if len(input_str) == 1:
		outpout_str.append('S')
	elif len(input_str) == 2:
		outpout_str = ['B', 'E']
	else:
		M_num = len(input_str) - 2
		M_list = ['M'] * M_num
		outpout_str.append('B')
		outpout_str.extend(M_list)  # 把M_list中的'M'分别添加进去
		outpout_str.append('E')
	return outpout_str


# 申请矩阵
def matrix(rows, cols):
	mat = [[1 for col in range(cols)] for row in range(rows)]
	return mat


# 计算概率 A B
def get_A_B(dict_path):
	init()
	global word_set  # 初始是set()
	global line_num  # 初始是-1
	with open(dict_path) as ifp:
		for line in ifp:
			line_num += 1
			if line_num % 10000 == 0:
				print(line_num)

			line = line.strip()
			if not line: continue
			# line = line.decode("gbk", "ignore")  # 设置为ignore，会忽略非法字符

			word_list = []
			for i in range(len(line)):
				if line[i] == " ": continue
				word_list.append(line[i])
			word_set = word_set | set(word_list)  # 训练预料库中所有字的集合

			lineArr = line.split(" ")
			line_state = []
			for item in lineArr:
				line_state.extend(getList(item))  # 一句话对应一行连续的状态
			if len(word_list) != len(line_state):
				print(sys.stderr, "[line_num = %d][line = %s]" % (line_num, line.endoce("utf-8", 'ignore')))
			else:
				for i in range(len(line_state)):
					if i > 0:
						# 用于计算转移概率	Count(Ci,Cj) / Count(Ci)
						A_dic[line_state[i - 1]][line_state[i]] += 1

					Count_dic[line_state[i]] += 1  # B 状态的出现次数 +1

					# 计算发射概率	Count(Oj,Ci)+1 / Count(Ci)
					if word_list[i] not in B_dic[line_state[i]]:
						B_dic[line_state[i]][word_list[i]] = 1.0
					else:  # 如果单词已经在词典中
						B_dic[line_state[i]][word_list[i]] += 1


def Output():  # 输出模型的 AB 到文件
	print("len(word_set) = %s " % (len(word_set)))

	for key in A_dic:  # 状态转移概率
		for key1 in A_dic[key]:
			A_dic[key][key1] = A_dic[key][key1] / Count_dic[key]
	print(A_dic)

	for key in B_dic:  # 发射概率(状态->词语的条件概率)
		for word in B_dic[key]:
			B_dic[key][word] = B_dic[key][word] / Count_dic[key]
	print(B_dic)

	with open(PROB_TRANS, 'w') as f:
		f.write(str(A_dic))
	with open(PROB_EMIT, 'w') as f:
		f.write(str(B_dic))
	return A_dic, B_dic


def main():
	get_A_B(INPUT_DATA)
	Output()


if __name__ == '__main__':
	main()
