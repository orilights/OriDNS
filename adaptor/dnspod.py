import json
import requests
from utils import *

PROVIDER = 'dnspod'
USER_AGENT = 'OriDNS Proxy/1.0.0'
headers = {'User-Agent': USER_AGENT}


def test(config: dict) -> bool:
    dp_id = config['auth'].get('id', '')
    dp_token = config['auth'].get('token', '')
    dp_api_domain_list = 'https://dnsapi.cn/Domain.List'
    payload = {'login_token': f'{dp_id},{dp_token}', 'format': 'json'}

    try:
        response = requests.post(dp_api_domain_list, headers=headers, data=payload)
    except Exception as e:
        logger.exception(e)
        raise ODNetworkError(PROVIDER, dp_api_domain_list)

    if response.ok:
        json_data = response.json()
        logger.debug(f'response: {json_data}')
        if json_data['status']['code'] == '1':
            return True
        else:
            logger.error('error code:', json_data['status']['code'])
            logger.info('refer: https://docs.dnspod.cn/api/common-return/')
    raise ODRequestFailed(PROVIDER, dp_api_domain_list, json.dumps(response.json()['status'], ensure_ascii=False))


def domain_list(config: dict) -> list[dict]:
    dp_id = config['auth'].get('id', '')
    dp_token = config['auth'].get('token', '')

    dp_api_domain_list = 'https://dnsapi.cn/Domain.List'
    payload = {'login_token': f'{dp_id},{dp_token}', 'format': 'json'}

    try:
        response = requests.post(dp_api_domain_list, headers=headers, data=payload)
    except Exception as e:
        logger.exception(e)
        raise ODNetworkError(PROVIDER, dp_api_domain_list)
    if response.ok:
        json_data = response.json()
        logger.debug(f'response: {json_data}')
        if json_data['status']['code'] == '1':
            domains = json_data['domains']
            res = []
            for domain in domains:
                res.append({
                    "id": str(domain['id']),
                    "name": domain['name'],
                    "status": domain['status'] == 'enable',
                    "provider": "dnspod",
                    "service": config['name']
                })
            return res
    return []


def domain_info(config: dict, domain_id: str):
    dp_id = config['auth'].get('id', '')
    dp_token = config['auth'].get('token', '')

    dp_api_domain_info = 'https://dnsapi.cn/Domain.Info'
    payload = {'login_token': f'{dp_id},{dp_token}', 'format': 'json', 'domain_id': domain_id}

    try:
        response = requests.post(dp_api_domain_info, headers=headers, data=payload)
    except Exception as e:
        logger.exception(e)
        raise ODNetworkError(PROVIDER, dp_api_domain_info)

    if response.ok:
        json_data = response.json()
        logger.debug(f'response: {json_data}')
        if json_data['status']['code'] == '1':
            info = json_data['domain']
            return {
                'id': str(info['id']),
                'name': info['name'],
                'status': info['status'] == 'enable',
                'created_at': info['created_on'],
                'ns': info['dnspod_ns'],
                'provider': 'dnspod',
            }
    raise ODRequestFailed(PROVIDER, dp_api_domain_info, json.dumps(response.json()['status'], ensure_ascii=False))


def record_list(config: dict, domain_id: str, domain_name: str):
    dp_id = config['auth'].get('id', '')
    dp_token = config['auth'].get('token', '')

    dp_api_record_list = 'https://dnsapi.cn/Record.List'
    payload = {'login_token': f'{dp_id},{dp_token}', 'format': 'json', 'domain_id': domain_id}

    try:
        response = requests.post(dp_api_record_list, headers=headers, data=payload)
    except Exception as e:
        logger.exception(e)
        raise ODNetworkError(PROVIDER, dp_api_record_list)

    if response.ok:
        json_data = response.json()
        logger.debug(f'response: {json_data}')
        if json_data['status']['code'] == '1':
            records = json_data['records']
            res = []
            for record in records:
                res.append({
                    "id": str(record['id']),
                    "name": record['name'],
                    "type": record['type'],
                    "ttl": record['ttl'],
                    "value": record['value'],
                    "status": record['status'] == 'enable',
                    "proxied": False,
                    "proxiable": False,
                    "service": config['name']
                })
            return res
    raise ODRequestFailed(PROVIDER, dp_api_record_list, json.dumps(response.json()['status'], ensure_ascii=False))


def record_create(config: dict, domain_id: str, domain_name: str, record_type: str, record_name: str, value: str,
                  ttl: int) -> bool:
    dp_id = config['auth'].get('id', '')
    dp_token = config['auth'].get('token', '')

    dp_api_record_add = 'https://dnsapi.cn/Record.Create'
    payload = {
        'login_token': f'{dp_id},{dp_token}',
        'format': 'json',
        'domain_id': domain_id,
        'sub_domain': record_name,
        'record_type': record_type,
        'record_line': '默认',
        'value': value,
        'ttl': ttl
    }

    try:
        response = requests.post(dp_api_record_add, headers=headers, data=payload)
    except Exception as e:
        logger.exception(e)
        raise ODNetworkError(PROVIDER, dp_api_record_add)

    if response.ok:
        json_data = response.json()
        logger.debug(f'response: {json_data}')
        if json_data['status']['code'] == '1':
            return True
    raise ODRequestFailed(PROVIDER, dp_api_record_add, json.dumps(response.json()['status'], ensure_ascii=False))


def record_update(config: dict, domain_id: str, domain_name: str, record_id: str, record_type: str, record_name: str,
                  value: str, ttl: int) -> bool:
    dp_id = config['auth'].get('id', '')
    dp_token = config['auth'].get('token', '')

    dp_api_record_update = 'https://dnsapi.cn/Record.Modify'
    payload = {
        'login_token': f'{dp_id},{dp_token}',
        'format': 'json',
        'domain_id': domain_id,
        'record_id': record_id,
        'sub_domain': record_name,
        'record_type': record_type,
        'record_line': '默认',
        'value': value,
        'ttl': int(ttl)
    }

    try:
        response = requests.post(dp_api_record_update, headers=headers, data=payload)
    except Exception as e:
        logger.exception(e)
        raise ODNetworkError(PROVIDER, dp_api_record_update)

    if response.ok:
        json_data = response.json()
        logger.debug(f'response: {json_data}')
        if json_data['status']['code'] == '1':
            return True
    raise ODRequestFailed(PROVIDER, dp_api_record_update, json.dumps(response.json()['status'], ensure_ascii=False))


def record_delete(config: dict, domain_id: str, record_id: str) -> bool:
    dp_id = config['auth'].get('id', '')
    dp_token = config['auth'].get('token', '')

    dp_api_record_delete = 'https://dnsapi.cn/Record.Remove'

    payload = {'login_token': f'{dp_id},{dp_token}', 'format': 'json', 'domain_id': domain_id, 'record_id': record_id}
    headers = {'User-Agent': USER_AGENT}

    try:
        response = requests.post(dp_api_record_delete, headers=headers, data=payload)
    except Exception as e:
        logger.exception(e)
        raise ODNetworkError(PROVIDER, dp_api_record_delete)

    if response.ok:
        json_data = response.json()
        logger.debug(f'response: {json_data}')
        if json_data['status']['code'] == '1':
            return True
    raise ODRequestFailed(PROVIDER, dp_api_record_delete, json.dumps(response.json()['status'], ensure_ascii=False))
