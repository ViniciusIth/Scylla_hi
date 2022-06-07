import os
import hikari
import lightbulb

# if os.name != "nt":
# 	import uvloop
# 	uvloop.install()

bot = lightbulb.BotApp(
	force_color=True,
	token=os.environ["TOKEN"],
	default_enabled_guilds=os.environ["TEST_GUILD_ID"].split(","),
	intents=hikari.Intents.ALL,
	help_slash_command=True,
	prefix="..",
)


@bot.command()
@lightbulb.command(name="ping", description="Ping the bot.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmdPing(ctx: lightbulb.Context) -> None:
	await ctx.respond(f"Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms")


@bot.command()
@lightbulb.option("text", "What you want the bot to say.")
@lightbulb.command("say", "Make the bot say something.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmdSay(ctx: lightbulb.SlashContext or lightbulb.Context) -> None:
	await ctx.respond(ctx.options.text)


@bot.command()
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option(name="extension", description="The extension to reload.")
@lightbulb.command(name="reload", description="Reload extensions")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmdReload(ctx: lightbulb.Context) -> None:
	if ctx.options.extension == "all":
		for extension in bot.extensions:
			bot.reload_extensions(extension)
			await ctx.respond('All reloaded succesfuly!')
			return
	bot.reload_extensions(f"scylla.commands.{ctx.options.extension}")
	await ctx.respond(f"{ctx.options.extension} reloaded succesfuly!")


def run() -> None:
	# if os.name != "nt":
	# 	import uvloop
	# 	uvloop.install()

	bot.load_extensions_from("scylla\\commands")
	bot.load_extensions_from("scylla\\auto")
	bot.run(asyncio_debug=True)
