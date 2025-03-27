class LarkAPIError(Exception):
    """General exception for LarkCore API errors."""

    pass


class LarkAPIPermissionError(LarkAPIError, PermissionError):
    """Exception raised for LarkCore API permission errors."""

    pass


class LarkInvalidRequestError(LarkAPIError):
    """Exception raised for LarkCore API Bad Request errors."""

    pass


class LarkInvalidSheetDataError(LarkAPIError):
    """Exception raised for LarkCore API Sheet Data errors."""

    pass
