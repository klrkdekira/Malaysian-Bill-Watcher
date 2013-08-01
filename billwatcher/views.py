from pyramid.view import view_config
from webhelpers import paginate

def views_include(config):
    config.add_route('bill.list', '/')
    config.add_route('bill.detail', '/detail/{rev_id}')

@view_config(route_name='bill.list', renderer='bill/list.html')
def bill_list(request):
    page = request.params.get('page', '1')

    records = request.db.bills.find().sort([['id', -1]])
    bills = []

    import pprint
    for bill in records:
        pprint.pprint(bill)
        # year = bill['id'].split('_')[-1]
        bills.extend(bill['item'])

    data = paginate.Page(bills, page,
                         items_per_page=20)

    # Quick hack for pager
    start = data.page - 2
    end = data.page + 3
    if start <= 0:
        start = 1
        end = 6
    if end >= data.page_count:
        end = data.page_count + 1
        start = end - 5

    return {'data': data,
            'start': start,
            'end': end}

@view_config(route_name='bill.detail', renderer='bill/detail.html')
def bill_detail(request):
    rev_id = request.matchdict['rev_id']
    bill = request.db.bills.find_one({'item.id': rev_id})
    import pprint
    pprint.pprint(bill)
    return {}