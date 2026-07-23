from typing import Optional

import requests
import allure
from requests import Response

from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel


class CrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel] = None) -> Response:
        body = model.model_dump() if model is not None else ""
        url = f"{Config.fetch("backendUrl")}{self.endpoint.value.url}"

        with allure.step(f"POST {url}"):
            allure.attach(str(body), "Request body", allure.attachment_type.JSON)

            response = requests.post(
                url = url,
                headers = self.request_spec,
                json = body
            )
            allure.attach(
                response.text,
                "Response body",
                allure.attachment_type.JSON
            )

        self.response_spec(response)
        return response

    def delete(self, user_id: int) -> Response:
        url = f"{Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id}"

        with allure.step(f"DELETE {url}"):

            response = requests.delete(
                url = url,
                headers = self.request_spec,
            )

            allure.attach(
                response.text,
                "Response body",
                allure.attachment_type.JSON
            )

        self.response_spec(response)
        return response
