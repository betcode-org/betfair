import logging
import betfairlightweight.errors.apiexceptions as apiexceptions
import betfairlightweight.errors.apierrors as apierrors


def api_login_error_handling(response):
    if response.get('loginStatus') != 'SUCCESS':
        raise apiexceptions.LoginError(response)


def api_keep_alive_error_handling(response):
    if response.get('status') != 'SUCCESS':
        raise apiexceptions.KeepAliveError(response)


def api_logout_error_handling(response):
    if response.get('status') != 'SUCCESS':
        raise apiexceptions.LogoutError(response)


def api_betting_error_handling(response, params=None):
    if response.get('result'):
        return
    elif 'error' in response:
        code = response['error']['code']
        description = apierrors.GENERIC_JSON_RPC_EXCEPTIONS.get(code)
        if not description:
            error_code = response['error']['data']['APINGException']['errorCode']
            description = apierrors.APING_EXCEPTION.get(error_code)
        logging.error('API betting %s: %s | %s' % (code, description, params))
        raise apiexceptions.APIError


def api_order_error_handling(response, params=None, method=None):
    if 'error' in response:
        code = response['error']['code']
        description = apierrors.GENERIC_JSON_RPC_EXCEPTIONS.get(code)
        logging.error('API betting %s: %s' % (code, description))
    elif response['result']['status'] != 'SUCCESS':
        response_error_code = response['result']['errorCode']
        description = apierrors.EXECUTION_REPORT_ERROR_CODE[response_error_code]
        logging.error('API Execution %s: %s' % (response['result']['status'], description))
        for order in response['result']['instructionReports']:
            if order['status'] != 'SUCCESS':
                logging.error('Bug error %s, request: %s' % (method, params))
                logging.error('Bug error %s, response: %s' % (method, response))
                error_code = order.get('errorCode')
                description = apierrors.INSTRUCTION_REPORT_ERROR_CODE[error_code]
                logging.error(' Instruction %s: %s' % (error_code, description))
