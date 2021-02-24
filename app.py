from flask import Flask, url_for, redirect, request, session, render_template

app = Flask(__name__)

events = [{'date': '24 февраля', 'subject': 'Физика', 'type': 'самостоятельная', 'prepare': 'параграфы 15-17wqdqwqewdqwdqwdqwdqwdqwdqwdqwdqwdqwddqwdqwd'},
          {'date': '24 февраля', 'subject': 'Алгебра', 'type': 'контрольная', 'prepare': 'параграфы 15-17wqdqwdwqd'},
          {'date': '24 февраля', 'subject': 'Алгебра', 'type': 'контрольная', 'prepare': 'параграфы 15-1dqwdqwdqwdqwd7'},
          {'date': '24 февраля', 'subject': 'Алгебра', 'type': 'контрольная', 'prepare': 'параграфы 15-1qwdqwdqwdqwd 7'}]
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', events=events, username='Тестовый пользователь')

if __name__ == "__main__":
    app.run(port=8080, host='localhost', debug=True)