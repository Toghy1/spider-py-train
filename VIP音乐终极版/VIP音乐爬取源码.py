import requests

while True:
    name = input('请输入歌曲的名称:')
    search_url = f'https://c.musicapp.migu.cn/v1.0/content/search_all.do?text={name}&pageNo=1&pageSize=20&isCopyright=1&sort=1&searchSwitch=%7B%22song%22%3A1%2C%22album%22%3A0%2C%22singer%22%3A0%2C%22tagSong%22%3A1%2C%22mvSong%22%3A0%2C%22bestShow%22%3A1%7D'
    search_res = requests.get(search_url)
    # 转化成JSON数据
    JSON = search_res.json()
    song_list = JSON['songResultData']['result']  # 这里面有8首歌曲！
    total_list = []
    count = 1
    for song_data in song_list:
        song_name = song_data['name']
        singers = song_data['singers'][0]['name']
        contentId = song_data['contentId']
        copyrightId = song_data['copyrightId']
        try:
            albumId = song_data['albums'][0]['id']
            albums_name = song_data['albums'][0]['name']
            list = [count,song_name,singers,albums_name,contentId,copyrightId,albumId]
        except:
            list = [count, song_name, singers, '0', contentId, copyrightId, '0']
        count += 1
        total_list.append(list)
    for li in total_list:
        print(li)

    choice = int(input("请输入您想要下载的歌曲的编号:"))-1
    url = f'https://c.musicapp.migu.cn/MIGUM3.0/strategy/listen-url/v2.3?copyrightId={total_list[choice][5]}&contentId={total_list[choice][4]}&resourceType=2&albumId={total_list[choice][-1]}&netType=01&toneFlag=PQ'
    headers = {'channel': '0140210'}
    res = requests.get(url, headers=headers)
    JSON1 = res.json()
    down_url = JSON1['data']['url']
    res1 = requests.get(down_url)
    open(f'{total_list[choice][1]}-{total_list[choice][2]}.mp3', 'wb').write(res1.content)
    print('已经下载好了！')













