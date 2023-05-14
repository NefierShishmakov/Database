from flask import Flask, render_template, request
from database import DatabaseController
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from database_parser import SQLRequestParser as SQLParser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'postgresql://mrx_db:123@localhost:5432/theatre'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def get_correct_json(data: dict) -> dict:
    for key, value in data.items():
        if value.find("_") != -1:
            data[key] = list(map(str, value.split("_")))
            for num, el in enumerate(data[key]):
                if el.isdigit():
                    data[key][num] = int(el)
        elif value.isdigit():
            data[key] = int(value)

    return data


@app.route('/', methods=['GET'])
def my_cool_site():
    return render_template('my_cool_site.html')


@app.route('/modify_forms', methods=['GET'])
def modify_forms():
    return render_template('modify_forms/modify_forms.html')


@app.route('/modify_forms/<form_name>', methods=['GET'])
def render_form(form_name):
    return render_template('modify_forms/' + str(form_name) + '.html')


@app.route('/modify_forms/modify_tables', methods=['POST'])
def modify_tables():
    data = request.get_json()
    controller = DatabaseController()
    controller.open_connection()

    response = "Success"

    try:
        controller.process_request(data)
    except Exception as ex:
        response = ex.__str__()
        response = response[:response.find('CONTEXT')]

    controller.close_connection()

    return {
        'response': response
    }


@app.route('/search_forms', methods=['GET'])
def search_forms():
    return render_template('search_forms/search_forms.html')


@app.route('/search_forms/<form_name>', methods=['GET'])
def render_search_forms(form_name):
    return render_template('search_forms/' + str(form_name) + '.html')


@app.route('/search_forms/employees_render_result', methods=['GET'])
def employees_render_result():
    data = get_correct_json(dict(request.args))

    table = 'employee'
    result_cursor = db.session.execute(text(SQLParser.parse_employee_request(table, data, 'amount')))

    result = {
        'amount': str(result_cursor.fetchall()[0][0])
    }

    result_cursor = db.session.execute(text(SQLParser.parse_employee_request(table, data, '')))
    keys = list(result_cursor.keys())
    values = result_cursor.fetchall()
    result['columns'] = keys
    result['values'] = values

    return render_template('search_forms/result_tables.html', articles=result)


@app.route('/search_forms/repertoire_plays_render_result', methods=['GET'])
def repertoire_plays_render_result():
    data = get_correct_json(dict(request.args))

    table = 'repertoire'

    result_cursor = db.session.execute(text(SQLParser.parse_repertoire_plays_request(table, data, 'amount')))

    result = {
        'amount': str(result_cursor.fetchall()[0][0])
    }

    result_cursor = db.session.execute(text(SQLParser.parse_repertoire_plays_request(table, data, '')))
    keys = list(result_cursor.keys())
    values = result_cursor.fetchall()
    result['columns'] = keys
    result['values'] = values

    return render_template('search_forms/result_tables.html', articles=result)


@app.route('/search_forms/authors_render_result', methods=['GET'])
def authors_render_result():
    data = get_correct_json(dict(request.args))

    table = 'author'

    result = {
        'amount': ''
    }

    result_cursor = db.session.execute(text(SQLParser.parse_authors_request(table, data)))
    keys = list(result_cursor.keys())
    values = result_cursor.fetchall()
    result['columns'] = keys
    result['values'] = values

    return render_template('search_forms/result_tables.html', articles=result)


@app.route('/search_forms/plays_render_result', methods=['GET'])
def plays_render_result():
    data = get_correct_json(dict(request.args))

    table = 'play'

    result = {
        'amount': ''
    }

    result_cursor = db.session.execute(text(SQLParser.parse_plays_request(table, data)))
    keys = list(result_cursor.keys())
    values = result_cursor.fetchall()
    result['columns'] = keys
    result['values'] = values

    return render_template('search_forms/result_tables.html', articles=result)


@app.route('/search_forms/actors_for_role_render_result', methods=['GET'])
def actors_for_role_render_result():
    data = get_correct_json(dict(request.args))
    table = 'role'

    result = {
        'amount': ''
    }

    result_cursor = db.session.execute(text(SQLParser.parse_actors_for_role_request(table, data)))

    keys = list(result_cursor.keys())
    values = result_cursor.fetchall()
    result['columns'] = keys
    result['values'] = values

    return render_template('search_forms/result_tables.html', articles=result)


