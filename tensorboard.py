'''
主要是讲解 :
tensorboard的可视化结构

    1. name_scope的用法 用于绘制Tensorboard 中的graph

    2. write=tf.summary.FileWriter("logs/",sess.graph)
'''


import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data", one_hot=True)

batch_size = 100  # 可优化
n_batch = int(mnist.train.num_examples/batch_size)

with tf.name_scope("input"):
    x = tf.placeholder(tf.float32, [None, 784],name="x-input")
    y = tf.placeholder(tf.float32, [None, 10] ,name="y-input")

# 创建简单神经网络（可优化）
with tf.name_scope("layer"):
    with tf.name_scope("wights"):
        W = tf.Variable(tf.zeros([784, 10]),name="W")
    with tf.name_scope("biases"):
        b = tf.Variable(tf.zeros([10]),name="b")
    with tf.name_scope("wx_plus_b"):
        wx_plus_b=tf.matmul(x, W) + b
    with tf.name_scope("predict"):
        predict = tf.nn.softmax(wx_plus_b)  # softmax将输出信号转化为概率值（10个概率值）



# 可使用交叉熵代价函数来优化
with tf.name_scope("loss"):
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y,logits=predict))
# 使用梯度下降法训练，使得loss最小（#可优化）
with tf.name_scope("train"):
    train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)





with tf.name_scope("accuracy"):
    # 比较概率最大的标签是否相同，结果存放在一个布尔型列表中
    with tf.name_scope("correct_predict"):
        correct_predict = tf.equal(tf.argmax(y, 1), tf.argmax(predict, 1))  # argmax返回一维张量中最大值所在的位置
    # 求准确率
    with tf.name_scope("accu"):
        accuracy = tf.reduce_mean(tf.cast(correct_predict, tf.float32))  # reduce_mean求平均值



with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    write=tf.summary.FileWriter("logs/",sess.graph)

    for epoch in range(1):  # 可优化
        for batch in range(n_batch):  # 把所有图片训练一次
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            sess.run(train_step, feed_dict={x: batch_xs, y: batch_ys})
        # 用测试数据来检验训练好的模型
        acc = sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels})
        print("Iter " + str(epoch) + "Test accuracy" + str(acc))


