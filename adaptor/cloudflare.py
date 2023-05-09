import json
import requests
from utils import *

PROVIDER = 'cloudflare'
USER_AGENT = 'OriDNS Proxy/1.0.0'


def test(config: dict) -> bool:
    cf_token = config['auth'].get('token', '')
    cf_api_zone_list = 'https://api.cloudflare.com/client/v4/zones'
    headers = {'User-Agent': USER_AGENT, 'Authorization': f'Bearer {cf_token}', 'Content-Type': 'application/json'}
    try:
        response = requests.get(cf_api_zone_list, headers=headers)
    except Exception as e:
        logger.exception(e)
        raise ODNetworkError(PROVIDER, cf_api_zone_list)

    if response.ok and response.status_code == 200:
        json_data = response.json()
        logger.debug(f'response: {json_data}')
        if json_data.get('success'):
            return True
        else:
            logger.error(f'errors: {json_data["errors"]}')
    raise ODRequestFailed(PROVIDER, cf_api_zone_list, json.dumps(response.json()['errors'], ensure_ascii=False))


def domain_list(config: dict) -> list[dict]:
    cf_token = config['auth'].get('token', '')
    cf_api_zone_list = 'https://api.cloudflare.com/client/v4/zones'
    headers = {'User-Agent': USER_AGENT, 'Authorization': f'Bearer {cf_token}', 'Content-Type': 'application/json'}

    try:
        response = requests.get(cf_api_zone_list, headers=headers)
    except Exception as e:
        logger.exception(e)
        raise ODNetworkError(PROVIDER, cf_api_zone_list)

    if response.ok:
        json_data = response.json()
        logger.debug(f'response: {json_data}')
        if json_data.get('success'):
            zones = json_data['result']
            res = []
            for zone in zones:
                res.append({
                    'id': zone['id'],
                    'name': zone['name'],
                    'status': zone['status'] == 'active',
                    'provider': 'cloudflare',
                    'service': config['name']
                })
            return res
    raise ODRequestFailed(PROVIDER, cf_api_zone_list, json.dumps(response.json()['errors'], ensure_ascii=False))


def domain_info(config: dict, domain_id: str):
    cf_token = config['auth'].get('token', '')
    cf_api_zone_info = f'https://api.cloudflare.com/client/v4/zones/{domain_id}'
    headers = {'User-Agent': USER_AGENT, 'Authorization': f'Bearer {cf_token}', 'Content-Type': 'application/json'}

    try:
        response = requests.get(cf_api_zone_info, headers=headers)
    except Exception as e:
        logger.exception(e)
        raise ODNetworkError(PROVIDER, cf_api_zone_info)

    if response.ok:
        json_data = response.json()
        logger.debug(f'response: {json_data}')
        if json_data.get('success'):
            info = json_data['result']
            return {
                'id': info['id'],
                'name': info['name'],
                'status': True,
                'created_at': info['created_on'],
                'ns': [],
                'provider': 'cloudflare',
            }
    raise ODRequestFailed(PROVIDER, cf_api_zone_info, json.dumps(response.json()['errors'], ensure_ascii=False))


def record_list(config: dict, domain_id: str, domain_name: str):
    cf_token = config['auth'].get('token', '')
    cf_api_record_list = f'https://api.cloudflare.com/client/v4/zones/{domain_id}/dns_records'
    headers = {'User-Agent': USER_AGENT, 'Authorization': f'Bearer {cf_token}', 'Content-Type': 'application/json'}

    try:
        response = requests.get(cf_api_record_list, headers=headers)
    except Exception as e:
        logger.exception(e)
        raise ODNetworkError(PROVIDER, cf_api_record_list)

    if response.ok:
        json_data = response.json()
        logger.debug(f'response: {json_data}')
        if json_data.get('success'):
            records = json_data['result']
            res = []
            for record in records:
                r_name = record['name']
                if r_name == domain_name:
                    r_name = '@'
                elif r_name.endswith(f'.{domain_name}'):
                    r_name = r_name[:-len(f'.{domain_name}')]
                res.append({
                    'id': record['id'],
                    'name': r_name,
                    'type': record['type'],
                    'value': record['content'],
                    'status': True,
                    'ttl': record['ttl'],
                    'proxied': record['proxied'],
                    'proxiable': record['proxiable'],
                    'service': config['name']
                })
            return res
    raise ODRequestFailed(PROVIDER, cf_api_record_list, json.dumps(response.json()['errors'], ensure_ascii=False))


def record_create(config: dict, domain_id: str, domain_name: str, record_type: str, record_name: str, value: str,
                  ttl: int) -> bool:
    cf_token = config['auth'].get('token', '')
    cf_api_record_add = f'https://api.cloudflare.com/client/v4/zones/{domain_id}/dns_records'
    if record_name == '@':
        record_name = domain_name
    else:
        record_name = f'{record_name}.{domain_name}'
    payload = {"content": value, "name": record_name, "type": record_type, "ttl": int(ttl)}
    headers = {'User-Agent': USER_AGENT, 'Authorization': f'Bearer {cf_token}', 'Content-Type': 'application/json'}

    try:
        response = requests.post(cf_api_record_add, headers=headers, json=payload)
    except Exception as e:
        logger.exception(e)
        raise ODNetworkError(PROVIDER, cf_api_record_add)

    if response.ok:
        json_data = response.json()
        logger.debug(f'response: {json_data}')
        if json_data.get('success'):
            return True
    raise ODRequestFailed(PROVIDER, cf_api_record_add, json.dumps(response.json()['errors'], ensure_ascii=False))


def record_update(config: dict, domain_id: str, domain_name: str, record_id: str, record_type: str, record_name: str,
                  value: str, ttl: int) -> bool:
    cf_token = config['auth'].get('token', '')
    cf_api_record_update = f'https://api.cloudflare.com/client/v4/zones/{domain_id}/dns_records/{record_id}'
    payload = {"content": value, "name": record_name, "type": record_type, "ttl": int(ttl)}
    headers = {'User-Agent': USER_AGENT, 'Authorization': f'Bearer {cf_token}', 'Content-Type': 'application/json'}

    try:
        response = requests.put(cf_api_record_update, headers=headers, json=payload)
    except Exception as e:
        logger.exception(e)
        raise ODNetworkError(PROVIDER, cf_api_record_update)

    if response.ok:
        json_data = response.json()
        logger.debug(f'response: {json_data}')
        if json_data.get('success'):
            return True
    raise ODRequestFailed(PROVIDER, cf_api_record_update, json.dumps(response.json()['errors'], ensure_ascii=False))


def record_delete(config: dict, domain_id: str, record_id: str) -> bool:
    cf_token = config['auth'].get('token', '')
    cf_api_record_delete = f'https://api.cloudflare.com/client/v4/zones/{domain_id}/dns_records/{record_id}'
    headers = {'User-Agent': USER_AGENT, 'Authorization': f'Bearer {cf_token}', 'Content-Type': 'application/json'}

    try:
        response = requests.delete(cf_api_record_delete, headers=headers)
    except Exception as e:
        logger.exception(e)
        raise ODNetworkError(PROVIDER, cf_api_record_delete)

    if response.ok:
        json_data = response.json()
        logger.debug(f'response: {json_data}')
        if json_data.get('success'):
            return True
    raise ODRequestFailed(PROVIDER, cf_api_record_delete, json.dumps(response.json()['errors'], ensure_ascii=False))
