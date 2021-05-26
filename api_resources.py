from async_parser import AsyncParserController
from data.db_session import create_session
from flask import abort, jsonify
from data.models import *
from flask_restful import Resource, reqparse
from utils import sort_parameters
from datetime import datetime, timedelta

def get_user_by_api_key(key) -> User:
    session = create_session()
    user = session.query(User).filter(User.key == key).all()
    if not user:
        return False
    return user[0]


history_parser = reqparse.RequestParser()
history_parser.add_argument(
    'key', required=True, type=str, help='Для доступа к API необходим ключ')

tedner_parser = reqparse.RequestParser()
tedner_parser.add_argument(
    'key', required=True, type=str, help='Для доступа к API необходим ключ')


class HistoryResource(Resource):
    def get(self, history_id: int):
        session = create_session()
        args = history_parser.parse_args()
        user = get_user_by_api_key(args['key'])
        if not user:
            return abort(401, 'Пользователя с таким ключом не существует')

        history: History = session.query(History).get(history_id)
        if not history:
            return abort(404, 'Запроса с таким id не существует')
        session.add(history)

        if history.user_id != user.id or user.role != 'admin':
            return abort(403, f'Этот запрос произведен не вами, ваш id: {user.id}')
        return jsonify({
            'history': history.to_dict(only=('id', 'state', 'tenders_count', 'tag', 'min_price', 'max_price', 'date_from', 'date_to', 'sort_filter', 'sort_direction', 'date')),
            'tenders': [tender.to_dict(only=('id', 'type', 'tender_date', 'tender_price', 'tender_date', 'tender_object', 'customer', 'tender_link')) for tender in history.tenders]
        })

    def delete(self, history_id: int):
        session = create_session()
        args = history_parser.parse_args()
        user = get_user_by_api_key(args['key'])
        if not user:
            return abort(401, 'Пользователя с таким ключом не существует')

        history = session.query(History).get(history_id)

        if not history:
            return abort(404, 'Запроса с таким id не существует')

        if history.user_id != user.id or user.role != 'admin':
            return abort(403, 'Этот запрос произведен не вами')

        session.delete(history)
        session.commit()
        return jsonify({'success': 'OK'})


class TenderResource(Resource):
    def get(self, tender_id: int):
        session = create_session()
        args = tedner_parser.parse_args()
        user = get_user_by_api_key(args['key'])
        if not user:
            return abort(401, 'Пользователя с таким ключом не существует')

        tender = session.query(Data).get(tender_id)
        if not tender:
            return abort(404, 'Тендера с таким id не существует')

        return jsonify({'tender': tender.to_dict(only=('id', 'type', 'tender_date', 'tender_price', 'tender_date', 'tender_object', 'customer', 'tender_link')),
                        'winner': tender.winner[0].to_dict(only=('name', 'position', 'price')),
                        'objects': [tender_object.to_dict(only=('position', 'name', 'unit', 'quantity', 'unit_price', 'price')) for tender_object in tender.objects]})

history_list_parser = reqparse.RequestParser()
history_list_parser.add_argument('key', required=True, type=str)

history_add_parser = reqparse.RequestParser()
history_add_parser.add_argument('key', required=True, help='Вам необходим ключ API для создания заявки')
history_add_parser.add_argument('tag', type=str)
history_add_parser.add_argument('min-price', type=int)
history_add_parser.add_argument('max-price', type=int)
history_add_parser.add_argument('date-from', type=str)
history_add_parser.add_argument('date-to', type=str)
history_add_parser.add_argument('search-filter', type=str, required=True, help='Необходимо указать ключ сортировки')
history_add_parser.add_argument('sort-direction', type=str, required=True, help='Необходимо указать направление сортировки')


class HistoryListResource(Resource):
    def get(self):
        args = history_list_parser.parse_args()
        key = args['key']
        user = get_user_by_api_key(key)
        if not user:
            return abort(401, 'Пользователя с таким ключом не существует')
        
        histories = user.history

        return jsonify(
            {
                'count': len(histories),
                'queries': [history.to_dict(only=('id', 'state', 'tenders_count', 
                'tag', 'min_price', 'max_price', 'date_from', 'date_to', 'sort_filter', 
                'sort_direction', 'date')) for history in histories]
            }
        )
    
    def post(self):
        parser = AsyncParserController(3, 3)
        parameters = {}
        args: dict = history_add_parser.parse_args()
        key = args['key']
        user = get_user_by_api_key(key)
        if not user:
            return abort(401, 'Пользователя с таким ключом не существует')
        
        if 'tag' in args:
            parameters['searchString'] = args['tag']
        
        min_price = args.get('min-price')
        max_price = args.get('max-price')

        if min_price and max_price and min_price > max_price:
            return jsonify({'error': 'минимальная цена не может быть больше максимальной'})
        
        if min_price:
            parameters['priceFromGeneral'] = str(min_price)
        if max_price:
            parameters['priceToGeneral'] = str(max_price)

        date_from = args.get('date-from')
        date_to = args.get('date-to')

        if date_from:
            try:
                datetime_from = datetime.strptime(date_from, '%d.%m.%Y')
                if datetime_from > datetime.now():
                    return jsonify({'error': 'дата начала парсинга не может быть позже текущей даты'})
            except:
                return jsonify({'error': 'неверный формат даты'})

        if date_to:
            try:
                datetime_from = datetime.strptime(date_from, '%d.%m.%Y')
                if datetime_from > datetime.now():
                    return jsonify({'error': 'дата конца парсинга не может быть позже текущей даты'})
            except:
                return jsonify({'error': 'неверный формат даты'})
        
        if not date_from and not date_to:
            datetime_to = datetime.now()
            date_to = datetime_to.strftime('%d.%m.%Y')
        
        if date_to and date_from:
            if datetime_from > datetime_to:
                return jsonify({'error': 'дата начала не может быть позже даты конца'})
            if datetime_to - datetime_from > timedelta(365):
                return jsonify({'error': 'разница в датах может быть не более года'})
        
        if date_from and not date_to:
            if datetime.now() - datetime_from < timedelta(365):
                parameters['publishDateTo'] = datetime.now().strftime('%d.%m.%Y')
            else:
                datetime_to = datetime_from + timedelta(365)
                parameters['publishDateTo'] = datetime_to.strftime('%d.%m.%Y')

        if date_to and not date_from:
            datetime_from = datetime_to - timedelta(365)
            parameters['publishDateFrom'] = datetime_from.strftime('%d.%m.%Y')
        
        search_filter = args.get('search-filter')
        parameters['search-filter'] = sort_parameters[search_filter][0]
        parameters['sortBy'] = sort_parameters[search_filter][1]

        sort_direction = args.get('sort-direction')
        if sort_direction == 'from-new':
            parameters['sortDirection'] = 'false'
        elif sort_direction == 'from-old':
            parameters['sortDirection'] = 'true'
        else:
            return jsonify({'error': 'неверное значение направления сортировки'})
        
        history_id, status = parser.create_parser(user.id, parameters)
        return jsonify({'sucess': 'OK', 'id': history_id, 'status': status})
