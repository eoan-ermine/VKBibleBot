from kutana import Plugin, t
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

ROWS_PER_PAGE = 3

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_books():
    r = requests.get("http://212.109.198.115/books")
    return r.json()["items"]

def get_page(books, page: int):
    return books[page * ROWS_PER_PAGE:(page + 1) * ROWS_PER_PAGE]

def get_keyboard(books, page: int):
    keyboard = VkKeyboard()
    rows = get_page(books, page)

    for i, row in enumerate(rows):
        for button in row:
            keyboard.add_button(button)
        keyboard.add_line()

    if page > 0:
        keyboard.add_button("Назад", color=VkKeyboardColor.PRIMARY, payload={"command": "select_book", "page": page - 1})
    if len(rows) == ROWS_PER_PAGE:    
        keyboard.add_button("Далее", color=VkKeyboardColor.PRIMARY, payload={"command": "select_book", "page": page + 1})
    return keyboard.get_keyboard()

plugin = Plugin(
    name = t("Выбор книги"),
    description = t("Позволяет выбрать книгу")
)
books = list(chunks([e["long_name"] for e in get_books()], 3))

@plugin.on_commands(["начать"])
async def __(msg, ctx):
    await ctx.reply(message="Выберите книгу", keyboard=get_keyboard(books, 0))

@plugin.vk.on_payloads([{"command": "select_book"}])
async def __(msg, ctx):
    await ctx.reply(message="Выберите книгу", keyboard=get_keyboard(books, ctx.payload["page"]))
