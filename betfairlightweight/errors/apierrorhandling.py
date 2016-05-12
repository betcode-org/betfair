import logging

from ..errors import apiexceptions
from ..parse import enums


def api_login_error_handling(response, params=None, method=None):
    if response.get('loginStatus') != 'SUCCESS':
        raise apiexceptions.LoginError(response)


def api_keep_alive_error_handling(response, params=None, method=None):
    if response.get('status') != 'SUCCESS':
        raise apiexceptions.KeepAliveError(response)


def api_logout_error_handling(response, params=None, method=None):
    if response.get('status') != 'SUCCESS':
        raise apiexceptions.LogoutError(response)


def api_betting_error_handling(response, params=None, method=None):
    if response.get('result'):
        return
    elif response.get('error'):
        raise apiexceptions.APIError(response, params, method)


def api_order_error_handling(response, params=None, method=None):
    if response.get('error'):
        raise apiexceptions.APIError(response, params, method)
    elif response['result']['status'] != 'SUCCESS':
        if 'errorCode' in response['result']:
            response_error_code = response['result']['errorCode']
            description = enums.ExecutionReportErrorCode[response_error_code].value
            logging.warning('API Execution %s: %s' % (response['result']['status'], description))
            for order in response['result']['instructionReports']:
                if order['status'] != 'SUCCESS':
                    error_code = order.get('errorCode')
                    description = enums.InstructionReportErrorCode[error_code].value
                    logging.warning(' Instruction %s: %s' % (error_code, description))
        else:
            logging.error(' No errorCode: %s' % response['result'])
