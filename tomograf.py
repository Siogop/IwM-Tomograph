import numpy as np
from imageio import imread
from matplotlib import pyplot as plt
from skimage import filters, restoration
from skimage.color import rgb2gray
from skimage.transform import resize, radon
from bresenham import bresenham_line
from scipy.ndimage.filters import median_filter

RANGE = 360

def compute_emitter(angle, r):
    angle = np.pi * angle/180
    x = int(np.floor(r * np.cos(angle)) + 100)
    y = int(np.floor(r * np.sin(angle)) + 100)
    return x, y

def compute_detectors(alpha, number, emitter, r):
    position_detectors = []
    for i in range(number):
        angle = (emitter + 180 - alpha/2 + alpha*(i/(number-1))) % 360
        position_detectors.append(compute_emitter(angle, r))
    return position_detectors

def normalize(sinogram):
    max = 1
    min = 100
    for z in range(len(sinogram)):
        for i in sinogram[z]:
            if i > max:
                max = i
            if i < min and i !=0:
                min = i
    for z in range(len(sinogram)):
        for i in range(len(sinogram[z])):
            sinogram[z, i] = (sinogram[z, i]-min)/max
    print(max)
    return sinogram



def sinogram(image, alpha, number, emitters, r, steps, p2, canvas):
    detectors_positions = []
    emitter_positions = []
    for i in range(0, RANGE, int(RANGE / emitters)):
        emitter_positions.append(compute_emitter(i, r))
        detectors_positions.append(compute_detectors(alpha, number, i, r))

    sinogram = np.zeros([len(emitter_positions), number])

    for i in range(len(emitter_positions)):
        #image[emitter_positions[i]] = 1
        if i%steps == 0:
            p2.imshow(sinogram, cmap='gray')
            canvas.draw()
        for d in range(len(detectors_positions[i])):
            #image[detectors_positions[i][d]] = 1

            line = bresenham_line(emitter_positions[i][0], emitter_positions[i][1], detectors_positions[i][d][0],
                                  detectors_positions[i][d][1])
            for b in line:
                sinogram[i, d] += image[b[0], b[1]]
    return sinogram

def reverseSinogram(image, alpha, number, emitters, height, width, r):
    detectors_positions = []
    emitter_positions = []
    for i in range(0, RANGE, int(RANGE / emitters)):
        emitter_positions.append(compute_emitter(i,r))
        detectors_positions.append(compute_detectors(alpha, number, i, r))

    reverse = np.zeros((2*height, 2*width))
    reverseCounter = np.zeros((2*height, 2*width))

    for i in range(len(emitter_positions)):
        for d in range(len(detectors_positions[i])):

            line = bresenham_line(emitter_positions[i][0], emitter_positions[i][1], detectors_positions[i][d][0],
                                  detectors_positions[i][d][1])
            for b in line:
                reverse[b[0], b[1]] += image[i][d]
                reverseCounter[b[0], b[1]] += 1
                #print("b",b)
                #print("id",i,d)
    for i in range(len(reverse)):
        for j in range(len(reverse[i])):
            if reverseCounter[i][j] != 0:
                reverse[i][j] = reverse[i][j]/reverseCounter[i][j]
    return reverse


def load(path):
    picture = resize(rgb2gray(imread(path)), (100, 100))
    height = len(picture)
    width = len(picture[0])
    image = np.zeros([2 * height, 2 * width])
    image[int(height / 2):int(3 * height / 2), int(width / 2):int(3 * width / 2)] = picture
    return image, height, width


def mse(image, image2):
    ms_error = np.sum((image.astype("float") - image2.astype("float")) ** 2)
    ms_error /= float(image.shape[0] * image.shape[1])
    print(ms_error)
    return ms_error

def msev2(image, image2):
    sum = 0
    for x in range(len(image)):
        for y in range(len(image[x])):
            sum += pow(abs(image[x][y] - image2[x][y]), 2)


    return np.sqrt(sum / pow(len(image), 2))

def main(image, alpha, number, emitters, steps, fig, canvas):
    #alpha = 180
    #number = 51
    #emitters = 90
    print("main")

    height = int(len(image)/2)
    width = int(len(image[0])/2)
    r = 96

    p1 = fig.add_subplot(221)
    p2 = fig.add_subplot(222)
    p3 = fig.add_subplot(223)
    p4 = fig.add_subplot(224)

    p1.imshow(image, cmap='gray')

    sinogramik = sinogram(image, alpha, number, emitters, r, steps, p2, canvas)
    sinogramNormalized = normalize(sinogramik)
    reverse = reverseSinogram(sinogramik, alpha, number, emitters, height, width, r)
    reverse = reverse[int(height / 2):int(3 * height / 2), int(width / 2):int(3 * width / 2)]
    reverseNormalized = normalize(reverse)
    reverseFiltered = median_filter(reverseNormalized, 2)

    #fig, plots = plt.subplots(2, 2)
    #plots[0].imshow(image, cmap='gray')

    #plots[0][0].imshow(image, cmap='gray')
    #plots[0][1].imshow(sinogramNormalized, cmap='gray')
    #plots[1][0].imshow(radon(image), cmap='gray')
    #plots[1][1].imshow(reverse, cmap='gray')
    #plt.show()

    p2.imshow(sinogramNormalized, cmap='gray')
    p3.imshow(reverseNormalized, cmap='gray')
    p4.imshow(reverseFiltered, cmap='gray')

    canvas.draw()

    return msev2(image[int(height / 2):int(3 * height / 2), int(width / 2):int(3 * width / 2)], reverse), msev2(image[int(height / 2):int(3 * height / 2), int(width / 2):int(3 * width / 2)], reverseFiltered)

