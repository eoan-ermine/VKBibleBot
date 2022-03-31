from kutana import Plugin, t
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from biblebot import utils

COLUMNS_PER_ROW = 5
ROWS_PER_PAGE = 3

def get_book_info(book_id: int):
    return requests.get(f"http://212.109.198.115/books.get?id={book_id}").json()

def get_chapters(book):
    return [i for i in range(1, book["chapters"] + 1)]

def get_keyboard(book_id: int, page: int):
    book = get_book_info(book_id)
    name = book["short_name"]

    return utils.get_selection_keyboard(
        list(utils.chunks(get_chapters(book), COLUMNS_PER_ROW)), ROWS_PER_PAGE, COLUMNS_PER_ROW, page, lambda: f"{name} — выбор главы — страница {page + 1}",
        lambda x: x, lambda x: {"command": "select_verse", "book": book_id, "chapter": x, "page": 0},
        lambda: {"command": "select_chapter", "book": book_id, "page": page - 1}, lambda: {"command": "select_chapter", "book": book_id, "page": page + 1}
    )

plugin = Plugin(
    name = t("Выбор главы"),
    description = t("Позволяет выбрать главу")
)

@plugin.vk.on_payloads([{"command": "select_chapter"}])
async def __(msg, ctx):
    await ctx.reply("Выберите главу", keyboard=get_keyboard(ctx.payload["book"], ctx.payload["page"]))
