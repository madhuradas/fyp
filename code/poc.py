from rnn import *
import numpy as np
import sys

inputs_targets = zip(*eval(open('inputs_targets.txt').read()))
inputs = inputs_targets[0]
targets = inputs_targets[1]

# print inputs, targets
class_to_ix = {cls: i for i, cls in enumerate(inputs)}
ques_to_ix = {ques: i for i,ques in enumerate(targets)}
ix_to_ques = {i: ques for i, ques in enumerate(targets)}

train_inps = [[class_to_ix[i]] for i in inputs]
train_outs = [[ques_to_ix[i]] for i in targets]

rnn = RNN(5,5,100)

rnn.train(train_inps,train_outs,1,1000)

print 'Finished training'

test_input = [class_to_ix[sys.argv[1]]]
probs = rnn.predict(test_input)[0][0:,0].tolist()  # gives list of probabilities
# import pdb;pdb.set_trace()
print 'Question Generated : ', targets[probs.index(max(probs))]