from encoder_decoder import *
import pickle

inputs = pickle.load(open('enc_dec_inputs.p'))
targets = pickle.load(open('enc_dec_targets.p'))

ix_to_first_word = pickle.load(open('ix_to_first_word.p'))
first_word_to_ix = pickle.load(open('first_word_to_ix.p'))
vocab_to_ix = pickle.load(open('vocab_to_ix.p'))
ix_to_vocab = pickle.load(open('ix_to_vocab.p'))
model_q = pickle.load(open('ques.p'))


encoder_decoder = encoder_decoder(len(first_word_to_ix.keys()), 30, 100, len(vocab_to_ix.keys()), 30, 100)
encoder_decoder.train(inputs, targets, vocab_to_ix, first_word_to_ix, model_q)

encoder_decoder.save('trained.p')
