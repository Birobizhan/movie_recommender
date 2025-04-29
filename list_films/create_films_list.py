import requests
from bs4 import BeautifulSoup

url = 'https://www.kinoafisha.info/rating/movies/2025/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

headers = soup.find_all('a', class_='movieItem_title')

with open('movies_new.txt', 'a', encoding='utf-8') as f:
    for header in headers:
        f.write(f'{header.text}\n')

# with open('top1000_movies.txt', 'r', encoding='utf-8') as file:
#     f = file.readlines()
# with open('movies_new.txt', 'r', encoding='utf-8') as file:
#     listik = file.readlines()
#
# with open('right_top1000.txt', 'a', encoding='utf-8') as file:
#     for i in f:
#         if i not in listik:
#             file.write(f'{i}')
