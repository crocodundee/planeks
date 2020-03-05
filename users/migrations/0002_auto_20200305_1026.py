from django.db import migrations
from users.groups import UserGroup
from users.settings import *


def set_default_groups(apps, schema_editor):
    obj_list = [UserGroup(**group) for group in DEFAULT_GROUPS]
    UserGroup.objects.bulk_create(obj_list)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_default_groups),
    ]
