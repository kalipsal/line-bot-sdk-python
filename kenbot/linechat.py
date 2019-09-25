import sys
import os
import inspect
import json
import logging
from asyncio import Queue, CancelledError
from sanic import Sanic, Blueprint, response
from sanic.request import Request
from typing import Text, List, Dict, Any, Optional, Callable, Iterable, Awaitable
from rasa.core.channels.channel import UserMessage, InputChannel, CollectingOutputChannel

try:
    from urlparse import urljoin  # pytype: disable=import-error
except ImportError:
    from urllib.parse import urljoin

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot import WebhookParser
from linebot.models import MessageEvent, TextMessage
from .channel import LineChatBotOutputChannel


channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)

parser = WebhookParser(channel_secret)
logger = logging.getLogger(__name__)


class LineChatInput(InputChannel):
    """A custom http input channel.

    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa Core and
    retrieve responses from the agent."""

    @classmethod
    def name(cls):
        return "linechat"

    async def _extract_sender(self, req: Request) -> Optional[Text]:
        return req.json.get("sender", None)

    # noinspection PyMethodMayBeStatic
    def _extract_message(self, req: Request) -> Optional[Text]:
        return req.json.get("message", None)

    def _extract_input_channel(self, req: Request) -> Text:
        return req.json.get("input_channel") or self.name()

    async def send_message(self, text, on_new_message, reply_token, source):
        output_channel = self.get_output_channel(reply_token, source)

        user_msg = UserMessage(
            text, output_channel, source.sender_id, input_channel=self.name()
        )
        await on_new_message(user_msg)

    def blueprint(self, on_new_message: Callable[[UserMessage], Awaitable[None]]):
        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        # noinspection PyUnusedLocal
        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request):
            return response.json({"status": "ok", "name": "kenbot"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request):
            sender_id = await self._extract_sender(request)
            text = self._extract_message(request)

            input_channel = self._extract_input_channel(request)

            collector = CollectingOutputChannel()
            # noinspection PyBroadException
            try:
                await on_new_message(
                    UserMessage(
                        text, collector, sender_id, input_channel=input_channel
                    )
                )
            except CancelledError:
                logger.error(
                    "Message handling timed out for "
                    "user message '{}'.".format(text)
                )
            except Exception:
                logger.exception(
                    "An exception occured while handling "
                    "user message '{}'.".format(text)
                )
            return response.json(collector.messages)

        @custom_webhook.route("/callback", methods=['POST'])
        async def callback(request: Request):
            signature = request.headers['x-line-signature']

            body = request.json
            logger.info("Request body: {}".format(body))

            try:
                print(parser)
                events = parser.parse(json.dumps(body), signature)
            except InvalidSignatureError:
                abort(400)

            print(events)

            for event in events:
                if not isinstance(event, MessageEvent):
                    continue
                if not isinstance(event.message, TextMessage):
                    continue
                if event.reply_token == '00000000000000000000000000000000' \
                        or event.reply_token == 'ffffffffffffffffffffffffffffffff':
                    continue

                text = event.message.text
                user_id = event.source.user_id

                await self.send_message(text, on_new_message, event.reply_token, event.source)

            return response.text("OK")

        return custom_webhook

    def get_output_channel(self, reply_token, source):
        return LineChatBotOutputChannel(reply_token, source)
