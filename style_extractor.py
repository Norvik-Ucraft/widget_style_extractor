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

    def get_computed_style(self):
        image_size = self.widget_coordinates()
        self.driver.set_window_size(image_size[1], image_size[0])

        for coordinates_pair in self.coordinate_list:
            element = self.driver.execute_script("return document.elementFromPoint(arguments[0], arguments[1])",
                                                 coordinates_pair[0], coordinates_pair[1])
            if element:
                css_property = self.driver.execute_script("return window.getComputedStyle(arguments[0], null);", element)
                keys = list(css_property.keys())[:]
                temp_computed_style = {}
                for key in keys:
                    key_number = re.findall(config.KEY_PATTERN, key)
                    uppercase_selector = re.findall(config.UPPERCASE_PATTERN, key)
                    extra_selector = re.findall(config.EXTRA_PATTERN, key)

                    if not key_number and not uppercase_selector and not extra_selector:
                        temp_computed_style[key] = css_property[key]

                self.computed_style.append(temp_computed_style)

        self.driver.quit()
        return self.computed_style
