# Reference code:
# Getting started with video —
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
# ——— Trying to get the video to save since OS extension isn't documented
# Changing colorspaces -
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html#converting-colorspaces
# ——— Used Object Tracking code + Finding HSV values to track to track desired color
# Learning contours -
# https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html#contour-features
# ——— Used rotated rectangle code to draw bounding box around tracked object
# To find HSV color to track
# ——— green = np.uint8([[[0,255,0 ]]])
# ——— hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
# ——— print (hsv_green)

import numpy as np
import cv2

cap = cv2.VideoCapture(0)


while(cap.isOpened()):
	# Capture frame-by-frame
	ret, frame = cap.read()

	### HSV ###
	# Convert BGR to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# Define range of green color in HSV
	lower_green = np.array([30,100,100])
	upper_green = np.array([90,255,255])

	# Threshold the HSV image to get only blue colors
	mask = cv2.inRange(hsv, lower_green, upper_green)

	# ### RGB ###
	# # Convert BGR to RGB
	# rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	#
	# # Define range of green color in HSV
	# lower_green = np.array([100,255,100])
	# upper_green = np.array([200,255,200])
	#
	# # Threshold the HSV image to get only blue colors
	# mask = cv2.inRange(rgb, lower_green, upper_green)


	# Bitwise-AND mask and original image
	# res = cv2.bitwise_and(frame,frame, mask= mask)

	# Arguments: src image, contour retrieval mode, contour approximation
	# Returns modified image, contours, hierarchy
	contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	if len(contours) > 0:
		green_area = max(contours, key=cv2.contourArea)
		# Rotated rectangle around tracked object
		rect = cv2.minAreaRect(green_area)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		cv2.drawContours(frame,[box],0,(0,0,255),2)

	cv2.imshow('frame',frame)
	# cv2.imshow('mask',mask)
	# cv2.imshow('res',res)

	k = cv2.waitKey(60) & 0xff
	# Press Escape to exit
	if k == 27:
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
