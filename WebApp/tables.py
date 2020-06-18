from flask_table import Table, Col, LinkCol, ButtonCol


class ArticlesTable(Table):
    classes = ['table', 'table-striped', 'table-bordered']
    author = Col('Author')
    category = Col('Category')
    date = Col('Date')
    header = Col('Header')
    opener = Col('Opener')
    #paragraphs = Col('Paragraphs')
    #comments = scrapy.Field()
    #image = LinkCol('<img src="/tmp/IKE2low.jpg" width="200" height="85">', endpoint='index')
    details = LinkCol('Details', endpoint='detail', url_kwargs=dict(id='id') ,  td_html_attrs={'class': 'btn btn-info'})
    #header = Col('header')


class CommentsTable(Table):
    classes = ['table', 'table-striped', 'table-bordered']
    name = Col("Name")
    text = Col("Text")
    date = Col("Date")
