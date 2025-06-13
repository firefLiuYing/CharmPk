import requests

headers = {
    'Host':'image.baidu.com',
    'Referer':'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=&st=-1&fm=index&fr=&hs=0&xthttps=111110&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E5%90%B9%E5%93%8D%E5%90%A7%E4%B8%8A%E4%BD%8E%E9%9F%B3%E5%8F%B7',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Cookie':'BAIDUID=287C03BCFF4AC9930B412AB16EA64E1E:FG=1; indexPageSugList=%5B%22%E5%B0%96%E9%94%90%E7%9F%B3%E5%A4%B4%22%2C%22%E4%B8%89%E5%8F%89%E6%88%9F%22%2C%22%E6%B5%AA%E6%BD%AE%22%2C%22%E6%B0%B4%E7%AE%AD%22%2C%22%E6%B8%B8%E6%88%8F%E7%80%91%E5%B8%83%E5%9B%BE%E7%89%87%22%2C%22%E7%80%91%E5%B8%83%E5%9B%BE%E7%89%87%22%2C%22%E8%B5%AB%E6%8B%89%E5%85%8B%E5%8B%92%E6%96%AF%E7%9A%84%E8%8B%B1%E6%96%87%22%2C%22%E9%87%91%E5%B1%9E%E5%9B%B4%E6%A0%8F%E5%9B%BE%E7%89%87%22%2C%22%E8%A5%BF%E5%BC%8F%E9%95%BF%E7%9F%9B%E5%9B%BE%E7%89%87%22%5D; PSTM=1721629734; BIDUPSID=E121D5A086976E7EB27F7F6FCD2C06F9; BDUSS=2dafjRqQzl2WWNqOVkwNi10MnpmV29wMW1SbU5-cGd4STNRTlRwYXVFVHo3a0ZuRVFBQUFBJCQAAAAAAAAAAAEAAAAyYjfwz8i80r7At9e1yMvAsKEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPNhGmfzYRpnQ; BDUSS_BFESS=2dafjRqQzl2WWNqOVkwNi10MnpmV29wMW1SbU5-cGd4STNRTlRwYXVFVHo3a0ZuRVFBQUFBJCQAAAAAAAAAAAEAAAAyYjfwz8i80r7At9e1yMvAsKEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPNhGmfzYRpnQ; H_WISE_SIDS_BFESS=61027_61801_61987; MAWEBCUID=web_bHRkczvMrbaSvWyVnyRmHOoLOTUuOGhXGLUgWGvmMSUZtdWXKq; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=62325_63147_63241_63324_63392_63401_63440_63506_63502_63527_63538_63567_63564_63582_63578; BAIDUID_BFESS=287C03BCFF4AC9930B412AB16EA64E1E:FG=1; H_WISE_SIDS=62325_63241_63440_63506_63564_63582_63578; ab_sr=1.0.1_ZWQ4OGFjZDRlZTk1MjFkYjk5OTc0ZTEzNDA3MTQyMjk3ZGE2ZDVlOTBhNjc1NTc4MWIxOTYyNWY1MjAwZjY0ZWMyNTIxMmE3YjVhNTEyYWM3MTIwYzQxYjRhMWUxMWIwZWVhNmVjMTRlYTFlOWUwODg4NjllNmQxMzY2M2E1YWRlYmUxYjVjMmI1MGJlNzg2ZmU2NDYxZGNiNzBmYzM5Ng=='
}

number = 1

for page in range(1,11):
    url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&word=%E5%90%B9%E5%93%8D%E5%90%A7%E4%B8%8A%E4%BD%8E%E9%9F%B3%E5%8F%B7&ie=utf-8&fp=result&fr=&ala=0&applid=10584219833264956580&pn={30 * page}&rn=30&nojc=0&gsm=78&newReq=1'
    response = requests.get(url = url,headers = headers)
    json_data = response.json()
    # print(number,"   ")
    # print(json_data,"\n")

    data_list = json_data['data']

    for data in data_list:
        images = data[7]
        for image in images:
            for num in range(0,29):
                img_data = image[num]['thumburl'].content
                with open(f'image/{number}.jpg', 'wb') as f:
                    f.write(img_data)
                number += 1

