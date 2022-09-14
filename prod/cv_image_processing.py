__author__ = ""
__email__ = ""
__phone__ = ""
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Dev"

import cv2 as cv
import numpy as np
import imutils
from imutils import contours, perspective
from scipy.spatial import distance as dist
import os

from prod import VariableClass, ErrorHandlingClass, global_conf_variables

try:
    values = global_conf_variables.get_values()

    GELPhotos = values[0]  # image from GelPhotos folder
    file_type = values[1]
    filtered = values[2]  # image for processing CV
    known_distance = values[7]
    known_width = values[8]
    processed_img = values[9]  # saved processed image location
except Exception as e:
    print(e)

try:
    def load_image():
        file_name = VariableClass.get_latest_image(filtered, file_type)
        img = cv.imread(file_name[1])
        # resize image to 1280x720 - images in GluPhotos are 1920x1080
        # data sheets for camera says images are HD 720p video, resolution 1280x720
        # img = imutils.resize(img, width=1280)
        return img
except Exception as e:
    ErrorHandlingClass.ErrorMessageHandler(e)


def save_image(processed_file, img):
    os.chdir(processed_img)
    cv.imwrite(processed_file, img)


def create_mask(img):
    pts_1080 = np.array([[960, 180], [960, 880], [1200, 880], [1200, 180]], np.int32)
    # pts_720 = np.array([[640, 60], [640, 720], [800, 720], [800, 60]], np.int32)
    mask = np.zeros(img.shape, np.uint8)
    cv.drawContours(mask, [pts_1080], -1, (255, 255, 255), -1, cv.LINE_AA)
    result = cv.bitwise_and(img, mask)
    return result


def color_thresh_HSV(img):
    original = img.copy()
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    hsv_lower = np.array([0, 0, 0])
    hsv_upper = np.array([0, 255, 255])
    mask = cv.inRange(hsv, hsv_lower, hsv_upper)
    result = cv.bitwise_and(original, original, mask=mask)
    return result


def thresholding(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (7, 7), 0)  # Gaussian filter with a 7 x 7 kernel
    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    edged = cv.Canny(gray, 170, 170)
    edged = cv.dilate(edged, None, iterations=1)
    edged = cv.erode(edged, None, iterations=1)
    return edged


def find_dist_less_than_xcentre(xA, yA, x_centre):
    #  finds the distance from 0, yA to xA, yA), if < x_centre, don't process
    #  cv.line(orig, (int(xA), int(yA)), (0, int(yA)), (255, 0, 255), 1)
    file_name = VariableClass.get_latest_image(filtered, file_type)
    dist_left_of_y_centre = (dist.euclidean((xA, yA), (0, yA)))

    if dist_left_of_y_centre >= x_centre:
        return True
    else:
        return False


def create_lines(img_orig, x_centre, xB, yB):
    cv.line(img_orig, (x_centre, x_centre), (x_centre, 0), (0, 255, 255), 1)
    cv.line(img_orig, (x_centre, x_centre), (int(xB), int(yB)), (0, 0, 255), 1)
    cv.line(img_orig, (int(xB), int(yB)), (x_centre, int(yB)), (255, 0, 255), 1)


