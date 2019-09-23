import sys
import os
import logging
from typing import Text, List, Dict, Any, Optional, Callable, Iterable, Awaitable
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, AudioSendMessage, VideoSendMessage

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
logger = logging.getLogger(__name__)

class LineChatBotOutputChannel:
    @classmethod
    def name(cls):
        return "linechat"

    def __init__(self, reply_token, source):
        self.reply_token = reply_token
        self.source = source

    @staticmethod
    def _convert_to_rocket_buttons(buttons):
        return [
            {
                "text": b["title"],
                "msg": b["payload"],
                "type": "button",
                "msg_in_chat_window": True,
            }
            for b in buttons
        ]

    async def send_response(self, recipient_id: Text, message: Dict[Text, Any]) -> None:
        """Send a message to the client."""
        print('REPLY')
        send_messages = []

        if message.get("quick_replies"):
            await self.send_quick_replies(
                recipient_id,
                message.pop("text"),
                message.pop("quick_replies"),
                **message
            )
        elif message.get("buttons"):
            await self.send_text_with_buttons(
                recipient_id, message.pop("text"), message.pop("buttons"), **message
            )
        if message.get("custom"):
            await self.send_custom_json(recipient_id, message.pop("custom"), **message)


        if message.get("attachment"):
            await self.send_attachment(
                recipient_id, message.pop("attachment"), **message
            )

        if message.get("elements"):
            await self.send_elements(message.pop("elements"), **message)

        for msg in message:
            content = message.get(msg)
            if content:
                if msg == "text":
                    send_messages.append(TextSendMessage(text=message.get("text")))

                if msg == "image":
                    send_messages.append(ImageSendMessage(original_content_url=content, preview_image_url=message.get("image")))

                if msg == "audio":
                    send_messages.append(AudioSendMessage(original_content_url=content.get('url'), duration=content.get('duration')))

                if msg == "video":
                    send_messages.append(VideoSendMessage(original_content_url=content.get('url'), duration=content.get('duration'), preview_image_url=content.get('preview')))

        line_bot_api.push_message(self.source.sender_id, send_messages)


    async def send_text_message(
            self, recipient_id: Text, text: Text, **kwargs: Any
    ) -> None:
        for message_part in text.split("\n\n"):
            line_bot_api.push_message(
                self.source.sender_id,
                [TextSendMessage(text=message_part), TextSendMessage(text=message_part)]
            )

    async def send_image_url(
            self, recipient_id: Text, image: Text, **kwargs: Any
    ) -> None:
        line_bot_api.push_message(
            self.source.sender_id,
            ImageSendMessage(original_content_url=image, preview_image_url=image)
        )

    async def send_audio(
            self, audio_url: Text, duration, **kwargs: Any
    ) -> None:
        line_bot_api.push_message(
            self.source.sender_id,
            AudioSendMessage(original_content_url=audio_url, duration=duration)
        )

    async def send_video(
            self, video_url: Text, preview: Text, duration, **kwargs: Any
    ) -> None:
        line_bot_api.push_message(
            self.source.sender_id,
            VideoSendMessage(original_content_url=video_url, duration=duration, preview_image_url=preview)
        )

    async def send_attachment(
            self, recipient_id: Text, attachment: Text, **kwargs: Any
    ) -> None:
        return self.rocket.chat_post_message(
            None, room_id=recipient_id, attachments=[attachment]
        )

    async def send_text_with_buttons(
            self,
            recipient_id: Text,
            text: Text,
            buttons: List[Dict[Text, Any]],
            **kwargs: Any
    ) -> None:
        # implementation is based on
        # https://github.com/RocketChat/Rocket.Chat/pull/11473
        # should work in rocket chat >= 0.69.0
        button_attachment = [{"actions": self._convert_to_rocket_buttons(buttons)}]

        return self.rocket.chat_post_message(
            text, room_id=recipient_id, attachments=button_attachment
        )

    async def send_elements(
            self, recipient_id: Text, elements: Iterable[Dict[Text, Any]], **kwargs: Any
    ) -> None:
        return self.rocket.chat_post_message(
            None, room_id=recipient_id, attachments=elements
        )

    async def send_custom_json(
            self, recipient_id: Text, json_message: Dict[Text, Any], **kwargs: Any
    ) -> None:
        text = json_message.pop("text")

        if json_message.get("channel"):
            if json_message.get("room_id"):
                logger.warning(
                    "Only one of `channel` or `room_id` can be passed to a RocketChat message post. Defaulting to `channel`."
                )
                del json_message["room_id"]
            return self.rocket.chat_post_message(text, **json_message)
        else:
            json_message.setdefault("room_id", recipient_id)
            return self.rocket.chat_post_message(text, **json_message)

