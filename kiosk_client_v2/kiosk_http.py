import http.client
import urllib
import debug as dbug
import gzip

ENCODING = "utf-8"
HTTP_CONN_DEBUG_LVL = 0

def http_request(params):
    host = params["host"]
    port = params["port"]
    method = params["method"]
    resource = params["resource"]
    data = params["data"]
    callback = params["callback"]
	
    conn = http.client.HTTPConnection(host, port)
    conn.set_debuglevel(HTTP_CONN_DEBUG_LVL)

    params = urllib.parse.urlencode(data)
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"} 
	
    conn.request(method, resource, params, headers)
    response = conn.getresponse()
    result = response.read()
    #print(result)
    conn.close()

    f = open("tmp.txt.gz", "wb")
    f.write(result)
    f.close()
    f = gzip.open("tmp.txt.gz", "r")
    result = f.read()
    #dbug.debug(result.decode(ENCODING))
    callback(result)


