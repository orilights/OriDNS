import json, time, os
from importlib import import_module

from flask import Flask, request
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from itsdangerous import URLSafeTimedSerializer as Serializer

from utils import logger, Result as R, ODNetworkError, ODRequestFailed

TOKEN_EXPIRE_TIME = int(os.getenv('TOKEN_EXPIRE_TIME', '1209600')) # 14 days

app = Flask(__name__)

# CORS
cors = CORS()
cors.init_app(app, resources={r"/*": {"origins": "*"}})

# Auth
auth = HTTPTokenAuth(scheme='Bearer')
auth_s = Serializer(os.getenv('SECRET_KEY', 'dev'), os.getenv('TOKEN_SALT', 'dev'))


def load_config() -> dict:
    global config, providers
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    providers = config['provider'].keys()
    logger.info(f'find providers: {providers}')


def get_domain_list():
    res = []
    for provider in providers:
        logger.info(provider)
        for service in config['provider'][provider]:
            logger.info(service['name'])
            try:
                module = import_module(f'adaptor.{provider}')
                res.extend(module.domain_list(service))
            except Exception as e:
                logger.error(e)
                continue
    logger.info(res)
    return res


config = {}
providers = []
load_config()
domains = get_domain_list()
domains_last_update = time.time()


@auth.verify_token
def verify_token(token):
    try:
        data = auth_s.loads(token, max_age=TOKEN_EXPIRE_TIME)
    except:
        return False
    if 'username' in data and data['username'] == config['user']['username']:
        return True
    return False


@auth.error_handler
def auth_error():
    return R.fail('invalid token')


@app.route('/ping')
def default():
    return R.ok(msg='pong')


@app.route('/login', methods=['POST'])
def user_login():
    req_data = request.form
    username = req_data.get('username', None)
    password = req_data.get('password', None)
    if username is None or password is None:
        return R.fail('invalid request')
    if username == config['user']['username'] and password == config['user']['password']:
        return R.ok(data={'token': auth_s.dumps({'username': username, 'exp': int(time.time()) + TOKEN_EXPIRE_TIME})})
    return R.fail('invalid username or password')


@app.route('/refresh_token', methods=['POST'])
@auth.login_required
def refresh_token():
    return R.ok(
        data={
            'token': auth_s.dumps({
                'username': config['user']['username'],
                'exp': int(time.time()) + TOKEN_EXPIRE_TIME
            })
        })


@app.route('/verify', methods=['GET'])
@auth.login_required
def verify():
    return R.ok()


@app.route('/service/list', methods=['GET'])
@auth.login_required
def service_list():
    global providers


@app.route('/domain/list', methods=['GET'])
@auth.login_required
def domain_list():
    global domains, domains_last_update
    if request.args.get('force_refresh', '0') == '1':
        domains = get_domain_list()
        if len(domains) > 0:
            domains_last_update = time.time()
    elif time.time() - domains_last_update > 600:
        domains = get_domain_list()
        if len(domains) > 0:
            domains_last_update = time.time()
    if len(domains) > 0:
        return R.ok(data=domains)
    return R.fail('获取域名列表失败')


@app.route('/domain/<domain_id>/info', methods=['GET'])
@auth.login_required
def domain_info(domain_id):
    provider = 'unknown'
    service = 'unknown'
    for domain in domains:
        if domain['id'] == domain_id:
            provider = domain['provider']
            service = domain['service']
            break
    if provider == 'unknown':
        return R.fail('domain not found')
    try:
        module = import_module(f'adaptor.{provider}')
        for service_config in config['provider'][provider]:
            if service_config['name'] == service:
                return R.ok(data=module.domain_info(service_config, domain_id))
    except ODNetworkError as e:
        return R.fail(str(e))
    except ODRequestFailed as e:
        return R.fail(str(e))
    except Exception as e:
        logger.error(e)
        return R.fail('未知错误')
    return R.fail('未知错误')


