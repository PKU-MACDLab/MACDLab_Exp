#!/usr/bin/env python

# organize imports
import cv2
import imutils
import numpy as np
import math
from std_msgs.msg import String
import rospy
# global variables
bg = None

#-------------------------------------------------------------------------------
# Function - To find the running average over the background
#-------------------------------------------------------------------------------
def run_avg(image, aWeight):
    global bg
    # initialize the background
    if bg is None:
        bg = image.copy().astype("float")
        return

    # compute weighted average, accumulate it and update the background
    cv2.accumulateWeighted(image, bg, aWeight)

#-------------------------------------------------------------------------------
# Function - To segment the region of hand in the image
#-------------------------------------------------------------------------------
def segment(image, threshold=25):
    global bg
    # find the absolute difference between background and current frame
    diff = cv2.absdiff(bg.astype("uint8"), image)

    # threshold the diff image so that we get the foreground
    thresholded = cv2.threshold(diff,
                                threshold,
                                255,
                                cv2.THRESH_BINARY)[1]

    # get the contours in the thresholded image
    temp2, cnts, temp1 = cv2.findContours(thresholded.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # return None, if no contours detected
    if len(cnts) == 0:
        return
    else:
        # based on contour area, get the maximum contour which is the hand
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)


# applying Cosine Rule to find angle for all defects (between fingers)
# with angle > 90 degrees and ignore defects
def find_num_defects(cnt, hull, clone, offset):
	defects = cv2.convexityDefects(cnt, hull)
	count_fingers = 0
	if defects is not None:
		first_detected = False
		for i in range(defects.shape[0]):
			s,e,f,d = defects[i,0]
			start = tuple(cnt[s][0])
			end = tuple(cnt[e][0])
			far = tuple(cnt[f][0])

			# find length of all sides of triangle
			a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
			b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
			c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

			# apply cosine rule here
			angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
			#print("angle:" + str(angle))
			# ignore angles > 90 and highlight rest with red dots
			if angle <= 90:
				if not first_detected:
					count_fingers += 1
					first_detected = True
					cv2.circle(clone, (start[0] + offset[0], start[1] + offset[1]), 3, [0,255,0], 2)
				count_fingers += 1
				cv2.circle(clone, (far[0] + offset[0], far[1] + offset[1]), 3, [0,255,0], 2)
				cv2.circle(clone, (end[0] + offset[0], end[1] + offset[1]), 3, [0,255,0], 2)
				#dist = cv2.pointPolygonTest(cnt,far,True)

			# draw a line from start to end i.e. the convex points (finger tips)
			# (can skip this part)
			cv2.line(clone,(start[0] + offset[0], start[1] + offset[1]), (end[0] + offset[0], end[1] + offset[1]), [0,0,255], 2)
			#cv2.circle(crop_img,far,5,[0,0,255],-1)
		return count_fingers
	return 0


#-------------------------------------------------------------------------------
# Main function
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    pub = rospy.Publisher('num_of_fingers', String, queue_size=10)
    rospy.init_node('detect', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    # initialize weight for running average
    aWeight = 0.5

    # get the reference to the webcam
    camera = cv2.VideoCapture(0)

    # region of interest (ROI) coordinates
    top, right, bottom, left = 10, 350, 225, 590

    # initialize num of frames
    num_frames = 0

    # keep looping, until interrupted
    while not rospy.is_shutdown():
        # get the current frame
        (grabbed, frame) = camera.read()

        # resize the frame
        frame = imutils.resize(frame, width=700)

        # flip the frame so that it is not the mirror view
        frame = cv2.flip(frame, 1)

        # clone the frame
        clone = frame.copy()

        # get the height and width of the frame
        (height, width) = frame.shape[:2]

        # get the ROI
        roi = frame[top:bottom, right:left]

        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # to get the background, keep looking till a threshold is reached
        # so that our running average model gets calibrated
        if num_frames < 10:
            run_avg(gray, aWeight)
        else:
            # segment the hand region
            hand = segment(gray)
            # check whether hand region is segmented
            if hand is not None:
                # if yes, unpack the thresholded image and
                # segmented region
                (thresholded, segmented) = hand
                #hull = cv2.convexHull(segmented)
                #cv2.putText(clone, defects, (right, top), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)

                # draw the segmented region and display the frame
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                #cv2.drawContours(clone, [hull + (right, top)], -1, (0, 0, 255))
                try:
                  hull = cv2.convexHull(segmented, returnPoints = False)
                except cv2.error:
                  print("The convex hull indices are not monotonous, which can be in the case when the input contour contains self-intersections in function 'convexityDefects'")
                defects = find_num_defects(segmented, hull, clone, (right, top))
                #defects = count(thresholded, segmented, clone)
                #print(defects)
                defects = min(5, defects)
                pub.publish(str(defects))
                #rospy.loginfo(defects)
                cv2.putText(clone, str(defects), (bottom, left), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                cv2.imshow("Thesholded", thresholded)

        # draw the segmented hand
        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

        # increment the number of frames
        num_frames += 1

        # display the frame with segmented hand
        cv2.imshow("Video Feed", clone)

        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            break
        if keypress == ord("r"):
        	num_frames = 0
        rate.sleep()

# free up memory
camera.release()
cv2.destroyAllWindows()
