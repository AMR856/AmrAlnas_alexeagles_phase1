#!/usr/bin/env python3
import cv2 as cv
import numpy as np
from helper_functions import filtering_small_contours, checking_contour_type, checking_inner_diameter_condition, taking_user_input

if __name__ == '__main__':
    
    # Reading the ideal and worn images and making blank images to draw contours on
    ideal_image = cv.imread('./task_images/ideal.jpg')
    worn_sample = cv.imread('./task_images/sample3.jpg')
    blank_ideal = np.zeros(ideal_image.shape, dtype='uint8')
    blank_worn = np.zeros(ideal_image.shape, dtype='uint8')
    blank_contours = np.zeros(ideal_image.shape, dtype='uint8')
    inner_diameter_mask_blank = np.zeros(ideal_image.shape[:2], dtype='uint8')

    ## Converting the images from BGR to Grayscale
    ideal_image_gray = cv.cvtColor(ideal_image, cv.COLOR_BGR2GRAY)
    sample_image_gray = cv.cvtColor(worn_sample, cv.COLOR_BGR2GRAY)

    mask = cv.circle(inner_diameter_mask_blank, (ideal_image.shape[1]//2, ideal_image.shape[0]//2), 110, 255, -1)
    inverted_mask = cv.bitwise_not(mask)

    masked_image_ideal = cv.bitwise_and(ideal_image_gray, ideal_image_gray, mask=mask)
    inverted_mask_image_ideal = cv.bitwise_and(ideal_image_gray, ideal_image_gray, mask=inverted_mask)
    masked_image_worn = cv.bitwise_and(sample_image_gray, sample_image_gray, mask=mask)
    inverted_mask_image_worn = cv.bitwise_and(sample_image_gray, sample_image_gray, mask=inverted_mask)

    diameter_condition, difference_inner_diameter = checking_inner_diameter_condition(masked_image_ideal, masked_image_worn, blank_contours)
    ## Thresholding the ideal and worn images
    threshold_ideal, thresh_ideal = cv.threshold(inverted_mask_image_ideal, 90, 255, cv.THRESH_BINARY)
    threshold_worn, thresh_worn = cv.threshold(inverted_mask_image_worn, 90, 255, cv.THRESH_BINARY)

    ## Taking XOR Bitwise to get the difference between the worn and the ideal
    differnce_image = cv.bitwise_xor(thresh_ideal, thresh_worn)
    overall_difference = differnce_image.copy()
    if diameter_condition != 'Normal':
        overall_difference = cv.bitwise_or(differnce_image, difference_inner_diameter)
    # Finding contours on the ideal, worn, and difference image (The program itself only needs the difference contours)
    contours_ideal , hierarchies_ideal = cv.findContours(thresh_ideal, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    contours_worn , hierarchies_worn = cv.findContours(thresh_worn, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    differnce_contours , hierarchies_difference = cv.findContours(differnce_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    # Getting the long contours (Removing the noise you can say)
    long_difference_contours = filtering_small_contours(differnce_contours)

    # Drawing contours on all the blank images
    cv.drawContours(blank_ideal, contours_ideal, -1, (0, 0, 255), 1)
    cv.drawContours(blank_worn, contours_worn, -1, (0, 0, 255), 1)
    cv.drawContours(blank_contours, long_difference_contours, -1, (0, 0, 255), 1)
    worn_teeth_count = 0
    missing_teeth_count = 0
    worn_teeth_count, missing_teeth_count = checking_contour_type(long_difference_contours, worn_teeth_count, missing_teeth_count)
    print(f'Number of missing teeth: {missing_teeth_count}')
    print('-------------------')
    print('-------------------')
    print(f'Number of worn teeth: {worn_teeth_count}')
    print('-------------------')
    print('-------------------')
    print(f'The condition of the inner diameter is: {diameter_condition}')
    cv.imshow('Difference', overall_difference)
    cv.imshow('Differnce Contours', blank_contours)
    cv.waitKey(0)
