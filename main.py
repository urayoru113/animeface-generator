import tensorflow as tf
import numpy as np
import os
import time
import cv2
from dcgan import DCGAN
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

epochs = 1500
batch_size = 128
s_size = 6
image_size = s_size*16
learning_rate = 0.0002
save_dir = './model_yan'
train_data_path = './data_yan'
test_dir = './test_yan'


def load_image(filepath=train_data_path):

    if not os.path.isdir(filepath):
        print(filepath + " is not existing")
        os._exit(1)
    files = [os.path.join(filepath, f) for f in os.listdir(filepath) if f.endswith('.jpg')]
    fileseq = tf.train.string_input_producer(files)
    reader = tf.WholeFileReader()
    _, value = reader.read(fileseq)
    #features = tf.parse_single_example(value, features={'image_raw': tf.FixedLenFeature([], tf.string)})
    images = tf.cast(tf.image.decode_jpeg(value, channels=3), tf.float32)
    images = tf.image.resize_images(images, (image_size, image_size))
    min_queue_examples = batch_size * 100
    im_batch = tf.train.batch(
        [images],
        batch_size=batch_size,
        capacity=min_queue_examples + 3 * batch_size
        )
    im_batch = tf.subtract(tf.div(im_batch, 127.5), 1.0)
    return im_batch, len(files)

def main():

    dcgan = DCGAN(s_size=s_size, batch_size=batch_size)
    train_im, total_imgs= load_image()
    total_batch = int(total_imgs/batch_size)
    losses = dcgan.loss(train_im)
    train_op = dcgan.train(losses, learning_rate=learning_rate)
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.33)
    config = tf.ConfigProto(gpu_options=gpu_options,
                        device_count={"CPU": 8},
                        inter_op_parallelism_threads=1,
                        intra_op_parallelism_threads=1)

    with tf.Session() as sess:

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)

        init = tf.global_variables_initializer()
        sess.run(init)
        g_saver = tf.train.Saver(dcgan.g.variables)
        d_saver = tf.train.Saver(dcgan.d.variables)

        if os.path.isdir(save_dir):
            g_saver.restore(sess, tf.train.latest_checkpoint(save_dir + '/g_model'))
            d_saver.restore(sess, tf.train.latest_checkpoint(save_dir + '/d_model'))
        else:
            os.mkdir(save_dir)

        sample_z = np.float32(np.random.uniform(-1, 1, [dcgan.batch_size, dcgan.z_dim]))
        images = dcgan.sample_images(5, 5, inputs=sample_z)

        print("Start training")
        for step in range(1, epochs+1):
            start_time = time.time()
            for batch in range(total_batch):
                _, g_loss, d_loss = sess.run([train_op, losses[dcgan.g], losses[dcgan.d]])
            print("epochs {} loss = G: {:.8f}, D: {:.8f} run time:{:.4f} sec"\
            .format(step, g_loss, d_loss, time.time()-start_time))
            g_saver.save(sess, save_dir + '/g_model/g.ckpt', global_step=step)
            d_saver.save(sess, save_dir + '/d_model/d.ckpt', global_step=step)

            with open('./test/%05d.jpg' % step, 'wb') as f:
                    f.write(sess.run(images))
        coord.request_stop()
        coord.join(threads)


if __name__ == '__main__':
    if not os.path.isdir(train_data_path):
        print("folder %s does not exists" %train_data_path)
        os._exit(1)
    if not os.path.isdir(test_dir):
        os.mkdir(test_dir)
    main()