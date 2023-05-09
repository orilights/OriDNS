class ODNetworkError(Exception):
    """OriDNS 网络错误"""

    def __init__(self, provider, api_endpoint, message=''):
        self.provider = provider
        self.api_endpoint = api_endpoint
        self.message = message

    def __str__(self):
        return f'API 请求失败，网络或服务器错误，provider:{self.provider}，endpoint:{self.api_endpoint}，附加信息：{self.message}'


class ODRequestFailed(Exception):
    """OriDNS 请求失败"""

    def __init__(
        self,
        provider,
        api_endpoint,
        message='',
    ):
        self.provider = provider
        self.api_endpoint = api_endpoint
        self.message = message

    def __str__(self):
        return f'API 返回错误，可能为请求参数或权限错误，provider:{self.provider}，endpoint:{self.api_endpoint}，附加信息：{self.message}'