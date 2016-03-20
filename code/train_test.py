from encoder_decoder import *
import pickle

inputs = pickle.load(open('enc_dec_inputs.p'))
targets = pickle.load(open('enc_dec_targets.p'))

ix_to_first_word = pickle.load(open('ix_to_first_word.p'))
first_word_to_ix = pickle.load(open('first_word_to_ix.p'))
vocab_to_ix = pickle.load(open('vocab_to_ix.p'))
ix_to_vocab = pickle.load(open('ix_to_vocab.p'))
model_q = pickle.load(open('ques.p'))
model_cls = pickle.load(open('class.p'))

# enc_dec = encoder_decoder(len(first_word_to_ix.keys()), 30, 100, len(vocab_to_ix.keys()), 30, 100)
# enc_dec.train(inputs, targets, 15, vocab_to_ix, first_word_to_ix, model_q)

# enc_dec.save('trained.p')

enc_dec = load('trained.p')
classes = open('classes.txt').read().split(';')
c = 0
for cls in classes:
    print 'Class : ', cls #eval(open('ques.txt').read()).values()[500]
    ques = enc_dec.predict_question([model_cls[cls]], ix_to_first_word, ix_to_vocab, model_q)
    print ques
	#pdb.set_trace()
    if cls in ques.split(' '):
        c += 1
print 'Accuracy : ', (c/float(len(classes))) * 100
