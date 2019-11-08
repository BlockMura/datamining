import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime as dt
domain_url = 'https://geekbrains.ru/'
blog_url = 'https://geekbrains.ru/posts'

def get_page_strict(soup):
    posts_list = []
    posts_data = soup.find_all('div', class_='post-item')


    for post in posts_data:
        post_url = f"{domain_url}{post.find('a').attrs.get('href')}"
        page_soup = get_page_soup(post_url)
        tmp = page_soup.find(class_="js-mediator-article").attrs.get('content')
        start = tmp.find('https')
        end = tmp.find('.jpg')
        au = page_soup.find(style="text-decoration:none;").attrs.get('href')
        page_dict = {
            "title": page_soup.find(class_="blogpost-title").text,  # Заголовок
            "image": tmp[int(start): int(end)], # Ссылка на первое изображение
            "text": page_soup.find('div', class_='blogpost-content content_text content js-mediator-article').text, # Текст статьи
            "pub_date": page_soup.find(class_='text-md text-muted m-r-md').attrs.get('datetime'), # Дата и время создания
            "autor": {"name": page_soup.find(class_='text-lg text-dark').text, #Данные автора
                      "url": f"{domain_url}{au}"},
        }

        posts_list.append(page_dict)


    return posts_list


def get_page_soup(url):
    page_data = requests.get(url)
    soup_data = BeautifulSoup(page_data.text, 'lxml')
    return soup_data


def parser(url):
    posts_list = []

    while True:
        soup = get_page_soup(url)
        posts_list.extend(get_page_strict(soup))
        try:
            url = soup.find('a', attrs={'rel': 'next'}, text='›').attrs.get('href')
        except AttributeError as e:
            break
        url = f"{domain_url}{url}"
    return posts_list


result_data = parser(blog_url)



with open (f'result_data_{int(dt.now().timestamp())}.json', 'w') as j_file:
    j_file.write(json.dumps(result_data))
