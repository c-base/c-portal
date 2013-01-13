from django.contrib.auth.models import User, Group

def protect_ldap_group(group):
    if group.name in [g.name for g in Group.objects.all()]:
        for member in group.members.all():
            user = User.objects.get(username=member.nickname)
            if not group.name in [g.name for g in user.groups.all()]:
                group.members.remove(member)
                group.save()
