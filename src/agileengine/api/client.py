import logging
import requests
from http import HTTPStatus

log = logging.getLogger('client')


class ImageClient:

    # TODO: fetch async
    base_url = "http://interview.agileengine.com"
    timeout = 3

    def __init__(self, api_key):
        self.api_key = api_key

    def get_images(self, page_num):
        headers = self._prepare_headers()
        if headers:
            url = f"{self.base_url}/images/?page={page_num}"
            resp = requests.get(url, headers=headers, timeout=self.timeout)
            if resp.status_code == HTTPStatus.OK:
                try:
                    images_data = resp.json()
                except ValueError:
                    log.error("Error parsing images response from url: %s", url)
                    return
                else:
                    return images_data
        else:
            return {}

    def get_image_details(self, image_id):
        headers = self._prepare_headers()
        if headers and image_id:
            url = f"{self.base_url}/images/{image_id}/"
            resp = requests.get(url, headers=headers, timeout=self.timeout)
            if resp.status_code == HTTPStatus.OK:
                try:
                    images_data = resp.json()
                except ValueError:
                    log.error("Error parsing images details response from url: %s", url)
                    return
                else:
                    return images_data
        else:
            return {}

    def _fetch_token(self):
        resp = requests.post(f"{self.base_url}/auth", json={"apiKey": self.api_key}, timeout=self.timeout)
        if resp.status_code == HTTPStatus.OK:
            try:
                token_data = resp.json()
            except ValueError:
                log.error("Error parsing auth token response")
                return
        else:
            log.warning("Error fetching auth token")
            return

        if token_data.get("auth") is True:
            return token_data.get("token")
        else:
            log.warning("Error fetching auth token")

    def _prepare_headers(self):
        token = self._fetch_token()
        if token:
            return {
                "Authorization": self._fetch_token(),
            }
        return {}