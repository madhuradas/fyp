import numpy as np
import pickle

def load(filename):
        '''
        Load model from file
        '''
        return pickle.load(open(filename))

class RNN(object):
    def __init__(self, output_dim, input_dim, hidden_size, learning_rate=1e-1, hidden_layers=1):
        '''
        Initialise the model parameters and hyper parameters
        '''
        # set the input and output shape
        self.input_dim = input_dim
        self.output_dim = output_dim

        # hyperparameters
        # hidden_layers yet to be implemented
        self.hidden_size = hidden_size  # size of hidden layer of neurons
        self.learning_rate = learning_rate  # learning rate, alpha

        # model parameters
        self.Wxh = np.random.randn(self.hidden_size, self.input_dim) * 0.01  # input to hidden
        self.Whh = np.random.randn(self.hidden_size, self.hidden_size) * 0.01  # hidden to hidden
        self.Why = np.random.randn(self.output_dim, self.hidden_size) * 0.01  # hidden to output
        self.bh = np.zeros((self.hidden_size, 1))  # hidden bias
        self.by = np.zeros((self.output_dim, 1))  # output bias

    def _minimize_loss(self, weights_derivatives_mem):
        '''
        Perform parameter update with Adagrad
        '''
        for (param, dparam, mem) in weights_derivatives_mem:
            mem += dparam * dparam
            param += -self.learning_rate * dparam / np.sqrt(mem + 1e-8)  # adagrad update

    def _BPTT(self, X, y, hprev):
        '''
        X : training example
        y : the output label
        hprev : Hx1 array of initial hidden state
        returns the loss, gradients on model parameters, and last hidden state
        '''
        xs, hs, ys, ps = {}, {}, {}, {}
        hs[-1] = np.copy(hprev)
        loss = 0
        # forward pass
        # range creates a list in memory whereas xrange is a sequence object that evaluates lazily
        for t in xrange(len(X)):
            xs[t] = np.zeros((self.input_dim, 1))  # encode in 1-of-k representation
            xs[t][X[t]] = 1
            hs[t] = np.tanh(np.dot(self.Wxh, xs[t]) + np.dot(self.Whh, hs[t - 1]) + self.bh)  # hidden state
            ys[t] = np.dot(self.Why, hs[t]) + self.by  # unnormalized log probabilities for next chars
            ps[t] = np.exp(ys[t]) / np.sum(np.exp(ys[t]))  # probabilities for next chars
            loss += -np.log(ps[t][y[t], 0])  # softmax (cross-entropy loss)
            # backward pass: compute gradients going backwards
            dWxh, dWhh, dWhy = np.zeros_like(self.Wxh), np.zeros_like(self.Whh), np.zeros_like(self.Why)
            dbh, dby = np.zeros_like(self.bh), np.zeros_like(self.by)
            dhnext = np.zeros_like(hs[0])
        for t in reversed(xrange(len(X))):
            dy = np.copy(ps[t])
            dy[y[t]] -= 1  # backprop into y
            dWhy += np.dot(dy, hs[t].T)
            dby += dy
            dh = np.dot(self.Why.T, dy) + dhnext  # backprop into h
            dhraw = (1 - hs[t] * hs[t]) * dh  # backprop through tanh nonlinearity
            dbh += dhraw
            dWxh += np.dot(dhraw, xs[t].T)

        dWhh += np.dot(dhraw, hs[t - 1].T)
        dhnext = np.dot(self.Whh.T, dhraw)
        for dparam in [dWxh, dWhh, dWhy, dbh, dby]:
            np.clip(dparam, -5, 5, out=dparam)  # clip to mitigate exploding gradients
        return loss, dWxh, dWhh, dWhy, dbh, dby, hs[len(X) - 1]


    def train(self, inputs, targets, seq_len, num_epochs):
        '''
        Invoke BPTT for num_epochs
        '''
        mWxh, mWhh, mWhy = np.zeros_like(self.Wxh), np.zeros_like(self.Whh), np.zeros_like(self.Why)
        mbh, mby = np.zeros_like(self.bh), np.zeros_like(self.by)  # memory variables for Adagrad
        smooth_loss = -np.log(1.0 / self.output_dim) * seq_len  # loss at iteration 0 (not sure if it should be self.input_dim)
        for i in xrange(num_epochs):
            hprev = np.zeros((self.hidden_size, 1))  # reset RNN memory every epoch
            for j in xrange(len(inputs)):
                # forward seq_length characters through the net and fetch gradient
                loss, dWxh, dWhh, dWhy, dbh, dby, hprev = self._BPTT(inputs[j], targets[j], hprev)
                smooth_loss = smooth_loss * 0.999 + loss * 0.001
                if i % 100 == 0:
                    print 'epoch %d, loss: %f' % (i, smooth_loss)  # print progress

                # minimize the loss by calling adagrad update
                weights_derivatives_mem = zip([self.Wxh, self.Whh, self.Why, self.bh, self.by],
                                              [dWxh, dWhh, dWhy, dbh, dby], [mWxh, mWhh, mWhy, mbh, mby])
                self._minimize_loss(weights_derivatives_mem)


    def predict(self, X, hprev=None):
        '''
        Given an input sequence, predict the output
        X : input sequence
        return output label/sequence
        '''
        if hprev is None:
            hprev = np.zeros((self.hidden_size, 1))
        xs, hs, ys, ps = {}, {}, {}, {}
        hs[-1] = np.copy(hprev)
        for t in xrange(len(X)):
            xs[t] = np.zeros((self.input_dim, 1))  # encode in 1-of-k representation
            xs[t][X[t]] = 1
            hs[t] = np.tanh(np.dot(self.Wxh, xs[t]) + np.dot(self.Whh, hs[t - 1]) + self.bh)  # hidden state
            ys[t] = np.dot(self.Why, hs[t]) + self.by  # unnormalized log probabilities
            ps[t] = np.exp(ys[t]) / np.sum(np.exp(ys[t]))
        return ps[len(X) - 1], hs[len(X) - 1]


    def evaluate(self, test_inputs, test_outputs):
        '''
        Emit a score depending on the number of correct predictions
        '''
        pass


    def save(self, filename):
        '''
        Save model to a file
        '''
        pickle.dump(self, open(filename, 'wb'))



if __name__ == '__main__':
    data = open('input.txt', 'r').read()  # should be simple plain text file
    chars = list(set(data))
    data_size, vocab_size = len(data), len(chars)
    print 'data has %d characters, %d unique.' % (data_size, vocab_size)
    char_to_ix = {ch: i for i, ch in enumerate(chars)}
    ix_to_char = {i: ch for i, ch in enumerate(chars)}
    rnn = RNN(vocab_size, vocab_size, 100)
    seq_length = 25
    # prepare the training data
    p = 0
    inputs = [[char_to_ix[ch] for ch in data[p:p + seq_length]] for p in range(len(data) - seq_length - 1)]
    targets = [[char_to_ix[ch] for ch in data[p + 1:p + seq_length + 1]] for p in range(len(data) - seq_length - 1)]
    # print inputs[0]
    # rnn.train(inputs, targets, seq_length, 1000)
    print 'Finished training'
    # rnn.save('char-rnn.p')
    rnn = load('char-rnn.p')
    test_input = [char_to_ix[ch] for ch in 'hey there! ']
    probs = rnn.predict(test_input)[0][0:,0].tolist()  # gives list of probabilities
    # import pdb;pdb.set_trace()
    print 'Prediction : ', chars[probs.index(max(probs))]