import os

import cv2

import detect
import base64
import config
import numpy as np

from PIL import Image
from screenshot import HttpService


class WidgetsCoordinates:
    def __init__(self):
        self.widget_coordinate_1 = []
        self.widget_coordinate_2 = []
        self.run_device = config.RUN_DEVICE

    @staticmethod
    def convert_save_65(base64_img, screenshot_path):
        path_exists = os.path.exists(screenshot_path)

        if not path_exists:
            os.mkdir(screenshot_path)

        with open(os.path.join(screenshot_path, config.SS_PATH), mode='wb') as file:
            file.write(base64.decodebytes(base64_img))

        image_path = os.path.join(screenshot_path, config.SS_PATH)

        return image_path

    def find_coordinate(self):
        opt = detect.parse_opt()
        screenshot_obj = HttpService(config.API_KEY, config.UC_SCREENSHOT_API_URL)
        status, img64 = screenshot_obj.post(opt.input_url)
        usr_img_path = self.convert_save_65(img64, 'media/')

        return usr_img_path

    def inference(self):
        opt = detect.parse_opt()
        screenshot_path = self.find_coordinate()

        img = np.asarray(Image.open(screenshot_path))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        opt.source = screenshot_path
        opt.device = self.run_device
        opt.weights = 'weights/best.pt'
        widget_coordinate_1, widget_coordinate_2 = detect.main(opt)

        return widget_coordinate_2, img.shape


output = WidgetsCoordinates()
output.find_coordinate()