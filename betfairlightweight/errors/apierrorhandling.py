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


def api_betting_error_handling(response, params=None, method=None):
    if response.get('result'):
        return
    elif response.get('error'):
        raise apiexceptions.APIError(response, params, method)


def api_order_error_handling(response, params=None, method=None):
    if response.get('error'):
        raise apiexceptions.APIError(response, params, method)
    elif response['result']['status'] != 'SUCCESS':
        response_error_code = response['result']['errorCode']
        description = apierrors.EXECUTION_REPORT_ERROR_CODE[response_error_code]
        logging.warning('API Execution %s: %s' % (response['result']['status'], description))
        for order in response['result']['instructionReports']:
            if order['status'] != 'SUCCESS':
                logging.warning('Bug error %s, request: %s' % (method, params))
                logging.warning('Bug error %s, response: %s' % (method, response))
                error_code = order.get('errorCode')
                description = apierrors.INSTRUCTION_REPORT_ERROR_CODE.get(error_code)
                logging.warning(' Instruction %s: %s' % (error_code, description))
