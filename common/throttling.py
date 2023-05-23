from rest_framework.throttling import UserRateThrottle


class UserLoginRateThrottle(UserRateThrottle):
    scope = 'user_login'
