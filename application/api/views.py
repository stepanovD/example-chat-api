__author__ = 'dmitry'
import json, datetime
from flask import g, request, redirect, url_for, jsonify, session, Response
from flask_security import login_user, logout_user
from flask_security.decorators import anonymous_user_required, auth_token_required
from flask_security.utils import verify_password, encrypt_password

from application.domain import *
from application.api import api
from application import user_datastore


# @api.before_request
# def before_request():
#     g.user = current_user


@api.route('/', methods=['GET', 'OPTIONS'])
@auth_token_required
def index():
    links = dict()
    if g.user.is_anonymous:
        links["login"] = url_for('api.login')
        links["registry"] = url_for('api.registry')
    else:
        links["logout"] = url_for('api.logout')
        links["self"] = url_for('api.user', user_id=g.user.get_id())
        links["users"] = url_for('api.users')
        links["roles"] = url_for('api.roles')
        links["chats"] = url_for('api.chats')
        links["messages"] = url_for('api.messages')

    return jsonify(_links=links)


@api.route('/login/', methods=['POST', 'OPTIONS'])
@anonymous_user_required
def login():
    data_json = request.get_json()

    session['remember_me'] = True
    user = User.query.filter_by(email=data_json["email"]).first_or_404()

    if verify_password(data_json["password"], user.password):
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)

        login_user(user, remember=remember_me)

        return jsonify(result=True, text="login successful", token=user.get_auth_token()), 200
    else:
        return jsonify(result=False, text="invalid password"), 400


@api.route('/logout/')
@auth_token_required
def logout():
    logout_user()
    return jsonify(result=True, text="logout successful"), 200


@api.route('/registry/', methods=['POST', "OPTIONS"])
@anonymous_user_required
def registry():
    data_json = request.get_json()

    session['remember_me'] = False

    user_exists = db.session.query(db.exists().where(User.email == data_json["email"])).scalar()

    if user_exists:
        return jsonify(text="User %r already exist" % data_json["email"]), 400

    created_user = user_datastore.create_user(email=data_json["email"], password=encrypt_password(data_json["password"]))
    user_datastore.add_role_to_user(created_user, Role.query.get(2))
    db.session.flush()
    db.session.commit()
    # flash("Registry successful. Please sign in.")
    return jsonify(result=True, text="registry successful", user_id=created_user.id), 200


################################################################################
############ USERS
################################################################################

@api.route('/users/', methods=["GET", "OPTIONS"])
@auth_token_required
# @auth_token_required
def users():
    all_users = [u for u in User.query.all()]
    result = users_schema.dump(all_users).data
    return Response(json.dumps(result), mimetype='application/json')


@api.route('/users/<user_id>/', methods=["GET", "OPTIONS"])
@auth_token_required
def user(user_id):
    if g.user.is_authenticated:
        user = get_user(user_id)
        if user:
            return user_schema.jsonify(user)
        return jsonify({"result": False, "message": "Access is denied"}), 403
    return jsonify({"result": False, "message": "required authentication "}), 403

def get_user(user_id):
    if g.user.is_authenticated:
        return User.query.get_or_404(user_id)
    return None


################################################################################
############ ROLES
################################################################################

@api.route('/roles/', methods=["GET", "OPTIONS"])
@auth_token_required
def roles():
    roles = Role.query.all()
    return Response(json.dumps(roles_schema.dump(roles).data), mimetype='application/json')


@api.route('/roles/<role_id>/', methods=["GET", "OPTIONS"])
@auth_token_required
def role(role_id):
    role = Role.query.get_or_404(role_id)
    return role_schema.jsonify(role)


################################################################################
############ CHATS
################################################################################

@api.route('/chats/', methods=["GET", "OPTIONS"])
@auth_token_required
def chats():
    if g.user.is_authenticated:
        chats = Chat.query.filter(Chat.users.contains(g.user)).all()
        return Response(json.dumps(chats_schema.dump(chats).data), mimetype='application/json')
    return jsonify({"result": False, "message": "required authentication "}), 403

@api.route('/chats/', methods=['POST'])
@auth_token_required
def create_chat():
    if g.user.is_authenticated:
        data_json = request.get_json()

        chat = Chat(title=data_json["title"], owner_id=g.user.get_id())

        chat.users = [g.user]

        db.session.add(chat)
        db.session.flush()
        db.session.commit()

        return jsonify({"result": True, "message": "chat is created", "link": url_for("api.chat", chat_id=chat.id)})

    return jsonify({"result": False, "message": "required authentication "}), 403

