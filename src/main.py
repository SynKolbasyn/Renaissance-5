import logging
import aiogram

import functions


with open("../game_data/token", "r") as file:
    API_TOKEN = file.read()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s\t| %(message)s",
    handlers=[
        logging.FileHandler(filename="../game_data/logs.log", mode="a"),
        logging.StreamHandler()
    ]
)

bot = aiogram.Bot(token=API_TOKEN)
dispatcher = aiogram.Dispatcher(bot)


async def setup_bot_commands(dispatcher):
    bot_commands = [
        aiogram.types.BotCommand(command="/start", description="Show start menu"),
        aiogram.types.BotCommand(command="/continue", description="Continue the game"),
        aiogram.types.BotCommand(command="/help", description="Show start menu"),
        aiogram.types.BotCommand(command="/info", description="Show player info"),
        aiogram.types.BotCommand(command="/inventory", description="Show player inventory"),
        aiogram.types.BotCommand(command="/change_lang", description="Changes language"),
        aiogram.types.BotCommand(command="/quests_progres", description="Quests progres info")
        ]
    await bot.set_my_commands(bot_commands)


@dispatcher.message_handler(commands="start")
async def proc_start(message: aiogram.types.Message):
    logging.info(f"Text: {message.text}\t| ID: {message.from_user.id}\t| User: {message.from_user.username}\t| "
                 f"Name: {message.from_user.full_name}")
    keyboard = aiogram.types.InlineKeyboardMarkup().add(*functions.get_action_buttons(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name
    ))
    # TODO: Rewrite '/start' message
    await message.answer_photo(
        open(
            functions.get_back_ground_image(
                message.from_user.id,
                message.from_user.username,
                message.from_user.full_name
            ),
            "rb"
        ),
        caption="Hi!\nI'm Renaissance!\nPowered by @umirotvoren1e.",
        reply_markup=keyboard
    )


@dispatcher.message_handler(commands="continue")
async def proc_continue(message: aiogram.types.Message):
    logging.info(f"Text: {message.text}\t| ID: {message.from_user.id}\t| User: {message.from_user.username}\t| "
                 f"Name: {message.from_user.full_name}")
    keyboard = aiogram.types.InlineKeyboardMarkup().add(*functions.get_action_buttons(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name
    ))
    await message.answer_photo(
        open(
            functions.get_back_ground_image(
                message.from_user.id,
                message.from_user.username,
                message.from_user.full_name
            ),
            "rb"
        ),
        caption="You continue from place where you stopped",
        reply_markup=keyboard
    )


@dispatcher.message_handler(commands="help")
async def proc_help(message: aiogram.types.Message):
    logging.info(f"Text: {message.text}\t| "
                 f"ID: {message.from_user.id}\t| "
                 f"User: {message.from_user.username}\t| "
                 f"Name: {message.from_user.full_name}")
    await message.reply("Hello, this is Renaissance - a telegram bot game.\n"
                        "To start or continue the game, you can use the /start or /continue commands, respectively.\n"
                        "The bot also has several auxiliary commands:\n"
                        "/info - shows your game information\n"
                        "/inventory - shows information about in-game inventory\n"
                        "/change_lang - allows you to change the game language\n"
                        "/quests_progres - shows information about current in-game quests\n"
                        "/help - shows this message\n"
                        "If you have any problems with the game or you want to offer your ideas for the game, write to @umirotvoren1e")


@dispatcher.message_handler(commands="info")
async def proc_info(message: aiogram.types.Message):
    logging.info(f"Text: {message.text}\t| "
                 f"ID: {message.from_user.id}\t| "
                 f"User: {message.from_user.username}\t| "
                 f"Name: {message.from_user.full_name}")
    answer = functions.get_player_info(message.from_user.id, message.from_user.username, message.from_user.full_name)
    await message.reply(answer)


@dispatcher.message_handler(commands="inventory")
async def proc_inventory(message: aiogram.types.Message):
    logging.info(f"Text: {message.text}\t| ID: {message.from_user.id}\t| User: {message.from_user.username}\t| "
                 f"Name: {message.from_user.full_name}")
    answer = functions.get_player_inventory_info(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name
    )
    await message.reply(answer)


@dispatcher.message_handler(commands="change_lang")
async def proc_change_lang(message: aiogram.types.Message):
    logging.info(f"Text: {message.text}\t| "
                 f"ID: {message.from_user.id}\t| "
                 f"User: {message.from_user.username}\t| "
                 f"Name: {message.from_user.full_name}")
    keyboard = aiogram.types.InlineKeyboardMarkup().add(*functions.get_languages_buttons())
    await message.answer_photo(
        open("../game_data/images/language.png", "rb"),
        caption="Choose game language",
        reply_markup=keyboard
    )


@dispatcher.message_handler(commands="quests_progres")
async def proc_tasks_progres(message: aiogram.types.Message):
    logging.info(f"Text: {message.text}\t| "
                 f"ID: {message.from_user.id}\t| "
                 f"User: {message.from_user.username}\t| "
                 f"Name: {message.from_user.full_name}")
    answer = functions.get_quests_progres(message.from_user.id, message.from_user.username, message.from_user.full_name)
    await message.reply(answer)


@dispatcher.message_handler()
async def main(message: aiogram.types.Message):
    logging.info(f"Text: {message.text}\t| "
                 f"ID: {message.from_user.id}\t| "
                 f"User: {message.from_user.username}\t| "
                 f"Name: {message.from_user.full_name}")
    await message.reply("Unknown action. Try '/start' or '/continue' command. Please write to @umirotvoren1e if you have problems with game")


@dispatcher.callback_query_handler(lambda a: (a.data in functions.get_all_actions()))
async def process_callback(callback_query: aiogram.types.CallbackQuery):
    logging.info(f"Text: {callback_query.message.caption}\t| "
                 f"Button: {callback_query.data}\t|"
                 f"ID: {callback_query.from_user.id}\t| "
                 f"User: {callback_query.from_user.username}\t| "
                 f"Name: {callback_query.from_user.full_name}")
    answer = functions.execute_action(
        callback_query.from_user.id,
        callback_query.from_user.username,
        callback_query.from_user.full_name,
        callback_query.data
    )
    keyboard = aiogram.types.InlineKeyboardMarkup().add(*functions.get_action_buttons(
        callback_query.from_user.id,
        callback_query.from_user.username,
        callback_query.from_user.full_name
    ))
    # try:
    await callback_query.message.edit_media(
        aiogram.types.InputMediaPhoto(
            open(
                functions.get_back_ground_image(
                    callback_query.from_user.id,
                    callback_query.from_user.username,
                    callback_query.from_user.full_name
                ),
                "rb"
            ),
            caption=answer
        ),
        reply_markup=keyboard
    )
    # except aiogram.exceptions.MessageNotModified as e:
    #     logging.info(e)


if __name__ == "__main__":
    aiogram.executor.start_polling(dispatcher, skip_updates=True, on_startup=setup_bot_commands)
