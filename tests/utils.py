from datetime import datetime

from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.types import User, Chat, Message, CallbackQuery, Update
from alembic.command import upgrade, downgrade

TEST_USER = User(id=123, is_bot=False, first_name='Test', last_name='Bot', username='testbot', language_code='ru-RU',
                 is_premium=True, added_to_attachment_menu=None, can_join_groups=None,
                 can_read_all_group_messages=None, supports_inline_queries=None)

TEST_USER_CHAT = Chat(id=12, type='private', title=None, username=TEST_USER.username,
                      first_name=TEST_USER.first_name, last_name=TEST_USER.last_name, photo=None, bio=None,
                      has_private_forwards=None, join_to_send_messages=None, join_by_request=None, description=None,
                      invite_link=None, pinned_message=None, permissions=None, slow_mode_delay=None,
                      message_auto_delete_time=None, has_protected_content=None, sticker_set_name=None,
                      can_set_sticker_set=None, linked_chat_id=None, location=None)


def get_message(text: str):
    return Message(message_id=123, date=datetime.now(), chat=TEST_USER_CHAT, from_user=TEST_USER,
                   sender_chat=TEST_USER_CHAT, forward_from=None, forward_from_chat=None, forward_from_message_id=None,
                   forward_signature=None, forward_sender_name=None, forward_date=None, is_automatic_forward=None,
                   reply_to_message=None, via_bot=None, edit_date=None, has_protected_content=None,
                   media_group_id=None, author_signature=None, text=text, entities=None, animation=None,
                   audio=None, document=None, photo=None, sticker=None,
                   video=None, video_note=None, voice=None, caption=None, caption_entities=None, contact=None,
                   dice=None, game=None, poll=None, venue=None, location=None, new_chat_members=None,
                   left_chat_member=None, new_chat_title=None, new_chat_photo=None, delete_chat_photo=None,
                   group_chat_created=None, supergroup_chat_created=None, channel_chat_created=None,
                   message_auto_delete_timer_changed=None, migrate_to_chat_id=None, migrate_from_chat_id=None,
                   pinned_message=None, invoice=None, successful_payment=None, connected_website=None,
                   passport_data=None, proximity_alert_triggered=None, video_chat_scheduled=None,
                   video_chat_started=None, video_chat_ended=None, video_chat_participants_invited=None,
                   web_app_data=None, reply_markup=None)


def get_callback_query(data: str | CallbackData):
    return CallbackQuery(id='test', from_user=TEST_USER, chat_instance='test', message=get_message('test'),
                         inline_message_id=None, data=data, game_short_name=None)


def get_update(message: Message = None, callback_query: CallbackQuery = None):
    return Update(
        update_id=187,
        message=message or None,
        edited_message=None,
        channel_post=None,
        edited_channel_post=None,
        inline_query=None,
        chosen_inline_result=None,
        callback_query=callback_query or None,
        shipping_query=None,
        pre_checkout_query=None,
        poll=None,
        poll_answer=None,
        my_chat_member=None,
        chat_member=None,
        chat_join_request=None
    )


def setup_database(revisions: list, alembic_config):
    for revision in revisions:
        upgrade(alembic_config, revision.revision)


def clear_database(revisions: list, alembic_config):
    revisions.reverse()
    for revision in revisions:
        downgrade(alembic_config, revision.revision or '-1')
