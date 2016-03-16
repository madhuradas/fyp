from rnn import *
from gensim.models import Word2Vec


class encoder_decoder:
	def __init__(self, enc_output_dim, enc_input_dim, enc_hidden_size, dec_output_dim, dec_input_dim, dec_hidden_size):
		self.encoder = RNN(enc_output_dim,enc_input_dim,enc_hidden_size)
		self.decoder = RNN(dec_output_dim,dec_input_dim,dec_hidden_size)

	def _minimize_loss(self, weights_derivatives_mem):
        '''
        Perform parameter update with Adagrad
        '''
        for (param, dparam, mem) in weights_derivatives_mem:
            mem += dparam * dparam
            param += -self.learning_rate * dparam / np.sqrt(mem + 1e-8)

	def train(self, inputs, targets, num_epochs):
        '''
        Invoke BPTT for num_epochs
        '''
        enc_mWxh, enc_mWhh, enc_mWhy = np.zeros_like(self.encoder.Wxh), np.zeros_like(self.encoder.Whh), np.zeros_like(self.encoder.Why)
        enc_mbh, enc_mby = np.zeros_like(self.encoder.bh), np.zeros_like(self.encoder.by)  # memory variables for Adagrad
        dec_mWxh, dec_mWhh, dec_mWhy = np.zeros_like(self.decoder.Wxh), np.zeros_like(self.decoder.Whh), np.zeros_like(self.decoder.Why)
        dec_mbh, dec_mby = np.zeros_like(self.decoder.bh), np.zeros_like(self.decoder.by)  # memory variables for Adagrad
        dec_smooth_loss = -np.log(1.0 / self.decoder.output_dim) * self.decoder.input_dim # loss at iteration 0 (not sure if it should be self.input_dim)
        enc_smooth_loss = -np.log(1.0 / self.encoder.output_dim) * self.encoder.input_dim
        for i in xrange(num_epochs):
            hprev = np.zeros((self.hidden_size, 1))  # reset RNN memory every epoch
            for j in xrange(len(inputs)):
                # Encoder forward pass
                enc_hprev, enc_ps = self.encoder.BPTT(inputs[j], targets[j], hprev, True)
                #smooth_loss = smooth_loss * 0.999 + loss * 0.001

                #Decoder Forward pass
                dec_hprev, dec_ps = self.decoder.BPTT(inputs[j], targets[j], enc_hprev, True)
                #Decoder Back pass
                dec_loss, dec_dWxh, dec_dWhh, dec_dWhy, dec_dbh, dec_dby, dec_hprev = self.decoder.BPTT(inputs[j], targets[j], dec_hprev)

                # minimize the loss for deocder
                dec_weights_derivatives_mem = zip([self.decoder.Wxh, self.decoder.Whh, self.decoder.Why, self.decoder.bh, self.decoder.by],
                                              [dec_dWxh, dec_dWhh, dec_dWhy, dec_dbh, dec_dby], [dec_mWxh, dec_mWhh, dec_mWhy, dec_mbh, dec_mby])
                self._minimize_loss(dec_weights_derivatives_mem)
                dec_smooth_loss = dec_smooth_loss * 0.999 + dec_loss * 0.001
                print 'epoch %d, DECODER loss: %f' % (i, dec_smooth_loss)  # print progress

                #Encoder Back pass
                enc_loss, enc_dWxh, enc_dWhh, enc_dWhy, enc_dbh, enc_dby, enc_hprev = self.encoder.BPTT(inputs[j], targets[j], enc_hprev)

                # minimize the loss for deocder
                enc_weights_derivatives_mem = zip([self.encoder.Wxh, self.encoder.Whh, self.encoder.Why, self.encoder.bh, self.encoder.by],
                                              [enc_dWxh, enc_dWhh, enc_dWhy, enc_dbh, enc_dby], [enc_mWxh, enc_mWhh, enc_mWhy, enc_mbh, enc_mby])
                self._minimize_loss(enc_weights_derivatives_mem)
                enc_smooth_loss = enc_smooth_loss * 0.999 + enc_loss * 0.001
                print 'epoch %d, ENCODER loss: %f' % (i, enc_smooth_loss)  # print progress

    def predict_question(self, X, ix_to_first_word):
        '''
        Given an input sequence, predict the output
        X : input sequence
        return output label/sequence
        '''
        ps,hs = self.encoder.predict(X)
        word = ix_to_first_word[ps.values().index(max(ps.values()))] 
        model = pickle.load(open('ques.p'))
        while (word != '?'):
            print word, " ",
            ps, hs = self.decoder.predict(model[word],hs)
            word = ix_to_first_word[ps.values().index(max(ps.values()))] 
        print word ,"\n"
        
        # if hprev is None:
        #     hprev = np.zeros((self.hidden_size, 1))
        # xs, hs, ys, ps = {}, {}, {}, {}
        # hs[-1] = np.copy(hprev)
        # for t in xrange(len(X)):
        #     xs[t] = np.reshape(X[t],(self.input_dim,1)) # encode in 1-of-k representation
        #     hs[t] = np.tanh(np.dot(self.Wxh, xs[t]) + np.dot(self.Whh, hs[t - 1]) + self.bh)  # hidden state
        #     ys[t] = np.dot(self.Why, hs[t]) + self.by  # unnormalized log probabilities
        #     ps[t] = np.exp(ys[t]) / np.sum(np.exp(ys[t]))
        # return ps[len(X) - 1], hs[len(X) - 1]
                
                