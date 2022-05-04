import os
import cv2
import detect
import base64
import config
import numpy as np
import logging

from PIL import Image
from screenshot import HttpService


class WidgetsCoordinates:
    def __init__(self):
        self.widget_coordinate_1 = []
        self.widget_coordinate_2 = []
        self.run_device = config.RUN_DEVICE

    @staticmethod
    def convert_save_65(base64_img, screenshot_path):
        try:
            path_exists = os.path.exists(screenshot_path)

            if not path_exists:
                os.mkdir(screenshot_path)

            with open(os.path.join(screenshot_path, config.SS_PATH), mode='wb') as file:
                file.write(base64.decodebytes(base64_img))

            image_path = os.path.join(screenshot_path, config.SS_PATH)

            return image_path
        except Exception as e:
            message = f'Something went wrong with converting image to normal rgb image, message: {e}'
            logging.error(message, exc_info=True)
            raise ValueError(message)

    def find_coordinate(self):
        try:
            opt = detect.parse_opt()
            screenshot_obj = HttpService(config.API_KEY, config.UC_SCREENSHOT_API_URL)
            status, img64 = screenshot_obj.post(opt.input_url)
            usr_img_path = self.convert_save_65(img64, 'media/')

            return usr_img_path
        except Exception as e:
            message = f'Something went wrong with getting screenshot path, message: {e}'
            logging.error(message, exc_info=True)
            raise ValueError(message)

    def inference(self):
        try:
            opt = detect.parse_opt()
            screenshot_path = self.find_coordinate()

            img = np.asarray(Image.open(screenshot_path))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            opt.source = screenshot_path
            opt.device = self.run_device
            opt.weights = 'weights/best.pt'
            widget_coordinate_1, widget_coordinate_2, widget_names = detect.main(opt)

            return widget_coordinate_2, img.shape, widget_names
        except Exception as e:
            message = f'Something went wrong with getting coordinates and widget names, message: {e}'
            logging.error(message, exc_info=True)
            raise ValueError(message)
