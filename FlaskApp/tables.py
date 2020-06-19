from flask_table import Table, Col, LinkCol


class ArticlesTable(Table):
    classes = ['table', 'table-striped', 'table-bordered']
    author = Col('Author')
    category = Col('Category')
    date = Col('Date')
    header = Col('Header')
    opener = Col('Opener')
    details = LinkCol('Details', endpoint='detail', url_kwargs=dict(id='id') ,  td_html_attrs={'class': 'btn btn-info'})


class CommentsTable(Table):
    classes = ['table', 'table-striped', 'table-bordered']
    name = Col("Name")
    text = Col("Text")
    date = Col("Date")
