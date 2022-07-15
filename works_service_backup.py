import jwt
import datetime
import requests
import time


class WorksServiceBackup:
    client_id = "QoUh4Noe7dzVQB76ntsA"
    client_secret = "ug4f3_bFA1"
    service_account = "k7817.serviceaccount@corisetec.com"
    current_ts = datetime.datetime.now().timestamp()
    expire_ts = (datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp()

    token_url = "https://auth.worksmobile.com/oauth2/v2.0/token"
    bot_url = "https://www.worksapis.com/v1.0/bots/3903073"
    bot_file_url = "https://www.worksapis.com/v1.0/bots/3903073/attachments"
    bot_channel_url = "https://www.worksapis.com/v1.0/bots/3903073/channels"
    users_url = "https://www.worksapis.com/v1.0/users"

    token_request_headers = {
        "content-Type": "application/x-www-form-urlencoded"
    }

    with open('private_20220711131600.key', 'r') as rsa_priv_file:
        private_key = priv_rsakey = rsa_priv_file.read().replace("-----BEGIN RSA PRIVATE KEY-----\n", "").replace(
            "-----END RSA PRIVATE KEY-----\n", "")

    encoded = jwt.encode({
        "iss": client_id,
        "sub": service_account,
        "iat": current_ts,
        "exp": expire_ts
    }, private_key,
        algorithm="RS256")

    payload = {
        "assertion": encoded,
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": 'bot,user'
    }

    tokens = requests.post(token_url, headers=token_request_headers, data=payload)
    tokens = tokens.json()
    access_token = tokens["access_token"]
    auth = "Bearer " + access_token

    def make_room(self):
        response = requests.post(self.bot_channel_url, headers={
            "Authorization": self.auth,
            "Content-Type": "application/json"
        }, json={
            "members": [
                '453280b9-4523-48bd-1a8f-03e80edeae3f',
                'e2a5b8fa-b46e-462d-102d-03aecd85cf0c',
                'cd1e3496-e279-4c58-1b2e-03c1c42d5bf0',
                'c29dc380-c16f-4ccb-1493-03583029a0e6',
                'e373b330-5bcf-446b-1046-0396c33e6350',
            ],
            "title": "주간 업무 보고 양식 자동화방"
        })
        print(response.json())

    def view_channel_users(self):
        response = requests.get("https://www.worksapis.com/v1.0/bots/3903073/channels/153975591/members",
                                headers={
                                    "Authorization": self.auth,
                                })
        print(response.json())

    def get_bots(self):
        response = requests.get(self.bot_url, headers={
            "Authorization": self.auth,
        })
        print(response.json())

    def get_users(self):
        response = requests.get(self.users_url, headers={
            "Authorization": self.auth,
        })
        print(response.json())


    def get_file_id(self, fileName, file):
        response = requests.post(self.bot_file_url, headers={
            "Authorization": self.auth,
            "Content-Type": "application/json"
        }, json=
                                 {'fileName': fileName})

        uploadUrl = response.json()['uploadUrl']
        print(response.json())

        response = requests.post(uploadUrl, headers={
            "Authorization": self.auth,
        }, files={
            'file': file,
        })

        return response.json()['fileId']

    def send_message_to_channel(self, file_id):
        response = requests.post("https://www.worksapis.com/v1.0/bots/3903073/channels/153979734/messages",
                                 headers={
                                     "Authorization": self.auth,
                                     "Content-Type": "application/json"
                                 }, json={
                "content": {
                    "type": "text",
                    "text": "금주의 주간 보고 양식 파일을 공유해드립니다! \n 본 프로그램은 CMEFND 서버에서, 매 주 목요일 오후 6시에"
                            " 실행 설정 됩니다."
                }
            })

        response = requests.post("https://www.worksapis.com/v1.0/bots/3903073/channels/153979734/messages",
                                 headers={
                                     "Authorization": self.auth,
                                     "Content-Type": "application/json"
                                 }, json={
                "content": {
                    "type": "file",
                    "fileId": file_id
                }
            })

        print(response)
