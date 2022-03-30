from kutana import Plugin, t
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from biblebot import utils

COLUMNS_PER_ROW = 3
ROWS_PER_PAGE = 3

def get_books():
    r = requests.get("http://212.109.198.115/books")
    return r.json()["items"]

def get_keyboard(books, page: int):
    keyboard = VkKeyboard()
    rows = utils.page(books, page, ROWS_PER_PAGE)

    for i, row in enumerate(rows):
        for book in row:
            keyboard.add_button(book["long_name"], payload={"command": "select_chapter", "book": book["id"], "page": 0})
        keyboard.add_line()

    if page > 0:
        keyboard.add_button("Назад", color=VkKeyboardColor.PRIMARY, payload={"command": "select_book", "page": page - 1})
    if len(rows) == ROWS_PER_PAGE and len(rows[-1]) == COLUMNS_PER_ROW:    
        keyboard.add_button("Далее", color=VkKeyboardColor.PRIMARY, payload={"command": "select_book", "page": page + 1})
    return keyboard.get_keyboard()

plugin = Plugin(
    name = t("Выбор книги"),
    description = t("Позволяет выбрать книгу")
)
books = list(utils.chunks(get_books(), COLUMNS_PER_ROW))

@plugin.on_commands(["начать"])
async def __(msg, ctx):
    await ctx.reply(message="Выберите книгу", keyboard=get_keyboard(books, 0))

@plugin.vk.on_payloads([{"command": "select_book"}])
async def __(msg, ctx):
    await ctx.reply(message="Выберите книгу", keyboard=get_keyboard(books, ctx.payload["page"]))
