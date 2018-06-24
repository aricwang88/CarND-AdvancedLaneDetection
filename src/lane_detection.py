import vision_util as vu
import numpy as np
import matplotlib.pyplot as plt

def filter_pipeline(src_img):
    '''
    Returns gradient and color filtered image.
    '''
    sobelx_thresh = (20, 230)
    hls_saturation_thresh = (180, 255)
    # Get Sobel(x)-filtered binary image.
    sobelx_binary = vu.abs_sobel_thresh(src_img, orient='x', thresh=sobelx_thresh)
    # Get Saturation-channel-thresholded binary image.
    hls_binary = vu.hls_select(src_img, thresh=hls_saturation_thresh)
    # Combined binary image having color and gradient thresholds applied.
    combined_binary = np.zeros_like(sobelx_binary)
    combined_binary[(sobelx_binary == 1) | (hls_binary == 1)] = 1
    return combined_binary


def calibration_pipeline():
    '''
    # Calibrates camera to undistort images.
    '''
    mtx, dist = vu.compute_calibration_matrix()
    vu.save_calibration_matrix(mtx, dist)
    # distort_test = vu.load_image('../camera_cal/calibration1.jpg')


def perspective_transform_pipeline(mtx, dist, img_path='../test_images/straight_lines1.jpg'):
    '''
    Finds the perspective-transform matrix which converts a source image to its bird's eye view form.
    :param mtx: Calibration matrix.
    :param dist: Distortion coefficients.
    :param img_path: Path of the sample path with which the transformation matrix would be found.
    :return: Perspective transform matrix.
    '''
    # Finding perspective transformation matrix to get bird's eye view on images.
    src_image = vu.load_image(img_path)
    undistorted = vu.undistort_image(src_image, mtx, dist)
    return vu.find_perspective_transform(undistorted)


def warp_pipeline(src_img, ptrans_mat):
    warped = vu.warp(src_img, ptrans_mat)
    binary_warped = filter_pipeline(warped)
    # vu.plot_transformed_image(
    #     src_img, binary_warped, 'Warped Image', 'Warped Binary Image', gray_cmap=True)
    return binary_warped


if __name__ == '__main__':
    mtx, dist = vu.load_calibration_matrix()
    ptrans_mat = perspective_transform_pipeline(mtx, dist)

    # Warp pipeline. Returns binarized warped image.
    src_img = vu.load_image('../test_images/test3.jpg')
    binary_warped = warp_pipeline(src_img, ptrans_mat)

    lane_lines_img, left_fit, right_fit = vu.lane_detection_pipeline(
        binary_warped, visualize_lane=True)
    vu.calculate_curvature(lane_lines_img, left_fit, right_fit)