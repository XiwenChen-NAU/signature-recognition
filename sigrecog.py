import cv2
import os
import numpy as np

def main():
    print('OpenCV version: '+ cv2.__version__)

    current_dir = os.path.dirname(__file__)

    input_folder = os.path.join(current_dir, 'data/training/021')
    input_file = '13_021.PNG'
    img = cv2.imread(os.path.join(input_folder, input_file), 0)

    print(prepare(img))


def prepare(input):
    # preprocessing the image input
    clean = cv2.fastNlMeansDenoising(input)
    tresh = cv2.adaptiveThreshold(clean, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    img = crop(tresh)

    # 40x10 image as a flatten array
    flatten_img = cv2.resize(img, (40, 10), interpolation = cv2.INTER_AREA).flatten()

    # resize to 400x100
    resized = cv2.resize(img, (400, 100), interpolation = cv2.INTER_AREA)
    columns = np.sum(resized, axis = 0) # sum of all columns
    lines = np.sum(resized, axis = 1) # sum of all lines

    #cv2.imshow('image', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    h, w = img.shape
    aspect = w / h

    return [*flatten_img, *columns, *lines, aspect]


def crop(img):
    inverted = 255 - img
    points = cv2.findNonZero(inverted)
    x, y, w, h = cv2.boundingRect(points)
    return img[y: y+h, x: x+w]


def load_images(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images


if __name__ == '__main__':
    main()