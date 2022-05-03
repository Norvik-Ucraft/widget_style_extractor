import requests
import logging


class HttpService:
    def __init__(self, api_key: str, service_url: str, content_type='application/json'):
        """
        :param api_key: Key to use the screenshot service.
        :param service_url: The url of the service that you need to do a request.
        :param content_type: The type of components passed.
        """
        self.service_url = service_url
        self.headers = {
            'x-uc-api-key': f'{api_key}',
            'Content-Type': f'{content_type}',
        }

    def post(self, url: str):
        """Takes fullpage screenshot from the provided url.
        :param url: The url to take the fullpage screenshot
        :return: A tuple of response status and the path to the taken screenshot.
        """
        try:
            is_success = True
            r = requests.post(
                self.service_url,
                headers=self.headers,
                data=f'{{\n  "page_url": "{url}",\n  "full_page": true\n}}'
            )
            if r.status_code == 201:
                result = r.text.split(',')[1]
                result = result.encode()
                return is_success, result
            else:
                is_success = False
                return is_success, r.status_code
        except Exception as e:
            message = f'Something went wrong with taking fullpage screenshot, :message {str(e)}'
            logging.error(message, exc_info=True)
