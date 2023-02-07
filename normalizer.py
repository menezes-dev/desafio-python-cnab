import unicodedata


def type(value):
    match value:
        case '1': return 'Debito'
        case '2': return 'Boleto'
        case '3': return 'Financiamento'
        case '4': return 'Credito'
        case '5': return 'Recebimento Emprestimo'
        case '6': return 'Vendas'
        case '7': return 'Recebimento TED'
        case '8': return 'Recebimento DOC'
        case '9': return 'Aluguel'


def value(value, type):
    real_value = float(value[0:10]/100.00)
    options = ['2', '3', '9']

    if type in options:
        return real_value*-1
    return real_value


def date(data):
    return f'{data[6:8]}/{data[4:6]}/{data[0:4]}'


def time(time):
    return f'{time[0:2]}:{time[2:4]}:{time[4:6]}'


def string(string):
    return unicodedata.normalize('NFD', string.strip()).encode('ascii', 'ignore').decode('utf-8')
