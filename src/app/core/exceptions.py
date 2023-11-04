class CacheIdentificationInferenceError(Exception):
    def __init__(self, message="Could not infer id for resource being cached."):
        self.message = message
        super().__init__(self.message)


class InvalidRequestError(Exception):
    def __init__(self, message="Type of request not supported."):
        self.message = message
        super().__init__(self.message)


class InvalidOutputTypeError(Exception):
    def __init__(self, message="output_type not allowed. If caching, use dict"):
        self.message = message
        super().__init__(self.message)
