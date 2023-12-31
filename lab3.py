# Skeleton code to be filled in by students for EECS 452 ball tracking lab
# Authors:
#   Ben Simpson
#   Siddharth Venkatesan
#   Ashish Nichanametla

###############
### INCLUDE ###
###############
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
from matplotlib import pyplot as plt
import numpy as np
from timer import Timer

########################
### HELPER FUNCTIONS ###
########################

# Function for performing color subtraction
# Inputs:
#   img     Image to have a color subtracted. shape: (N, M, C)
#   color   Color to be subtracted.  Integer ranging from 0-255
# Output:
#   Grayscale image of the size as img with higher intensity denoting greater color difference. shape: (N, M)
def color_subtract(img, color):

    # TODO: Convert img to HSV format

    # TODO: Extract only h-values (2D Array)

    # TODO: Take the difference of each pixel and the chosen H-value
    # HINT: Pay attention to integer overflow here. What happens when
    # subtracting unsigned ints and the result is negative?
    # Use integer casting before you subtract and take the absolute value, then
    # use it again when you return a 2D array of unsigned ints as your difference image

    # TODO: Take absolute value of the pixels
    #hsv
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(img1)
    h = np.abs(h - color)

    #np.abs(img1(:,:,1) - color)
    #s = img1(:,:,2)
    #v = img1(:,:,3)
    
    final_img = h #cv2.merge([h,s,v])

    return final_img

# Function to find the centroid and radius of a detected region
# Inputs:
#   img         Binary image
#   USE_IDX_IMG Binary flag. If true, use the index image in calculations; if
#               false, use a double nested for loop.
# Outputs:
#   center      2-tuple denoting centroid
#   radius      Radius of found circle
def identify_ball(img, USE_IDX_IMG):
    # Find centroid and number of pixels considered valid
    h, w = img.shape
    # Double-nested for loop code
    if USE_IDX_IMG == False:
        k = 0
        x_sum = 0
        y_sum = 0
        for y in range(w):
            for x in range(h):
                if img[x,y] != 0:    # Uncomment this line when editing here
                    # TODO: Calculate x_sum, y_sum, and k
                    x_sum += x
                    y_sum += y
                    k += 1
        print(k)
        if(k != 0):
            # TODO: Calculate the center and radius using x_sum, y_sum, and k.
            C_x = x_sum / k
            C_y = y_sum / k
            C_x = int(C_x)
            C_y = int(C_y)
        else:
            # TODO: Don't forget to account for the boundary condition where k = 0.
            C_x = 0
            C_y = 0
            # pass
        center = (C_x, C_y)
        radius = int(np.sqrt(k / np.pi))
        print(C_x, C_y)
        print(radius)

    # Use index image
    else:
        # Calculate number of orange pixels
        k = np.sum(img)

        if k == 0:
            # No orange pixels.  Return some default value
            return (0,0), 0

        # Index image vectors
        x_idx = np.expand_dims(np.arange(w),0)
        y_idx = np.expand_dims(np.arange(h),1)
        print(x_idx.shape, y_idx.shape)
        print(k, img.shape)

        # TODO: Calculate the center and radius using the index image vectors
        #       and numpy commands
        C_x = (x_idx @ img.T) / k
        C_y = (img.T @ y_idx) / k
        print(C_x.shape, C_y.shape)
        C_x = int(np.sum(C_x))
        C_y = int(np.sum(C_y))

        print(C_x, C_y)
        center = (C_x, C_y)
        radius = int(np.sqrt(k/255 / np.pi))
        print(radius)

    return center, radius

# Function to find the centroid and radius of a detected region using OpenCV's
# built-in functions.
# Inputs:
#   img         Binary image
# Outputs:
#   center      2-tuple denoting centroid
#   radius      Radius of found circle
def contours_localization(img):

    # TODO: Use OpenCV's findContours function to identify contours in img.
    #       Assume the biggest contour is the ball and determine its center and
    #       radius. Do not forget to deal with the boundary case where no
    #       contours are found.

    center, radius = (0,0), 0

    return center, radius

################################
### CONSTANTS AND PARAMETERS ###
################################
# Flag for indicating how we perform color thresholding
USE_DIFFERENCE_IMAGE = True
# Flag for indicating how we perform ball localization
USE_LOCALIZATION_HEURISTIC = True
# Flag to indicate computation method for localization heuristic
USE_IDX_IMG = False

# Flag for indicating if we want the function timers to print every frame
FTP = True

# Values for color thresholding (default trackbar values)
# TODO: Find and tune these. Uncomment lines below and assign values to variables.
H_val = 19  # H-value of ball for difference image
thold_val = 15 # Threshold value for difference image

######################
### INITIALIZATION ###
######################

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

#################
### TRACKBARS ###
#################

# Empty callback function for slider updates
def nothing(x):
    pass

