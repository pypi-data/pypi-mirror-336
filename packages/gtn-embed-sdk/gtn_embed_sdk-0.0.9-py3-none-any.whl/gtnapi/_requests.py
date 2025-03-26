import json

import gtnapi
from gtnapi._connection import Connection
from typing import TypedDict


class Requests:

    @classmethod
    def __send_request(cls, method, endpoint, params) -> TypedDict('response', {'http_status': int, 'response': dict}):
        """
        send a request to the backend
        :param method: HTTP method
        :param endpoint: endpoint to call
        :param params: parameters to tbe send to the endpoint
        :return: HTTP status and the response dict
        """
        con = None
        try:
            # make sure to begin with a '/'
            if not endpoint[0] == '/':
                endpoint = '/' + endpoint

            con = Connection(gtnapi.get_api_url() + endpoint,
                             'Bearer ' + gtnapi.get_token()['accessToken'],
                             gtnapi.get_app_key())
            if method == 'POST':
                r = con.open_post(params)
            elif method == 'GET':
                r = con.open_get(params)
            elif method == 'PATCH':
                r = con.open_patch(params)
            elif method == 'DELETE':
                r = con.open_delete(params)
            else:
                return {
                    "http_status": 405,
                    "response": {
                        "status": "FAILED",
                        "reason": "unknown method: " + method
                    }
                }

            if r.status_code == 200:
                return {
                    "http_status": r.status_code,
                    "response": json.loads(r.text)
                }
            else:
                try:
                    return {
                        "http_status": r.status_code,
                        "response": json.loads(r.text)
                    }
                except Exception as e:
                    # possible JSON decode error
                    return {
                        "http_status": r.status_code,
                        "response": {}
                    }
        except Exception as e:
            print(e)
            return {
                "http_status": -1,
                "response": {}
            }
        finally:
            if con:
                con.close()

    @classmethod
    def get(cls, endpoint: str, **kwargs) -> dict:
        """
        call to the HTTP GET method
        :param endpoint: endpoint to call
        :param kwargs: parameters to tbe send to the endpoint
        :return: HTTP status and the response dict
        """
        return cls.__send_request("GET", endpoint, kwargs)

    @classmethod
    def post(cls, endpoint: str, **kwargs) -> dict:
        """
        call to the HTTP POST method
        :param endpoint: endpoint to call
        :param kwargs: parameters to tbe send to the endpoint
        :return: HTTP status and the response dict
        """
        return cls.__send_request("POST", endpoint, kwargs)

    @classmethod
    def patch(cls, endpoint: str, **kwargs) -> dict:
        """
        call to the HTTP PATCH method
        :param endpoint: endpoint to call
        :param kwargs: parameters to tbe send to the endpoint
        :return: HTTP status and the response dict
        """
        return cls.__send_request("PATCH", endpoint, kwargs)

    @classmethod
    def delete(cls, endpoint: str, **kwargs) -> dict:
        """
        call to the HTTP DELETE method
        :param endpoint: endpoint to call
        :param kwargs: parameters to tbe send to the endpoint
        :return: HTTP status and the response dict
        """
        return cls.__send_request("DELETE", endpoint, kwargs)
