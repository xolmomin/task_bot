import json

import telebot
from django.conf import settings
from django.http.response import HttpResponse

from app.models import TgUser, History

# @usingjsonbot

bot = telebot.TeleBot(settings.BOT_TOKEN)


def web_hook_view(request):
    if request.method == 'POST':
        bot.process_new_updates([telebot.types.Update.de_json(request.body.decode("utf-8"))])
        return HttpResponse(status=200)
    return HttpResponse('404 not found')


@bot.message_handler(commands=['start', 'help'])
def start(message):
    user_id = message.from_user.id
    if TgUser.objects.filter(user_id=user_id).exists():
        TgUser.objects.filter(user_id=user_id).update(first_name=message.from_user.first_name,
                                                      last_name=message.from_user.last_name,
                                                      username=message.from_user.username)
    else:
        TgUser.objects.create(user_id=user_id, first_name=message.from_user.first_name,
                              last_name=message.from_user.last_name, username=message.from_user.username)

    text = "🔸 @ShowJsonBot v2019.07 - Bot returns json for all sent messages.\n" \
           "Messages editing and inline queries are also supported.\n" \
           "For support or if you have questions about bots' development - contact @RocketBotsBot\n" \
           "Enjoy! ☺️"
    bot.send_message(user_id, text)


@bot.message_handler(
    content_types=['document', 'audio', 'photo', 'text', 'sticker', 'video', 'video_note', 'voice', 'location',
                   'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo',
                   'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created',
                   'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message'])
def json_message(message):
    user_id = message.from_user.id
    if TgUser.objects.filter(user_id=user_id).exists():
        TgUser.objects.filter(user_id=user_id).update(first_name=message.from_user.first_name,
                                                      last_name=message.from_user.last_name,
                                                      username=message.from_user.username)
    else:
        TgUser.objects.create(user_id=user_id, first_name=message.from_user.first_name,
                              last_name=message.from_user.last_name, username=message.from_user.username)

    data = json.dumps({'update_id': bot.last_update_id,
                       'message': message.json}, indent=1)
    text = '`' + data + '`'
    tg_user = TgUser.objects.filter(user_id=user_id).first()
    History(tg_user=tg_user, text=str(data)).save()
    if message.chat.type == "private":
        bot.send_message(message.from_user.id, text, parse_mode='MARKDOWN')

    if message.chat.type == "group":
        bot.send_message(message.chat.id, text, parse_mode='MARKDOWN')

    if message.chat.type == "supergroup":
        bot.send_message(message.chat.id, text, parse_mode='MARKDOWN')
