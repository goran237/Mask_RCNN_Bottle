import os
import sys
import random
import math
import re
import time
import numpy as np
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def main():
    ROOT_DIR = os.path.abspath("../../")

    sys.path.append(ROOT_DIR)  # To find local version of the library
    from mrcnn import utils
    from mrcnn import visualize
    from mrcnn.visualize import display_images
    import mrcnn.model as modellib
    from mrcnn.model import log

    from samples.bottle import bottle

    # Directory to save logs and trained model
    MODEL_DIR = os.path.join(ROOT_DIR, "logs")

    # Path to Ballon trained weights
    # You can download this file from the Releases page
    # https://github.com/matterport/Mask_RCNN/releases
    BALLON_WEIGHTS_PATH = "C:\\Users\\Goran\\PycharmProjects\\Mask_RCNN_2\\samples\\bottle\\model\\mask_rcnn_bottle_0039.h5"  # TODO: update this path

    config = bottle.CustomConfig()
    BALLOON_DIR = "C:\\Users\\Goran\\PycharmProjects\\Mask_RCNN_2\\samples\\bottle\\dataset"

    class InferenceConfig(config.__class__):
        # Run detection on one image at a time
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1

    config = InferenceConfig()
    config.display()

    # Device to load the neural network on.
    # Useful if you're training a model on the same
    # machine, in which case use CPU and leave the
    # GPU for training.
    DEVICE = "/cpu:0"  # /cpu:0 or /gpu:0

    # Inspect the model in training or inference modes
    # values: 'inference' or 'training'
    # TODO: code for 'training' test mode not ready yet
    TEST_MODE = "inference"

    # Load validation dataset
    dataset = bottle.CustomDataset()
    dataset.load_custom(BALLOON_DIR, "val")

    # Must call before using the dataset
    dataset.prepare()

    print("Images: {}\nClasses: {}".format(len(dataset.image_ids), dataset.class_names))

    # Create model in inference mode
    with tf.device(DEVICE):
        model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR,
                                  config=config)

        # Set path to balloon weights file

        # Download file from the Releases page and set its path
        # https://github.com/matterport/Mask_RCNN/releases
        # weights_path = "/path/to/mask_rcnn_balloon.h5"

        # Or, load the last model you trained
        weights_path = BALLON_WEIGHTS_PATH

        # Load weights
        print("Loading weights ", weights_path)
        model.load_weights(weights_path, by_name=True)

        image_id = random.choice(dataset.image_ids)
        image, image_meta, gt_class_id, gt_bbox, gt_mask = \
            modellib.load_image_gt(dataset, config, image_id, use_mini_mask=False)
        info = dataset.image_info[image_id]
        print("image ID: {}.{} ({}) {}".format(info["source"], info["id"], image_id,
                                               dataset.image_reference(image_id)))

        # Run object detection
        results = model.detect([image], verbose=1)

        # Display results
        ax = get_ax(1)
        r = results[0]
        visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
                                    dataset.class_names, r['scores'], ax=ax,
                                    title="Predictions")
        log("gt_class_id", gt_class_id)
        log("gt_bbox", gt_bbox)
        log("gt_mask", gt_mask)



if __name__ == "__main__":
    main()


def get_ax(rows=1, cols=1, size=16):
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.

    Adjust the size attribute to control how big to render images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size * cols, size * rows))
    return ax