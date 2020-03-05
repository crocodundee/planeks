GROUPS = {
    'ADMINS': 'Администраторы',
    'EDITORS': 'Редакторы',
    'USERS': 'Пользователи',
}

DEFAULT_GROUP = 3

DEFAULT_GROUPS = [
    {'name': 'Администраторы', 'moderation': False},
    {'name': 'Редакторы', 'moderation': False},
    {'name': 'Пользователи', 'moderation': True},
]
