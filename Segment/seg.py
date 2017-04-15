'''
    最大序列的逆推输出和分词实现。
'''

from Segment.viterbi import viterbi


def load_model(f_name):
	ifp = open(f_name, 'r')
	return eval(ifp.read())  # eval参数是一个字符串, 可以把这个字符串当成表达式来求值,


def cut(sentence, P_START, A, B):
	prob, pos_list = viterbi(sentence, ('B', 'M', 'E', 'S'), P_START, A, B)
	return (prob, pos_list)


if __name__ == '__main__':
	PROB_EMIT = "matrix\prob_emit.txt"  # 发射概率
	PROB_TRANS = "matrix\prob_trans.txt"  # 转移概率

	# 初始状态概率( jieba 的经验值)    
	P_START = {'B': 0.7689828525554734, 'E': 0.0, 'M': 0.0, 'S': 0.2310171474445266}
	A = load_model(PROB_TRANS)	# 转移概率 
	B = load_model(PROB_EMIT)	# 发射概率
	A, B = dict(A), dict(B)

	test_str = u"今天天气特别好"
	prob, pos_list = cut(test_str, P_START, A, B)
	print(test_str)
	print(pos_list)
	result = ''
	for id in range(len(pos_list)):
		state = pos_list[id]
		if state == 'B':
			result +=test_str[id]
		elif state == 'M':
			result += test_str[id]
		elif state == 'E':
			result += test_str[id]+'/'
		else:
			result += test_str[id] + '/'
	print(result)



