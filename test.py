import cv2 as cv

def crop_an_image(image, x, y):
    height = int(image.shape[0] * y)
    length = int(image.shape[1] * x)

    left_cutoff = image[:, length:]
    top_cutoff = image[height:, :]
    right_cutoff = image[:, :length]
    bottom_cutoff = image[:height, :]

    return left_cutoff, top_cutoff, right_cutoff, bottom_cutoff

example = 'bestOf/resources/examples/dark.jpg'
ex_image = cv.imread(example)

left, top, right, bottom = crop_an_image(ex_image, 0.4, 0.4)

cv.imshow('left_cutoff', left)
cv.imshow('top_cutoff', top)
cv.imshow('right_cutoff', right)
cv.imshow('bottom_cutoff', bottom)
cv.waitKey(0)