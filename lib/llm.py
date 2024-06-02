import os
import openai
import json
from lib.utils import parse_json
from dotenv import dotenv_values
from time import sleep

config = dotenv_values(".env")

MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

API_KEYS = config["LLM_API_KEYS"].strip().split(",")


CLIENTS = [
    openai.OpenAI(
        api_key=api_key,
        base_url="https://api.together.xyz/v1",
    )
    for api_key in API_KEYS
]

N_CLIENTS = len(API_KEYS)
current_cliend_index = 0


def get_answer(messages, temperature=0.7):
    global current_cliend_index, N_CLIENTS, MODEL_NAME

    sleep(1)

    client = CLIENTS[current_cliend_index]
    print(f"Current client index: {current_cliend_index}")
    current_cliend_index = (current_cliend_index + 1) % N_CLIENTS

    chat_completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=temperature,
        # max_tokens=1024,
    )

    answer = chat_completion.choices[0].message.content
    answer = answer.replace("\\_", "_")
    print(f"Answer: {answer}")
    answer = parse_json(answer)
    return answer


def create_background_prompt(query, theme, background_color):
    system_prompt = f"""Ты являешься цифровым дизайнером, который использует Stable Diffusion для генерации фоновых изображений для рекламных баннеров и презентаций. Твоя задача - по запросу пользователя и выбранной теме рекламного баннера придумать два текста: prompt - текст на английском языке, описывающий генерируемое изображение фона для Stable Diffusion и negative_prompt - текст на английском языке, описывающий нежелательные черты и элементы генерируемого изображения фона.

Помни: сгенерированный фон будет вставлен в рекламный баннер, сгенерированный фон должен соответствовать запроосу пользователя и выбранной теме. Фон не должен быть сложным, он должен стремиться быть более абстрактным.

Фон должен быть минималистичным и не сливаться с остальными элементами.

Если запрос пользователя и тема противоречат друг другу, то ты должен отдавать предпочтение запросу пользователя.

Ответ должен быть исключительно в формате JSON с полями: prompt, negative_prompt. Помни, твой ответ должен быть без ошибок обработан с помощью json.loads (Python язык программирования).
"""

    user_prompt = f"""Запрос пользователя:
\"\"\"{query}\"\"\"

Заданная тема:
\"\"\"{theme}\"\"\"

Цвет тон фона: {background_color}
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    llm_answer = get_answer(messages)

    return llm_answer


def change_background_prompt(
    query, theme, previous_background_prompt, background_color
):
    system_prompt = f"""Ты являешься цифровым дизайнером, который использует Stable Diffusion для генерации фоновых изображений для рекламных баннеров и презентаций. На данном этапе уже есть сгенерированное изображение фона, которое пользователь хочет изменить. Твоя задача - по запросу пользователя и выбранной теме рекламного баннера изменить существующий промпт, чтобы он соответствовал запросу пользователя и выбранной теме. Для этого ты должен придумать два текста: prompt - текст на английском языке, описывающий генерируемое изображение фона для Stable Diffusion и negative_prompt - текст на английском языке, описывающий нежелательные черты и элементы генерируемого изображения фона.

Помни: сгенерированный фон будет вставлен в рекламный баннер, сгенерированный фон должен соответствовать запроосу пользователя и выбранной теме. Фон не должен быть сложным, он должен стремиться быть более абстрактным.

Фон должен быть минималистичным и не сливаться с остальными элементами.

Если запрос пользователя и тема противоречат друг другу, то ты должен отдавать предпочтение запросу пользователя.

Ответ должен быть исключительно в формате JSON с полями: prompt, negative_prompt. Помни, твой ответ должен быть без ошибок обработан с помощью json.loads (Python язык программирования).
"""

    user_prompt = f"""Запрос пользователя:
\"\"\"{query}\"\"\"

Заданная тема:
\"\"\"{theme}\"\"\"

Предыдущий промпт:
\"\"\"{previous_background_prompt}\"\"\"

Цвет тон фона: {background_color}
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    llm_answer = get_answer(messages)

    return llm_answer


