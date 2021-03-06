import argparse

import tensorflow as tf
from calamari_ocr.utils import glob_all
from tqdm import tqdm
import os

usage_str = 'python tensorflow_rename_variables.py --checkpoints=path_to_models.json ' \
            '--replace_from=substr --replace_to=substr --add_prefix=abc --dry_run'


def rename(checkpoint, replace_from, replace_to, add_prefix, dry_run):
    tf.reset_default_graph()
    with tf.Session() as sess:
        for var_name, _ in tf.contrib.framework.list_variables(checkpoint):
            # Load the variable
            var = tf.contrib.framework.load_variable(checkpoint, var_name)

            # Set the new name
            new_name = var_name
            if None not in [replace_from, replace_to]:
                new_name = new_name.replace(replace_from, replace_to)
            if add_prefix:
                new_name = add_prefix + new_name

            if dry_run:
                print('%s would be renamed to %s.' % (var_name, new_name))
            else:
                print('Renaming %s to %s.' % (var_name, new_name))
                # Rename the variable
                var = tf.Variable(var, name=new_name)

        if not dry_run:
            # Save the variables
            saver = tf.train.Saver()
            sess.run(tf.global_variables_initializer())
            saver.save(sess, checkpoint)


def main():
    parser = argparse.ArgumentParser(description=usage_str)
    parser.add_argument('--checkpoints', nargs='+', type=str, required=True)
    parser.add_argument('--replace_from')
    parser.add_argument('--replace_to')
    parser.add_argument('--add_prefix')
    parser.add_argument('--dry_run', action='store_true')

    args = parser.parse_args()

    for ckpt in tqdm(glob_all(args.checkpoints)):
        ckpt = os.path.splitext(ckpt)[0]
        rename(ckpt, args.replace_from, args.replace_to, args.add_prefix, args.dry_run)


if __name__ == '__main__':
    main()
