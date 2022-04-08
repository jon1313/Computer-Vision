import requests
from tqdm import tqdm


def hack(game_ids, level_keys, score):

    for game_id in tqdm(game_ids):

        cookies = {
            # 'sid': '',
            # '': '',
            # 'ag_user': '%40trollmannen',
            # 'ag_avatar': '',
            # 'ag_uid': '',
            # 'entity': '',
        }

        headers = {
            'Host': 'swag-services.addictinggames.com',
            # 'User-Agent': '',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://cdn2.addictinggames.com',
            'Referer': 'https://cdn2.addictinggames.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Gpc': '1',
            'Connection': 'close',
        }

        for level_key in level_keys:
            json_data = {
                'game': game_id,
                'level_key': level_key,
                'value': score,
            }

            response = requests.post('https://swag-services.addictinggames.com/v1/score',
                                     headers=headers, cookies=cookies, json=json_data, verify=False)

            print(game_id, level_key, score, '->', response)


if __name__ == '__main__':
    game_ids = []  # good luck
    level_keys = ['score', 'best_score']
    score = 1.797693134862315e+308
    hack(game_ids, level_keys, score)
