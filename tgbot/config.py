from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    db_connection_string: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool
    user_key: str


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            user_key=env.str("USER_KEY")
        ),
        db=DbConfig(
            db_connection_string=env.str('DB_CONNECTION_STRING')
        ),
        misc=Miscellaneous()
    )
