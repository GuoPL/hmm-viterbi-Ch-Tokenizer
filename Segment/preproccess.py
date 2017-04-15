#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from tqdm import tqdm
'''
先要对语料库进行处理，使语料库的每个字的后面紧跟该字的状态

	1、去掉人民日报标注语料的词性标注
	2、去掉空行
	3、对每个词tokenizer
'''


CORPUS_ORIGIN = "../data/199801.txt"
CORPUS_SEG = "../data/corpus.txt"
CORPUS_POS = "../data/corpus_POS.txt"


def read_file(path, encoding='gbk'):
	content = []
	with open(path, encoding=encoding) as f:
		for line in f:
			content.append(line.strip())
	print('\n读%s文件完成' % path)
	return content


def del_pos():
	with open(CORPUS_ORIGIN, 'r') as f:
		with open(CORPUS_SEG, 'w+') as c:
			while True:
				line = f.readline()
				if line:
					Rst = line.split()
					Rst = Rst[1:]
					for i in Rst:
						i = i[:-2]
						if '/' in i:
							i = i[:-1]
						c.write(i + ' ')
					c.write('\n')
				elif line == '\n':
					continue
				else:
					break


def del_head():
	with open(CORPUS_ORIGIN, 'r') as f:
		with open(CORPUS_POS, 'w+') as pos:
			for line in f:
				Rst = line.split()[1:]
				for item in Rst:
					pos.write(item + ' ')
				pos.write('\n')


def del_n():
	with open("data/corpus.txt", 'r') as src:
		with open("data/corpu.txt", 'w+') as c:
			while True:
				line = src.readline()
				if line and line != '\n':
					c.write(line)
				elif line == '\n':
					continue
				else:
					break


def tokenize():
	'''当加入标签后，切片顺序被改变'''
	str = ""
	src = read_file("data/corpu.txt")
	with open("data/state.txt", 'w') as dst:
		for i in tqdm(range(len(src))):
			line = src[i]
			splited = line.split(' ')
			for word in splited:
				if len(word) == 1:
					word = word + '/S'
					str = str + 'S'
				elif len(word) == 2:
					word = word.replace(word[0], word[0] + '/B')
					word = word.replace(word[-1], word[-1] + '/E')
					str = str + 'BE'
				else:	# 环/B保/M局/M//Mn/E
					temp = []
					temp.append(word[0] + '/B')
					str = str + 'B'
					for k in range(1, len(word)-1):
						temp.append(word[k]+'/M')
						str = str + 'M'
					temp.append(word[-1] + '/E')
					str = str + 'E'
					word = ''
					for j in range(len(temp)):
						word += temp[j]
				dst.write(word + ' ')
			dst.write('\n')
			str = str + '\n'

	with open('data/flag.txt', 'w') as f:
		f.write(str)


if __name__ == '__main__':
	# del_pos()
	# del_n()
	# tokenize()
	del_head()


