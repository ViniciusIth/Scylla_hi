import typing
import lightbulb
import hikari

plugin = lightbulb.Plugin('info')


@plugin.command()
@lightbulb.option(
	'member', 'O nome do membro que terá suas informações extraídas', hikari.Member
)
@lightbulb.command(name='member', description='Retorna informações sobre o mebro')
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def cmdMember(ctx: lightbulb.Context, member: hikari.Member = None) -> None:
	user: hikari.User = ctx.app.cache.get_user(ctx.options.member.user or member.user)
	member: hikari.Member = ctx.app.cache.get_member(
		ctx.get_guild(), ctx.options.member or member
	)

	roles_list = getRolesSorted(member)
	mention = ', '.join(roles_list) or '```O usuário não possui cargos.```'

	presence = member.get_presence()

	if presence is not None:
		if len(presence.activities) != 0:
			activity, status = (presence.activities[0], presence.visible_status)
			match activity.type:
				# case isinstance(activity, hikari.ActivityType.CUSTOM):
				# activity = activity
				case hikari.ActivityType.PLAYING:
					action = f'Jogando: {activity}'
				case hikari.ActivityType.STREAMING:
					action = f'Streamando: {activity}'
				case hikari.ActivityType.LISTENING:
					action = f'Ouvindo: {activity.details} - {activity.name}'
		else:
			action, status = (
				' ~ ~ Aparentemente, o usuário não está fazendo nada ~ ~ ',
				presence.visible_status,
			)
	else:
		action, status = (
			' ~ ~ Aparentemente, o usuário não está fazendo nada ~ ~ ',
			'Offline',
		)

	permission = [
		f'✅ {permission.name}' for permission in member.get_top_role().permissions
	]
	permission = '\n'.join(permission)

	message = hikari.Embed(title='Informações do usuário')
	message.set_thumbnail(user.avatar_url)
	message.add_field(name='User', value=f'```{user.username}#{user.discriminator}```')
	message.add_field(name='ID', value=f'```{user.id}```')
	message.add_field(name=f'Cargos [{len(roles_list)}]', value=mention, inline=False)
	message.add_field(name='Nickname', value=f'```{member.nickname}```')
	message.add_field(name='Status', value=f'```{status}```')
	message.add_field(name='Atividade', value=f'```{action}```', inline=False)
	message.add_field(
		name='Permissões Globais', value=f'```{permission}```', inline=False
	)
	message.add_field(
		name='Registrado em',
		value=f'```{user.created_at.strftime("%d/%m/%Y, %H:%M")}```',
	)
	message.add_field(
		name='Entrou em',
		value=f'```{member.joined_at.strftime("%d/%m/%Y, %H:%M")}```',
	)

	await ctx.respond(message)


@cmdMember.child()
@lightbulb.option(
	name='user', description='O usuário que terá sua imagem exposta.', type=hikari.User
)
@lightbulb.command('avatar', 'Pega a image de perfil um usuário.')
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def memberAvatar(ctx: lightbulb.Context, user: hikari.User = None) -> None:
	user: hikari.User = ctx.options.user or user or ctx.author

	await ctx.respond(
		f'Aqui está a imagem de perfil de {user.username}:\n {user.avatar_url}'
	)


@cmdMember.child()
@lightbulb.option(
	name='member',
	description='O usuário que terá sua imagem exposta.',
	type=hikari.Member,
)
@lightbulb.command('atividade', 'Mostra o que o usuário está fazendo.')
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def memberActivity(ctx: lightbulb.Context, member: hikari.User = lightbulb.Context.member) -> None:
	member: hikari.Member = ctx.options.member or member

	presence = member.get_presence()

	if presence is not None:
		if len(presence.activities) != 0:
			activity, status = (presence.activities[0], presence.visible_status)
			match activity.type:
				# case isinstance(activity, hikari.ActivityType.CUSTOM):
				# activity = activity
				case hikari.ActivityType.PLAYING:
					activity = f'Jogando: {activity}'
				case hikari.ActivityType.STREAMING:
					activity = f'Streamando: {activity}'
				case hikari.ActivityType.LISTENING:
					activity = f'Ouvindo: {activity.details} - {activity.name}'
		else:
			activity, status = (
				' ~ ~ Aparentemente, o usuário não está fazendo nada ~ ~ ',
				presence.visible_status,
			)
	else:
		activity, status = (
			' ~ ~ Aparentemente, o usuário não está fazendo nada ~ ~ ',
			'Offline',
		)

	message = hikari.Embed(title=f'Atividade de {member.username}')
	message.add_field('Status', f'```{status}```')
	message.add_field('Atividade', f'{activity}')
	await ctx.respond(message)


# region Server

@plugin.command()
@lightbulb.command(name='server', description='Retorna informações sobre o servidor')
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def cmdServer(ctx: lightbulb.Context) -> None:
	server = ctx.get_guild()
	message = hikari.Embed(
		title=server.name,
		description=server.description or 'No description or not a Community Guild',
	)

	await ctx.respond(message)


@cmdServer.child()
@lightbulb.command(name='icon', description='Retorna o icone do servidor.')
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def serverIcon(ctx: lightbulb.Context) -> None:
	guild = ctx.get_guild()
	icon_url = guild.icon_url

	if not icon_url:
		await ctx.respond('O servidor não possui icone.')
		return

	await ctx.respond(
		f'Aqui está a imagem de perfil de {guild.name}:\n {guild.icon_url}'
	)

# endregion


def getRolesSorted(member: hikari.Member) -> typing.Sequence[hikari.Role]:
	role_list = member.get_roles()
	roles_dict = {role.position: role for role in role_list if role.position != 0}
	roles_sorted = [roles_dict[k] for k in sorted(roles_dict)]
	return roles_sorted

# TODO Create a findActivity function

def load(bot):
	print(f'Succesfully loaded {plugin.name}!')
	bot.add_plugin(plugin)


def unload(bot):
	print(f'Succesfully unloaded {plugin.name}!')
	bot.remove_plugin(plugin)
