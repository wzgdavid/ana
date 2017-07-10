# encoding:utf-8 
import requests
from bs4 import BeautifulSoup
login_page = 'https://login.51job.com/login.php'
r = requests.get(login_page)
r.encoding = r.apparent_encoding
print r.encoding
print r.text