def for_pie_chart(data):
    order_status = {'-2': 'Chờ xác nhận hủy',
        '-1': 'Đã hủy',
        '0': 'Chờ xác nhận',
        '1': 'Đã xác nhận',
        '2': 'Đang đóng gói',
        '3': 'Đang vận chuyển',
        '4': 'Hoàn thành',
    }
    term_result = {}
    result = []
    for status in data:
        status = str(status)
        if status in term_result.keys():
            term_result[status] += 1
        else:
            term_result[status] = 1
    for status in term_result.keys():
        result.append({'value': term_result.get(status, 0), 'name': order_status[status]})
    return result

def for_line_chart(data):
    term_result = {}
    for order in data:
        if order['date'] in term_result.keys():
            if order['pay_status'] == 0:
                term_result[order['date']][0] += 1
            else:
                term_result[order['date']][1] += 1
        else:
            if order['pay_status'] == 0:
                term_result[order['date']] = [1,0]
            else:
                term_result[order['date']] = [0,1]
    result = {'date': [], '0' : [], '1': []}
    for date in term_result.keys():
        result['date'].append(date)
        result['0'].append(term_result[date][0])
        result['1'].append(term_result[date][1])
    return result

def for_bar_chart_1(data):
    term_result = {}
    for order in data:
        for detail in order['details']:
            if detail['product']['name'] in term_result.keys():
                term_result[detail['product']['name']] += detail['quantity']
            else:
                term_result[detail['product']['name']] = detail['quantity']
    print(term_result)

