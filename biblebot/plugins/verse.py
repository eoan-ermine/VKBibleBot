from kutana import Plugin, t
import requests

plugin = Plugin(
    name = t("Стих"),
    description = t("Позволяет получить текст стиха")
)

@plugin.vk.on_payloads([{"command": "verse"}])
async def __(msg, ctx):
    payload = ctx.payload
    await ctx.reply(
        requests.get(
            "http://212.109.198.115/verse",
            params={"book": payload["book"], "chapter": payload["chapter"], "verse": payload["verse"]}
        ).json()["text"]
    )
