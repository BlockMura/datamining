import requests
from bs4 import BeautifulSoup
import json


domain_url = 'https://geekbrains.ru/'
blog_url = 'https://geekbrains.ru/posts'


def get_page_strict(soup):
    posts_list = []
    posts_data = soup.find_all('div', class_='post-item')

    for post in posts_data:
        post_dict = {
            'post_url': f"{domain_url}{post.find('a').attrs.get('href')}",
            'post_title': post.find(class_='post_item__title').text,
            'post_date': post.find(class_='small m-t-xs').text
        }

        posts_list.append(post_dict)
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

with open (f'result_data.json', 'w') as j_file:
    j_file.write(json.dumps(result_data))

print(1)