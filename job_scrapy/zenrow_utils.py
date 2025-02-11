from urllib.parse import urlencode

def get_zenrows_api_url(url: str, api_key: str) -> str:
    """
    Returns the Zenrows API URL for the given URL and API key.
    """
    payload = {
        'url': url,
        # 'js_render': 'true',
        # 'premium_proxy': 'true',
    }

    api_url = f'https://api.zenrows.com/v1/?apikey={api_key}&{urlencode(payload)}'

    print(f'API URL: {api_url}')
    return api_url