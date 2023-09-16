from .time_print import time_print
from colorama import Fore, Back, Style
import http.client as httplib #needed for http requests
import sys

def checkInternetHttplib(url, timeout):
    time_print(Fore.WHITE + 'Checking Network Connection...')
    connection = httplib.HTTPConnection(url, timeout=timeout)
    try:
        connection.request("HEAD", "/")
        response = connection.getresponse()
        if response.status == 200:
            time_print(Fore.GREEN + 'Connection to internet made.' + Fore.WHITE)
            return True
        elif response.status == 301:
            time_print(Fore.LIGHTRED_EX + 'Error 301: Moved Permanently or Server Problem.')
        elif response.status == 401:
            time_print(Fore.LIGHTRED_EX + 'Error 401: Unauthorized Access.')
        elif response.status == 402:
            time_print(Fore.LIGHTRED_EX + 'Error 402: Payment Required.')
        elif response.status == 404:
            time_print(Fore.LIGHTRED_EX + 'Error 404: Not Found.')
        elif response.status == 502:
            time_print(Fore.LIGHTRED_EX + 'Error 502: Bad Gateway. Server Problem.')
        else:
            time_print(Fore.LIGHTRED_EX + 'Error ' + str(response.status) + ': Connection Error')
        connection.close()
        sys.exit()
    except Exception as exep:
        time_print(exep)
        sys.exit(Fore.LIGHTRED_EX + 'Error, no internet connection')