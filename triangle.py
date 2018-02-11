from PIL import Image, ImageFilter
import numpy as np
from skimage.filters import scharr, sobel
from scipy.spatial import Delaunay
import gizeh
import argparse

def render(args):
  im = np.asarray(Image.open(args.input_file).convert('LA').filter(ImageFilter.GaussianBlur(args.blur_rad)))[:,:,0]
  surface = gizeh.Surface(width=int(im.shape[1]*args.scale), height=int(im.shape[0]*args.scale))

  # Get vertex points 
  points = zip(*np.where(sobel(im) > args.threshold))
  Image.fromarray((sobel(im)).astype(np.float32)*255/np.max(sobel(im))).show()
  Image.fromarray((sobel(im)>args.threshold).astype(np.float32)*255).show()
  if(len(points) > args.max_points-4):
    np.random.shuffle(points)
    points = points[:args.max_points-4]
  points.append((0,0))
  points.append((im.shape[0]-1,0))
  points.append((im.shape[0]-1,im.shape[1]-1))
  points.append((0,im.shape[1]-1))

  # Run Delaunay triangulation to get simplices
  simplices = Delaunay(points).simplices


  source = np.asarray(Image.open(args.input_file).convert('RGB'))
  copy = np.copy(source)
  for simplex in simplices:
    tri_verts = np.array([points[j] for j in simplex])
    contained_points = rasterize_triangle(np.array([points[j] for j in simplex]))
    average = [0,0,0]
    for x, y in contained_points:
      average += source[x,y]
    average /= len(contained_points)
    vec_tri = gizeh.polyline(points=tri_verts[:,::-1]*args.scale, close_path=True, stroke_width=1, stroke=(average/256.0), fill=(average/256.0))
    vec_tri.draw(surface)
    '''for x, y in contained_points:
      copy[x,y] = average'''
  surface.write_to_png(args.output_file)
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



parser = argparse.ArgumentParser()
parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('--blur_rad', type=int,
                   help='Pre-edge detection blur radius (Gaussian).', default=0)
parser.add_argument('--threshold', type=float,
                   help='Edge inclusion threshold.', default=0.1)
parser.add_argument('--max_points', type=int,
                   help='Max number of points to select for Delaunay triangulation.', default=1000)
parser.add_argument('--scale', type=float,
                   help='Size scale factor for output.', default=1)

args = parser.parse_args()
render(args)