@app.route('/domain/<domain_id>/record/list', methods=['GET'])
@auth.login_required
def record_list(domain_id):
    domain_name = 'unknown'
    provider = 'unknown'
    service = 'unknown'
    for domain in domains:
        if domain['id'] == domain_id:
            domain_name = domain['name']
            provider = domain['provider']
            service = domain['service']
            break
    if provider == 'unknown':
        return R.fail('domain not found')

    module = import_module(f'adaptor.{provider}')
    for service_config in config['provider'][provider]:
        if service_config['name'] == service:
            return R.ok(data=module.record_list(service_config, domain_id, domain_name))
    return R.fail('未知错误')


@app.route('/domain/<domain_id>/record/create', methods=['POST'])
@auth.login_required
def record_create(domain_id):
    req_data = request.form
    r_type = req_data.get('type', None)
    r_name = req_data.get('name', None)
    r_value = req_data.get('value', None)
    r_ttl = req_data.get('ttl', None)
    if r_type is None or r_name is None or r_value is None or r_ttl is None:
        return R.fail('invalid request')
    domain_name = 'unknown'
    provider = 'unknown'
    service = 'unknown'
    for domain in domains:
        if domain['id'] == domain_id:
            domain_name = domain['name']
            provider = domain['provider']
            service = domain['service']
            break
    if provider == 'unknown':
        return R.fail('domain not found')
    try:
        module = import_module(f'adaptor.{provider}')
        for service_config in config['provider'][provider]:
            if service_config['name'] == service:
                return R.ok(
                    data=module.record_create(service_config, domain_id, domain_name, r_type, r_name, r_value, r_ttl))
    except ODNetworkError as e:
        return R.fail(str(e))
    except ODRequestFailed as e:
        return R.fail(str(e))
    except Exception as e:
        logger.exception(e)
        return R.fail('未知错误')
    return R.fail('未知错误')


@app.route('/domain/<domain_id>/record/<record_id>/update', methods=['POST'])
@auth.login_required
def record_update(domain_id, record_id):
    req_data = request.form
    r_type = req_data.get('type', None)
    r_name = req_data.get('name', None)
    r_value = req_data.get('value', None)
    r_ttl = req_data.get('ttl', None)
    if r_type is None or r_name is None or r_value is None or r_ttl is None:
        return R.fail('invalid request')
    domain_name = 'unknown'
    provider = 'unknown'
    service = 'unknown'
    for domain in domains:
        if domain['id'] == domain_id:
            domain_name = domain['name']
            provider = domain['provider']
            service = domain['service']
            break
    if provider == 'unknown':
        return R.fail('domain not found')
    try:
        module = import_module(f'adaptor.{provider}')
        for service_config in config['provider'][provider]:
            if service_config['name'] == service:
                return R.ok(data=module.record_update(service_config, domain_id, domain_name, record_id, r_type, r_name,
                                                      r_value, r_ttl))
    except ODNetworkError as e:
        return R.fail(str(e))
    except ODRequestFailed as e:
        return R.fail(str(e))
    except Exception as e:
        logger.error(e)
        return R.fail('未知错误')
    return R.fail('未知错误')


@app.route('/domain/<domain_id>/record/<record_id>/delete', methods=['GET'])
@auth.login_required
def record_delete(domain_id, record_id):
    provider = 'unknown'
    service = 'unknown'
    for domain in domains:
        if domain['id'] == domain_id:
            provider = domain['provider']
            service = domain['service']
            break
    if provider == 'unknown':
        return R.fail('domain not found')
    try:
        module = import_module(f'adaptor.{provider}')
        for service_config in config['provider'][provider]:
            if service_config['name'] == service:
                return R.ok(data=module.record_delete(service_config, domain_id, record_id))
    except ODNetworkError as e:
        return R.fail(str(e))
    except ODRequestFailed as e:
        return R.fail(str(e))
    except Exception as e:
        logger.error(e)
        return R.fail('未知错误')
    return R.fail('未知错误')


if __name__ == '__main__':
    app.run('0.0.0.0', 3000, debug=True)