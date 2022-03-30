from kutana import Plugin, t
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from biblebot import utils

COLUMNS_PER_ROW = 5
ROWS_PER_PAGE = 3

def get_chapters(book_id: int):
    r = requests.get(f"http://212.109.198.115/books.get?id={book_id}")
    return [i for i in range(1, r.json()["chapters"] + 1)]

def get_keyboard(book_id: int, page: int):
    keyboard = VkKeyboard()
    rows = utils.page(list(utils.chunks(get_chapters(book_id), COLUMNS_PER_ROW)), page, ROWS_PER_PAGE)

    for i, row in enumerate(rows):
        for button in row:
            keyboard.add_button(button)
        keyboard.add_line()

    if page > 0:
        keyboard.add_button("Назад", color=VkKeyboardColor.PRIMARY, payload={"command": "select_chapter", "book": book_id, "page": page - 1})
    if len(rows) == ROWS_PER_PAGE:    
        keyboard.add_button("Далее", color=VkKeyboardColor.PRIMARY, payload={"command": "select_chapter", "book": book_id, "page": page + 1})
    return keyboard.get_keyboard()


plugin = Plugin(
    name = t("Выбор главы"),
    description = t("Позволяет выбрать главу")
)

@plugin.vk.on_payloads([{"command": "select_chapter"}])
async def __(msg, ctx):
    await ctx.reply("Выберите главу", keyboard=get_keyboard(ctx.payload["book"], ctx.payload["page"]))
