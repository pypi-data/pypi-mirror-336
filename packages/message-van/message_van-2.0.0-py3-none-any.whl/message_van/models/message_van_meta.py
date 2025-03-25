from abc import ABCMeta
from inspect import getfile
from pathlib import Path

from message_van.models import MessageHandlers
from message_van.signatures import list_signatures
from message_van.util import get_src_dir


class MessageVanMeta(ABCMeta):
    _message_handlers: MessageHandlers

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        cls._message_handlers = None

        return cls

    async def register_handlers(cls) -> None:
        if cls._message_handlers is None:
            await cls._register_handlers()

    async def _register_handlers(cls) -> None:
        cls_file = Path(getfile(cls))
        src_dir = get_src_dir(cls_file)

        cls._message_handlers = MessageHandlers()

        for signature in list_signatures(src_dir):
            cls._message_handlers.register(signature)
