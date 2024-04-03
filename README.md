# Simple-Object-Finding
Finding and cutting out objects from a photo using simple image operations

## Overview
This Python script uses OpenCV and NumPy to compare two images, identifying and extracting differences between them. It operates by analyzing pixel-by-pixel variations, highlighting these differences in one image and extracting the altered regions.
The extracted object is then modified to be on transparent background and a mask is convoluted on its whole surface in order to cover blank spaces and mistaken pixels.

## Features
- Detection of Pixel-wise Differences: Identifies differences between two images by comparing RGB values of each pixel.
- Highlighting Changes: Marks the changed areas in one of the images with bounding boxes for easy visualization.
- Extraction with Transparency: Creates a new image with only the changed areas, applying transparency to unchanged pixels.

## Example
Imput provided for the script:
<p align="center">
  <img src="dublin.jpg" width="400" alt="photo1">
  <img src="dublin_edited.jpg" width="400" alt="photo 2">
</p>

Output:

![output1](output_Dublin.png)

![output2](output_kevin.png)


