from typing import Tuple
import numpy as np
import cv2 as cv
import sys
from fixed_values import inner_diameter_normal_size, minimum_value_missing_teeth, maximum_value_missing_teeth, valid_choices

def filtering_small_contours(all_contours: Tuple[np.ndarray]) -> list:
    """
    Finds and returns large contours that represent worn or missing teeth 
    or the diameter of the gear.

    Args:
        all_contours (list[np.ndarray]): All contours found in the image.

    Returns:
        list[np.ndarray]: A list of large contours.
    """
    long_difference_contours = []
    for contour in all_contours:
        if len(contour) >= 15:
            long_difference_contours.append(contour)
    return long_difference_contours

def checking_contour_type(contours: list[np.ndarray], worn_teeth_count: int, missing_teeth_count: int) -> Tuple[int, int]:
    """
    Checks if the contour is worn or missing from its area

    Args:
        contours (list[np.ndarray]): All contours found in the image (Except the inner diameter).
        worn_teeth_count (int): The current count of the worn teeth in the image
        missing_teeth_count (int): The current count of the missing teeth in the image

    Returns:
        Tuple[int, int]: A tuple contains the current count of the missing and worn teeth
    """
    contour_area = 0
    for contour in contours:
        contour_area = cv.contourArea(contour)
        if contour_area >= minimum_value_missing_teeth and contour_area <= maximum_value_missing_teeth :
            missing_teeth_count += 1
        else:
            worn_teeth_count += 1
    return (worn_teeth_count, missing_teeth_count)

def checking_inner_diameter_condition(ideal: np.ndarray, worn_sample: np.ndarray, blank: np.ndarray) -> list[str, np.ndarray]:
    """
    Checks the condition of the inner diameter (Missing, Bigger, Smaller) and it returns
    it as a string, also return the XORed porition of the inner diameter to XOR it with
    the another part of the image

    Args:
        ideal (np.ndarray): The masked ideal image (only the diameter portion of the image is given)
        worn_sample (np.ndarray): The worn sample image (only the diameter portion of the image is given)
        blank (np.ndarray): A blank image to draw contours on

    Returns:
        list[str, np.ndarray]: The condition of the inner diameter and the XORed portion
    """
    _, thresh_ideal = cv.threshold(ideal, 90, 255, cv.THRESH_BINARY)
    _, thresh_worn = cv.threshold(worn_sample, 90, 255, cv.THRESH_BINARY)
    difference = cv.bitwise_xor(thresh_ideal, thresh_worn)
    differnce_contour , _ = cv.findContours(difference,
                                            cv.RETR_EXTERNAL,
                                            cv.CHAIN_APPROX_NONE)
    cv.drawContours(blank, differnce_contour, -1, (0, 0, 255), 1)
    try:
        contour_area = cv.contourArea(differnce_contour[0])
    except IndexError as err:
        return ['Normal', None]
    if contour_area == inner_diameter_normal_size:
        return ['Missing', difference]
    elif contour_area > inner_diameter_normal_size:
        return ['Bigger', difference]
    else:
        return ['Smaller', difference]

def taking_user_input() -> str:
    """
    Tasks the user input to know which sample image to use

    Args:
        void

    Returns:
        file_name (str): The file name of the sample
    """
    with open('./task_images/Samples Description.txt', 'r', encoding='utf8') as file:
        lines = file.readlines()
        for line in lines[1:]:
            print(line, end='')
        print('')
    print('Which sample Do you want to try: ', end='')
    file_name = ''
    choice = input()
    if int(choice) in valid_choices:
        file_name = f'./task_images/sample{str(choice)}.jpg'
        return file_name
    else:
        print('Invalid sample number')
        sys.exit(1)
