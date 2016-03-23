from encoder_decoder import *
import pickle
import sys

def train():
	enc_dec = encoder_decoder(len(first_word_to_ix.keys()), 30, 100, len(vocab_to_ix.keys()), 30, 100)
	enc_dec.train(inputs, targets, 15, vocab_to_ix, first_word_to_ix, model_q)
	enc_dec.save('../../../data/trained.pickle')

def test():
	enc_dec = load('../../../data/trained.pickle')
	classes = open('../create_dataset/classes.txt').read().split(';')
	c = 0
	for cls in classes:
	    print 'Class : ', cls #eval(open('ques.txt').read()).values()[500]
	    ques = enc_dec.predict_question([model_cls[cls]], ix_to_first_word, ix_to_vocab, model_q)
	    print ques
		#pdb.set_trace()
	    if cls in ques.split(' '):
	        c += 1
	    if cls=='other' and ques == 'Which of the following is present in the image ?':
	    	c += 1
	print 'Accuracy : ', (c/float(len(classes))) * 100

if __name__ == "__main__":

	if len(sys.argv) == 1:
		print "Pass argument : train or test"
		exit()
	inputs = pickle.load(open('../../../data/enc_dec_inputs.pickle'))
	targets = pickle.load(open('../../../data/enc_dec_targets.pickle'))
	ix_to_first_word = pickle.load(open('../../../data/ix_to_first_word.pickle'))
	first_word_to_ix = pickle.load(open('../../../data/first_word_to_ix.pickle'))
	vocab_to_ix = pickle.load(open('../../../data/vocab_to_ix.pickle'))
	ix_to_vocab = pickle.load(open('../../../data/ix_to_vocab.pickle'))
	model_q = pickle.load(open('../../../data/questions.pickle'))
	model_cls = pickle.load(open('../../../data/classes.pickle'))
	if sys.argv[1] == "train":
		train()
	if sys.argv[1] == "test":
		test()
