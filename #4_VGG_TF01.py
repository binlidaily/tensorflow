
# coding: utf-8

# <a href="https://colab.research.google.com/github/binlidaily/tensorflow/blob/master/%234_VGG_TF.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# In[ ]:


# !ls tensorflow


# In[ ]:


# !git clone https://binlidaily:520134lin@github.com/binlidaily/tensorflow.git
# !ls tensorflow


# In[2]:


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import data
from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf
import numpy as np
# import keras
# mnist = keras.datasets.mnist
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings("ignore",category=DeprecationWarning)

# mnist = input_data.read_data_sets('data/', one_hot=True)   # 读取数据集 这个 one_hot=True 要慎重选啊
mnist = input_data.read_data_sets('./data/', reshape=False)   # 读取数据集


# In[3]:


# 读取训练数据及测试数据
train_data, train_label = mnist.train.images, mnist.train.labels
test_data, test_label = mnist.test.images, mnist.test.labels

# 打乱训练数据及测试数据
n_train = len(train_data)
i_train = range(n_train)
np.random.shuffle(i_train)
train_data = train_data[i_train]

n_test = len(test_data)
i_test = range(n_test)
np.random.shuffle(i_test)
test_data = test_data[i_test]

print(np.shape(train_data), np.shape(test_data))


# In[4]:


w, h, c = 28, 28, 1

x = tf.placeholder(tf.float32, [None, w, h, c], name='x')
y_ = tf.placeholder(tf.int32, [None], name='y_')


# In[5]:


