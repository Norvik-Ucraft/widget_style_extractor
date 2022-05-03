import os
import detect
import base64
import config

from screenshot import HttpService


def convert_save_65(base64_img, screenshot_path):
    path_exists = os.path.exists(screenshot_path)

    if not path_exists:
        os.mkdir(screenshot_path)

    with open(os.path.join(screenshot_path, config.SS_PATH), mode='wb') as file:
        file.write(base64.decodebytes(base64_img))

    image_path = os.path.join(screenshot_path, config.SS_PATH)

    return image_path


def find_coordinate():
    opt = detect.parse_opt()
    screenshot_obj = HttpService(config.API_KEY, config.UC_SCREENSHOT_API_URL)
    status, img64 = screenshot_obj.post(opt.input_url)
    usr_img_path = convert_save_65(img64, 'media/')

    return usr_img_path


def inference(screenshot_path, run_device='0'):
    opt = detect.parse_opt()
    opt.source = screenshot_path
    opt.device = run_device
    opt.weights = 'weights/best.pt'
    widget_coordinate_1, widget_coordinate_2 = detect.main(opt)

    return widget_coordinate_2


screenshot_path = find_coordinate()
coordinates = inference(screenshot_path)
