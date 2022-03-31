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
    return utils.get_selection_keyboard(
        books, ROWS_PER_PAGE, COLUMNS_PER_ROW, page, lambda: f"Выбор книги — страница {page + 1}",
        lambda x: x["long_name"], lambda x: {"command": "select_chapter", "book": x["id"], "page": 0},
        lambda: {"command": "select_book", "page": page - 1}, lambda: {"command": "select_book", "page": page + 1}
    )

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
