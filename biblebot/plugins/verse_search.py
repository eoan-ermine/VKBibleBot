from kutana import Plugin, t
import requests

plugin = Plugin(
    name = t("Поиск стиха"),
    description = t("Позволяет получить текст стиха по человекочитаемому запросу")
)
books = requests.get("http://212.109.198.115/books").json()["items"]

@plugin.on_commands([e["short_name"] for e in books] + [e["long_name"] for e in books])
async def __(msg, ctx):
    await ctx.reply("\n".join(requests.get(
        "http://212.109.198.115/verses.search",
        params={"query": msg.text}
    ).json()["items"]))
