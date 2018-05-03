import tensorflow as tf
import numpy as np
import os
import cv2
from dcgan import DCGAN

epochs = 1000
batch_size = 8
image_size = 96
save_dir = './model'
def load_image(filepath='./image'):
    dataset = []
    if not os.path.isdir(filepath):
        print(filepath + " is not existing")
        return 1
    for f in os.listdir(filepath):
        if f.endswith('.jpg'):
            im = cv2.imread(filepath + "/" + f, cv2.IMREAD_COLOR)
            im = cv2.resize(im, (image_size, image_size))
            #cv2.imshow("image", im)
            #cv2.waitKey(0)
        dataset.append(im)
    dataset = np.array(dataset, dtype=np.float32)
    return dataset

def get_batch(data, index, size = 1):
    return data[index:index+size]

def main():
    
    dcgan = DCGAN(s_size=6, batch_size=batch_size)
    train_im = load_image()
    losses = dcgan.loss(train_im)
    train_op = dcgan.train(losses)
    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        saver = tf.train.Saver()
        if os.path.isdir(save_dir):
            saver.restore(sess, save_dir + '/model.ckpt')
        else:
            sess.run(init)
            
            
        for step in range(epochs):
            _, g_loss, d_loss = sess.run([train_op, losses[dcgan.g], losses[dcgan.d]])
            
            if step%10 == 0:
                print("step {} loss = G: {:.8f}, D: {:.8f}".format(step, g_loss, d_loss))
                saver.save(sess, save_dir + '/model.ckpt')


if __name__ == '__main__':
    main()
