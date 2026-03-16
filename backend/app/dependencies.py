from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, jwk, JWTError
import httpx
import os

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "dev-p2iro3psonbr3wtf.us.auth0.com")
API_AUDIENCE = "https://dev-p2iro3psonbr3wtf.us.auth0.com/api/v2/"
ALGORITHMS = ["RS256"]

http_bearer = HTTPBearer()

async def get_jwk():
    url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()["keys"]



def get_kid(token):
    unverified_header = jwt.get_unverified_header(token)
    return unverified_header.get("kid")

async def verify_auth0_token(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = credentials.credentials
    try:
        jwks = await get_jwk()
        kid = get_kid(token)
        print(kid)
        key = next((k for k in jwks if k["kid"] == kid), None)
        if not key:
            raise HTTPException(status_code=401, detail="Invalid token header")
        public_key = jwk.construct(key)
        payload = jwt.decode(
            token,
            public_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
