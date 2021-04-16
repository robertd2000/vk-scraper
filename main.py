# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
import json
import time

import requests


def get_response():
    token = 'cda82ebbcda82ebbcda82ebb81cddf4348ccda8cda82ebbadd1a9349fc41858c53580e2'
    version = 5.21
    domain = 'stassatori89'
    all_posts = []
    for step in range(0, 1000, 100):
        response = requests.get('https://api.vk.com/method/wall.get', params={
            'access_token': token,
            'v': version,
            'domain': domain,
            'count': 100,
            'offset': step
        })
        data = response.json()['response']['items']
        all_posts.extend(data)
        time.sleep(.5)
        return all_posts


def data_writer(all_posts):
    with open('stas.csv', 'w', encoding='utf-8') as f:
        pen = csv.writer(f)
        pen.writerow(('likes', 'text', 'url'))

        for item in all_posts:
            likes_count = item['likes']['count']
            post_text = item['text']
            img_url = ''
            try:
                if item['attachments'][0]['type']:
                    img_url = item['attachments'][0]['photo']['photo_1280']
                else:
                    img_url = 'pass'
            except Exception as ex:
                pass

            pen.writerow((int(likes_count), post_text, img_url))


def sort_by_likes(file_name):
    reader = csv.reader(file_name)
    list = []
    next(reader)
    for file in reader:
        if len(file) != 0:
            new_item = {
                'likes': int(file[0]),
                'text': file[1]
            }
            list.append(new_item)

    res = sorted(list, key=lambda x: x['likes'], reverse=True)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # all_posts = get_response()
    # data_writer(all_posts)
    with open('stas.csv', 'r', encoding='utf-8') as f:
        sort_by_likes(f)
