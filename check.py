import requests
import sys
import time
from colorama import Fore, Style, init

# Inisialisasi colorama
init()

def check_host(url):
    try:
        # Menambahkan "https://" jika tidak ada di URL
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        response = requests.get(url, timeout=2)

        response_messages = {
            100: "Continue",
            101: "Switching Protocols",
            200: "OK",
            201: "Created",
            202: "Accepted",
            203: "Non-Authoritative Information",
            204: "No Content",
            205: "Reset Content",
            206: "Partial Content",
            300: "Multiple Choices",
            301: "Moved Permanently",
            302: "Found",
            303: "See Other",
            304: "Not Modified",
            305: "Use Proxy",
            307: "Temporary Redirect",
            400: "Bad Request",
            401: "Unauthorized",
            402: "Payment Required",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            406: "Not Acceptable",
            407: "Proxy Authentication Required",
            408: "Request Timeout",
            409: "Conflict",
            410: "Gone",
            411: "Length Required",
            412: "Precondition Failed",
            413: "Request Entity Too Large",
            414: "Request-URI Too Long",
            415: "Unsupported Media Type",
            416: "Requested Range Not Satisfiable",
            417: "Expectation Failed",
            500: "Internal Server Error",
            501: "Not Implemented",
            502: "Bad Gateway",
            503: "Service Unavailable",
            504: "Gateway Timeout",
            505: "HTTP Version Not Supported",
        }

        if response.status_code in response_messages:
            message = f"Host {url} is reachable. Response code: {response.status_code} {response_messages[response.status_code]}"
            color = Fore.GREEN if 200 <= response.status_code < 300 else Fore.RED  # Warna hijau jika 2xx, merah jika selain 2xx
        else:
            message = f"Host {url} is reachable. Response code: {response.status_code}"
            color = Fore.RED

        # Menangani kasus khusus Server is Down
        if response.status_code == 503 and "server is down" in response.text.lower():
            message = f"Warning: Server at {url} is reporting Service Unavailable. (Custom message: server is down)"
            color = Fore.RED

        print(color + message + Style.RESET_ALL)
    except requests.exceptions.Timeout:
        print(Fore.RED + f"Request to host {url} timed out. Server may be slow to respond." + Style.RESET_ALL)
    except requests.exceptions.RequestException:
        print(Fore.RED + f"Failed to connect to host {url}." + Style.RESET_ALL)

# Memeriksa apakah argumen diberikan pada saat menjalankan skrip
if len(sys.argv) != 2:
    print("Usage: python check.py <url>")
else:
    # Mengambil URL dari argumen command line
    target_url = sys.argv[1]

    # Loop untuk melakukan pemeriksaan dengan jeda 2 detik
    while True:
        check_host(target_url)
        time.sleep(2)