@api.route('/chats/<chat_id>/', methods=["GET", "OPTIONS"])
@auth_token_required
def chat(chat_id):
    if g.user.is_authenticated:
        chat = get_chat(chat_id)
        if chat is not None:
            return chat_schema.jsonify(chat)
        else: return jsonify({"result": False, "message": "Access is denied"}), 403
    return jsonify({"result": False, "message": "required authentication "}), 403

@api.route('/chats/<chat_id>/', methods=['PUT'])
@auth_token_required
def update_chat(chat_id):
    if g.user.is_authenticated:
        chat = get_chat(chat_id)
        if chat is not None:
            data_json = request.get_json()
            user = get_user(data_json["user_id"])
            if user not in chat.users:
                chat.users.append(get_user(data_json["user_id"]))
                db.session.commit()
                return chat_schema.jsonify(chat)
            else:
                return jsonify({"result": False, "message": "User already exist in chat"}), 400
        else: return jsonify({"result": False, "message": "Access is denied"}), 403
    return jsonify({"result": False, "message": "required authentication "}), 403

@api.route('/chats/<chat_id>/users/', methods=["GET", "OPTIONS"])
@auth_token_required
def chat_users(chat_id):
    if g.user.is_authenticated:
        chat = get_chat(chat_id)
        if chat is not None:
            return Response(json.dumps(users_schema.dump(chat.users).data), mimetype='application/json')
        else:
            return jsonify({"result": False, "message": "Access is denied"}), 403
    return jsonify({"result": False, "message": "required authentication "}), 403

@api.route('/chats/<chat_id>/messages/', methods=["GET", "OPTIONS"])
@auth_token_required
def chat_messages(chat_id):
    if g.user.is_authenticated:
        chat = get_chat(chat_id)
        if chat is not None:
            page = 1
            if request.args.has_key('page'):
                page = int(request.args['page'])

            messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.id.desc()).paginate(page, 20)
            return Response(json.dumps(messages_schema.dump(messages.items).data), mimetype='application/json')
        else:
            return jsonify({"result": False, "message": "Access is denied"}), 403

    return jsonify({"result": False, "message": "required authentication "}), 403


def get_chat(chat_id):
    if g.user.is_authenticated:
        chat = Chat.query.get_or_404(chat_id)
        if g.user in chat.users:
            return chat
    return None

################################################################################
############ MESSAGES
################################################################################

@api.route('/messages/', methods=["GET", "OPTIONS"])
@auth_token_required
def messages():
    if g.user.is_authenticated:
        page = 1
        if request.args.has_key('page'):
            page = int(request.args['page'])

        messages = Message.query.filter_by(chat_id=None).order_by(Message.id.desc()).paginate(page, 20)
        return Response(json.dumps(messages_schema.dump(messages.items).data), mimetype='application/json')

    return jsonify({"result": False, "message": "required authentication "}), 403

@api.route('/messages/<message_id>/', methods=["GET", "OPTIONS"])
@auth_token_required
def message(message_id):
    if g.user.is_authenticated:
        message = get_message(message_id)
        if message is not None:
            return message_schema.jsonify(message)
        else:
            return jsonify({"result": False, "message": "Access is denied"}), 403

    return jsonify({"result": False, "message": "required authentication "}), 403

@api.route('/messages/', methods=['POST'])
@auth_token_required
def create_message():
    if g.user.is_authenticated:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400
        post_message, errors = message_schema.load(json_data)

        if errors:
            return jsonify(errors), 422

        new_message = Message(content=post_message["content"], user_id=g.user.get_id())
        # new_message.user_id = g.user.get_id()

        if "chat_id" in json_data.keys():
            if get_chat(json_data["chat_id"]):
                new_message.chat_id = json_data["chat_id"]
            else:
                return jsonify({"result": False, "message": "Chat %r access denied" % json_data["chat_id"]}), 403
        db.session.add(new_message)
        db.session.flush()
        db.session.commit()
        return jsonify({"result": True, "message": "message created", "link": url_for("api.message", message_id=new_message.id)}), 200
    return jsonify({"result": False, "message": "required authentication "}), 403

def get_message(message_id):
    if g.user.is_authenticated:
        message = Message.query.get_or_404(message_id)
        if message.chat_id is None or get_chat(message.chat_id):
            return message
    return None