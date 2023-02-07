import os
from flask import Flask, render_template, request
import normalizer
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/file', methods=['POST'])
def data():
    file = request.files.get('uploadedFile')
    name_file = file.filename
    file.save(os.path.join('./', name_file))
    open_file = open(name_file)

    data_file = []

    for line in open_file:
        data_file.append(
            (
                normalizer.type(line[0:1]),
                normalizer.date(line[1:9]),
                normalizer.value(line[9:19], line[0:1]),
                line[19:30],
                line[30:42],
                normalizer.time(line[42:48]),
                normalizer.string(line[48:62]),
                normalizer.string(line[62:82])
            )
        )

    open_file.close()

    connection = sqlite3.connect('cnab.sqlite')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE cnab (type text, data text, value real, cpf text, card text, time text, owner text, store text)')
    cursor.executemany('INSERT INTO cnab(type, data, value, cpf, card, time, owner, store) VALUES(?,?,?,?,?,?,?,?)', data_file)
    connection.commit()

    stores = []
    cursor.execute('SELECT DISTINCT store FROM cnab')
    for line in cursor.fetchall():
        stores.append(line[0])

    stores_transactions = []
    stores_balances = []

    for store in stores:
        transactions = cursor.execute('SELECT * FROM cnab WHERE store = ?', (store, ))
        stores_transactions.append(transactions.fetchall())
        balance = cursor.execute('SELECT SUM(value) FROM cnab WHERE store = ?', (store, ))
        formatted_balance = balance.fetchall()[0][0]
        stores_balances.append(f'{formatted_balance:10.2f}')

    stores_amount = len(stores)

    connection.close()

    return render_template('tables.html', stores=stores_transactions, balances=stores_balances, amount=stores_amount)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
