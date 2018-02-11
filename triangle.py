from PIL import Image, ImageFilter
import numpy as np
from skimage.filters import scharr, sobel
from scipy.spatial import Delaunay
im = np.asarray(Image.open("land.jpeg").convert('LA'))[:,:,0]
print im
points = zip(*np.where(sobel(im) > np.random.rand(im.shape[0], im.shape[1])))
print Delaunay(points).simplices