# TODO: Make trackbar window
# TODO: Create trackbars. Use variables you defined in the CONSTANTS AND
#       PARAMETERS section to initialize the trackbars. (Section 3.4)

def H_trackbar(val):
    global H_val
    H_val = val
def thold_trackbar(val):
    global thold_val
    thold_val = val

##############
### TIMERS ###
##############

color_threshold_timer = Timer(desc="  color threshold",printflag=True)
contours_timer = Timer(desc="  contours",printflag=FTP)
img_disp_timer = Timer(desc="  display images",printflag=FTP)
# TODO: Add timers for difference image calculation, box filtering, and thresholding (Section 4)
diff_image_timer = Timer(desc="  difference_image",printflag=FTP)
box_filter_timer = Timer(desc="  box filtering",printflag=FTP)
threshold_timer = Timer(desc="  thresholding",printflag=FTP)
#################
### MAIN LOOP ###
#################

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame_start = time.time() # Start timer for whole frame

    #######################
    ### READ INPUT DATA ###
    #######################
    # TODO: Read trackbar positions (Section 3.4)
    H_max = 255
    thold_max = 100
    title_window = 'Track bar'
    trackbar_nameH = 'H max %d' % H_max
    trackbar_nameT = 'thold max %d' % thold_max
    
    cv2.namedWindow(title_window)
    cv2.createTrackbar(trackbar_nameH, title_window, np.uint8(H_val), H_max, H_trackbar)
    cv2.createTrackbar(trackbar_nameT, title_window, np.uint8(thold_val), thold_max, thold_trackbar)

    # Grab raw NumPy array representing the image
    image = frame.array

    ##########################
    ### COLOR THRESHOLDING ###
    ##########################
    color_threshold_timer.start_time()

    # Use difference image method
    if USE_DIFFERENCE_IMAGE == True:
        # thresh = np.zeros_like(image[:, :, 1]) # Delete this line once you add your code (Section 3.2)
        # Calculate difference image
        # TODO: 1) Generate difference image using color subtract function (Section 3.1)
        diff_image_timer.start_time()
        diff_img = color_subtract(image, H_val)
        #cv2.imshow("img", diff_img)
        # TODO: 2) Time function (Section 4)
        diff_image_timer.end_time()
        
        # Box filter
        # TODO: 1) Implement box filter (Section 3.3)
        box_filter_timer.start_time()
        box_img = cv2.boxFilter(diff_img, -1, (5,5))
        #cv2.imshow("img1", box_img)
        # TODO: 2) Time function (Section 4)
        box_filter_timer.end_time()
        print(box_img.shape)
        
        # Threshold
        # TODO: 1) Threshold (Section 3.2)
        # color_threshold_timer.
        threshold_timer.start_time()
        _, thresh = cv2.threshold(box_img, thold_val, 255, cv2.THRESH_BINARY_INV)
        threshold_timer.end_time()
        # cv2.imshow("img1", thresh)
        # TODO: 2) Time function (Section 4)

    # Use HSV range method
    else:
        thresh = np.zeros_like(image[:, :, 1]) # Delete this line once you add your code
        # TODO: Perform HSV thresholding
        # thresh = Your code here

    color_threshold_timer.end_time()

    #########################
    ### BALL LOCALIZATION ###
    #########################
    contours_timer.start_time()
    # Use the heuristic
    if USE_LOCALIZATION_HEURISTIC == True:
        center, radius = identify_ball(thresh, USE_IDX_IMG)

    # Use OpenCV's findContours function
    else:
        center, radius = contours_localization(thresh)

    # Draw the circle
    cv2.circle(image, center, radius, (0,255,0), 2)
    contours_timer.end_time()

    ####################################################
    ### DISPLAY THE IMAGE, DEAL WITH KEYPRESSES, ETC ###
    ####################################################
    # Show the image
    img_disp_timer.start_time()
    cv2.imshow("Raw Image", image)
    # TODO: Show the difference frame (Section 3.1)
    
    # Hint: Show the "thresh" image in a new window called "Difference Image"
    # cv2.namedWindow(title_window)
    
    # cv2.imshow("difference frame", diff_img)

    # TODO: Show the binary frame (Section 3.2)
    cv2.imshow("img1", thresh)
    # cv2.imshow("img1", box_img)
    # cv2.imshow("img1", thresh)

    img_disp_timer.end_time()

    # Get keypress
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    # TODO: if the 'c' key is pressed, capture and display the camera image
    # using pyplot (Section 2)
    if key == ord("c"):
        camera.capture('/home/pi/Desktop/image1.jpg')
        cap = cv2.imread('/home/pi/Desktop/image1.jpg')
        image = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)
        plt.imshow(image)
        plt.show()
    # Show time to process whole frame
    frame_end = time.time()
    elapsed_time = frame_end-frame_start
    print("Frame processed in %.04f s (%02.2f frames per second)"%(elapsed_time, 1.0/elapsed_time))

# Close all windows
cv2.destroyAllWindows()