def generate_image_prompt(query, theme, background_color):
    system_prompt = f"""Ты являешься цифровым дизайнером, который использует Stable Diffusion для генерации изображений для рекламных баннеров и презентаций. Твоя задача - по запросу пользователя, цвету фона и выбранной теме рекламного баннера придумать два текста: prompt - текст на английском языке, описывающий генерируемое изображение для Stable Diffusion и negative_prompt - текст на английском языке, описывающий нежелательные черты и элементы генерируемого изображения. 

Так же учти, что после генерации изображения, задний фон изображения будет вырезан с помощью отдельной нейронной сети, поэтому передний фон и задний фон должны отчётливо выделяться.

Помни: сгенерированное изображение будет вставлено в рекламный баннер, сгенерированное изображение должно соответствовать запроосу пользователя и выбранной теме. Сгенерированное изображение не должно быть сложным. Сгенерированное изображение должно быть похожим на векторную иллюстрацию или на другие графические элементы, присущие баннерам и презентациям. 

Если запрос пользователя и тема противоречат друг другу, то ты должен отдавать предпочтение запросу пользователя.

Ответ должен быть исключительно в формате JSON с полями: prompt, negative_prompt. Помни, твой ответ должен быть без ошибок обработан с помощью json.loads (Python язык программирования).
"""

    user_prompt = f"""Запрос пользователя:
\"\"\"{query}\"\"\"

Заданная тема:
\"\"\"{theme}\"\"\"

Цвет заднего фона:
\"\"\"{background_color}\"\"\"
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    llm_answer = get_answer(messages)

    return llm_answer


def change_image_propmt(previous_prompt, query, theme):
    system_prompt = f"""Ты являешься цифровым дизайнером, который использует Stable Diffusion для генерации изображений для рекламных баннеров и презентаций. Твоя задача - по запросу пользователя и выбранной теме рекламного баннера изменить предыдущий промпт сгенерированного изображения. Для этого ты должен придумать два текста: prompt - текст на английском языке, описывающий генерируемое изображение для Stable Diffusion и negative_prompt - текст на английском языке, описывающий нежелательные черты и элементы генерируемого изображения. 

Так же учти, что после генерации изображения, задний фон изображения будет вырезан с помощью отдельной нейронной сети, поэтому передний фон и задний фон должны отчётливо выделяться.

Помни: сгенерированное изображение будет вставлено в рекламный баннер, сгенерированное изображение должно соответствовать запроосу пользователя и выбранной теме. Сгенерированное изображение не должно быть сложным. Сгенерированное изображение должно быть похожим на векторную иллюстрацию или на другие графические элементы, присущие баннерам и презентациям. 

Если запрос пользователя и тема противоречат друг другу, то ты должен отдавать предпочтение запросу пользователя.

Ответ должен быть исключительно в формате JSON с полями: prompt, negative_prompt. Помни, твой ответ должен быть без ошибок обработан с помощью json.loads (Python язык программирования).
"""

    user_prompt = f"""Запрос пользователя:
\"\"\"{query}\"\"\"

Заданная тема:
\"\"\"{theme}\"\"\"

Предыдущий промпт:
\"\"\"{previous_prompt}\"\"\"
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    llm_answer = get_answer(messages)

    return llm_answer


def get_theme_object(query):
    system_prompt = f"""Ты являешься профессиональным цифровым дизайнером, который создаёт дизайн для рекламных баннеров и для слайдов презентаций. Твоя задача - по запросу пользователя придумать тему дизайна (описание баннера и цвета), а именно придумать:
- description: концепция дизайна баннера, описание того, что из себя представляет баннер, который хочет создать пользователь. Прояви здесь креативность.
- background_color: цвет фона баннера.
- button_color: цвет кнопки на баннере.
- button_text_color: цвет текста на кнопке.
- header_text_color: цвет текста на заголовке баннера.
- text_color: цвет остального текста на баннере.

Помни: цвета должны сочетаться друг с другом стилистически. Пользователь может ввести не полное описание темы, а лишь заголовок баннера, в таком случае тебе нужно проявить креативность и всё равно создать дизайн.

Все цвета должны быть в формате RGB (Пример: [255, 120, 0])

Ответ должен быть исключительно в формате JSON с полями: description, background_color, button_color, button_text_color, header_text_color, text_color. Помни, твой ответ должен быть без ошибок обработан с помощью json.loads (Python язык программирования).
"""

    user_prompt = f"""Запрос пользователя:
\"\"\"{query}\"\"\"
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    llm_answer = get_answer(messages)
    return llm_answer


def structure_query(query):
    system_prompt = f"""Ты являешься профессиональным аналитиком текстов. Твоя задача - по запросу пользователя определить:
