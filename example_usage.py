# example.py（パッケージの外に配置）
from address_search import ZipCode, RequestsHttpClient, is_err
from address_search.main import fetch_and_format_address, handle_fetch_error

http_client = RequestsHttpClient()
zipcode = ZipCode("1000001")
result = fetch_and_format_address(zipcode, include_kana=True, http_client=http_client)

if is_err(result):
    handle_fetch_error(result.error)
else:
    print(result.value)
