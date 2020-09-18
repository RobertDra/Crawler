import requests
from requests_html import HTMLSession
import json

class Crawler(object):
    def __init__(self, url, email, password):
        self.base_url = url
        self.urls = []
        self.result = {}
        self.cookie = {}
        self.values = {'l_email': email,
                       'l_password': password}
        self.session = None
        self.html_content = []
        self.links = []


    def login(self):
        response = requests.post(self.base_url, params=self.values)
        cookie_name = response.headers["Set-Cookie"].split(';')[0]
        cookie_name = cookie_name.split('=')
        self.cookie[cookie_name[0]] = cookie_name[1]

    def connect(self):
        try:
            self.session = HTMLSession()
            self.html_content.append(self.session.post(self.base_url, data=self.values, cookies=self.cookie))
        except requests.exceptions.RequestException as e:
            print(e)

    def crawl(self):
        self.links.extend(list(self.html_content[0].html.links))

        for link in self.links:
            self.html_content.append(self.session.post(self.base_url + link[1:], cookies=self.cookie))
            new_links = list(self.html_content[-1].html.links)
            for new_link in new_links:
                if new_link[1] != '.' and new_link not in self.links:
                    self.links.append(new_link)

    def find_images(self):
        for link in self.links:
            response = self.session.post(self.base_url + link[1:], cookies=self.cookie)
            title = list(response.html.find('img'))
            amount_images = (len(title))
            self.result[link] = [{"amonut images: ": amount_images}]

    def make_file(self):
        with open('abc.json', 'w') as outfile:
            json.dump(self.result, outfile, ensure_ascii=False)
            
    def start(self):
        self.login()
        self.connect()
        self.crawl()
        self.find_images()
        self.make_file()