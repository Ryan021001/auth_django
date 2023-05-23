import jwt


class JWTManager:

    @staticmethod
    def create_token(payload: any, secret_key, algorithm='HS256') -> str:
        token = jwt.encode(payload, secret_key, algorithm=algorithm)
        return token

    @staticmethod
    def decode_token(token, algorithms='HS256', secret_key='HS256') -> any:
        payload = jwt.decode(jwt=token, key=secret_key, algorithms=algorithms)
        return payload
