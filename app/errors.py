class AppError(Exception):
    pass


class JWTExpiredError(AppError):
    pass


class AppTokenMissingClaimsError(AppError):
    pass
