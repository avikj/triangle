from PIL import Image, ImageFilter
import numpy as np
from skimage.filters import scharr, sobel
from scipy.spatial import Delaunay
threshold = .1
MAX_POINTS = 1000
def render(input_file='hari.jpeg'):
  im = np.asarray(Image.open(input_file).convert('LA'))[:,:,0]
  print im
  bools = (sobel(im) > threshold)
  points = zip(*np.where(bools))
  Image.fromarray(bools.astype(np.float32)*255).show()
  if(len(points) > MAX_POINTS-4):
    np.random.shuffle(points)
    points = points[:MAX_POINTS-4]
  points.append((0,0))
  points.append((im.shape[0]-1,0))
  points.append((im.shape[0]-1,im.shape[1]-1))
  points.append((0,im.shape[1]-1))
  simplices = Delaunay(points).simplices
  source = np.asarray(Image.open(input_file).convert('RGB'))
  copy = np.copy(source)
  for simplex in simplices:
    tri_verts = [points[j] for j in simplex]
    contained_points = rasterize_triangle(np.array([points[j] for j in simplex]))
    average = [0,0,0]
    for x, y in contained_points:
      average += source[x,y]
    average /= len(contained_points)
    for x, y in contained_points:
      copy[x,y] = average
  return Image.fromarray(copy)
def rasterize_triangle(tri_verts):
  result = []
  for x in range(min(tri_verts[:,0]), max(tri_verts[:,0])+1):
    for y in range(min(tri_verts[:,1]), max(tri_verts[:,1])+1):
      if in_triangle(tri_verts, (x, y)):
        result.append((x, y))
  return result
def in_triangle(tri_verts, point):
  return areax2(point, tri_verts[1], tri_verts[2])+areax2(tri_verts[0], point, tri_verts[2])+areax2(tri_verts[0], tri_verts[1], point) == areax2(tri_verts[0], tri_verts[1], tri_verts[2])
def areax2(a,b,c):
  return abs(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))

fn = raw_input('enter a filename: ')
render(fn).save('triangle-'+fn)