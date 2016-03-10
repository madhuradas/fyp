import numpy as np
import pickle 

class RNN(object):
	def __init__(self,output_dim,input_dim,hidden_size,learning_rate=1e-1,hidden_layers=1):
		'''
		Initialise the model parameters and hyper parameters
		'''
		# set the input and output shape
		self.input_dim = input_dim
		self.output_dim = output_dim

		# hyperparameters 
		# hidden_layers yet to be implemented
		self.hidden_size = hidden_size # size of hidden layer of neurons
		self.learning_rate = learning_rate # learning rate, alpha

		# model parameters
		self.Wxh = np.random.randn(self.hidden_size, self.input_dim) * 0.01 # input to hidden
		self.Whh = np.random.randn(self.hidden_size, self.hidden_size) * 0.01 # hidden to hidden
		self.Why = np.random.randn(self.output_dim, self.hidden_size) * 0.01 # hidden to output
		self.bh = np.zeros((self.hidden_size, 1)) # hidden bias
		self.by = np.zeros((self.output_dim, 1)) # output bias

	def minimize_loss(self,):
		pass

	def loss(self,):
		pass

	def train(self,inputs,targets,hprev,seq_len):
		# range creates a list in memory
		# xrange is a sequence object that evaluates lazily
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