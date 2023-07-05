from marshmallow.exceptions import ValidationError
from builder import build_query
from functions import check_path
from model import RequestSchema
from flask import request, jsonify, Blueprint
from db import db
from sqlalchemy import text

main_bp = Blueprint('main', __name__)


@main_bp.route("/perform_query", methods=["POST"])
def perform_query():
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    data = request.json
    try:
        data = RequestSchema().load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    if not check_path(file_name=data["file_name"]):
        return f"Файла {data['file_name']} не существует"

    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    first_result = build_query(
        cmd=data['cmd1'],
        value=data['value1'],
        file_name=data['file_name'],
        data=None,
    )
    second_result = build_query(
        cmd=data['cmd2'],
        value=data['value2'],
        file_name=data['file_name'],
        data=first_result,
    )
    # вернуть пользователю сформированный результат
    return jsonify(second_result)


@main_bp.route("/test", methods=["GET"])
def test_page():
    return "Test completed successfully"


@main_bp.route("/test_db", methods=["GET"])
def test_db():
    result = db.session.execute(
        text(
            'SELECT 1'
        )
    ).scalar()
    return jsonify(
        {
            'result': result
        }
    )