1. element - какой элемент пользователь хочет изменить. Это может быть:
    - background: фон баннера.
    - button: кнопка баннера.
    - header: заголовок баннера.
    - text: текст баннера.
    - image: изображение баннера.
    - none: пользователь ничего не хочет менять в баннере.
2. action - как именно он хочет изменить выбранный элемент. Это может быть:
    - set: дать элементу новое значение
    - change: изменить существующий элемент
    - delete: удалить выбранный элемент
    - none: пользователь ничего не хочет менять в баннере.

Ответ должен быть исключительно в формате JSON с полями: element, action. Значение поля element должно быть одним из: background, button, header, text, image, none. Значение поля action должно быть одним из: set, change, delete, none.
Помни, твой ответ должен быть без ошибок обработан с помощью json.loads (Python язык программирования).
"""

    user_prompt = f"""Запрос пользователя:
\"\"\"{query}\"\"\"
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    llm_answer = get_answer(messages)
    return llm_answer


def generate_text(query, theme, header):
    system_prompt = f"""Ты являешься профессиональным цифровым дизайнером, который создаёт дизайн для рекламных баннеров и для слайдов презентаций. Твоя задача - на основе запроса пользователя, темы дизайна и заголовка баннера придумать побочный текст баннера, а именно нужно придумать:
- text: побочный текст баннера.

Помни: цвета должны сочетаться друг с другом стилистически. Пользователь может ввести не полное описание темы, а лишь заголовок баннера, в таком случае тебе нужно проявить креативность и всё равно создать дизайн.

Если запрос пользователя и тема противоречат друг другу, то ты должен отдавать предпочтение запросу пользователя.

Следуй инструкциям из запроса пользователя.

Ответ должен быть исключительно в формате JSON с полями: text. Помни, твой ответ должен быть без ошибок обработан с помощью json.loads (Python язык программирования).
"""

    user_prompt = f"""Запрос пользователя:
\"\"\"{query}\"\"\"

Тема дизайна:
\"\"\"{theme}\"\"\"

Заголовок баннера:
\"\"\"{header}\"\"\"
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    llm_answer = get_answer(messages)
    return llm_answer


def change_text(query, theme, prev_text, prev_text_color, header):
    system_prompt = f"""Ты являешься профессиональным цифровым дизайнером, который создаёт дизайн для рекламных баннеров и для слайдов презентаций. На данном этапе на баннере уже имеется побочный текст, который пользователь хочет изменить. Твоя задача - на основе запроса пользователя, темы дизайна, предыдущего текста, предыдущего цвета текста и заголовка баннера придумать побочный текст баннера, а именно нужно придумать:
- text: побочный текст баннера.
- text_color: цвет побочного текста баннера в формате RGB (Пример: [255, 120, 0]).

Помни: цвета должны сочетаться друг с другом стилистически. Пользователь может ввести не полное описание темы, а лишь заголовок баннера, в таком случае тебе нужно проявить креативность и всё равно создать дизайн.

Если запрос пользователя и тема противоречат друг другу, то ты должен отдавать предпочтение запросу пользователя.

Не изменяй те поля, которые пользователь не упоминает в запросе. Следуй инструкциям из запроса пользователя.

Ответ должен быть исключительно в формате JSON с полями: text, text_color. Помни, твой ответ должен быть без ошибок обработан с помощью json.loads (Python язык программирования).
"""

    user_prompt = f"""Запрос пользователя:
\"\"\"{query}\"\"\"

Тема дизайна:
\"\"\"{theme}\"\"\"

Заголовок баннера:
\"\"\"{header}\"\"\"

Заголовок баннера:
\"\"\"{header}\"\"\"

Предыдущий текст:
\"\"\"{prev_text}\"\"\"

Предыдущий цвет текста:
\"\"\"{prev_text_color}\"\"\"
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    llm_answer = get_answer(messages)
    return llm_answer


