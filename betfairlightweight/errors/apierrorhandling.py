import logging
import errors.apierrors as apierrors


def api_login_error_handling(response):
    if 'sessionToken' not in response:
        print(response)
        description = apierrors.LOGIN_EXCEPTIONS[response['loginStatus']]
        logging.error('API login %s: %s' % (response['loginStatus'], description))


def api_keep_alive_error_handling(response):
    if response['token'] == '':
        logging.error('API keepAlive %s: %s' % (response['status'], response['error']))


def api_logout_error_handling(response):
    if response['status'] != 'SUCCESS':
        logging.error('API logout %s: %s' % (response['status'], response['error']))


def api_betting_error_handling(response, params=None):
    if 'error' in response:
        code = response['error']['code']
        description = apierrors.GENERIC_JSON_RPC_EXCEPTIONS.get(code)
        if not description:
            errorCode = response['error']['data']['APINGException']['errorCode']
            description = apierrors.APING_EXCEPTION.get(errorCode)
        logging.error('API betting %s: %s | %s' % (code, description, params))
    else:
        return response
