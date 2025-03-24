from dataclasses import dataclass

PING = '{"method": "PING"}'
PONG = '{"method": "PONG"}'


def subscription(params: list[str]) -> dict:
    return {
        "method": "SUBSCRIPTION",
        "params": params,
    }


def unsubscribe(params: list[str]) -> dict:
    return {
        "method": "UNSUBSCRIPTION",
        "params": params,
    }


@dataclass
class ListenKeyExtendedMessage:
    listen_key: str
    expires_at: int
