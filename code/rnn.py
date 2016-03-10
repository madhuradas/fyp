import numpy as np
import pickle 

class RNN:
	def __init__(self,hidden_size,):
		pass

	def minimize(self,):
		pass

	def train(self,):
		pass

	def predict(self,):
		pass

	def evaluate(self,):
		pass

	def save(self,filename):
		'''
		Save model to a file
		'''
		pickle.dump(self,open(filename,'wb'))

	def load(self,filename):
		'''
		Load model from file
		'''
		return pickle.load(open(filename))


if __name__ == '__main__':
	rnn = RNN()
	pass