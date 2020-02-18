#############
## Imports ##
#############

""" Global """
import keras
import cv2
import numpy as np
import argparse
import tqdm

""" Local """
import Model
import constants

###############
## Functions ##
###############

def parse_args():
    parser = argparse.ArgumentParser(description="Arguments for training")
    parser.add_argument("-i", "--image_path", dest="image_path", help="Path to image", required=True)
    parser.add_argument("-m", "--model_path", dest="model_path", help="Path to the model weights", required=True)
    parser.add_argument("-o", "--output_path", dest="output_path", help="Path to save the predicted mask", required=True)
    parser.add_argument("-ps", "--patch_size", dest="patch_size", help="Patch size", default=constants.PATCH_SIZE, type=int)
    return parser.parse_args()

def load_model(model_path, patch_size):
    model = Model.wsi_segmenter(patch_size)
    model.load_weights(model_path)
    return model

def inference(model, image, patch_size):
    for i in range(0, image.shape[0], patch_size):
        for j in range(0, image.shape[1], patch_size):
            patch_img = cv2.resize(image[i:i+patch_size, j:j+patch_size], (patch_size, patch_size))
            patch_mask = model.predict(patch_img, verbose=0)
            return patch_mask

##########
## MAIN ##
##########

if __name__ == "__main__":
    args = parse_args()
    model = load_model(args.model_path, args.patch_size)
    image = cv2.imread(args.image_path) / 255.
    mask = inference(model, image, args.patch_size)
    print(mask)