def add_text_to_lines(orig, img_orig, dist_cam_to_gate, height_in_mm, color, height_of_triangle, mX2, mY2, mX1, mY1):
    #  text for distance in mm side A
    cv.putText(orig, "{:.1f}mm".format(dist_cam_to_gate), (int(mX2), int(mY2 - 10)),
               cv.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

    #  text for distance in mm height
    cv.putText(orig, "{:.1f}mm".format(height_in_mm), (int(mX1), int(mY1 - 10)),
               cv.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
    cv.putText(img_orig, "{:.1f}px".format(height_of_triangle), (int(mX1), int(mY1) - 10),
               cv.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)


def find_area(orig, x_centre, midpoint, xA, yA, xB, yB, color, refObj, img_orig):
    # find base
    create_lines(img_orig, x_centre, xB, yB)
    base = (dist.euclidean((x_centre, x_centre), (x_centre, 0)))

    # find side a
    create_lines(img_orig, x_centre, xB, yB)
    side_a = (dist.euclidean((x_centre, x_centre), (xB, yB)))
    side_a_dist = (dist.euclidean((x_centre, x_centre), (xB, yB)) / refObj[2])
    (mX2, mY2) = midpoint((x_centre, x_centre), (xB, yB))

    # find side b
    side_b = (dist.euclidean((x_centre, 0), (xB, yB)))

    # find area of triangle
    s = (side_b + side_a + base) / 2
    area_of_triangle = (s * (s - side_b) * (s - side_a) * (s - base)) ** 0.5
    height_of_triangle = (area_of_triangle * 2) / base
    create_lines(img_orig, x_centre, xB, yB)
    # height_line = (dist.euclidean((xB, yB), (x_centre, yB)))
    (mX1, mY1) = midpoint((xB, yB), (x_centre, yB))

    result = find_dist_less_than_xcentre(xB, yB, x_centre)

    KNOWN_DISTANCE = known_distance
    KNOWN_WIDTH = known_width
    # RBB = cv.minAreaRect(c)

    b = 47
    height_in_mm = (height_of_triangle * KNOWN_WIDTH) / b
    # print(height_in_mm)

    f = 9
    dist_cam_to_gate = (side_a * KNOWN_WIDTH) / f

    add_text_to_lines(orig, img_orig, dist_cam_to_gate, height_in_mm, color, height_of_triangle, mX2, mY2, mX1, mY1)

    focal_length = (height_of_triangle * KNOWN_DISTANCE) / KNOWN_WIDTH
    fl_to_dist = (KNOWN_WIDTH * focal_length) / height_of_triangle
    # print(focal_length, fl_to_dist, 'ff', height_in_mm)

    return side_a_dist, fl_to_dist, height_of_triangle, height_in_mm, dist_cam_to_gate, result


def cv_processing():
    img = load_image()
    img_orig = img.copy()
    img = create_mask(img)
    img = color_thresh_HSV(img)
    edged = thresholding(img)

    dists = []
    pix_coords = []

    x_centre = round(img.shape[1] / 2)
    y_centre = round(img.shape[0] / 2)

    # find contours in the edge map
    cnts = cv.findContours(edged.copy(), cv.RETR_EXTERNAL,
                           cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # sort the contours from left-to-right and, then initialize the
    # distance colors and reference object
    (cnts, _) = contours.sort_contours(cnts)
    # colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255), (255, 255, 0),
    #           (255, 0, 255))
    colors = (255, 0, 255)

    refObj = None

    width = 370  # tweak this to get actual distance from cam to tailgate

    def midpoint(ptA, ptB):
        return (ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5

    for C in cnts:
        # ignore small contours
        if cv.contourArea(C) < 30:
            continue

        # compute the rotated bounding box of the contour
        box = cv.minAreaRect(C)
        box = cv.boxPoints(box) if imutils.is_cv2() else cv.boxPoints(box)

        box = perspective.order_points(box)

        # compute the center of the bounding box
        cX = np.average(box[:, 0])
        cY = np.average(box[:, 1])

        if refObj is None:
            (tl, tr, br, bl) = box
            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)
            # compute the Euclidean distance between the midpoints, construct the reference object
            D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
            refObj = (box, (cX, cY), D / width)
            continue

        orig = img.copy()
        cv.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 1)
        cv.drawContours(orig, [refObj[0].astype("int")], -1, (0, 255, 0), 1)

        refCoords = np.vstack([refObj[0], refObj[1]])
        objCoords = np.vstack([box, (cX, cY)])

        ((xA, yA), (xB, yB), color) = (refCoords[3], objCoords[3], colors)  # get 4th point in the BB, clockwise
        cv.circle(img_orig, (int(xB), int(yB)), 5, color, -1)

        (side_a_dist, fl_to_dist, height_in_mm, dist_cam_to_gate, height_of_triangle, result) = find_area(orig,
                                                                                                          x_centre,
                                                                                                          midpoint, xA,
                                                                                                          yA, xB, yB,
                                                                                                          color,
                                                                                                          refObj,
                                                                                                          img_orig)

        # cv.imshow("Image", orig)
        # cv.waitKey(0)

        dists.append(int(dist_cam_to_gate))  # distance from camera to object
        dists.append(int(height_in_mm))  # distance in mm from chain to object
        dists.append(int(height_of_triangle))
        pix_coords.append(int(xA))
        pix_coords.append(int(yA))
        pix_coords.append(int(xB))
        pix_coords.append(int(yB))
        dists.append(bool(result))

        result = find_dist_less_than_xcentre(xB, yB, x_centre)
        if result is True:
            file_name = VariableClass.get_latest_image(filtered, file_type)
            save_image(file_name[1], img_orig)
        else:
            pass

        return dists, pix_coords

