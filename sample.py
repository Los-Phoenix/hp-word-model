from __future__ import print_function
import numpy as np 
import tensorflow as tf 

import argparse 
import time 
import os 
from six.moves import cPickle 

from loader import TextLoader 
from model import Model 

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--save_dir', type=str, default='save',
						help='model directory to store checkpointed models')
	parser.add_argument('-n', type=int, default=5000,
                        help='number of words to sample')
	parser.add_argument('--prime', type=str, default='Harry ',
						help='prime text')
	args = parser.parse_args()
	sample(args)

def sample(args):
	with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
		saved_args = cPickle.load(f)
	with open(os.path.join(args.save_dir, 'words_vocab.pkl'), 'rb') as f:
		words, vocab = cPickle.load(f)
	model = Model(saved_args, True)
	with tf.Session() as sess:
		tf.initialize_all_variables().run()
		saver = tf.train.Saver(tf.all_variables())
		ckpt = tf.train.get_checkpoint_state(args.save_dir)
		if ckpt and ckpt.model_checkpoint_path:
			saver.restore(sess, ckpt.model_checkpoint_path)
			sample = model.sample(sess, words, vocab, args.n, args.prime)
			# with open('sample.txt', 'w+') as f:
			# 	f.write(sample)
			print(sample)

if __name__ == '__main__':
	main()

	