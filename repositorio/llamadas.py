import requests


def get(url, headers=None, params=None):

    return requests.get(
        url,
        params=params,
        headers=headers,
        timeout=30
    )


def post(url, headers=None, params=None):

    return requests.post(
        url,
        headers=headers,
        params=params
    )
    