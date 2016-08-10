import django_tables2 as tables


class MaterializedTable(tables.Table):
    class Meta:
        attrs = {
            'class': 'striped bordered highlight responsive-table',
        }
        empty_text = "No records"
