from encoder_decoder import *
import pickle
import sys
import time

def train(model_file):
    enc_dec = encoder_decoder(len(first_word_to_ix.keys()), 30, 100, len(vocab_to_ix.keys()), 30, 100)
    enc_dec.train(inputs, targets, 15, vocab_to_ix, first_word_to_ix, model_q)
    enc_dec.save('../../../data/' + model_file)

def test(model_file):
    enc_dec = load('../../../data/' + model_file)
    classes = open('../create_dataset/classes_obj.txt').read().split(';')
    # del classes[classes.index('other')]
    # del classes[classes.index('people')]
    obj = eval(open("../create_dataset/objects.txt").read())
    c = 0
    for i in range(len(classes)):
        print 'Class : ', classes[i] #eval(open('ques.txt').read()).values()[500]
        print 'Object : ', obj[i]
        ques = enc_dec.predict_question([model_cls[classes[i]]], ix_to_first_word, ix_to_vocab, model_q)
        print ques
        #time.sleep(2)
        #pdb.set_trace()
        if classes[i] == 'clothing' and ques == 'What is the person in the image wearing ?':
            c += 1
        elif classes[i] in ques.split(' '):
            c += 1
        elif classes[i] == "vehicles" and "vehicle(s)" in ques.split(' '):
             c+=1
        elif classes[i] == "instruments" and "instrument(s)" in ques.split(' '):
            c+=1
        elif classes[i] == 'other' and ques == 'Which of the following is present in the image ?':
            c += 1
    print  c
    print 'Accuracy : ', (c/float(len(classes))) * 100

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print "Run script as : "
        print "[1] python train_test.py train model_file"
        print "[2] python train_test.py test model_file"
        exit()
    inputs = pickle.load(open('../../../data/enc_dec_inputs.pickle'))
    targets = pickle.load(open('../../../data/enc_dec_targets.pickle'))
    ix_to_first_word = pickle.load(open('../../../data/ix_to_first_word.pickle'))
    first_word_to_ix = pickle.load(open('../../../data/first_word_to_ix.pickle'))
    vocab_to_ix = pickle.load(open('../../../data/vocab_to_ix.pickle'))
    ix_to_vocab = pickle.load(open('../../../data/ix_to_vocab.pickle'))
    model_q = pickle.load(open('../../../data/questions.pickle'))
    model_cls = pickle.load(open('../../../data/classes_obj.pickle'))
    if sys.argv[1] == "train":
        train(sys.argv[2])
    if sys.argv[1] == "test":
        test(sys.argv[2])
