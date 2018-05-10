import tensorflow as tf
import numpy as np
import cv2
import os
from dcgan import DCGAN
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

save_dir = './model_yan'
batch_size = 128
dcgan = DCGAN(s_size=6, batch_size=batch_size)
sample_z = np.random.uniform(-1, 1, [dcgan.batch_size, dcgan.z_dim])
sample_z = np.float32(sample_z)
images = dcgan.sample_images(5, 5, sample_z)

with tf.Session() as sess:
    if os.path.isdir(save_dir + '/g_model'):
        saver = tf.train.Saver(dcgan.g.variables)
        saver.restore(sess, tf.train.latest_checkpoint(save_dir + '/g_model'))
    else:
        print("fold %s does not exists" % save_dir)
        os._exit(1)

    generated = sess.run(images)
    with open('test.jpg', 'wb') as f:
        f.write(generated)

