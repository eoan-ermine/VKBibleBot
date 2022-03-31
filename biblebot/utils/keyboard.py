from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from biblebot import utils

def get_selection_keyboard(chunks, rows_per_page, columns_per_row, page, title, item_content, item_payload, next_payload, prev_payload):
    keyboard = VkKeyboard()
    rows = list(utils.page(chunks, page, rows_per_page))

    keyboard.add_button(title(), color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()

    for row in rows:
        for item in row:
            keyboard.add_button(item_content(item), payload=item_payload(item))
        keyboard.add_line()

    if page > 0:
        keyboard.add_button("Назад", color=VkKeyboardColor.PRIMARY, payload=next_payload())
    if len(rows) == rows_per_page and len(rows[-1]) == columns_per_row:    
        keyboard.add_button("Далее", color=VkKeyboardColor.PRIMARY, payload=prev_payload())
    return keyboard.get_keyboard()
