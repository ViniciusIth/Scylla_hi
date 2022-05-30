# pylint: skip-file
import lightbulb

plugin = lightbulb.Plugin(...)

@plugin.command()
@lightbulb.command(...)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def test(ctx: lightbulb.Context):
	...


def load(bot):
	print(f"Succesfully loaded {plugin.name}!")
	bot.add_plugin(plugin)

def unload(bot):
	print(f"Succesfully unloaded {plugin.name}!")
	bot.remove_plugin(plugin)