import uuid
import os
import cv2
import numpy as np
from PIL import Image
import colorsys
from collections import Counter
import yaml
from time import time 



def sort_dict_by_value(my_dict):
      sorted_dict = dict(sorted(my_dict.items(), key=lambda item: item[1], reverse=True))
      return sorted_dict
    
def counting(my_list):
  # Count occurrences of each element
  element_count = Counter(my_list)
  # Print each element and its occurrence
  return element_count

def normalize_rgb(x):
    """
    Normalize a list of sample image data in the range of 0 to 1
    : x: List of image data.  The image shape is (32, 32, 3)
    : return: Numpy array of normalized data
    """
    return np.array((x - np.min(x)) / (np.max(x) - np.min(x)))
  
def de_normalize_value(color_tuple):
      ls = []
      for i in color_tuple:
        ls.append(round(i * 255))
      return tuple(ls)


def padding(image_path, a = 100):
      # Load the image
  image = Image.open(image_path)
  # Define padding size for each side
  top, bottom, left, right = a,a,a,a  # Adjust as needed
  # Choose padding color: (255, 255, 255) for white, (0, 0, 0) for black
  padding_color = (255, 255, 255)  # White padding, change to (0, 0, 0) for black
  # Calculate new image size with padding
  new_width = image.width + left + right
  new_height = image.height + top + bottom
  # Create a new image with the specified padding color
  padded_image = Image.new("RGB", (new_width, new_height), padding_color)
  # Paste the original image onto the center of the new image
  padded_image.paste(image, (left, top))
  # Save the padded image
#   padded_image.save(save_path)
  return padded_image

def fix_background(b_mask, img):
      # OPTION-1: Isolate object with black background
  # if save_path.endswith('.png'):
  #       transparent = True
  # else:
  #       transparent = False
  transparent = False
  if not transparent:
    # Create 3-channel mask
    mask3ch = cv2.cvtColor(b_mask, cv2.COLOR_GRAY2BGR)
    # Isolate object with binary mask
    isolated = cv2.bitwise_and(mask3ch, img)
  else:
    # OPTION-2: Isolate object with transparent background (when saved as PNG)
    isolated = np.dstack([img, b_mask])
  return isolated


def mask_img(img, c):
  '''
    batch_yolo_result = model.predict(conf=0.2, source=source_image, save=False)
    for single_image_result in batch_yolo_result:
        img = np.copy(single_image_result.orig_img)
        for ci, single_object_result in enumerate(single_image_result):
            isolated = mask_img(img=img, c=single_object_result)    
            isolated = remove_padding(isolated)

  '''
  # Create binary mask
  b_mask = np.zeros(img.shape[:2], np.uint8)
  #  Extract contour result
  contour = c.masks.xy.pop()
  #  Changing the type
  contour = contour.astype(np.int32)
  #  Reshaping
  contour = contour.reshape(-1, 1, 2)
  # Draw contour onto mask
  _ = cv2.drawContours(b_mask, [contour], -1, (255, 255, 255), cv2.FILLED)
  isolated = fix_background(b_mask, img)
  return isolated
 

def remove_padding(padded_image, padding_size=100):
    """
    Removes padding from a padded image.

    :param padded_image: Padded Image object.
    :param padding_size: Size of the padding to remove from each side (default is 100).
    :return: Original Image object without padding.
    """
    # Get the size of the padded image
    # Get the dimensions of the padded image
    # Get the dimensions of the padded image
    height, width = padded_image.shape[:2]

    # Define the bounding box to crop
    left = padding_size
    top = padding_size
    right = width - padding_size
    bottom = height - padding_size

    # Crop the image to remove padding
    original_image = padded_image[top:bottom, left:right]

    return original_image
    
