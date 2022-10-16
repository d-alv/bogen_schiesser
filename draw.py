import cv2 as cv
import numpy as np

img = cv.imread('photos/cat_image.jpg')

def rescaleFrame(frame, scale=.2):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

img = rescaleFrame(img)
blank = np.zeros((500,500,3), dtype='uint8')
#cv.imshow('cat', img)

# blank[:] = 0,255,0
# cv.imshow('Green', blank)


cv.rectangle(blank, (0,0), (250,250), (0,255,0), thickness=2)
cv.imshow('blank', blank)

cv.circle(blank, (250,250), 40, (0,0,255), thickness=3)
cv.imshow('circle', blank)


canny = cv.Canny(img, 125, 175)
cv.imshow('edges', canny)

cv.waitKey(0)