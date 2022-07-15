import time

import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# display = Display(visible=0, size=(800, 600))
# display.start()

class WorksService:
    client_id = "QoUh4Noe7dzVQB76ntsA"
    client_secret = "ug4f3_bFA1"
    service_account = "k7817.serviceaccount@corisetec.com"

    auth_url = "https://auth.worksmobile.com/oauth2/v2.0/authorize"
    redirect_url = "http://49.247.7.123:5000/oauth/redirect_url"

    token_url = "https://auth.worksmobile.com/oauth2/v2.0/token"
    bot_url = "https://www.worksapis.com/v1.0/bots/3903073"
    bot_file_url = "https://www.worksapis.com/v1.0/bots/3903073/attachments"
    bot_channel_url = "https://www.worksapis.com/v1.0/bots/3903073/channels"
    users_url = "https://www.worksapis.com/v1.0/users"

    groups_url = "https://www.worksapis.com/v1.0/groups"

    org_unit_id = "1396eb65-fd49-466e-29c7-03b0f370d37f"

    corise_group_url = "https://www.worksapis.com/v1.0/orgunits"

    token_request_headers = {
        "content-Type": "application/x-www-form-urlencoded"
    }

    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": 'bot,user,group.folder,group,file,directory',
        "response_type": "code",
        "state": "test",
        "redirect_uri": redirect_url
    }

    browser = webdriver.Chrome()

    email = "johnyim12345678@corisetec.com"
    password = "Wingwing!135"

    browser.get(
        'https://auth.worksmobile.com/oauth2/v2.0/authorize?client_id=QoUh4Noe7dzVQB76ntsA&redirect_uri=http%3A%2F%2F49.247.7.123%3A5000%2Foauth%2Fredirect_url&scope=bot%2Cuser%2Cgroup.folder%2Cgroup.folder.read%2Cfile%2Cfile.read%2Corgunit%2Corgunit.read&response_type=code&state=test')
    elem = browser.find_element(By.XPATH, '//*[@id="inputId"]')
    elem.send_keys(email)
    elem = browser.find_element(By.XPATH, '//*[@id="password"]')
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)

    html = browser.execute_script("return document.body.outerHTML;")
    html = str(html)
    a = html.split('"code":"')[1]
    code = a.split('","errorCode')[0]
    # print(code)

    browser.quit()

    body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
    }

    response = requests.post('https://auth.worksmobile.com/oauth2/v2.0/token',
                             headers=
                             token_request_headers,
                             data=body).json()
    access_token = response['access_token']
    auth = "Bearer " + access_token

    # print(auth)

    # def make_room(self):
    #     response = requests.post(self.bot_channel_url, headers={
    #         "Authorization": self.auth,
    #         "Content-Type": "application/json"
    #     }, json={
    #         "members": [
    #             '453280b9-4523-48bd-1a8f-03e80edeae3f',
    #             'e2a5b8fa-b46e-462d-102d-03aecd85cf0c',
    #             'cd1e3496-e279-4c58-1b2e-03c1c42d5bf0',
    #             'c29dc380-c16f-4ccb-1493-03583029a0e6',
    #             'e373b330-5bcf-446b-1046-0396c33e6350',
    #         ],
    #         "title": "주간 업무 보고 양식 자동화방"
    #     })
    #     print(response.json())

    def view_channel_users(self):
        response = requests.get("https://www.worksapis.com/v1.0/bots/3903073/channels/153975591/members",
                                headers={
                                    "Authorization": self.auth,
                                })
        print(response.json())

    def get_target_file_id(self, folder, file_name):
        response = requests.get(
            "https://www.worksapis.com/v1.0/groups/7c883c5e-17bf-487d-24ab-0367b70ddec6/folder/files/QDEwMDEwMDAwMDQ5MDA4MTF8MzQ3MjQ3OTk2NDQ2MDg3NTI3MnxEfDM0NzI0Nzk5NDk4MzQ1NDAwNDA/children",
            headers={"Authorization": self.auth})
        files = response.json()['files']
        # folder_exists = False
        file_id = "error"

        for file in files:
            if file['fileName'] == folder:
                file_id = file["fileId"]
                folder_exists = True
                break

        # if not folder_exists:
        #     response = requests.post(
        #         "https://www.worksapis.com/v1.0/groups/7c883c5e-17bf-487d-24ab-0367b70ddec6/folder/files/QDEwMDEwMDAwMDQ5MDA4MTF8MzQ3MjQ3OTk2NDQ2MDg3NTI3MnxEfDM0NzI0Nzk5NDk4MzQ1NDAwNDA/createfolder",
        #         headers={"Authorization": self.auth, "Content-Type": "application/json"},
        #         json={"fileName": folder})
        #     file_id = response.json()['fileId']

        response = requests.get(
            "https://www.worksapis.com/v1.0/groups/7c883c5e-17bf-487d-24ab-0367b70ddec6/folder/files/" + file_id + "/children",
            headers={"Authorization": self.auth, "Content-Type": "application/json"},
            )
        files = response.json()["files"]
        file_id = "error"
        for file in files:
            if file['fileName'] == file_name:
                file_id = file['fileId']
                print(file)
        print(file_id)
        response = requests.get(
            "https://www.worksapis.com/v1.0/groups/7c883c5e-17bf-487d-24ab-0367b70ddec6/folder/files/" + file_id + "/download",
            headers={"Authorization": self.auth}, stream=True)
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

    # 해외 데이터팀 아이디: 7c883c5e-17bf-487d-24ab-0367b70ddec6

    def get_group_files(self):
        response = requests.get(
            "https://www.worksapis.com/v1.0/groups/7c883c5e-17bf-487d-24ab-0367b70ddec6/folder/files/QDEwMDEwMDAwMDQ5MDA4MTF8MzQ3MjQ3OTk2NDQ2MDk5ODkyMXxEfDM0NzI0Nzk5NDk4MzQ1NDAwNDA/children",
            headers={"Authorization": self.auth})
        print(response.json())


WorksService().get_target_file_id('2022년', '주간업무보고_해외데이터팀(2022년7월3주).xlsx')
