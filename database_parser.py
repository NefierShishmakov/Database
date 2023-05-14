class SQLRequestParser:
    @staticmethod
    def parse_insert_request(table_name: str, data: dict) -> str:
        request = "INSERT INTO " + table_name + "("
        for key in data.keys():
            request += "{}, ".format(str(key))

        request = request[:-2]  # delete last comma and space
        request += ") VALUES("

        for value in data.values():
            if isinstance(value, str):
                request += "'{}', ".format(value)
            elif isinstance(value, int):
                request += "{}, ".format(value)

        request = request[:-2]  # delete last comma and space
        request += ")"

        return request

    @staticmethod
    def parse_update_request(table_name: str, data: dict) -> str:
        first_element = list(data.items())[0]
        condition_key = first_element[0]
        condition_value = first_element[1]

        del data[condition_key]

        request = "UPDATE " + table_name + " SET "

        for key, value in data.items():
            if isinstance(value, str):
                request += "{} = '{}', ".format(key, value)
            elif isinstance(value, int):
                request += "{} = {}, ".format(key, value)

        request = request[:-2]  # delete last comma and space

        if isinstance(condition_value, str):
            request += " WHERE {} = '{}'".format(condition_key, condition_value)
        elif isinstance(condition_value, int):
            request += " WHERE {} = {}".format(condition_key, condition_value)

        return request

    @staticmethod
    def parse_delete_request(table_name: str, data: dict) -> str:
        request = "DELETE FROM " + table_name + " WHERE "

        for key, value in data.items():
            if isinstance(value, str):
                request += "{} = '{}' ".format(key, value)
            elif isinstance(value, int):
                request += "{} = {} ".format(key, value)
            request += "AND "

        request = request[:request.rfind('AND')]  # delete AND statement
        request = request[:-1]  # delete last space

        return request

    @staticmethod
    def parse_employee_request(table_name: str, data: dict, condition: str) -> str:
        request = "SELECT "

        if condition == 'amount':
            request += " count(id) amount"
        else:
            request += " surname, name, third_name"
        request += " FROM " + table_name

        if data:
            keys = {
                'kids': "kids",
                'work_experience': "work_experience",
                'salary': "salary",
                'age': "extract(YEAR FROM age(birth_date))",
                'birth_year': "date_part('year', birth_date)",
            }

            request += " WHERE "

            for key, value in data.items():
                if isinstance(value, list):
                    key_phrase = keys[key]
                    if isinstance(value[0], str):
                        request += ("(" + key_phrase + " >= " + "'{}'".format(value[0]) + " AND " + key_phrase +
                                    " <= " + "'{}'".format(value[1]) + ")")
                    elif isinstance(value[0], int):
                        request += ("(" + key_phrase + " >= " + "{}".format(value[0]) + " AND " + key_phrase +
                                    " <= " + "{}".format(value[1]) + ")")
                elif isinstance(value, str):
                    request += ("(" + "{} = '{}'".format(key, value) + ")")
                elif isinstance(value, int):
                    request += ("(" + "{} = {}".format(key, value) + ")")
                request += " AND "
            request = request[:request.rfind('AND')]  # delete AND statement
            request = request[:-1]

        return request

    @staticmethod
    def parse_repertoire_plays_request(table_name: str, data: dict, condition: str) -> str:
        request = "SELECT "

        if condition == 'amount':
            request += "count(r.id) amount"
        else:
            request += "r.play_name, r.start_date, r.start_time"
        request += " FROM " + table_name + " r INNER JOIN play p on r.play_name = p.name "
        request += "WHERE "

        keys = {
            'start_date': "r.start_date",
        }

        for key, value in data.items():
            if isinstance(value, list):
                key_phrase = keys[key]
                if isinstance(value[0], str):
                    request += ("(" + key_phrase + " >= " + "'{}'".format(value[0]) + " AND " + key_phrase +
                                " <= " + "'{}'".format(value[1]) + ")")
                elif isinstance(value[0], int):
                    request += ("(" + key_phrase + " >= " + "{}".format(value[0]) + " AND " + key_phrase +
                                " <= " + "{}".format(value[1]) + ")")
            elif value == 'true':
                if key == 'is_played':
                    request += ("(" + "r.is_premiere = true" + " AND " + "r.start_date < now()::date)")
                elif key == 'is_current_season':
                    request += ("(" + "date_part('year', r.start_date) = 2023" + ")")
            else:
                request += "p.{} = '{}'".format(key, value)
            request += " AND "

        request = request[:request.rfind('AND')]  # delete AND statement
        request = request[:-1]

        return request

    @staticmethod
    def parse_authors_request(table_name: str, data: dict) -> str:
        request = "SELECT DISTINCT a.surname, a.name, a.third_name"
        request += " FROM " + table_name + " a "
        request += "INNER JOIN play p on a.id = p.author_id "
        request += "INNER JOIN repertoire r on p.name = r.play_name"

        if data:
            keys = {
                'start_date': "r.start_date",
                'century': "a.century",
                'country': "a.country",
                'genre': "p.genre"
            }

            request += " WHERE "

            for key, value in data.items():
                key_phrase = ''
                if key != 'is_played':
                    key_phrase = keys[key]
                if isinstance(value, list):
                    if isinstance(value[0], str):
                        request += ("(" + key_phrase + " >= " + "'{}'".format(value[0]) + " AND " + key_phrase +
                                    " <= " + "'{}'".format(value[1]) + ")")
                    elif isinstance(value[0], int):
                        request += ("(" + key_phrase + " >= " + "{}".format(value[0]) + " AND " + key_phrase +
                                    " <= " + "{}".format(value[1]) + ")")
                elif value == 'true':
                    request += ("(" + "r.is_premiere = true AND r.start_date < now()::date" + ")")
                elif isinstance(value, str):
                    request += "{} = '{}'".format(key_phrase, value)
                elif isinstance(value, int):
                    request += "{} = {}".format(key_phrase, value)
                request += " AND "
            request = request[:request.rfind('AND')]  # delete AND statement
            request = request[:-1]

        return request

    @staticmethod
    def parse_plays_request(table_name: str, data: dict) -> str:
        request = "SELECT DISTINCT p.name"

        if 'start_date' in data:
            request += ", r.start_date, r.start_time"
        request += " FROM " + table_name + " p INNER JOIN author a on p.author_id = a.id "
        if 'start_date' in data:
            request += "INNER JOIN repertoire r on p.name = r.play_name "

        request += "WHERE "

        keys = {
            'start_date': "r.start_date",
            'id': "a.id",
            'genre': "p.genre",
            'country': "a.country",
            'century': "a.century"
        }

        for key, value in data.items():
            key_phrase = keys[key]
            if isinstance(value, list):
                request += "((r.is_premiere = true AND r.start_date < now()::date) AND "
                request += ("(" + key_phrase + " >= " + "'{}'".format(value[0]) + " AND " + key_phrase +
                            " <= " + "'{}'".format(value[1]) + "))")
            elif isinstance(value, str):
                request += ("(" + "{} = '{}'".format(key_phrase, value) + ")")
            elif isinstance(value, int):
                request += ("(" + "{} = {}".format(key_phrase, value) + ")")
            request += " AND "
        request = request[:request.rfind('AND')]  # delete AND statement
        request = request[:-1]

        return request

    @staticmethod
    def parse_actors_for_role_request(table_name: str, data: dict) -> str:
        role_request = "(SELECT r.min_weight r_minw, r.max_weight r_maxw, r.min_height r_minh, r.max_height r_maxh, " \
                       "r.min_age r_mina, r.max_age r_maxa, r.sex r_s, r.voice r_v FROM " + table_name + " r"
        role_request += " WHERE "

        for key, value in data.items():
            role_request += "r.{} = '{}'".format(key, value)
        role_request += ") as r2"

        employee_request = "(SELECT e.surname e_surname, e.name e_name, e.third_name e_third_name, " \
                           "e.sex e_sex, e.birth_date e_birth, a.voice a_voice, a.height a_height, a.weight a_weight " \
                           "FROM employee e INNER JOIN actor a on e.id = a.id) as ea"

        request = "SELECT e_surname, e_name, e_third_name FROM "
        request += employee_request
        request += " INNER JOIN "
        request += role_request
        request += " ON (ea.e_sex = r2.r_s AND ea.a_voice = r2.r_v " \
                   "AND (extract(YEAR FROM age(ea.e_birth)) >= r2.r_mina AND extract(YEAR FROM age(ea.e_birth)) <= r2.r_maxa) " \
                   "AND (ea.a_height >= r2.r_minh AND ea.a_height <= r2.r_maxh) " \
                   "AND (ea.a_weight >= r2.r_minw AND ea.a_weight <= r2.r_maxw))"

        return request

    @staticmethod
    def parse_actors_request(table_name: str, data: dict, condition: str) -> str:
        request = "SELECT "

        if condition == 'amount':
            request += "count(DISTINCT e.id)"
        else:
            request += "DISTINCT e.surname, e.name, e.third_name"
        request += " FROM " + table_name + " c INNER JOIN employee e ON c.actor_id = e.id "
        request += "WHERE c.contest_rank != 'Участник' AND "

        keys = {
            'sex': "e.sex",
            'age': "extract(YEAR FROM age(e.birth_date))",
            'award_date': "c.award_date",
            'name': "c.name",
        }

        for key, value in data.items():
            key_phrase = keys[key]
            if isinstance(value, list):
                if key_phrase == "c.name":
                    request += "(" + key_phrase + " IN ("
                    for el in value:
                        request += "'{}', ".format(el)
                    request = request[:-2]
                    request += "))"
                elif isinstance(value[0], str):
                    request += ("(" + key_phrase + " >= " + "'{}'".format(value[0]) + " AND " + key_phrase +
                                " <= " + "'{}'".format(value[1]) + ")")
                elif isinstance(value[0], int):
                    request += ("(" + key_phrase + " >= " + "{}".format(value[0]) + " AND " + key_phrase +
                                " <= " + "{}".format(value[1]) + ")")
            elif isinstance(value, str):
                request += "{} = '{}'".format(key_phrase, value)
            elif isinstance(value, int):
                request += "{} = {}".format(key_phrase, value)
            request += " AND "
        request = request[:request.rfind('AND')]  # delete AND statement
        request = request[:-1]

        return request

    @staticmethod
    def parse_roles_for_actor_request(table_name: str, data: dict, condition: str) -> str:
        request = "SELECT "

        if condition == 'amount':
            request += "count(DISTINCT afr.role_name)"
        else:
            request += "DISTINCT afr.role_name"
        request += " FROM " + table_name + " afr"
        request += " INNER JOIN repertoire r on afr.repertoire_play_id = r.id"
        request += " INNER JOIN play p on r.play_name = p.name"
        request += " WHERE "

        keys = {
            'actor_id': "afr.actor_id",
            'start_date': "r.start_date",
            'genre': "p.genre",
            'director_producer_id': "r.director_producer_id",
            'age_genre': "p.age_genre"
        }

        for key, value in data.items():
            key_phrase = keys[key]
            if isinstance(value, list):
                if isinstance(value[0], str):
                    request += ("(" + key_phrase + " >= " + "'{}'".format(value[0]) + " AND " + key_phrase +
                                " <= " + "'{}'".format(value[1]) + ")")
                elif isinstance(value[0], int):
                    request += ("(" + key_phrase + " >= " + "{}".format(value[0]) + " AND " + key_phrase +
                                " <= " + "{}".format(value[1]) + ")")
            elif isinstance(value, str):
                request += ("(" + "{} = '{}'".format(key_phrase, value) + ")")
            elif isinstance(value, int):
                request += ("(" + "{} = {}".format(key_phrase, value) + ")")
            request += " AND "
        request = request[:request.rfind('AND')]  # delete AND statement
        request = request[:-1]

        return request

    @staticmethod
    def parse_sold_tickets_request(table_name: str, data: dict) -> str:
        request = "SELECT "

        if ('is_premiere' in data) or ('start_date' in data):
            request += "count(*) sold_tickets "
        else:
            request += "r.play_name, r.start_date, r.start_time, count(t.repertoire_play_id) sold_tickets "

        request += "FROM " + table_name + " t "
        request += "INNER JOIN repertoire r on t.repertoire_play_id = r.id "
        request += "WHERE t.is_sold = true AND "

        keys = {
            'repertoire_play_id': "t.repertoire_play_id",
            'is_premiere': "r.is_premiere",
            'start_date': "r.start_date",
        }

        for key, value in data.items():
            key_phrase = keys[key]
            if isinstance(value, list):
                if isinstance(value[0], str):
                    request += ("(" + key_phrase + " >= " + "'{}'".format(value[0]) + " AND " + key_phrase +
                                " <= " + "'{}'".format(value[1]) + ")")
                elif isinstance(value[0], int):
                    request += ("(" + key_phrase + " >= " + "{}".format(value[0]) + " AND " + key_phrase +
                                " <= " + "{}".format(value[1]) + ")")
            elif isinstance(value, int) or value == 'true':
                request += ("(" + "{} = {}".format(key_phrase, value) + ")")
            elif isinstance(value, str):
                request += ("(" + "{} = '{}'".format(key_phrase, value) + ")")
            request += " AND "
        request = request[:request.rfind('AND')]  # delete AND statement
        request = request[:-1]

        if ('is_premiere' not in data) and ('start_date' not in data):
            request += " GROUP BY (r.play_name, r.start_date, r.start_time)"

        return request

    @staticmethod
    def parse_performance_revenue_result(table_name: str, data: dict) -> str:
        request = "SELECT sum(t.price) cash "
        request += "FROM " + table_name + " t "
        request += "INNER JOIN repertoire r ON t.repertoire_play_id = r.id "
        request += "WHERE "

        keys = {
            'repertoire_play_id': "t.repertoire_play_id",
            'start_date': "r.start_date",
        }

        for key, value in data.items():
            key_phrase = keys[key]
            if isinstance(value, list):
                if isinstance(value[0], str):
                    request += ("(" + key_phrase + " >= " + "'{}'".format(value[0]) + " AND " + key_phrase +
                                " <= " + "'{}'".format(value[1]) + ")")
                elif isinstance(value[0], int):
                    request += ("(" + key_phrase + " >= " + "{}".format(value[0]) + " AND " + key_phrase +
                                " <= " + "{}".format(value[1]) + ")")
            elif isinstance(value, int):
                request += ("(" + "{} = {}".format(key_phrase, value) + ")")
            elif isinstance(value, str):
                request += ("(" + "{} = '{}'".format(key_phrase, value) + ")")
            request += " AND "
        request = request[:request.rfind('AND')]  # delete AND statement
        request = request[:-1]

        return request

    @staticmethod
    def parse_performances_vacant_seats(table_name: str, data: dict) -> str:
        request = "SELECT t.place, t.row, r.play_name, r.start_date, r.start_time "
        request += "FROM " + table_name + " t "
        request += "INNER JOIN repertoire r on r.id = t.repertoire_play_id "
        request += "WHERE t.is_sold = false AND "

        keys = {
            'repertoire_play_id': "t.repertoire_play_id",
            'is_premiere': "r.is_premiere",
        }

        for key, value in data.items():
            key_phrase = keys[key]
            if isinstance(value, list):
                if isinstance(value[0], str):
                    request += ("(" + key_phrase + " >= " + "'{}'".format(value[0]) + " AND " + key_phrase +
                                " <= " + "'{}'".format(value[1]) + ")")
                elif isinstance(value[0], int):
                    request += ("(" + key_phrase + " >= " + "{}".format(value[0]) + " AND " + key_phrase +
                                " <= " + "{}".format(value[1]) + ")")
            elif isinstance(value, int) or value == 'true':
                request += ("(" + "{} = {}".format(key_phrase, value) + ")")
            elif isinstance(value, str):
                request += ("(" + "{} = '{}'".format(key_phrase, value) + ")")
            request += " AND "
        request = request[:request.rfind('AND')]  # delete AND statement
        request = request[:-1]

        request += " ORDER BY (r.play_name, r.start_date, r.start_time)"

        return request

    @staticmethod
    def parse_performances_vacant_seats_count(table_name: str, data: dict) -> str:
        count_request = "(SELECT t.repertoire_play_id, count(t.repertoire_play_id) free_places "
        count_request += "FROM " + table_name + " t "
        count_request += "INNER JOIN repertoire r on r.id = t.repertoire_play_id "
        count_request += "WHERE t.is_sold = false AND "

        keys = {
            'repertoire_play_id': "t.repertoire_play_id",
            'is_premiere': "r.is_premiere",
        }

        for key, value in data.items():
            key_phrase = keys[key]
            if isinstance(value, list):
                if isinstance(value[0], str):
                    count_request += ("(" + key_phrase + " >= " + "'{}'".format(value[0]) + " AND " + key_phrase +
                                " <= " + "'{}'".format(value[1]) + ")")
                elif isinstance(value[0], int):
                    count_request += ("(" + key_phrase + " >= " + "{}".format(value[0]) + " AND " + key_phrase +
                                " <= " + "{}".format(value[1]) + ")")
            elif isinstance(value, int) or value == 'true':
                count_request += ("(" + "{} = {}".format(key_phrase, value) + ")")
            elif isinstance(value, str):
                count_request += ("(" + "{} = '{}'".format(key_phrase, value) + ")")
            count_request += " AND "
        count_request = count_request[:count_request.rfind('AND')]  # delete AND statement
        count_request = count_request[:-1]

        count_request += " GROUP BY t.repertoire_play_id) as ea"

        request = "SELECT rep.play_name, rep.start_date, rep.start_time, free_places FROM repertoire rep "
        request += "INNER JOIN " + count_request
        request += " ON rep.id = ea.repertoire_play_id"

        return request

    @staticmethod
    def parse_repertoires_play_producer_request(table_name: str, data: dict, job_title: str) -> str:
        request = "SELECT e.name " + job_title + "_name "
        request += "FROM " + table_name + " r "
        request += "INNER JOIN employee e ON e.id = r.{}_producer_id ".format(job_title)

        for key, value in data.items():
            request += "WHERE r.{} = {}".format(key, value)

        return request

    @staticmethod
    def parse_repertoires_play_author_request(table_name: str, data: dict) -> str:
        request = "SELECT a.surname, a.name, a.third_name "
        request += "FROM " + table_name + " r "
        request += "INNER JOIN play p on r.play_name = p.name "
        request += "INNER JOIN author a on p.author_id = a.id "

        for key, value in data.items():
            request += "WHERE r.{} = {}".format(key, value)

        return request

    @staticmethod
    def parse_repertoires_play_actors_request(table_name: str, data: dict) -> str:
        first_part = "(SELECT afr.actor_id, e.surname, e.name, e.third_name, afr.role_name, afr.repertoire_play_id, " \
                     "r.is_main FROM " + table_name + " r2 INNER JOIN actor_for_role afr on r2.id = afr.repertoire_play_id " \
                     "INNER JOIN role r on afr.role_name = r.role_name " \
                     "INNER JOIN employee e ON e.id = afr.actor_id " \

        for key, value in data.items():
            first_part += "WHERE r2.{} = {}) as r2are ".format(key, value)

        second_part = "(SELECT r2are.actor_id, r2are.surname actor_surname, r2are.name actor_name, " \
                      "r2are.third_name actor_third_name, dub.actor_id dub_actor_id FROM "

        third_part = second_part + first_part
        third_part += "LEFT JOIN actor_for_role dub ON " \
                      "(dub.actor_id != r2are.actor_id AND dub.role_name = r2are.role_name " \
                      "AND dub.repertoire_play_id = r2are.repertoire_play_id AND dub.understudy = true)) as r2ad "

        request = "SELECT r2ad.actor_surname, r2ad.actor_name, r2ad.actor_third_name, e.surname dub_surname, " \
                  "e.name dub_name, e.third_name dub_third_name FROM " + third_part
        request += "LEFT JOIN employee e ON r2ad.dub_actor_id = e.id"

        return request

