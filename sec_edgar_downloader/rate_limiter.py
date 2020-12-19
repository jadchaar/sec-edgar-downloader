import typing

from datetime import datetime

PWN = typing.TypeVar('PWN')
CENTRAL_STATE = {}

class RateLimiter:
    def __init__(self: PWN, session_name: str) -> None:
        self._name = session_name

    def __enter__(self: PWN, *args, **kwargs) -> PWN:
        self.inc()
        return self

    def __exit__(self: PWN, type, value, tb) -> None:
        self.dec()

    def inc(self: PWN) -> None:
        CENTRAL_STATE[self._name] = CENTRAL_STATE.get(self._name, {'count': 0, 'time-index': datetime.utcnow()})
        time_diff = datetime.utcnow() - CENTRAL_STATE[self._name]['time-index']
        if time_diff.seconds > 0:
            CENTRAL_STATE[self._name] = {'count': 0, 'time-index': datetime.utcnow()}

        CENTRAL_STATE[self._name]['count'] = CENTRAL_STATE[self._name]['count'] + 1

    def dec(self: PWN) -> None:
        CENTRAL_STATE[self._name] = CENTRAL_STATE.get(self._name, {'count': 1, 'time-index': datetime.utcnow()})
        CENTRAL_STATE[self._name]['count'] -= 1

    def ready(self) -> bool:
        return CENTRAL_STATE[self._name]['count'] < 11
