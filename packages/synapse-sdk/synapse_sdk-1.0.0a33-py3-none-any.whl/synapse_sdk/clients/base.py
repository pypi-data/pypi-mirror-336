import json
import os
from pathlib import Path

import requests

from synapse_sdk.clients.exceptions import ClientError
from synapse_sdk.utils.file import files_url_to_path_from_objs


class BaseClient:
    name = None
    base_url = None

    def __init__(self, base_url):
        self.base_url = base_url
        requests_session = requests.Session()
        self.requests_session = requests_session

    def _get_url(self, path):
        if not path.startswith(self.base_url):
            return os.path.join(self.base_url, path)
        return path

    def _get_headers(self):
        return {}

    def _request(self, method: str, path: str, **kwargs) -> dict | str:
        """Request handler for all HTTP methods.

        Args:
            method (str): HTTP method to use.
            path (str): URL path to request.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            dict | str: JSON response or text response.
        """
        url = self._get_url(path)
        headers = self._get_headers()
        headers.update(kwargs.pop('headers', {}))

        # List to store opened files to close after request
        opened_files = []

        if method in ['post', 'put', 'patch']:
            # If files are included in the request, open them as binary files
            if kwargs.get('files') is not None:
                for name, file in kwargs['files'].items():
                    # Handle both string and Path object cases
                    if isinstance(file, str):
                        file = Path(file)
                    if isinstance(file, Path):
                        opened_file = file.open(mode='rb')
                        kwargs['files'][name] = (file.name, opened_file)
                        opened_files.append(opened_file)
                if 'data' in kwargs:
                    for name, value in kwargs['data'].items():
                        if isinstance(value, dict):
                            kwargs['data'][name] = json.dumps(value)
            else:
                headers['Content-Type'] = 'application/json'
                if 'data' in kwargs:
                    kwargs['data'] = json.dumps(kwargs['data'])

        try:
            # Send request
            response = getattr(self.requests_session, method)(url, headers=headers, **kwargs)
            if not response.ok:
                raise ClientError(
                    response.status_code, response.json() if response.status_code == 400 else response.reason
                )
        except requests.ConnectionError:
            raise ClientError(408, f'{self.name} is not responding')

        # Close all opened files
        for opened_file in opened_files:
            opened_file.close()

        return self._post_response(response)

    def _post_response(self, response):
        try:
            return response.json()
        except ValueError:
            return response.text

    def _get(self, path, url_conversion=None, pydantic_model=None, **kwargs):
        """
        Perform a GET request and optionally convert response to a pydantic model.

        Args:
            path (str): URL path to request.
            url_conversion (dict, optional): Configuration for URL to path conversion.
            pydantic_model (Type, optional): Pydantic model to convert the response to.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            The response data, optionally converted to a pydantic model.
        """
        response = self._request('get', path, **kwargs)

        if url_conversion:
            if url_conversion['is_list']:
                files_url_to_path_from_objs(response['results'], **url_conversion, is_async=True)
            else:
                files_url_to_path_from_objs(response, **url_conversion)

        if pydantic_model:
            return self._validate_response_with_pydantic_model(response, pydantic_model)

        return response

    def _post(self, path, pydantic_model=None, **kwargs):
        response = self._request('post', path, **kwargs)
        if pydantic_model:
            return self._validate_response_with_pydantic_model(response, pydantic_model)
        else:
            return response

    def _put(self, path, pydantic_model=None, **kwargs):
        response = self._request('put', path, **kwargs)
        if pydantic_model:
            return self._validate_response_with_pydantic_model(response, pydantic_model)
        else:
            return response

    def _patch(self, path, pydantic_model=None, **kwargs):
        response = self._request('patch', path, **kwargs)
        if pydantic_model:
            return self._validate_response_with_pydantic_model(response, pydantic_model)
        else:
            return response

    def _delete(self, path, pydantic_model=None, **kwargs):
        response = self._request('delete', path, **kwargs)
        if pydantic_model:
            return self._validate_response_with_pydantic_model(response, pydantic_model)
        else:
            return response

    def _list(self, path, url_conversion=None, list_all=False, **kwargs):
        response = self._get(path, **kwargs)
        if list_all:
            return self._list_all(path, url_conversion, **kwargs), response['count']
        else:
            return response

    def _list_all(self, path, url_conversion=None, params=None, **kwargs):
        response = self._get(path, url_conversion, params=params, **kwargs)
        yield from response['results']
        if response['next']:
            yield from self._list_all(response['next'], url_conversion, **kwargs)

    def exists(self, api, *args, **kwargs):
        return getattr(self, api)(*args, **kwargs)['count'] > 0

    def _validate_response_with_pydantic_model(self, response, pydantic_model):
        """Validate a response with a pydantic model."""
        # Check if model is a pydantic model (has the __pydantic_model__ attribute)
        if (
            hasattr(pydantic_model, '__pydantic_model__')
            or hasattr(pydantic_model, 'model_validate')
            or hasattr(pydantic_model, 'parse_obj')
        ):
            pydantic_model.model_validate(response)
            return response
        else:
            # Not a pydantic model
            raise TypeError('The provided model is not a pydantic model')
