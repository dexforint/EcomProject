import asyncio
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from dotenv import dotenv_values
from lib.asr import speech2text
from lib.design_controller import DesignController

# import keyboards as kb
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from lib.utils import get_random_string

config = dotenv_values(".env")

bot = Bot(token=config["TELEGRAM_API_KEY"])
dp = Dispatcher()

id2project = {}


@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    await message.answer(
        "Привет!\n\nЯ являюсь цифровым помощником для разработки дизайнерских решений рекламных продуктов (баннеров, скринсейверов и т.д.).\n\n-Чтобы начать работу над новым проектом выполните команду /create_project."
    )


@dp.message(Command("create_project"))
async def create_project(message: types.Message):
    user_id = message.from_user.id
    user_project = id2project.get(user_id, None)
    if user_project is None:
        id2project[user_id] = {
            "design": None,
            "first_query": True,
            "variations": [],
        }
        await message.answer(
            "Проект создан!\n   Введите описание для ваших визуальных материалов.\n    Чтобы сделать вариации дизайна - выполните команду **/get_variations**, затем выберите один из них.\n    Чтобы изменить один из элементов дизайна - просто введите свой запрос, понятно объяснив его. **Старайтесь** не перегружать запрос (один запрос - одно изменение).\n    Чтобы отрендерить изображение - введите **/render_image**. Чтобы получить дизайн в формате PPTX - введите **/render_pptx**.\n\nПосле того, как вы закончите работу с данным проектом выполните команду **/close_project**."
        )
    else:
        await message.answer(
            "Вы уже работаете над проектом. Чтобы закрыть его выполните команду **/close_project**."
        )


@dp.message(Command("get_variations"))
async def get_variations(message: types.Message):
    user_id = message.from_user.id
    user_project = id2project.get(user_id, None)

    if user_project is None:
        await message.answer(
            "Вы не работаете над проектом. Чтобы создать проект, выполните команду **/create_project**."
        )
        return

    # !TODO
    await message.answer(
        "Проект закрыт. Чтобы создать новый проект выполните команду **/create_project**."
    )


@dp.message(Command("render_image"))
async def render_image(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    user_project = id2project.get(user_id, None)

    if user_project is None:
        await message.answer(
            "Вы не работаете над проектом. Чтобы создать проект, выполните команду **/create_project**."
        )
        return

    num = 0
    if not (command.args is None):
        try:
            num = int(command.args)
            assert num in range(8)
        except:
            await message.answer(
                "Не удалось прочитать число. Число должно быть от 1 до 7 включительно."
            )

    # !TODO


@dp.message(Command("render_pptx"))
async def render_image(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    user_project = id2project.get(user_id, None)

    if user_project is None:
        await message.answer(
            "Вы не работаете над проектом. Чтобы создать проект, выполните команду **/create_project**."
        )
        return

    num = 0
    if not (command.args is None):
        try:
            num = int(command.args)
            assert num in range(8)
        except:
            await message.answer(
                "Не удалось прочитать число. Число должно быть от 1 до 7 включительно."
            )

    # !TODO

    # await message.answer(
    #     text="",
    #     photo="",
    #     caption=""
    # )


# !######################
@dp.message(Command("test"))
async def test(message: types.Message, command: CommandObject):
    kb = [
        [
            types.InlineKeyboardButton(text="Каталог", callback_data="catalog"),
            types.InlineKeyboardButton(text="Без пюрешки", callback_data="base"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=kb,
    )

    await message.reply("Тестовое сообщение", reply_markup=keyboard)


# !######################


@dp.message(Command("close_project"))
async def close_project(message: types.Message):
    user_id = message.from_user.id
    user_project = id2project.get(user_id, None)

    if user_project is None:
        await message.answer(
            "Вы не работаете над проектом. Чтобы создать проект, выполните команду **/create_project**."
        )
    else:
        id2project.pop(user_id, None)
        await message.answer(
            "Проект закрыт. Чтобы создать новый проект, выполните команду **/create_project**."
        )


# !Обработка простых сообщений
@dp.message()
async def message(message: types.Message):
    user_id = message.from_user.id
    user_project = id2project.get(user_id, None)

    if user_project is None:
        await message.answer(
            "Чтобы создать проект выполните команду **/create_project**."
        )
    else:
        if message.voice:
            file_id = message.voice.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path

            name = get_random_string(4)
            file_path = f"./audio/{name}.mp3"
            await bot.download_file(file_path, file_path)
            text = speech2text(file_path)
        else:
            text = message.text

        if user_project["first_query"]:

            user_project["first_query"] = False

        else:
            pass

        await message.answer("Обработка запроса")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
