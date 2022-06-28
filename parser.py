import requests
import json
import time
import csv

token = 'c00d6a6f2ecd014c7042c8e6c58007316c4ba42d5deaa5fa37bba526c332e6e274a3adf4271ff6b33d58e'



def test():
    
    groups_id = get_groups_info(5, 'цитаты', token)

    print(groups_id)


def get_groups_info(groups_count, search_request, token, filename=None):
    req = requests.get(f'https://api.vk.com/method/groups.search?q={search_request}&v=5.131&count={groups_count}&access_token={token}')

    #парсим список групп
    groups_id = [group['id'] for group in req.json()['response']['items']]
    
    groups_members = []
    #print(groups_id)
    for group_id in groups_id:
        req = requests.get(f'https://api.vk.com/method/groups.getById?group_id={group_id}&fields=members_count&v=5.131&count=50&access_token={token}')
        groups_members.append([group_id, req.json()['response'][0]['members_count'], req.json()['response'][0]['name']])
        time.sleep(0.34)
    
    if(filename):
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'followers', 'name'])
            #print(groups_members)
            writer.writerows(groups_members)

    return groups_id


def parse_data(search_request, groups_count, offsets_count, filename, flag='w'):
    
    groups_id = get_groups_info(groups_count, search_request, token, 'ff.csv')
    
    num = 0
    texts = []
    

    for i in range(0, len(groups_id)):
        print(f"Парсим группу № {i} с id = {groups_id[i]}")
        #print(texts)
        offset = 0

        for k in range(offsets_count): 
            print(f'Offset: {offset}')
            posts = requests.get(f'https://api.vk.com/method/wall.get?owner_id=-{groups_id[i]}&offset={offset}&count=100&v=5.131&access_token={token}').json()['response']['items']
            
            
            for post in posts:
                #print(post['text'])
                txt = post['text'].replace('\n',' ')
                #txt = post['text'].split('#')[0]
                #txt = txt.replace('\n', ' ')
                texts.append(['study', txt])
                            
            offset += 100

    #print(texts)

    if(filename):
        if flag == 'w':
            with open(filename, 'w', encoding='utf-16') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['category', 'text'])
                writer.writerows(texts)
        elif flag == 'a':
            with open(filename, 'a', encoding='utf-16') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(texts)



if __name__ == "__main__":

    parse_data('рэу', 1, 1, 'data_reu.csv', 'w')
    #test()
