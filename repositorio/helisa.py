import requests


def get(url, headers=None, params=None):

    return requests.get(
        url,
        headers=headers,
        params=params
    )


def post(url, headers=None, params=None):

    return requests.post(
        url,
        headers=headers,
        params=params
    )
    