def generate_button(query, theme):
    system_prompt = f"""Ты являешься профессиональным цифровым дизайнером, который создаёт дизайн для рекламных баннеров и для слайдов презентаций. Твоя задача - на основе запроса пользователя и темы дизайна придумать описание кнопки баннера, а именно нужно придумать:
- background_color: цвет кнопки в формате RGB (Пример: [255, 120, 0]).
- text_color: цвет текста на кнопке в формате RGB (Пример: [255, 120, 0]).
- text: текст кнопки (Например: "Подробнее").

Помни: цвета должны сочетаться друг с другом стилистически. Не надо делать белый текст на белом фоне и тому подобное. Пользователь может ввести не полное описание темы, а лишь заголовок баннера, в таком случае тебе нужно проявить креативность и всё равно создать дизайн.

Если запрос пользователя и тема противоречат друг другу, то ты должен отдавать предпочтение запросу пользователя.

Следуй инструкциям из запроса пользователя. Не изменяй те поля, которые пользователь не упоминает в запросе. Следуй инструкциям из запроса пользователя.

Ответ должен быть исключительно в формате JSON с полями: background_color, text_color, text. Помни, твой ответ должен быть без ошибок обработан с помощью json.loads (Python язык программирования).
"""
    user_prompt = f"""Запрос пользователя:
\"\"\"{query}\"\"\"

Тема дизайна:
\"\"\"{theme}\"\"\"
"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    llm_answer = get_answer(messages)
    return llm_answer


def change_button(query, theme, prev_background_color, prev_text_color, prev_text):
    system_prompt = f"""Ты являешься профессиональным цифровым дизайнером, который создаёт дизайн для рекламных баннеров и для слайдов презентаций. На данном этапе на баннере уже имеется кнопка, которую пользователь хочет изменить. Твоя задача - на основе запроса пользователя, темы дизайна, предыдущего цвета кнопки, предыдущего цвета текста на кнопке и предыдущего текста на кнопке придумать описание кнопки баннера, а именно нужно придумать:
- background_color: цвет кнопки в формате RGB (Пример: [255, 120, 0]).
- text_color: цвет текста на кнопке в формате RGB (Пример: [255, 120, 0]).
- text: текст кнопки (Например: "Подробнее").

Помни: цвета должны сочетаться друг с другом стилистически. Пользователь может ввести не полное описание темы, а лишь заголовок баннера, в таком случае тебе нужно проявить креативность и всё равно создать дизайн.

Если запрос пользователя и тема противоречат друг другу, то ты должен отдавать предпочтение запросу пользователя.

Следуй инструкциям из запроса пользователя. Не изменяй те поля, которые пользователь не упоминает в запросе. Следуй инструкциям из запроса пользователя.

Ответ должен быть исключительно в формате JSON с полями: background_color, text_color, text. Помни, твой ответ должен быть без ошибок обработан с помощью json.loads (Python язык программирования).
"""

    user_prompt = f"""Запрос пользователя:
\"\"\"{query}\"\"\"

Тема дизайна:
\"\"\"{theme}\"\"\"

Предыдущий цвет кнопки:
\"\"\"{prev_background_color}\"\"\"

Предыдущий цвет текста на кнопке:
\"\"\"{prev_text_color}\"\"\"

Предыдущий текст на кнопке:
\"\"\"{prev_text}\"\"\"
"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    llm_answer = get_answer(messages)
    return llm_answer


def generate_header(query, theme):
    system_prompt = f"""Ты являешься профессиональным цифровым дизайнером, который создаёт дизайн для рекламных баннеров и для слайдов презентаций. Твоя задача - на основе запроса пользователя и темы дизайна придумать описание заголовка баннера, а именно нужно придумать:
- text_color: цвет текста заголовка в формате RGB (Пример: [255, 120, 0]).
- text: текст заголовка .

Помни: цвета должны сочетаться друг с другом стилистически. Пользователь может ввести не полное описание темы, а лишь заголовок баннера, в таком случае тебе нужно проявить креативность и всё равно создать дизайн.

Если запрос пользователя и тема противоречат друг другу, то ты должен отдавать предпочтение запросу пользователя.

Следуй инструкциям из запроса пользователя. Не изменяй те поля, которые пользователь не упоминает в запросе. Следуй инструкциям из запроса пользователя.

Ответ должен быть исключительно в формате JSON с полями: background_color, text_color, text. Помни, твой ответ должен быть без ошибок обработан с помощью json.loads (Python язык программирования).
"""
    user_prompt = f"""Запрос пользователя:
\"\"\"{query}\"\"\"

Тема дизайна:
\"\"\"{theme}\"\"\"
"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    llm_answer = get_answer(messages)
    return llm_answer


def change_header(query, theme, prev_text_color, prev_text):
    system_prompt = f"""Ты являешься профессиональным цифровым дизайнером, который создаёт дизайн для рекламных баннеров и для слайдов презентаций. На данном этапе на баннере уже имеется заголовок, котоый пользователь хочет изменить. Твоя задача - на основе запроса пользователя, темы дизайна, предыдущего цвета заголовка и предыдущего цвета текста заголовка придумать описание заголовка, а именно нужно придумать:
