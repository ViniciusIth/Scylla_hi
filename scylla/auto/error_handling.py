import lightbulb

plugin = lightbulb.Plugin("ErrorPlugin")

# @plugin.listener(lightbulb.CommandErrorEvent)
# async def onError(event: lightbulb.CommandErrorEvent) -> None:
# 	if isinstance(event.exception, lightbulb.CommandInvocationError):
# 		await event.context.respond(f"Something went wrong during invocation \
# 			of command `{event.context.command.name}` \
# 				\nError Log ```{event.exception.original}```")

# 	raise event.exception.original


def load(bot):
	print(f"Succesfully loaded {plugin.name}!")
	bot.add_plugin(plugin)

def unload(bot):
	print(f"Succesfully unloaded {plugin.name}!")
	bot.remove_plugin(plugin)