@app.route('/search_forms/actors_render_result', methods=['GET'])
def actors_render_result():
    data = get_correct_json(dict(request.args))
    table = 'contest'

    result_cursor = db.session.execute(text(SQLParser.parse_actors_request(table, data, 'amount')))

    result = {
        'amount': str(result_cursor.fetchall()[0][0])
    }

    result_cursor = db.session.execute(text(SQLParser.parse_actors_request(table, data, '')))
    keys = list(result_cursor.keys())
    values = result_cursor.fetchall()
    result['columns'] = keys
    result['values'] = values

    return render_template('search_forms/result_tables.html', articles=result)


@app.route('/search_forms/roles_for_actor_render_result', methods=['GET'])
def roles_for_actor_render_result():
    data = get_correct_json(dict(request.args))
    table = 'actor_for_role'

    result_cursor = db.session.execute(text(SQLParser.parse_roles_for_actor_request(table, data, 'amount')))

    result = {
        'amount': str(result_cursor.fetchall()[0][0])
    }

    result_cursor = db.session.execute(text(SQLParser.parse_roles_for_actor_request(table, data, '')))
    keys = list(result_cursor.keys())
    values = result_cursor.fetchall()
    result['columns'] = keys
    result['values'] = values

    return render_template('search_forms/result_tables.html', articles=result)


@app.route('/search_forms/sold_tickets_render_result', methods=['GET'])
def sold_tickets_render_result():
    data = get_correct_json(dict(request.args))

    table = 'ticket'

    result = {
        'amount': ''
    }

    result_cursor = db.session.execute(text(SQLParser.parse_sold_tickets_request(table, data)))
    keys = list(result_cursor.keys())
    values = result_cursor.fetchall()
    result['columns'] = keys
    result['values'] = values

    return render_template('search_forms/result_tables.html', articles=result)


@app.route('/search_forms/performance_revenue_render_result', methods=['GET'])
def performance_revenue_render_result():
    data = get_correct_json(dict(request.args))
    table = 'ticket'

    result = {
        'amount': ''
    }

    result_cursor = db.session.execute(text(SQLParser.parse_performance_revenue_result(table, data)))
    keys = list(result_cursor.keys())
    values = result_cursor.fetchall()
    result['columns'] = keys
    result['values'] = values

    return render_template('search_forms/result_tables.html', articles=result)


@app.route('/search_forms/performances_vacant_seats_render_result', methods=['GET'])
def performances_vacant_seats_render_result():
    data = get_correct_json(dict(request.args))

    table = 'ticket'

    result = {
        'amount': ''
    }

    result_cursor = db.session.execute(text(SQLParser.parse_performances_vacant_seats(table, data)))
    keys = list(result_cursor.keys())
    values = result_cursor.fetchall()
    result['columns'] = keys
    result['values'] = values

    return render_template('search_forms/result_tables.html', articles=result)


@app.route('/search_forms/performances_vacant_seats_count_render_result', methods=['GET'])
def performances_vacant_seats_count_render_result():
    data = get_correct_json(dict(request.args))

    table = 'ticket'

    result = {
        'amount': ''
    }

    result_cursor = db.session.execute(text(SQLParser.parse_performances_vacant_seats_count(table, data)))
    keys = list(result_cursor.keys())
    values = result_cursor.fetchall()
    result['columns'] = keys
    result['values'] = values

    return render_template('search_forms/result_tables.html', articles=result)


def get_dict(keys, values) -> dict:
    return {'columns': keys, 'values': values}


@app.route('/search_forms/repertoires_play_render_result', methods=['GET'])
def repertoires_play_render_result():
    data = get_correct_json(dict(request.args))
    table = 'repertoire'

    result = {}

    result_cursor = db.session.execute(text(SQLParser.parse_repertoires_play_producer_request(table, data, 'director')))
    result['director'] = get_dict(list(result_cursor.keys()), result_cursor.fetchall())
    result_cursor = db.session.execute(text(SQLParser.parse_repertoires_play_producer_request(table, data, 'artist')))
    result['artist'] = get_dict(list(result_cursor.keys()), result_cursor.fetchall())
    result_cursor = db.session.execute(text(SQLParser.parse_repertoires_play_producer_request(table, data, 'conductor')))
    result['conductor'] = get_dict(list(result_cursor.keys()), result_cursor.fetchall())

    result_cursor = db.session.execute(text(SQLParser.parse_repertoires_play_author_request(table, data)))
    result['author'] = get_dict(list(result_cursor.keys()), result_cursor.fetchall())

    result_cursor = db.session.execute(text(SQLParser.parse_repertoires_play_actors_request(table, data)))
    result['actors'] = get_dict(list(result_cursor.keys()), result_cursor.fetchall())

    return render_template('search_forms/result_tables_actor.html', articles=result)


if __name__ == "__main__":
    app.run(debug=True)