- text_color: цвет текста заголовка в формате RGB (Пример: [255, 120, 0]).
- text: текст заголовка.

Помни: цвета должны сочетаться друг с другом стилистически. Пользователь может ввести не полное описание темы, а лишь заголовок баннера, в таком случае тебе нужно проявить креативность и всё равно создать дизайн.

Если запрос пользователя и тема противоречат друг другу, то ты должен отдавать предпочтение запросу пользователя.

Следуй инструкциям из запроса пользователя. Не изменяй те поля, которые пользователь не упоминает в запросе.

Ответ должен быть исключительно в формате JSON с полями: text_color, text. Помни, твой ответ должен быть без ошибок обработан с помощью json.loads (Python язык программирования).
"""

    user_prompt = f"""Запрос пользователя:
\"\"\"{query}\"\"\"

Тема дизайна:
\"\"\"{theme}\"\"\"

Предыдущий цвет текста заголовка:
\"\"\"{prev_text_color}\"\"\"

Предыдущий текст заголовка:
\"\"\"{prev_text}\"\"\"
"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    llm_answer = get_answer(messages)
    return llm_answer


def generate_text(query, theme, header):
    system_prompt = f"""Ты являешься профессиональным цифровым дизайнером, который создаёт дизайн для рекламных баннеров и для слайдов презентаций. Твоя задача - на основе запроса пользователя и темы дизайна придумать описание заголовка баннера, а именно нужно придумать:
- text_color: цвет текста в формате RGB (Пример: [255, 120, 0]).
- text: текст.

Помни: цвета должны сочетаться друг с другом стилистически. Пользователь может ввести не полное описание темы, а лишь заголовок баннера, в таком случае тебе нужно проявить креативность и всё равно создать дизайн.

Если запрос пользователя и тема противоречат друг другу, то ты должен отдавать предпочтение запросу пользователя.

Следуй инструкциям из запроса пользователя. Не изменяй те поля, которые пользователь не упоминает в запросе. Следуй инструкциям из запроса пользователя.

Ответ должен быть исключительно в формате JSON с полями: text_color, text. Помни, твой ответ должен быть без ошибок обработан с помощью json.loads (Python язык программирования).
"""
    user_prompt = f"""Запрос пользователя:
\"\"\"{query}\"\"\"

Тема дизайна:
\"\"\"{theme}\"\"\"

Заголовок:
\"\"\"{header}\"\"\"
"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    llm_answer = get_answer(messages)
    return llm_answer


def change_text(query, theme, prev_text_color, prev_text, header):
    system_prompt = f"""Ты являешься профессиональным цифровым дизайнером, который создаёт дизайн для рекламных баннеров и для слайдов презентаций. На данном этапе на баннере уже имеется заголовок, котоый пользователь хочет изменить. Твоя задача - на основе запроса пользователя, темы дизайна, предыдущего цвета заголовка и предыдущего цвета текста заголовка придумать описание заголовка, а именно нужно придумать:
- text_color: цвет текста заголовка в формате RGB (Пример: [255, 120, 0]).
- text: текст заголовка.

Помни: цвета должны сочетаться друг с другом стилистически. Пользователь может ввести не полное описание темы, а лишь заголовок баннера, в таком случае тебе нужно проявить креативность и всё равно создать дизайн.

Если запрос пользователя и тема противоречат друг другу, то ты должен отдавать предпочтение запросу пользователя.

Следуй инструкциям из запроса пользователя. Не изменяй те поля, которые пользователь не упоминает в запросе.

Ответ должен быть исключительно в формате JSON с полями: text_color, text. Помни, твой ответ должен быть без ошибок обработан с помощью json.loads (Python язык программирования).
"""

    user_prompt = f"""Запрос пользователя:
\"\"\"{query}\"\"\"

Тема дизайна:
\"\"\"{theme}\"\"\"

Предыдущий цвет текста:
\"\"\"{prev_text_color}\"\"\"

Предыдущий текст:
\"\"\"{prev_text}\"\"\"

Заголовок:
\"\"\"{header}\"\"\"
"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    llm_answer = get_answer(messages)
    return llm_answer
