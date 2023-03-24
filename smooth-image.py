import imageio.v3 as iio
import numpy as np
# import numba as nb
import sys
from multiprocessing.pool import Pool
from datetime import datetime

NUM_THREADS = 8

# @nb.jit #numba the function
def colour_dist(colour1: list[int], colour2: list[int]) -> int:
  dr = abs(colour1[0] - colour2[0]);
  dg = abs(colour1[1] - colour2[1]);
  db = abs(colour1[2] - colour2[2]);
  return dr + dg + db

# @nb.jit #numba the function
def is_valid(i: int, j: int, im: list[list[int]]) -> bool:
  return (0 <= i < len(im) and 0 <= j < len(im[0]))

# @nb.jit #numba the function
def avg_colour(row: int, col: int, cur_colour: list[int], colours: list[list[int]]) -> list[int]:
  r_avg = 0
  g_avg = 0
  b_avg = 0
  n = 0
  d = 0
  for c in colours:
    r_avg += c[0]*c[3]
    g_avg += c[1]*c[3]
    b_avg += c[2]*c[3]
    n += c[3]
    d += c[4]
  if (n == 0): n = 1
  avg = [r_avg//n, g_avg//n, b_avg//n]
  return avg if (colour_dist(avg, cur_colour) <= threshold and d < threshold*n and n > area/1.3) else cur_colour

# @nb.jit #numba the function
def smooth_colour(im: list[list[int]], row: int, col: int, radius: int, threshold: int) -> list[int]:
  cur_colour = im[row][col]
  colours = []
  for i in range(row-radius, row+radius+1):
    for j in range(col-radius, col+radius+1):
      if (is_valid(i, j, im)):
        d = colour_dist(im[i][j], cur_colour)
        if (d <= threshold):
          # put greater weight on the colours closer
          r = radius-abs(row-i)
          c = radius-abs(col-j)
          colours.append(im[i][j]+[r**2+c**2]+[d])
  return avg_colour(row, col, cur_colour, colours)

# @nb.jit #numba the function
def process_pixel(point: tuple) -> tuple:
  return (point[0], point[1], smooth_colour(im, point[0], point[1], radius, threshold))

# @nb.jit #numba the function
def smooth_image():
  rows = np.zeros(shape=(height*width, 2), dtype="int32")
  for i in range(height*width):
    rows[i] = (i//width, i%width)
  
  processed = 0
  n = (len(im)*len(im[0]))

  with Pool(NUM_THREADS) as pool:
    for result in pool.imap_unordered(process_pixel, rows):
      im_out[result[0]][result[1]] = result[2]
      processed += 1
      dots = (((processed)*100)//(n)+1)
      print("  processing: [ {prog}{spaces} ] {0:.3f}%".format(((processed)*100)/n, prog='.'*dots, spaces=' '*(100-dots+1)), end='\r')

  pool.close()
  pool.join()


if __name__ == "__main__": 
  if (len(sys.argv) < 4):
    print("Usage: python smooth-image.py IMAGE(.png recommended) RADIUS THRESHOLD")
    exit(1)

  file = str(sys.argv[1])
  radius = int(sys.argv[2])
  threshold = int(sys.argv[3])
  area = (radius * 2 + 1)**2

  im = iio.imread(file).tolist()
  height = len(im)
  width = len(im[0])
  im_out = np.zeros(shape=(height, width, 3), dtype="uint8")

  start = datetime.now()
  smooth_image()
  done = datetime.now()
  
  new_filename = file[:file.index('.')]+'-smooth'+file[file.index('.'):]
  iio.imwrite(uri=new_filename, image=im_out)
  
  print(' '*128, end='\r')
  print("Done {sec}s. Smooth image saved to: {file}".format(sec=(done-start).seconds, file=new_filename))
