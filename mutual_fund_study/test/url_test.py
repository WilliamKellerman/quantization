from urllib.parse import urlencode
from urllib.parse import urljoin
from urllib.parse import urlparse

url = 'http://test.dis.e.sogou/adlist?offset=0&auth=69CF80EA062863279B72612FA5443B6F&requestId=0025500016111592878436805&count=1&network=1'
parsed = urlparse(url)
print(parsed)
newurl = parsed.geturl()

query_args = {
    'q': 'query string',
    'foo': 'bar',
}
encoded_args = urlencode(query_args)
print('Encoded:', encoded_args)

print(urljoin('http://www.example.com/path/file.html',
              'anotherfile.html'))
print(urljoin('http://www.example.com/path/file.html',
              '../anotherfile.html'))


