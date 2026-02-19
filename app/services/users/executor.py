from ._core import User
from models.models import User as UserModel

class Executor(User):
    def __init__(self, user: UserModel):
        ...