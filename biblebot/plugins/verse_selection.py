from kutana import Plugin, t
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from biblebot import utils

COLUMNS_PER_ROW = 5
ROWS_PER_PAGE = 3

def get_book_info(book_id: int):
    return requests.get(f"http://212.109.198.115/books.get?id={book_id}").json()

def get_verses(book_id: int, chapter: int):
    r = requests.get(f"http://212.109.198.115/chapter?book_id={book_id}&chapter={chapter}")
    return [i for i in range(1, r.json()["verses"] + 1)]

def get_keyboard(book_id: int, chapter: int, page: int):
    book = get_book_info(book_id)
    name = book["short_name"]

    return utils.get_selection_keyboard(
        list(utils.chunks(get_verses(book_id, chapter), COLUMNS_PER_ROW)), ROWS_PER_PAGE, COLUMNS_PER_ROW, page, lambda: f"{name}:{chapter} — выбор стиха — страница {page + 1}",
        lambda x: x, lambda x: {"command": "verse", "book": book_id, "chapter": chapter, "verse": x},
        lambda: {"command": "select_verse", "book": book_id, "chapter": chapter, "page": page - 1}, lambda: {"command": "select_verse", "book": book_id, "chapter": chapter, "page": page + 1}
    )

plugin = Plugin(
    name = t("Выбор стиха"),
    description = t("Позволяет выбрать стих")
)

@plugin.vk.on_payloads([{"command": "select_verse"}])
async def __(msg, ctx):
    await ctx.reply("Выберите стих", keyboard=get_keyboard(ctx.payload["book"], ctx.payload["chapter"], ctx.payload["page"]))
