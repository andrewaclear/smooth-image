import imageio.v3 as iio
import numpy as np
import sys

def colour_dist(colour1: list[int], colour2: list[int]) -> int:
  dr = abs(colour1[0] - colour2[0]);
  dg = abs(colour1[1] - colour2[1]);
  db = abs(colour1[2] - colour2[2]);
  return dr + dg + db

def is_valid(i: int, j: int, im: list[list[int]]) -> bool:
  return (0 <= i < len(im) and 0 <= j < len(im[0]))

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

if __name__ == "__main__": 
  if (len(sys.argv) < 4):
    print("Usage: python smooth-image.py IMAGE(.png recommended) RADIUS THRESHOLD")
    exit(1)

  file = str(sys.argv[1])
  radius = int(sys.argv[2])
  threshold = int(sys.argv[3])
  area = (radius * 2 + 1)**2

  im = iio.imread(file).tolist()
  im_blur = iio.imread(file_blur).tolist()
  im_out = np.zeros(shape=(len(im), len(im[0]), 3), dtype="uint8")

  for row in range(len(im)):
    for col in range(len(im[0])):
      # print("previous: ", im[row, col])
      im_out[row, col] = smooth_colour(im, row, col, radius, threshold);
      # print("average: ", im_out[row, col])
    print("processing: {0:.3f}% {test}".format((row*100)/len(im), test='.'*((row*100)//len(im)+1)), end='\r')

  iio.imwrite(uri=file[:file.index('.')]+'-smooth'+file[file.index('.'):], image=im_out)
