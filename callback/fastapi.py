import re
from typing import Optional
from django.db import IntegrityError

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel, validator

from callback.models import Game, Player
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .utils import get_game_by_id, get_player_by_id, get_user_by_name_and_email

description = """
We use JWT for auth.0
"""

app = FastAPI(
    title="Test Project API",
    description=description,
    version="0.0.2"
)


class User(BaseModel):
    username: str
    password: str


class LoginMessage(BaseModel):
    access_token: str


class UserMessage(BaseModel):
    user: str


class StatusMessage(BaseModel):
    status: str
    id: Optional[int] = None
    success: Optional[bool] = None


class ErrorMessage(BaseModel):
    status: str
    message: str


class PlayerItem(BaseModel):
    name: str
    email: str

    @validator('name')
    def check_name(cls, value: str):
        if re.match(r"[a-f0-9]+$", value) is None:
            raise ValueError(
                'the player`s name must contain only letters from a to f and numbers from 0 to 9'
            )
        return value


class GameItem(BaseModel):
    name: str


class PlayerGame(BaseModel):
    game_id: int
    player_id: int

    class Config:
        orm_mode = True


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


# callback to get your configion
@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


# provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token to use authorization
# later in endpoint protected
@app.post('/login', tags=['Auth'], responses={200: {"model": LoginMessage}})
def login(user: User, Authorize: AuthJWT = Depends()):
    """
    Use username=test and password=test for now.
    This endpoint will response you with access_token
    to use in header like: "Authorization: Bearer $TOKEN"
    to get protectedendpoints
    """
    if user.username != "test" or user.password != "test":
        raise HTTPException(status_code=401, detail="Bad username or password")

    # subject identifier for who this token
    # is for example id or username from database
    access_token = Authorize.create_access_token(subject=user.username)
    return JSONResponse(
        status_code=200, content={"access_token": access_token}
    )


# protect endpoint with function jwt_required(), which requires
# a valid access token in the request headers to access.
@app.get('/user', tags=['Auth'], responses={200: {"model": UserMessage}})
def user(Authorize: AuthJWT = Depends()):
    """
    Endpoint response with user that fits "Authorization: Bearer $TOKEN"
    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return JSONResponse(status_code=200, content={"user": current_user})


@app.get(
    '/protected_example',
    tags=['Auth'],
    responses={200: {"model": UserMessage}}
)
def protected_example(Authorize: AuthJWT = Depends()):
    """
    Just for test of Auth.

    Auth usage example:
    $ curl http://ip:8000/user

    {"detail":"Missing Authorization Header"}

    $ curl -H "Content-Type: application/json" -X POST \
    -d '{"username":"test","password":"test"}' http://localhost:8000/login

    {"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWF0IjoxNjAzNjkyMjYxLCJuYmYiOjE2MDM2OTIyNjEsImp0aSI6IjZiMjZkZTkwLThhMDYtNDEzMy04MzZiLWI5ODJkZmI3ZjNmZSIsImV4cCI6MTYwMzY5MzE2MSwidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZX0.ro5JMHEVuGOq2YsENkZigSpqMf5cmmgPP8odZfxrzJA"}

    $ export TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWF0IjoxNjAzNjkyMjYxLCJuYmYiOjE2MDM2OTIyNjEsImp0aSI6IjZiMjZkZTkwLThhMDYtNDEzMy04MzZiLWI5ODJkZmI3ZjNmZSIsImV4cCI6MTYwMzY5MzE2MSwidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZX0.ro5JMHEVuGOq2YsENkZigSpqMf5cmmgPP8odZfxrzJA

    $ curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/user

    {"user":"test"}

    $ curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/protected_example

    {"user":"test", "test": true}
    """
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return JSONResponse(status_code=200, content={"user": current_user})


@app.post(
    '/new_player',
    tags=['Main'],
    responses={200: {"model": StatusMessage}, 400: {"model": ErrorMessage}}
)
async def create_new_player(
    player: PlayerItem, Authorize: AuthJWT = Depends()
):
    """
    Creates new player.
    """
    Authorize.jwt_required()

    new_player = Player()
    new_player.name = player.name
    new_player.email = player.email

    db_player = get_user_by_name_and_email(player.name, player.email)
    if db_player:
        return JSONResponse(
            status_code=404,
            content={
                "message": "player with such name or email already exists"
            }
        )
    new_player.save()

    return JSONResponse(
        content={"status": "success", "id": new_player.id, "success": True}
    )


@app.post(
    '/new_game',
    tags=['Main'],
    responses={200: {"model": StatusMessage}, 400: {"model": ErrorMessage}}
)
def create_new_game(game: GameItem, Authorize: AuthJWT = Depends()):
    """
    Creates new game.
    """
    Authorize.jwt_required()

    new_game = Game()
    new_game.name = game.name
    new_game.save()

    return JSONResponse(
        content={"status": "success", "id": new_game.id, "success": True}
    )


@app.post(
    '/add_player_to_game',
    tags=['Main'],
    responses={200: {"model": StatusMessage}, 400: {"model": ErrorMessage}}
)
async def add_player_to_game(
    player_game: PlayerGame, Authorize: AuthJWT = Depends()
):
    """
    Adds existing player to existing game.
    """
    Authorize.jwt_required()

    db_game = get_game_by_id(player_game.game_id)

    try:
        players_count = db_game.players.count()
    except AttributeError:
        return JSONResponse(
            status_code=404,
            content={
                "message": "the game with such id doesn't exist"
            }
        )

    if players_count >= 5:
        return JSONResponse(
            status_code=404,
            content={
                "message": "count of players must be less than 5 or equal 5"
            }
        )

    player = get_player_by_id(player_game.player_id)

    try:
        db_game.players.add(player)
    except IntegrityError:
        return JSONResponse(
            status_code=404,
            content={
                "message": "the player with such id doesn't exist"
            }
        )

    return JSONResponse(
        content={
            "status": "success", "id": player_game.game_id, "success": True
        }
    )
