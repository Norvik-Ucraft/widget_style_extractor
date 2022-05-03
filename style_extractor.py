import os
import re
import detect
import config
import logging

from selenium import webdriver
from main import WidgetsCoordinates
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


class StyleExtractor:
    def __init__(self):
        self.driver = None
        self.coordinate_list = []
        self.computed_style = []

    def widget_coordinates(self):
        options = Options()
        coordinates = WidgetsCoordinates()
        opt = detect.parse_opt()

        options.headless = True
        service = Service('./driver/geckodriver.exe')
        get_coordinates, image_shape = coordinates.inference()

        for coordinates_tuple in get_coordinates:
            self.coordinate_list.append(coordinates_tuple['center'])

        self.driver = webdriver.Firefox(service=service, options=options)
        self.driver.get(opt.input_url)

        return image_shape
