__all__ = ['check_connection']

import http.client


def check_connection(hostname: str) -> bool:
    try:
        connection = http.client.HTTPConnection(hostname, timeout=5)
        connection.request("HEAD", "/")
        response = connection.getresponse()

        status_code = response.status
        connection.close()
        return status_code == 200
    except Exception:
        return False
