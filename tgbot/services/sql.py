import time

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from tgbot import models
from tgbot.models.base_model import BaseModel


class SQL:
    def __init__(self, config):
        self.config = config

        self._max_connect_tries = 5
        self._max_tries_after_fail = 3
        self._sleep_after_try = 30
        self._client = None
        self._session = None

        self._create_engine()
        self._create_session()

    def _create_engine(self) -> None:
        self._client = create_engine(
            self.config.db.db_connection_string,
            echo=False,
            pool_pre_ping=True,
            max_overflow=20
        )

    def _create_session(self) -> None:
        try_restarts_after_fail = 0

        def _attempt_create_session(tries: int):
            for _ in range(self._max_connect_tries):
                try:
                    self._session = Session(self.client)
                    return
                except Exception:
                    self._session = None
                    time.sleep(self._sleep_after_try)

            if self.session is None and tries != self._max_tries_after_fail:
                tries += 1
                time.sleep(self._sleep_after_try)
                _attempt_create_session(tries)

        _attempt_create_session(try_restarts_after_fail)
        if self.session is None:
            raise Exception(
                'SQL session are not available after '
                f'{self._max_tries_after_fail} tries. Bot loop is closed!'
            )

    def protected_commit(self) -> None:
        try:
            self.session.commit()
        except Exception as e:
            print(str(e))
            self.session.rollback()
            raise e

    @property
    def client(self) -> Engine:
        return self._client

    @property
    def session(self) -> Session:
        return self._session


class Initializer:
    def __init__(self, config, sql) -> None:
        self.config = config
        self.sql = sql
        self._sql_client: Engine = self.sql.client
        self._sql_session: Session = self.sql.session

        self._sql_available: bool = False
        self._max_sql_start_tries: int = 10
        self._max_sql_restarts_after_fail: int = 3
        self._sleep_after_sql_start_fail: int = 30

    def _init_environment(self) -> None:
        self._run_sql_session()

        BaseModel.metadata.create_all(self._sql_client)

    def _run_sql_session(self) -> None:
        print('Waiting for sql session...')
        try_sql_restarts_after_fail = 0

        def _wait_sql_session(tries: int):
            for _ in range(self._max_sql_start_tries):
                self._sql_available = self._sql_session.is_active
                if self._sql_available:
                    return
                time.sleep(1)
            if (
                not self._sql_available and
                tries != self._max_sql_restarts_after_fail
            ):
                print(
                    'SQL session are not available, trying to connect again...'
                )
                tries += 1
                time.sleep(self._sleep_after_sql_start_fail)
                _wait_sql_session(tries)

        _wait_sql_session(try_sql_restarts_after_fail)
        if not self._sql_available:
            raise Exception(
                'SQL session are not available after '
                f'{self._max_sql_restarts_after_fail} tries. '
                f'Bot loop is closed!'
            )
        print('SQL session available!')

        print('Start registering table models!')
        time.sleep(0.1)
        models.setup()
        print('All table models successfully registered!')

    def run(self) -> None:
        self._init_environment()
