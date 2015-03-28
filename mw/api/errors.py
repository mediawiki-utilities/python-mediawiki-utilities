class DocError(Exception):
    def __init__(self, message, doc):
        super().__init__(message)

        self.doc = doc
        """
        The document returned by the API that brought about this error.
        """


class APIError(DocError):
    def __init__(self, doc):

        code = doc.get('error', {}).get('code')
        message = doc.get('error', {}).get('message')

        super().__init__("{0}:{1}".format(code, message), doc)

        self.code = code
        """
        The error code returned by the api -- if available.
        """

        self.message = message
        """
        The error message returned by the api -- if available.
        """

class AuthenticationError(DocError):
    def __init__(self, doc):
        result = doc['login']['result']
        super().__init__(result, doc)

        self.result = result
        """
        The result code of an authentication attempt.
        """


class MalformedResponse(DocError):
    def __init__(self, key, doc):

        super().__init__("Expected to find '{0}' in result.".format(key), doc)

        self.key = key
        """
        The expected, but missing key from the API call.
        """
