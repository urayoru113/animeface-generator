import tensorflow as tf
import numpy as np

from dcgan import DCGAN


batch_size = 8


dcgan = DCGAN(s_size=6, batch_size=batch_size)
images = dcgan.sample_images(1, 1)
save_dir = './model'

with tf.Session() as sess:
    saver = tf.train.Saver()
    saver.restore(sess, save_dir + '/model.ckpt')

    generated = sess.run(images)
    with open('test.jpg', 'wb') as f:
        f.write(generated)