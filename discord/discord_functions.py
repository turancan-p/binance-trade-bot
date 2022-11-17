from discord_webhook import DiscordWebhook, DiscordEmbed
from settings.configs import DISCORD_WEBHOOK_URL


webhook = DiscordWebhook(url=f'{DISCORD_WEBHOOK_URL}', username="T-Crypto")


def send_message(symbol, type, budget, amount, price, total_process, pnl, win_rate):
    if DISCORD_WEBHOOK_URL == "":
        return "Web Hook Empty"
    else:
        color = 'f8bb03'
        if type == "BUY":
            color = '03f848'
        elif type == "SELL":
            color = 'f83403'

        embed = DiscordEmbed(
            title=f'{type}', description=f'{symbol}', color=color
        )
        embed.set_author(
            name="Turan Can Pamuk",
            url="https://github.com/turancan-p",
            icon_url="https://avatars.githubusercontent.com/u/98945441?s=400&u=878c9810439a0f66ce09042a0b13e6a45653fd5a&v=4",
        )

        embed.set_footer(text="Process Date:")
        embed.set_timestamp()
        embed.add_embed_field(name="Budget", value=f'{budget}')
        embed.add_embed_field(name="Coin Amount", value=f'{amount}')
        embed.add_embed_field(name="Process Price", value=f'{price}', inline=False)
        embed.add_embed_field(name="PNL", value=f'{pnl}', inline=False)
        embed.add_embed_field(name="Total Process", value=f'{total_process}')
        embed.add_embed_field(name="Win Rate", value=f'{win_rate}')

        webhook.add_embed(embed)
        response = webhook.execute()
        return response


