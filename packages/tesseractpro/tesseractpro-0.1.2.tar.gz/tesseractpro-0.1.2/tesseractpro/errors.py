class ApiTokenError(Exception):
    """Raises when the API token is invalid"""
    pass


class AuthenticationTimeoutError(Exception):
    pass


class ToolHandleCountError(Exception):
    pass


class ToolExistsError(Exception):
    pass
