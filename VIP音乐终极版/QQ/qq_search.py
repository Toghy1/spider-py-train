import requests
import os

# 请求头通用配置
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# ====================== 1. QQ音乐 搜索+下载 ======================
def qq_music_search(keyword):
    """QQ音乐搜索歌曲"""
    url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
    params = {
        "w": keyword,
        "format": "json",
        "p": 1,
        "n": 10,
        "cr": 1
    }
    try:
        res = requests.get(url, params=params, headers=HEADERS, timeout=10)
        data = res.json()
        song_list = data["data"]["song"]["list"]
        result = []
        for idx, song in enumerate(song_list):
            name = song["songname"]
            singer = song["singer"][0]["name"]
            songmid = song["songmid"]
            print(f"【QQ音乐】{idx+1}. {name} - {singer} | MID:{songmid}")
            result.append({"name":name, "singer":singer, "mid":songmid})
        return result
    except Exception as e:
        print(f"QQ音乐搜索失败：{e}")
        return []

def qq_music_get_download_url(songmid):
    """获取QQ音乐下载链接"""
    api_url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
    post_data = {
        "req_0": {
            "module": "vkey.GetVkeyServer",
            "method": "CgiGetVkey",
            "param": {
                "guid": "1234567890",
                "songmid": [songmid],
                "songtype": [0],
                "uin": "0",
                "loginflag": 0,
                "platform": "20"
            }
        },
        "comm": {"format": "json", "ct": 24, "cv": 10000}
    }
    try:
        res = requests.post(api_url, json=post_data, headers=HEADERS, timeout=10)
        info = res.json()["req_0"]["data"]["midurlinfo"][0]
        purl = info["purl"]
        if not purl:
            return None
        return f"http://dl.stream.qqmusic.qq.com/{purl}"
    except:
        return None

# ====================== 2. 网易云音乐 搜索+下载 ======================
def wy_music_search(keyword):
    """网易云搜索歌曲"""
    url = "https://music.163.com/api/search/get/web"
    data = {"s": keyword, "type": 1, "limit": 10}
    try:
        res = requests.post(url, data=data, headers=HEADERS, timeout=10)
        data = res.json()
        song_list = data["result"]["songs"]
        result = []
        for idx, song in enumerate(song_list):
            name = song["name"]
            singer = "/".join([i["name"] for i in song["ar"]])
            sid = song["id"]
            print(f"【网易云】{idx+1}. {name} - {singer} | ID:{sid}")
            result.append({"name":name, "singer":singer, "sid":sid})
        return result
    except Exception as e:
        print(f"网易云搜索失败：{e}")
        return []

def wy_music_get_download_url(sid):
    """网易云获取播放下载链接"""
    url = f"https://music.163.com/song/media/outer/url?id={sid}.mp3"
    try:
        res = requests.get(url, headers=HEADERS, allow_redirects=False, timeout=10)
        if res.status_code == 302:
            return res.headers["Location"]
        return None
    except:
        return None

# ====================== 3. 咪咕音乐 搜索+下载 ======================
def migu_music_search(keyword):
    """咪咕音乐搜索"""
    base_url = f'https://c.musicapp.migu.cn/v1.0/content/search_all.do?text={keyword}&pageNo=1&pageSize=20&isCopyright=1&sort=1&searchSwitch=%7B%22song%22%3A1%2C%22album%22%3A0%2C%22singer%22%3A0%2C%22tagSong%22%3A1%2C%22mvSong%22%3A0%2C%22bestShow%22%3A1%7D'
    try:
        res = requests.get(base_url, headers=HEADERS, timeout=10)
        data = res.json()
        song_list = data.get("songData", [])
        result = []
        for idx, song in enumerate(song_list):
            name = song["songName"]
            singer = song["singerName"]
            songId = song["songId"]
            print(f"【咪咕音乐】{idx+1}. {name} - {singer} | ID:{songId}")
            result.append({"name":name, "singer":singer, "sid":songId, "songInfo":song})
        return result
    except Exception as e:
        print(f"咪咕搜索失败：{e}")
        return []

# ====================== 通用下载函数 ======================
def download_music(down_url, save_name):
    """通用音乐下载"""
    if not down_url:
        print("无有效下载链接，下载失败！")
        return False
    save_path = f"{save_name}.mp3"
    try:
        print(f"开始下载：{save_name}")
        stream = requests.get(down_url, stream=True, headers=HEADERS, timeout=15)
        total_size = int(stream.headers.get("content-length", 0))
        with open(save_path, "wb") as f:
            for chunk in stream.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"下载完成！保存路径：{os.path.abspath(save_path)}")
        return True
    except Exception as e:
        print(f"下载异常：{e}")
        return False

# ====================== 主程序入口 ======================
def main():
    print("===== 多平台音乐下载工具（仅学习使用）=====")
    print("1.QQ音乐  2.网易云音乐  3.咪咕音乐  0.退出")
    while True:
        try:
            choice = input("\n请选择平台序号：")
            if choice == "0":
                print("程序退出！")
                break
            song_name = input("请输入要搜索的歌曲名：").strip()
            if not song_name:
                continue

            if choice == "1":
                songs = qq_music_search(song_name)
                if not songs:continue
                num = int(input("输入序号下载："))-1
                if 0<=num<len(songs):
                    url = qq_music_get_download_url(songs[num]["mid"])
                    download_music(url, f'{songs[num]["name"]}-{songs[num]["singer"]}')

            elif choice == "2":
                songs = wy_music_search(song_name)
                if not songs:continue
                num = int(input("输入序号下载："))-1
                if 0<=num<len(songs):
                    url = wy_music_get_download_url(songs[num]["sid"])
                    download_music(url, f'{songs[num]["name"]}-{songs[num]["singer"]}')

            elif choice == "3":
                songs = migu_music_search(song_name)
                if not songs:continue
                num = int(input("输入序号下载："))-1
                if 0<=num<len(songs):
                    # 咪咕简易试听链接
                    info = songs[num]["songInfo"]
                    down_url = info.get("listenUrl", "")
                    download_music(down_url, f'{songs[num]["name"]}-{songs[num]["singer"]}')
            else:
                print("输入序号错误！")
        except:
            print("输入格式错误，请重新操作！")

if __name__ == "__main__":
    main()