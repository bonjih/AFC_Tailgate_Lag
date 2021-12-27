import math

import cv2 as cv
import numpy as np
import imutils
from imutils import contours, perspective
from scipy.spatial import distance as dist
import glob
import os


# load recent image
def load_image(configs):
    global latest_file  # file name to global used only for function save_image()
    global known_distance
    global known_width

    known_distance = configs[6]
    known_width = configs[7]
    file_type = configs[1]

    list_of_files = glob.glob('./*.{}'.format(file_type))

    latest_file = max(list_of_files, key=os.path.getctime)
    file_name = latest_file[2:]
    img = cv.imread(file_name)
    # resize image to 1280x720 - images in GluPhotos are 1920x1080
    # data sheets for camera says images are HD 720p video, resolution 1280x720
    # img = imutils.resize(img, width=1280)
    return img


def save_image(processed_file, img):
    file_name = processed_file
    path = './saved_processed_images/'
    cv.imwrite(os.path.join(path, file_name), img)


def create_mask(img):
    img = load_image(img)
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


def find_area(orig, x_centre, midpoint, xA, yA, color, refObj):
    # find base
    cv.line(orig, (x_centre, x_centre), (x_centre, 0), (0, 255, 255), 1)
    base = (dist.euclidean((x_centre, x_centre), (x_centre, 0)))

    # find side a
    cv.line(orig, (x_centre, x_centre), (int(xA), int(yA)), color, 2)
    side_a = (dist.euclidean((x_centre, x_centre), (xA, yA)))
    side_a_dist = (dist.euclidean((x_centre, x_centre), (xA, yA)) / refObj[2])
    (mX2, mY2) = midpoint((x_centre, x_centre), (xA, yA))

    # find side b
    cv.line(orig, (x_centre, 0), (int(xA), int(yA)), color, 2)
    side_b = (dist.euclidean((x_centre, 0), (xA, yA)))

    # find area of triangle
    s = (side_b + side_a + base) / 2
    area_of_triangle = (s * (s - side_b) * (s - side_a) * (s - base)) ** 0.5
    height_of_triangle = (area_of_triangle * 2) / base

    a = 150
    b = 9
    c = (height_of_triangle * a) / b

    e = 150
    f = 9
    g = (side_a * e) / f

    cv.putText(orig, "{:.1f}mm".format(g), (int(mX2), int(mY2 - 10)),
               cv.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

    KNOWN_DISTANCE = known_distance
    KNOWN_WIDTH = known_width
    # RBB = cv.minAreaRect(c)

    focal_length = (height_of_triangle * KNOWN_DISTANCE) / KNOWN_WIDTH
    fl_to_dist = (KNOWN_WIDTH * focal_length) / height_of_triangle
    print(focal_length, fl_to_dist, 'ff', c)

    return side_a_dist, fl_to_dist, height_of_triangle, c, g


def cv_processing(img):
    img = create_mask(img)
    img = color_thresh_HSV(img)

    dists = []
    pix_coords = []

    img_shape_x = img.shape[1]
    img_shape_y = img.shape[0]

    x_centre = round(img_shape_x / 2)
    y_centre = round(img_shape_y / 2)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (7, 7), 0)  # Gaussian filter with a 7 x 7 kernel

    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    edged = cv.Canny(gray, 170, 170)
    edged = cv.dilate(edged, None, iterations=1)
    edged = cv.erode(edged, None, iterations=1)

    # find contours in the edge map
    cnts = cv.findContours(edged.copy(), cv.RETR_EXTERNAL,
                           cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # sort the contours from left-to-right and, then initialize the
    # distance colors and reference object
    (cnts, _) = contours.sort_contours(cnts)
    colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255), (255, 255, 0),
              (255, 0, 255))

    refObj = None

    width = 370  # tweak this to get actual distance from cam to tailgate

    def midpoint(ptA, ptB):
        return (ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5

    for c in cnts:
        # ignore small contours
        if cv.contourArea(c) < 30:
            continue

        # compute the rotated bounding box of the contour
        box = cv.minAreaRect(c)
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
        cv.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
        cv.drawContours(orig, [refObj[0].astype("int")], -1, (0, 255, 0), 2)

        refCoords = np.vstack([refObj[0], refObj[1]])
        objCoords = np.vstack([box, (cX, cY)])

        for ((xA, yA), (xB, yB), color) in zip(refCoords, objCoords, colors):
            cv.circle(orig, (int(xA), int(yA)), 5, color, -1)
            cv.circle(orig, (int(xB), int(yB)), 5, color, -1)
            # cv.line(orig, (int(xA), int(yA)), (int(xB), int(yB)),
            #         color, 2)

            # compute the Euclidean distance between the coordinates,
            # and then convert the distance in pixels to distance in units
            # d = (dist.euclidean((xA, yA), (xB, yB)) / refObj[2]) / 25.4
            # (mX, mY) = midpoint((xA, yA), (xB, yB))
            # cv.putText(orig, "{:.1f}mm".format(d), (int(mX), int(mY - 10)),
            #            cv.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
            #
            # str_coords = (str(xB) + " / " + str( yB))
            # cv.putText(orig, str(str_coords), (int(xB), int(yB)), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

            # compute the Euclidean distance between x_centre and object (tailgate), by making triangles
            # get height of triangle to base (x_centre)
            # and then convert the distance in pixels to distance in units

            a = int(xA) - x_centre

            (side_a_dist, fl_to_dist, c, g, height_of_triangle) = find_area(orig, x_centre, midpoint, xA, yA, color,
                                                                            refObj)

            # cv.imshow("Image", orig)
            # cv.waitKey(0)

            dists.append(int(g))  # distance from camera to object
            dists.append(int(c))
            dists.append(int(height_of_triangle))
            pix_coords.append(int(xA))
            pix_coords.append(int(yA))
            pix_coords.append(int(xB))
            pix_coords.append(int(yB))

        save_image(latest_file, orig)

        return dists, pix_coords
