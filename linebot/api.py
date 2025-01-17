# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

"""linebot.api module."""

from __future__ import unicode_literals

import json

from .__about__ import __version__
from .exceptions import LineBotApiError
from .http_client import HttpClient, RequestsHttpClient
from .models import (
    Error, Profile, MemberIds, Content, RichMenuResponse, MessageQuotaResponse,
    MessageQuotaConsumptionResponse, IssueLinkTokenResponse, IssueChannelTokenResponse,
    MessageDeliveryBroadcastResponse, MessageDeliveryMulticastResponse,
    MessageDeliveryPushResponse, MessageDeliveryReplyResponse,
    InsightMessageDeliveryResponse, InsightFollowersResponse, InsightDemographicResponse,
)


class LineBotApi(object):
    """LineBotApi provides interface for LINE messaging API."""

    DEFAULT_API_ENDPOINT = 'https://api.line.me'

    def __init__(self, channel_access_token, endpoint=DEFAULT_API_ENDPOINT,
                 timeout=HttpClient.DEFAULT_TIMEOUT, http_client=RequestsHttpClient):
        """__init__ method.

        :param str channel_access_token: Your channel access token
        :param str endpoint: (optional) Default is https://api.line.me
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is linebot.http_client.HttpClient.DEFAULT_TIMEOUT
        :type timeout: float | tuple(float, float)
        :param http_client: (optional) Default is
            :py:class:`linebot.http_client.RequestsHttpClient`
        :type http_client: T <= :py:class:`linebot.http_client.HttpClient`
        """
        self.endpoint = endpoint
        self.headers = {
            'Authorization': 'Bearer ' + channel_access_token,
            'User-Agent': 'line-bot-sdk-python/' + __version__
        }

        if http_client:
            self.http_client = http_client(timeout=timeout)
        else:
            self.http_client = RequestsHttpClient(timeout=timeout)

    def reply_message(self, reply_token, messages, notification_disabled=False, timeout=None):
        """Call reply message API.

        https://developers.line.biz/en/reference/messaging-api/#send-reply-message

        Respond to events from users, groups, and rooms.

        Webhooks are used to notify you when an event occurs.
        For events that you can respond to, a replyToken is issued for replying to messages.

        Because the replyToken becomes invalid after a certain period of time,
        responses should be sent as soon as a message is received.

        Reply tokens can only be used once.

        :param str reply_token: replyToken received via webhook
        :param messages: Messages.
            Max: 5
        :type messages: T <= :py:class:`linebot.models.send_messages.SendMessage` |
            list[T <= :py:class:`linebot.models.send_messages.SendMessage`]
        :param bool notification_disabled: (optional) True to disable push notification
            when the message is sent. The default value is False.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        data = {
            'replyToken': reply_token,
            'messages': [message.as_json_dict() for message in messages],
            'notificationDisabled': notification_disabled,
        }

        self._post(
            '/v2/bot/message/reply', data=json.dumps(data), timeout=timeout
        )

    def push_message(self, to, messages, notification_disabled=False, timeout=None):
        """Call push message API.

        https://developers.line.biz/en/reference/messaging-api/#send-push-message

        Send messages to users, groups, and rooms at any time.

        :param str to: ID of the receiver
        :param messages: Messages.
            Max: 5
        :type messages: T <= :py:class:`linebot.models.send_messages.SendMessage` |
            list[T <= :py:class:`linebot.models.send_messages.SendMessage`]
        :param bool notification_disabled: (optional) True to disable push notification
            when the message is sent. The default value is False.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        data = {
            'to': to,
            'messages': [message.as_json_dict() for message in messages],
            'notificationDisabled': notification_disabled,
        }

        self._post(
            '/v2/bot/message/push', data=json.dumps(data), timeout=timeout
        )

    def multicast(self, to, messages, notification_disabled=False, timeout=None):
        """Call multicast API.

        https://developers.line.biz/en/reference/messaging-api/#send-multicast-message

        Send messages to multiple users at any time.

        :param to: IDs of the receivers
            Max: 150 users
        :type to: list[str]
        :param messages: Messages.
            Max: 5
        :type messages: T <= :py:class:`linebot.models.send_messages.SendMessage` |
            list[T <= :py:class:`linebot.models.send_messages.SendMessage`]
        :param bool notification_disabled: (optional) True to disable push notification
            when the message is sent. The default value is False.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        data = {
            'to': to,
            'messages': [message.as_json_dict() for message in messages],
            'notificationDisabled': notification_disabled,
        }

        self._post(
            '/v2/bot/message/multicast', data=json.dumps(data), timeout=timeout
        )

    def broadcast(self, messages, notification_disabled=False, timeout=None):
        """Call broadcast API.

        https://developers.line.biz/en/reference/messaging-api/#send-broadcast-message

        Send messages to multiple users at any time.

        :param messages: Messages.
            Max: 5
        :type messages: T <= :py:class:`linebot.models.send_messages.SendMessage` |
            list[T <= :py:class:`linebot.models.send_messages.SendMessage`]
        :param bool notification_disabled: (optional) True to disable push notification
            when the message is sent. The default value is False.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        data = {
            'messages': [message.as_json_dict() for message in messages],
            'notificationDisabled': notification_disabled,
        }

        self._post(
            '/v2/bot/message/broadcast', data=json.dumps(data), timeout=timeout
        )

    def get_message_delivery_broadcast(self, date, timeout=None):
        """Get number of sent broadcast messages.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-broadcast-messages

        Gets the number of messages sent with the /bot/message/broadcast endpoint.

        :param str date: Date the messages were sent. The format is `yyyyMMdd` (Timezone is UTC+9).
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        response = self._get(
            '/v2/bot/message/delivery/broadcast?date={date}'.format(date=date),
            timeout=timeout
        )

        return MessageDeliveryBroadcastResponse.new_from_json_dict(response.json)

    def get_message_delivery_reply(self, date, timeout=None):
        """Get number of sent reply messages.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-reply-messages

        Gets the number of messages sent with the /bot/message/reply endpoint.

        :param str date: Date the messages were sent. The format is `yyyyMMdd` (Timezone is UTC+9).
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        response = self._get(
            '/v2/bot/message/delivery/reply?date={date}'.format(date=date),
            timeout=timeout
        )

        return MessageDeliveryReplyResponse.new_from_json_dict(response.json)

    def get_message_delivery_push(self, date, timeout=None):
        """Get number of sent push messages.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-push-messages

        Gets the number of messages sent with the /bot/message/push endpoint.

        :param str date: Date the messages were sent. The format is `yyyyMMdd` (Timezone is UTC+9).
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        response = self._get(
            '/v2/bot/message/delivery/push?date={date}'.format(date=date),
            timeout=timeout
        )

        return MessageDeliveryPushResponse.new_from_json_dict(response.json)

    def get_message_delivery_multicast(self, date, timeout=None):
        """Get number of sent multicast messages.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-multicast-messages

        Gets the number of messages sent with the /bot/message/multicast endpoint.

        :param str date: Date the messages were sent. The format is `yyyyMMdd` (Timezone is UTC+9).
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        response = self._get(
            '/v2/bot/message/delivery/multicast?date={date}'.format(date=date),
            timeout=timeout
        )

        return MessageDeliveryMulticastResponse.new_from_json_dict(response.json)

    def get_profile(self, user_id, timeout=None):
        """Call get profile API.

        https://developers.line.biz/en/reference/messaging-api/#get-profile

        Get user profile information.

        :param str user_id: User ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Profile`
        :return: Profile instance
        """
        response = self._get(
            '/v2/bot/profile/{user_id}'.format(user_id=user_id),
            timeout=timeout
        )

        return Profile.new_from_json_dict(response.json)

    def get_group_member_profile(self, group_id, user_id, timeout=None):
        """Call get group member profile API.

        https://developers.line.biz/en/reference/messaging-api/#get-group-member-profile

        Gets the user profile of a member of a group that
        the bot is in. This can be the user ID of a user who has
        not added the bot as a friend or has blocked the bot.

        :param str group_id: Group ID
        :param str user_id: User ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Profile`
        :return: Profile instance
        """
        response = self._get(
            '/v2/bot/group/{group_id}/member/{user_id}'.format(group_id=group_id, user_id=user_id),
            timeout=timeout
        )

        return Profile.new_from_json_dict(response.json)

    def get_room_member_profile(self, room_id, user_id, timeout=None):
        """Call get room member profile API.

        https://developers.line.biz/en/reference/messaging-api/#get-room-member-profile

        Gets the user profile of a member of a room that
        the bot is in. This can be the user ID of a user who has
        not added the bot as a friend or has blocked the bot.

        :param str room_id: Room ID
        :param str user_id: User ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Profile`
        :return: Profile instance
        """
        response = self._get(
            '/v2/bot/room/{room_id}/member/{user_id}'.format(room_id=room_id, user_id=user_id),
            timeout=timeout
        )

        return Profile.new_from_json_dict(response.json)

    def get_group_member_ids(self, group_id, start=None, timeout=None):
        """Call get group member IDs API.

        https://developers.line.biz/en/reference/messaging-api/#get-group-member-ids

        Gets the user IDs of the members of a group that the bot is in.
        This includes the user IDs of users who have not added the bot as a friend
        or has blocked the bot.

        :param str group_id: Group ID
        :param str start: continuationToken
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MemberIds`
        :return: MemberIds instance
        """
        params = None if start is None else {'start': start}

        response = self._get(
            '/v2/bot/group/{group_id}/members/ids'.format(group_id=group_id),
            params=params,
            timeout=timeout
        )

        return MemberIds.new_from_json_dict(response.json)

    def get_room_member_ids(self, room_id, start=None, timeout=None):
        """Call get room member IDs API.

        https://developers.line.biz/en/reference/messaging-api/#get-room-member-ids

        Gets the user IDs of the members of a group that the bot is in.
        This includes the user IDs of users who have not added the bot as a friend
        or has blocked the bot.

        :param str room_id: Room ID
        :param str start: continuationToken
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MemberIds`
        :return: MemberIds instance
        """
        params = None if start is None else {'start': start}

        response = self._get(
            '/v2/bot/room/{room_id}/members/ids'.format(room_id=room_id),
            params=params,
            timeout=timeout
        )

        return MemberIds.new_from_json_dict(response.json)

    def get_message_content(self, message_id, timeout=None):
        """Call get content API.

        https://developers.line.biz/en/reference/messaging-api/#get-content

        Retrieve image, video, and audio data sent by users.

        :param str message_id: Message ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Content`
        :return: Content instance
        """
        response = self._get(
            '/v2/bot/message/{message_id}/content'.format(message_id=message_id),
            stream=True, timeout=timeout
        )

        return Content(response)

    def leave_group(self, group_id, timeout=None):
        """Call leave group API.

        https://developers.line.biz/en/reference/messaging-api/#leave-group

        Leave a group.

        :param str group_id: Group ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        self._post(
            '/v2/bot/group/{group_id}/leave'.format(group_id=group_id),
            timeout=timeout
        )

    def leave_room(self, room_id, timeout=None):
        """Call leave room API.

        https://developers.line.biz/en/reference/messaging-api/#leave-room

        Leave a room.

        :param str room_id: Room ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        self._post(
            '/v2/bot/room/{room_id}/leave'.format(room_id=room_id),
            timeout=timeout
        )

    def get_rich_menu(self, rich_menu_id, timeout=None):
        """Call get rich menu API.

        https://developers.line.me/en/docs/messaging-api/reference/#get-rich-menu

        :param str rich_menu_id: ID of the rich menu
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.RichMenuResponse`
        :return: RichMenuResponse instance
        """
        response = self._get(
            '/v2/bot/richmenu/{rich_menu_id}'.format(rich_menu_id=rich_menu_id),
            timeout=timeout
        )

        return RichMenuResponse.new_from_json_dict(response.json)

    def create_rich_menu(self, rich_menu, timeout=None):
        """Call create rich menu API.

        https://developers.line.me/en/docs/messaging-api/reference/#create-rich-menu

        :param rich_menu: Inquired to create a rich menu object.
        :type rich_menu: T <= :py:class:`linebot.models.rich_menu.RichMenu`
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: str
        :return: rich menu id
        """
        response = self._post(
            '/v2/bot/richmenu', data=rich_menu.as_json_string(), timeout=timeout
        )

        return response.json.get('richMenuId')

    def delete_rich_menu(self, rich_menu_id, timeout=None):
        """Call delete rich menu API.

        https://developers.line.me/en/docs/messaging-api/reference/#delete-rich-menu

        :param str rich_menu_id: ID of an uploaded rich menu
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        self._delete(
            '/v2/bot/richmenu/{rich_menu_id}'.format(rich_menu_id=rich_menu_id),
            timeout=timeout
        )

    def get_rich_menu_id_of_user(self, user_id, timeout=None):
        """Call get rich menu ID of user API.

        https://developers.line.me/en/docs/messaging-api/reference/#get-rich-menu-id-of-user

        :param str user_id: IDs of the user
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: str
        :return: rich menu id
        """
        response = self._get(
            '/v2/bot/user/{user_id}/richmenu'.format(user_id=user_id),
            timeout=timeout
        )

        return response.json.get('richMenuId')

    def link_rich_menu_to_user(self, user_id, rich_menu_id, timeout=None):
        """Call link rich menu to user API.

        https://developers.line.me/en/docs/messaging-api/reference/#link-rich-menu-to-user

        :param str user_id: ID of the user
        :param str rich_menu_id: ID of an uploaded rich menu
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        self._post(
            '/v2/bot/user/{user_id}/richmenu/{rich_menu_id}'.format(
                user_id=user_id,
                rich_menu_id=rich_menu_id
            ),
            timeout=timeout
        )

    def link_rich_menu_to_users(self, user_ids, rich_menu_id, timeout=None):
        """Links a rich menu to multiple users.

        https://developers.line.biz/en/reference/messaging-api/#link-rich-menu-to-users

        :param user_ids: user IDs
            Max: 150 users
        :type user_ids: list[str]
        :param str rich_menu_id: ID of an uploaded rich menu
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        self._post(
            '/v2/bot/richmenu/bulk/link',
            data=json.dumps({
                'userIds': user_ids,
                'richMenuId': rich_menu_id,
            }),
            timeout=timeout
        )

    def unlink_rich_menu_from_user(self, user_id, timeout=None):
        """Call unlink rich menu from user API.

        https://developers.line.me/en/docs/messaging-api/reference/#unlink-rich-menu-from-user

        :param str user_id: ID of the user
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        self._delete(
            '/v2/bot/user/{user_id}/richmenu'.format(user_id=user_id),
            timeout=timeout
        )

    def unlink_rich_menu_from_users(self, user_ids, timeout=None):
        """Unlinks rich menus from multiple users.

        https://developers.line.biz/en/reference/messaging-api/#unlink-rich-menu-from-users

        :param user_ids: user IDs
            Max: 150 users
        :type user_ids: list[str]
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        self._post(
            '/v2/bot/richmenu/bulk/unlink',
            data=json.dumps({
                'userIds': user_ids,
            }),
            timeout=timeout
        )

    def get_rich_menu_image(self, rich_menu_id, timeout=None):
        """Call download rich menu image API.

        https://developers.line.me/en/docs/messaging-api/reference/#download-rich-menu-image

        :param str rich_menu_id: ID of the rich menu with the image to be downloaded
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Content`
        :return: Content instance
        """
        response = self._get(
            '/v2/bot/richmenu/{rich_menu_id}/content'.format(rich_menu_id=rich_menu_id),
            timeout=timeout
        )

        return Content(response)

    def set_rich_menu_image(self, rich_menu_id, content_type, content, timeout=None):
        """Call upload rich menu image API.

        https://developers.line.me/en/docs/messaging-api/reference/#upload-rich-menu-image

        Uploads and attaches an image to a rich menu.

        :param str rich_menu_id: IDs of the richmenu
        :param str content_type: image/jpeg or image/png
        :param content: image content as bytes, or file-like object
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        self._post(
            '/v2/bot/richmenu/{rich_menu_id}/content'.format(rich_menu_id=rich_menu_id),
            data=content,
            headers={'Content-Type': content_type},
            timeout=timeout
        )

    def get_rich_menu_list(self, timeout=None):
        """Call get rich menu list API.

        https://developers.line.me/en/docs/messaging-api/reference/#get-rich-menu-list

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: list(T <= :py:class:`linebot.models.responses.RichMenuResponse`)
        :return: list[RichMenuResponse] instance
        """
        response = self._get(
            '/v2/bot/richmenu/list',
            timeout=timeout
        )

        result = []
        for richmenu in response.json['richmenus']:
            result.append(RichMenuResponse.new_from_json_dict(richmenu))

        return result

    def set_default_rich_menu(self, rich_menu_id, timeout=None):
        """Set the default rich menu.

        https://developers.line.biz/en/reference/messaging-api/#set-default-rich-menu

        :param str rich_menu_id: ID of an uploaded rich menu
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        self._post(
            '/v2/bot/user/all/richmenu/{rich_menu_id}'.format(
                rich_menu_id=rich_menu_id,
            ),
            timeout=timeout
        )

    def get_default_rich_menu(self, timeout=None):
        """Get the ID of the default rich menu set with the Messaging API.

        https://developers.line.biz/en/reference/messaging-api/#get-default-rich-menu-id

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        response = self._get(
            '/v2/bot/user/all/richmenu',
            timeout=timeout
        )

        return response.json.get('richMenuId')

    def cancel_default_rich_menu(self, timeout=None):
        """Cancel the default rich menu set with the Messaging API.

        https://developers.line.biz/en/reference/messaging-api/#cancel-default-rich-menu

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        self._delete(
            '/v2/bot/user/all/richmenu',
            timeout=timeout
        )

    def get_message_quota(self, timeout=None):
        """Call Get the target limit for additional messages.

        https://developers.line.biz/en/reference/messaging-api/#get-quota

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MessageQuotaResponse`
        :return: MessageQuotaResponse instance
        """
        response = self._get(
            '/v2/bot/message/quota',
            timeout=timeout
        )

        return MessageQuotaResponse.new_from_json_dict(response.json)

    def get_message_quota_consumption(self, timeout=None):
        """Get number of messages sent this month.

        https://developers.line.biz/en/reference/messaging-api/#get-consumption

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MessageQuotaConsumptionResponse`
        :return: MessageQuotaConsumptionResponse instance
        """
        response = self._get(
            '/v2/bot/message/quota/consumption',
            timeout=timeout
        )

        return MessageQuotaConsumptionResponse.new_from_json_dict(response.json)

    def issue_link_token(self, user_id, timeout=None):
        """Issues a link token used for the account link feature.

        https://developers.line.biz/en/reference/messaging-api/#issue-link-token

        :param str user_id: User ID for the LINE account to be linked
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.IssueLinkTokenResponse`
        :return: IssueLinkTokenResponse instance
        """
        response = self._post(
            '/v2/bot/user/{user_id}/linkToken'.format(
                user_id=user_id
            ),
            timeout=timeout
        )

        return IssueLinkTokenResponse.new_from_json_dict(response.json)

    def issue_channel_token(self, client_id, client_secret,
                            grant_type='client_credentials', timeout=None):
        """Issues a short-lived channel access token.

        https://developers.line.biz/en/reference/messaging-api/#issue-channel-access-token

        :param str client_id: Channel ID.
        :param str client_secret: Channel secret.
        :param str grant_type: `client_credentials`
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.IssueChannelTokenResponse`
        :return: IssueChannelTokenResponse instance
        """
        response = self._post(
            '/v2/oauth/accessToken',
            data={
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': grant_type,
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=timeout
        )

        return IssueChannelTokenResponse.new_from_json_dict(response.json)

    def revoke_channel_token(self, access_token, timeout=None):
        """Revokes a channel access token.

        https://developers.line.biz/en/reference/messaging-api/#revoke-channel-access-token

        :param str access_token: Channel access token.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        self._post(
            '/v2/oauth/revoke',
            data={'access_token': access_token},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=timeout
        )

    def get_insight_message_delivery(self, date, timeout=None):
        """Get the number of messages sent on a specified day.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-delivery-messages

        :param str date: Date for which to retrieve number of sent messages.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        response = self._get(
            '/v2/bot/insight/message/delivery?date={date}'.format(date=date),
            timeout=timeout
        )

        return InsightMessageDeliveryResponse.new_from_json_dict(response.json)

    def get_insight_followers(self, date, timeout=None):
        """Get the number of users who have added the bot on or before a specified date.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-followers

        :param str date: Date for which to retrieve the number of followers.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        response = self._get(
            '/v2/bot/insight/followers?date={date}'.format(date=date),
            timeout=timeout
        )

        return InsightFollowersResponse.new_from_json_dict(response.json)

    def get_insight_demographic(self, timeout=None):
        """Retrieve the demographic attributes for a bot's friends.

        https://developers.line.biz/en/reference/messaging-api/#get-demographic

        :param str date: Date for which to retrieve the number of followers.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        response = self._get(
            '/v2/bot/insight/demographic',
            timeout=timeout
        )

        return InsightDemographicResponse.new_from_json_dict(response.json)

    def _get(self, path, params=None, headers=None, stream=False, timeout=None):
        url = self.endpoint + path

        if headers is None:
            headers = {}
        headers.update(self.headers)

        response = self.http_client.get(
            url, headers=headers, params=params, stream=stream, timeout=timeout
        )

        self.__check_error(response)
        return response

    def _post(self, path, data=None, headers=None, timeout=None):
        url = self.endpoint + path

        if headers is None:
            headers = {'Content-Type': 'application/json'}
        headers.update(self.headers)
        print(data)

        response = self.http_client.post(
            url, headers=headers, data=data, timeout=timeout
        )

        self.__check_error(response)
        return response

    def _delete(self, path, data=None, headers=None, timeout=None):
        url = self.endpoint + path

        if headers is None:
            headers = {}
        headers.update(self.headers)

        response = self.http_client.delete(
            url, headers=headers, data=data, timeout=timeout
        )

        self.__check_error(response)
        return response

    @staticmethod
    def __check_error(response):
        if 200 <= response.status_code < 300:
            pass
        else:
            error = Error.new_from_json_dict(response.json)
            raise LineBotApiError(response.status_code, error)
