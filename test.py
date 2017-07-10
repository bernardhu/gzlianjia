import requests

url = "http://captcha.lianjia.com/human"

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"_csrf\"\r\n\r\nODFkSFVZMjZOdVMbYRQARAljHS4yIGoAVFUwPxQMc31SZSEiEWheTw\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"uuid\"\r\n\r\n595e14964aee6\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"bitvalue\"\r\n\r\n8\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
                'cache-control': "no-cache",
                    'postman-token': "b2a2a99a-b68f-8d41-d211-ee4a7e0d795f"
                        }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
