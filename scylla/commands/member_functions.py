import typing
import hikari

def getRolesSorted(member: hikari.Member) -> typing.Sequence[hikari.Role]:
	'''
	Return the roles the user has, ordered by their position
	# Returns
	typing.Sequence[hikari.Role]
	'''
	role_list = member.get_roles()
	roles_dict = {role.position: role for role in role_list if role.position != 0}
	roles_sorted = [roles_dict[k] for k in sorted(roles_dict, reverse=True)]
	return roles_sorted

def getActivityStatus(member: hikari.Member) -> typing.Dict[str, str]:
	'''
	Return a member activity and status
	# Returns
	typing.Dict[str, str]
	key = 'activity' or 'status'
	'''
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

			return {'activity':action, 'status':status}

		action, status = (
			' ~ ~ Aparentemente, o usuário não está fazendo nada ~ ~ ',
			presence.visible_status,
		)

		return {'activity':action, 'status':status}

	action, status = (
		' ~ ~ Aparentemente, o usuário não está fazendo nada ~ ~ ',
		'Offline',
	)

	return {'activity':action, 'status':status}


# TODO move to 'Functions' folder