from kutana import Plugin, t
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from biblebot import utils

COLUMNS_PER_ROW = 5
ROWS_PER_PAGE = 3

def get_verses(book_id: int, chapter: int):
    r = requests.get(f"http://212.109.198.115/chapter?book_id={book_id}&chapter={chapter}")
    return [i for i in range(1, r.json()["verses"] + 1)]

def get_keyboard(book_id: int, chapter: int, page: int):
    keyboard = VkKeyboard()
    rows = utils.page(list(utils.chunks(get_verses(book_id, chapter), COLUMNS_PER_ROW)), page, ROWS_PER_PAGE)

    for i, row in enumerate(rows):
        for verse in row:
            keyboard.add_button(verse, payload={"command": "verse", "book": book_id, "chapter": chapter, "verse": verse})
        keyboard.add_line()

    if page > 0:
        keyboard.add_button("Назад", color=VkKeyboardColor.PRIMARY, payload={"command": "select_verse", "book": book_id, "chapter": chapter, "page": page - 1})
    if len(rows) == ROWS_PER_PAGE and len(rows[-1]) == COLUMNS_PER_ROW:    
        keyboard.add_button("Далее", color=VkKeyboardColor.PRIMARY, payload={"command": "select_verse", "book": book_id, "chapter": chapter, "page": page + 1})
    return keyboard.get_keyboard()

plugin = Plugin(
    name = t("Выбор стиха"),
    description = t("Позволяет выбрать стих")
)

@plugin.vk.on_payloads([{"command": "select_verse"}])
async def __(msg, ctx):
    await ctx.reply("Выберите стих", keyboard=get_keyboard(ctx.payload["book"], ctx.payload["chapter"], ctx.payload["page"]))
