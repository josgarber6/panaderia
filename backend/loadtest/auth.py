from bs4 import BeautifulSoup

HOST = "http://localhost:8000"

def admin_login(self):
    response = self.client.get(HOST + "/account/login/")
    csrftoken = response.cookies["csrftoken"]

    soup = BeautifulSoup(response.content, "html.parser")
    form = soup.find("form")
    form_data = {field.get("name"): field.get("value") for field in form.find_all("input")}

    form_data.update({"auth-username": "admin", "auth-password": "admin"})
    
    self.client.headers.update({"X-CSRFToken": csrftoken})
    response_post = self.client.post(HOST + "/account/login/", data=form_data)
    soup = BeautifulSoup(response_post.content, "html.parser")
    form = soup.find("form")
    form_data = {field.get("name"): field.get("value") for field in form.find_all("input")}

    form_data.update({"token-otp_token": '059448'})

    self.client.post(HOST + "/account/login/", data=form_data)

def customer_login(self):
    response = self.client.get(HOST + "/account/login/")
    csrftoken = response.cookies["csrftoken"]

    soup = BeautifulSoup(response.content, "html.parser")
    form = soup.find("form")
    form_data = {field.get("name"): field.get("value") for field in form.find_all("input")}

    form_data.update({"auth-username": "drkenobi", "auth-password": "contra123"})
    
    self.client.headers.update({"X-CSRFToken": csrftoken})
    response_post = self.client.post(HOST + "/account/login/", data=form_data)
    soup = BeautifulSoup(response_post.content, "html.parser")
    form = soup.find("form")
    form_data = {field.get("name"): field.get("value") for field in form.find_all("input")}

    form_data.update({"token-otp_token": '064284'})

    self.client.post(HOST + "/account/login/", data=form_data)

def logout(self):
    self.client.post(HOST + "/account/logout/")