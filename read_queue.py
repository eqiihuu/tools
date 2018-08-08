import sys
import tensorflow as tf


# Test on simple floats
'''
q = tf.FIFOQueue(4, "float")
init = q.enqueue_many(([0.1, 0.2, 0.3, 0.4],))
x = q.dequeue()
y = x + 1
q_inc = q.enqueue([y])

with tf.Session() as sess:
    sess.run(init)
    for i in range(2):
        sess.run(q_inc)
    quelen = sess.run(q.size())
    for i in range(quelen):
        print (sess.run(q.dequeue()))
'''

# Test on complicated floats
'''
num_thread = 1
len_queue = 5
x_input_data = tf.random_normal([2], mean=-1, stddev=4)
q = tf.FIFOQueue(len_queue,"float")

x_input_data = tf.Print(x_input_data, data=[x_input_data], message="Raw inputs data generated:", summarize=6)
enqueue_op = q.enqueue_many(x_input_data)  # add to queue
qr = tf.train.QueueRunner(q,enqueue_ops=[enqueue_op]*num_thread)  # QueueRunner
tf.train.add_queue_runner(qr)

input = q.dequeue()
input = tf.Print(input, data=[q.size(), input], message="No elements left, input:")

# fake graph
y = input + 1

sess = tf.Session()
coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(coord=coord, sess=sess)  # start input threads

for i in range(10):
    print("----------------------:")
    print(sess.run(y))

coord.request_stop()
coord.join(threads)

sess.close()
'''