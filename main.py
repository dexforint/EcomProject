import asyncio
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from dotenv import dotenv_values

# import keyboards as kb
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

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
    # id2project[user_id] = {"default_layout": ThemeLayout(), "buffer_layouts": []}
    user_project = id2project.get(user_id, None)
    if user_project is None:
        await message.answer(
            "Проект создан!\n   Введите описание для ваших визуальных материалов. Сервис предоставит несколько вариантов. Выберите один из них, с которым вы будете дальше работать. \n    Чтобы сделать вариации дизайна - выполните команду **/get_variations**, затем выберите один из них.\n    Чтобы изменить один из элементов дизайна - просто введите свой запрос, понятно объяснив его. **Старайтесь** не перегружать запрос (один запрос - одно изменение).\n    Чтобы отрендерить изображение в определённом формате - введите **/render_image <NUM>**, где <NUM> - одно из чисел:\n1. Информационные доски \n2. Настольные демонстрационные системы\n3. Экраны блокировки персональных компьютеров\n4. Интранет-портал\n5. Дайджест новостей\n6. ТВ-панель\n7. Информационное сообщение\n\nЧтобы получить дизайн в формате PPTX - введите **/render_pptx <NUM>**. .\n\nПосле того, как вы закончите работу с данным проектом выполните команду **/close_project**."
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


@dp.callback_query(F.data.startswith("exportimage_"))
async def catalog(callback: types.CallbackQuery):
    kb = [
        [
            types.InlineKeyboardButton(text="Каталог", callback_data="catalog"),
            types.InlineKeyboardButton(text="С пюрешкой", callback_data="base"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=kb,
    )

    await callback.answer("Уведомление")
    # await callback.message.answer("Вы выбрали способ подачи", reply_markup=keyboard)
    await callback.message.edit_text("Вы выбрали способ подачи", reply_markup=keyboard)
    await callback.message.answer_document(open("file.png", "RB"))


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
            "!Чтобы создать проект выполните команду **/create_project**."
        )
    else:
        if message.voice:
            file_id = message.voice.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            file_name = f"./audio/{file_id}.mp3"
            print(file_path)
            await bot.download_file(file_path, file_name)

        await message.answer("Обработка запроса")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
