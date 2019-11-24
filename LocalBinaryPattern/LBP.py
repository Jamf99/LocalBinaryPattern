import cv2
import numpy as np
from matplotlib import pyplot as plt
import timeit
from skimage import feature

class LBP:
	def __init__(self, input):
		self.image = cv2.imread(input, 0)

		self.transformed_img = cv2.imread(input, 0)

		self.height = len(self.image)
		self.width = len(self.image[0])

	def execute(self):
		img_lbp = np.zeros((self.height, self.width, 3), np.uint8)

		#  ===== Start counting time in microseconds =====

		start = timeit.default_timer()

		# Taking advantage of the spatial locality
		for line in range(self.height):
			for column in range(self.width):
		 		img_lbp[line, column] = self._calculateLBP(self.image, column, line)

		# Without taking advantage of the spatial locatity
		# for column in range(self.width):
		#	for line in range(self.height):
	    #		img_lbp[line, column] = self._calculateLBP(self.image, column, line)

		stop = timeit.default_timer()

		#  ===== End counting time in microseconds =====

		print("Time: {} seconds".format(stop - start))

		self._histogram(self.image, self.transformed_img, "Result from algorithm developed")
		self._displayImages(self.transformed_img, "Result from algorithm developed")

	def _displayImages(self, transformed_img, title):
		plt.figure()
		plt.axis("off")
		plt.title(title)
		plt.imshow(transformed_img, cmap='gray')
		plt.show()

	def _calculateLBP(self, pixel, column, line):
		values = self._thresholded(pixel[line,column], self._get_positions_8_1(pixel, column, line))
		weights_8 = [1, 2, 4, 8, 16, 32, 64, 128]
		# weights_16 = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
		lbp = 0
		for i in range(0, len(values)):
			lbp += values[i]*weights_8[i]
		self.transformed_img.itemset((line,column), lbp)
		return lbp

	# Obtain pixel positions with radius 1 and 8 neighbors
	def _get_positions_8_1(self, pixels, column, line):
		top_left      = self._get_pixel_value(pixels,line-1, column-1)
		top_up        = self._get_pixel_value(pixels,line-1, column)
		top_right     = self._get_pixel_value(pixels,line-1, column+1)
		right         = self._get_pixel_value(pixels,line, column+1)
		left          = self._get_pixel_value(pixels,line, column-1)
		bottom_left   = self._get_pixel_value(pixels,line+1, column-1)
		bottom_down   = self._get_pixel_value(pixels,line+1, column)
		bottom_right  = self._get_pixel_value(pixels,line+1, column+1)

		positions = [top_left, top_up, top_right, left, right, bottom_left, bottom_down, bottom_right]

		return positions

	#Obtain pixel positions with radius 2 and 8 neighbors
	def _get_positions_8_2(self, pixels, column, line):
		top_left      = self._get_pixel_value(pixels,line-1, column-1)
		top_up        = self._get_pixel_value(pixels,line-2, column)
		top_right     = self._get_pixel_value(pixels,line-1, column+1)
		right         = self._get_pixel_value(pixels,line, column+2)
		left          = self._get_pixel_value(pixels,line, column-2)
		bottom_left   = self._get_pixel_value(pixels,line+1, column-1)
		bottom_down   = self._get_pixel_value(pixels,line+2, column)
		bottom_right  = self._get_pixel_value(pixels,line+1, column+1)

		positions = [top_left, top_up, top_right, left, right, bottom_left, bottom_down, bottom_right]

		return positions

	# Obtain pixel positions with radius 2 and 16 neighbors
	def _get_positions_16_2(self, pixels, column, line):
		top_left_down        = self._get_pixel_value(pixels,line-1, column-2)
		top_left_center      = self._get_pixel_value(pixels,line-1, column-1)
		top_left_up          = self._get_pixel_value(pixels,line-2, column-1)
		top_up     	         = self._get_pixel_value(pixels,line-2, column)
		top_right_up         = self._get_pixel_value(pixels,line-2, column+1)
		top_right_center     = self._get_pixel_value(pixels,line-1, column+1)
		top_right_down       = self._get_pixel_value(pixels,line-1, column+2)
		left                 = self._get_pixel_value(pixels,line, column-2)
		right                = self._get_pixel_value(pixels,line, column+2)
		bottom_left_up       = self._get_pixel_value(pixels,line+1, column-2)
		bottom_left_center   = self._get_pixel_value(pixels,line+1, column-1)
		bottom_left_down     = self._get_pixel_value(pixels,line+2, column-1)
		bottom_down     	 = self._get_pixel_value(pixels,line+2, column)
		bottom_right_down    = self._get_pixel_value(pixels,line+2, column+1)
		bottom_right_center  = self._get_pixel_value(pixels,line+1, column+1)
		bottom_right_up      = self._get_pixel_value(pixels,line+1, column+2)

		positions = [top_left_down, top_left_center, top_left_up, top_up, top_right_up, top_right_center,
						top_right_down, left, right, bottom_left_up, bottom_left_center, bottom_left_down,
						bottom_down, bottom_right_down, bottom_right_center, bottom_right_up]

		return positions

	def _thresholded(self, center, neighbours):
	    result = []
	    for neighbour in neighbours:
	        if neighbour >= center:
	            result.append(1)
	        else:
	            result.append(0)
	    return result

	def _get_pixel_value(self, pixel, line, column, default=0):
		try:
			return pixel[line,column]
		except IndexError:
			return default

	def _histogram(self, img, transformed_img, title):
		hist,bins = np.histogram(img.flatten(),256,[0,256])
		cdf = hist.cumsum()
		cdf_normalized = cdf * hist.max()/ cdf.max()
		plt.plot(cdf_normalized, color = 'b')
		plt.hist(transformed_img.flatten(),256,[0,256], color = 'r')
		plt.xlim([0,256])
		plt.title(title)
		plt.legend(('Cumulative Distribution Function (CDF)','Histogram'), loc = 'upper left')
		plt.show()
		cv2.waitKey(0)
		cv2.destroyAllWindows()
