import http.client

conn = http.client.HTTPConnection("captcha.lianjia.com")

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"_csrf\"\r\n\r\nODFkSFVZMjZOdVMbYRQARAljHS4yIGoAVFUwPxQMc31SZSEiEWheTw\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"uuid\"\r\n\r\n595e14964aee6\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"bitvalue\"\r\n\r\n8\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"

headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
                'cache-control': "no-cache",
                    'postman-token': "b2267001-06d2-980a-0850-ceaa1abdce2f"
                        }

conn.request("POST", "/human", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
