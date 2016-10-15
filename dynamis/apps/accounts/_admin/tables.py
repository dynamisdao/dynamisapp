from django.contrib.auth import get_user_model

import django_tables2 as tables
from django_tables2.utils import A

from dynamis.apps.policy.models import PolicyApplication
from dynamis.utils.tables import MaterializedTable


User = get_user_model()


class UserTable(MaterializedTable):
    email = tables.LinkColumn('admin-namespace:user-detail', kwargs={'pk': A('pk')})
    email_verified = tables.TemplateColumn(
        template_name='accounts/admin/partials/user_email_column.html',
    )
    keybase_username = tables.TemplateColumn(
        template_name='accounts/admin/partials/user_keybase_username_column.html',
    )

    class Meta(MaterializedTable.Meta):
        model = User
        order_by = ('pk',)
        fields = (
            'pk',
            'email',
            'email_verified',
            'keybase_username',
            'is_active',
            'is_superuser',
            'is_staff',
            'last_login',
        )


class PolicyTable(MaterializedTable):
    id = tables.LinkColumn('admin-namespace:policy-detail', kwargs={'pk': A('id')})
    user_email = tables.LinkColumn('admin-namespace:user-detail', kwargs={'pk': A('user.pk')}, accessor='user.email',
                                   verbose_name="user's email")
    user_pk = tables.Column(verbose_name='user id', accessor='user.pk')

    class Meta(MaterializedTable.Meta):
        model = PolicyApplication
        order_by = ('id',)
        fields = (
            'id',
            # 'is_final',
            # 'is_signed',
            'state'
        )