def build_network(input_tensor, regularizer, is_train=True):
    # 第一层：输入层 本来是 224x224x3, 现在是 28x28x1，卷积层的大小都是 3

    with tf.variable_scope('layer1-conv12'):
        # 28x28x1 -> 28x28x64
        print('layer1-conv12')
        print(input_tensor.get_shape())
        conv1_weights = tf.get_variable('weight1', [3, 3, c, 64], initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv1_bias = tf.get_variable('bias1', [64], initializer=tf.constant_initializer(0.0))
        conv1 = tf.nn.conv2d(input_tensor, conv1_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu1 = tf.nn.relu(tf.nn.bias_add(conv1, conv1_bias))

        print(relu1.get_shape())
        # 28x28x64 -> 28x28x64
        conv2_weights = tf.get_variable('weight2', [3, 3, 64, 64], initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv2_bias = tf.get_variable('bias2', [64], initializer=tf.constant_initializer(0.0))
        conv2 = tf.nn.conv2d(relu1, conv2_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu2 = tf.nn.relu(tf.nn.bias_add(conv2, conv2_bias))

    # 28x28x64 -> 14x14x64
    with tf.variable_scope('layer2-pool1'):
        print('layer2-pool1')
        print(relu2.get_shape())
        pool1 = tf.nn.max_pool(relu2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    with tf.variable_scope('layer3-conv34'):
        # 14x14x64 -> 14x14x128
        print('layer3-conv34')
        print(pool1.get_shape())
        conv3_weights = tf.get_variable('weight3', [3, 3, 64, 128], initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv3_bias = tf.get_variable('bias3', [128], initializer=tf.constant_initializer(0.0))
        conv3 = tf.nn.conv2d(pool1, conv3_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu3 = tf.nn.relu(tf.nn.bias_add(conv3, conv3_bias))

        # 14x14x128 -> 14x14x128
        print(relu3.get_shape())
        conv4_weights = tf.get_variable('weight4', [3, 3, 128, 128], initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv4_bias = tf.get_variable('bias4', [128], initializer=tf.constant_initializer(0.0))
        conv4 = tf.nn.conv2d(relu3, conv4_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu4 = tf.nn.relu(tf.nn.bias_add(conv4, conv4_bias)) 

    # 14x14x128 -> 7x7x128
    with tf.variable_scope('layer4-pool2'):
        print('layer4-pool2')
        print(relu4.get_shape())
        pool2 = tf.nn.max_pool(relu4, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    with tf.variable_scope('layer5-conv56'):
        # 7x7x128 -> 7x7x256
        print('layer5-conv56')
        print(pool2.get_shape())
        conv5_weights = tf.get_variable('weight5', [3, 3, 128, 256], initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv5_bias = tf.get_variable('bias5', [256], initializer=tf.constant_initializer(0.0))
        conv5 = tf.nn.conv2d(pool2, conv5_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu5 = tf.nn.relu(tf.nn.bias_add(conv5, conv5_bias))

        # 7x7x256 -> 7x7x256
        print(relu5.get_shape())
        conv6_weights = tf.get_variable('weight6', [3, 3, 256, 256], initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv6_bias = tf.get_variable('bias6', [256], initializer=tf.constant_initializer(0.0))
        conv6 = tf.nn.conv2d(relu5, conv6_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu6 = tf.nn.relu(tf.nn.bias_add(conv6, conv6_bias)) 

    with tf.variable_scope('layer6-pool3'):
        # 7x7x256 -> 4x4x256
        print('layer6-pool3')
        print(relu6.get_shape())
        pool3 = tf.nn.max_pool(relu6, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    with tf.variable_scope('layer7-conv78'):
        # 4x4x256 -> 4x4x512
        print('layer7-conv78')
        print(pool3.get_shape())
        conv7_weights = tf.get_variable('weight7', [3, 3, 256, 512], initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv7_bias = tf.get_variable('bias7', [512], initializer=tf.constant_initializer(0.0))
        conv7 = tf.nn.conv2d(pool3, conv7_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu7 = tf.nn.relu(tf.nn.bias_add(conv7, conv7_bias))

        # 4x4x512 -> 4x4x512
        print(relu7.get_shape())
        conv8_weights = tf.get_variable('weight8', [3, 3, 512, 512], initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv8_bias = tf.get_variable('bias8', [512], initializer=tf.constant_initializer(0.0))
        conv8 = tf.nn.conv2d(relu7, conv8_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu8 = tf.nn.relu(tf.nn.bias_add(conv8, conv8_bias)) 

    # 4x4x512 -> 2x2x512
    with tf.variable_scope('layer8-pool4'):
        print('layer8-pool4')
        print(relu8.get_shape())
        pool4 = tf.nn.max_pool(relu8, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    with tf.variable_scope('layer9-conv910'):
        # 2x2x512 -> 2x2x512
        print('layer9-conv910')
        print(pool4.get_shape())
        conv9_weights = tf.get_variable('weight9', [3, 3, 512, 512], initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv9_bias = tf.get_variable('bias9', [512], initializer=tf.constant_initializer(0.0))
        conv9 = tf.nn.conv2d(pool4, conv9_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu9 = tf.nn.relu(tf.nn.bias_add(conv9, conv9_bias))

        # 2x2x512 -> 2x2x512
        print(relu9.get_shape())
        conv10_weights = tf.get_variable('weight10', [3, 3, 512, 512], initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv10_bias = tf.get_variable('bias10', [512], initializer=tf.constant_initializer(0.0))
        conv10 = tf.nn.conv2d(relu9, conv10_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu10 = tf.nn.relu(tf.nn.bias_add(conv10, conv10_bias)) 

    # 2x2x512 -> 1x1x512
    with tf.variable_scope('layer10-pool5'):
        print('layer10-pool5')
        print(relu10.get_shape())
        pool5 = tf.nn.max_pool(relu10, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    print(pool5.get_shape())
    pool_shape = pool5.get_shape().as_list()
    print(pool_shape)
    print(len(pool_shape))
    n_nodes = pool_shape[1] * pool_shape[2] * pool_shape[3]
    pool5_reshaped = tf.reshape(pool5, [-1, n_nodes])
  #   n_nodes = 1
  #   pool5_reshaped = tf.contrib.layers.flatten(pool5)

    with tf.variable_scope('layer11-fc1'):
        print('layer11-fc1')
        print(pool5_reshaped.get_shape())

        fc1_weights = tf.get_variable('weight', [n_nodes, 4096], initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer is not None:
            tf.add_to_collection('losses', regularizer(fc1_weights))
        fc1_biases = tf.get_variable('bias', [4096], initializer=tf.constant_initializer(0.1))
        fc1 = tf.nn.relu(tf.matmul(pool5_reshaped, fc1_weights) + fc1_biases)
        if is_train:
            fc1 = tf.nn.dropout(fc1, 0.5)

    with tf.variable_scope('layer12-fc2'):
        fc2_weights = tf.get_variable('weight', [4096, 4096], initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer is not None:
            tf.add_to_collection('losses', regularizer(fc2_weights))
        fc2_biases = tf.get_variable('bias', [4096], initializer=tf.constant_initializer(0.1))
        fc2 = tf.nn.relu(tf.matmul(fc1, fc2_weights) + fc2_biases)
        if is_train:
            fc2 = tf.nn.dropout(fc2, 0.5)

    with tf.variable_scope('layer13-fc3'):
        fc3_weights = tf.get_variable('weight', [4096, 10], initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer is not None:
            tf.add_to_collection('losses', regularizer(fc3_weights))
        fc3_biases = tf.get_variable('bias', [10], initializer=tf.constant_initializer(0.1))
        logit = tf.matmul(fc2, fc3_weights) + fc3_biases

    return logit


# In[6]:


regularizer = tf.contrib.layers.l2_regularizer(0.001)
y = build_network(x, regularizer, False)
cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=y_)
cross_entropy_mean = tf.reduce_mean(cross_entropy)
loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))

train_op = tf.train.AdamOptimizer(0.001).minimize(loss)
correct_prediction = tf.equal(tf.cast(tf.argmax(y, 1), tf.int32), y_)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


# In[7]:


def get_batch(data, label, batch_size):
    for start_idx in range(0, len(data) - batch_size + 1, batch_size):
        slice_idx = slice(start_idx, start_idx + batch_size)
        yield data[slice_idx], label[slice_idx]


# In[ ]:


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    train_num = 10
    batch_size = 64
  
    for i in range(train_num):
      train_loss, train_acc, batch_num = 0, 0, 0
      for train_data_batch, train_label_batch in get_batch(train_data, train_label, batch_size):
          _, err, acc = sess.run([train_op, loss, accuracy], feed_dict={
              x: train_data_batch, y_: train_label_batch
          })
          train_loss += err
          train_acc += acc
          batch_num += 1
          if batch_num % 64 == 0:
            print('batch_num', batch_num)
      print('training loss:', train_loss / batch_num)
      print('train accuracy:', train_acc / batch_num)

      test_loss, test_acc, batch_num = 0, 0, 0
      for test_data_batch, test_label_batch in get_batch(test_data, test_label, batch_size):
          err, acc = sess.run([loss, accuracy], feed_dict={
              x: test_data_batch, y_: test_label_batch
          })
          test_loss += err
          test_acc += acc
          batch_num += 1

      print('testing loss:', test_loss / batch_num)
      print('testing accuracy:', test_acc / batch_num)


# In[ ]:





# In[ ]:




