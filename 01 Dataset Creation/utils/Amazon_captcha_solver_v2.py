#!/usr/bin/env python3
import random
import bezier
import pyautogui
import numpy as np
from time import sleep
from random import uniform as randfloat
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.keys import Keys
import time


def slow_type(element, text: str):
    """Send a text to an element one character at a time with a delay."""
    for character in text:
        element.send_keys(character)
        sleep(randfloat(0.05, 0.3))
    element.send_keys(Keys.ENTER)


def resting_mouse(driver):
    """move mouse to right of screen."""

    panelWidht = driver.execute_script('return window.outerWidth;')
    start = pyautogui.position()
    end = random.randint(panelWidht - 100, panelWidht), random.randint(400, 850)

    x2 = (start[0] + end[0]) / 2  # midpoint x
    y2 = (start[1] + end[1]) / 2  ##midpoint y

    control1X = (start[0] + x2) / 2
    control2X = (end[0] + x2) / 2

    # Two intermediate control points that may be adjusted to modify the curve.
    control1 = control1X, y2  ##combine midpoints to create perfect curve
    control2 = control2X, y2  ## using y2 for both to get a more linear curve

    # Format points to use with bezier
    control_points = np.array([start, control1, control2, end])
    points = np.array([control_points[:, 0], control_points[:, 1]])  # Split x and y coordinates
    # You can set the degree of the curve here, should be less than # of control points
    degree = 3
    # Create the bezier curve
    curve = bezier.Curve(points, degree)

    curve_steps = 70  # How many points the curve should be split into. Each is a separate pyautogui.moveTo() execution
    delay = 0.008  # Time between movements. 1/curve_steps = 1 second for entire curve

    # Move the mouse
    for j in range(1, curve_steps + 1):
        # The evaluate method takes a float from [0.0, 1.0] and returns the coordinates at that point in the curve
        # Another way of thinking about it is that i/steps gets the coordinates at (100*i/steps) percent into the curve
        x, y = curve.evaluate(j / curve_steps)
        pyautogui.moveTo(x, y)  # Move to point in curve
        pyautogui.sleep(delay)  # Wait delay
    sleep(2)


def bezier_mouse(location, size, panelHeight):  ##move mouse to middle of element
    x, relY = location["x"], location["y"]  ##abs X and relative Y
    absY = relY + panelHeight
    w, h = size["width"], size["height"]
    wCenter = w / 2
    hCenter = h / 2
    xCenter = int(wCenter + x)
    yCenter = int(hCenter + absY)

    start = pyautogui.position()
    end = xCenter, yCenter

    x2 = (start[0] + end[0]) / 2  # midpoint x
    y2 = (start[1] + end[1]) / 2  ##midpoint y

    control1X = (start[0] + x2) / 2
    control1Y = (end[1] + y2) / 2

    control2X = (end[0] + x2) / 2
    control2Y = (start[1] + y2) / 2

    # Two intermediate control points that may be adjusted to modify the curve.
    control1 = control1X, y2  ##combine midpoints to create perfect curve
    control2 = control2X, y2

    # Format points to use with bezier
    control_points = np.array([start, control1, control2, end])
    points = np.array([control_points[:, 0], control_points[:, 1]])  # Split x and y coordinates
    # You can set the degree of the curve here, should be less than # of control points
    degree = 3

    # Create the bezier curve
    curve = bezier.Curve(points, degree)

    curve_steps = 70  # How many points the curve should be split into. Each is a separate pyautogui.moveTo() execution
    delay = 0.008  # Time between movements. 1/curve_steps = 1 second for entire curve

    # Move the mouse
    for j in range(1, curve_steps + 1):
        # The evaluate method takes a float from [0.0, 1.0] and returns the coordinates at that point in the curve
        # Another way of thinking about it is that i/steps gets the coordinates at (100*i/steps) percent into the curve
        x, y = curve.evaluate(j / curve_steps)
        pyautogui.moveTo(x, y)  # Move to point in curve
        pyautogui.sleep(delay)  # Wait delay


def custom_Amazon_captcha_solver(driver, driver_close=False):
    # Disable pyautogui pauses
    pyautogui.MINIMUM_DURATION = 0
    pyautogui.MINIMUM_SLEEP = 0
    pyautogui.PAUSE = 0
    # avoid Exception when mouse if in a top corner
    pyautogui.FAILSAFE = False

    # instanciate Chrome websriver
    # driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(0.5)

    try:
        driver.get("https://www.amazon.com/errors/validateCaptcha")
    except TimeoutException:
        driver.execute_script("window.stop();")

    link_xpath = '/html/body/div[1]/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img'
    captcha_link = driver.find_element(By.XPATH, link_xpath).get_attribute('src')


    captcha = AmazonCaptcha.fromlink(captcha_link)  # pass it to `fromlink` class method
    solution = captcha.solve()

    sleep(2)
    e1 = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div/form/div[1]/div/div/h4')
    e2 = driver.find_element(By.XPATH, '//*[@id="captchacharacters"]')

    panelHeight = driver.execute_script('return window.outerHeight - window.innerHeight;')

    location1 = e1.location  ## coords of element1
    location2 = e2.location  ## coords of element2
    size1 = e1.size  ## size of element1
    size2 = e2.size  ## size of element2
    sleep(3)
    bezier_mouse(location1, size1, panelHeight)
    e1.click()
    sleep(2)
    bezier_mouse(location2, size2, panelHeight)
    slow_type(e2, solution)
    sleep(2)
    resting_mouse(driver)
    sleep(2)

    if driver_close:
        driver.close()
