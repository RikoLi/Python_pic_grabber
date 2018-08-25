import requests as rq
import getpass
import os
import re
import time

'''接下来要适配中文搜索'''

def login(username, password):
    # Create headers
    headers = {
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, sdch, b',
        'accept-language':'zh-CN,zh;q=0.8,en;q=0.6',
        'referer':'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
        'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36'
    }
    # Simulate login
    url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
    res = rq.get(url, headers)
    # Find postkey
    pattern = r'"pixivAccount.postKey":"([0-9a-z]*)"'
    matcher = re.compile(pattern)
    postkey = (matcher.findall(res.text))[0]
    # Create POST data pack
    data = {
        'pixiv_id':username,
        'captcha':'',
        'g_recaptcha_response':'',
        'password':password,
        'post_key':postkey,
        'source':'pc',
        'ref':'wwwtop_accounts_index',
        'return_to':'https://www.pixiv.net/'
    }
    # Post login request
    res = rq.post(url, headers=headers, data=data)
    res.encoding = 'utf-8'
    return res

def searchPics(keyword, page_num, headers):
    #获取插图详细页列表
    pattern = r'/360x360_10_webp/img-master/img/([0-9a-z/_]*.[a-z]*)'
    matcher = re.compile(pattern)
    img_url_list = []
    for i in range(1, page_num+1):
        url = 'https://www.pixiv.net/search.php?s_mode=s_tag&word=' + keyword + '&order=date_d&p=' + str(i)
        res = rq.get(url, headers=headers)  
        #写临时文件，解决content直接加载不全的问题
        with open('temp.txt', 'wb') as f:
            f.write(res.content)
        with open('temp.txt', 'rb') as f:
            temp_html = f.read().decode()
        img_list = matcher.findall(temp_html)
        for each in img_list:
            temp = each.replace('_square1200', '')
            img_url_list.append('https://i.pximg.net/img-original/img/'+temp)
        time.sleep(1)
    print('Get', len(img_url_list), 'URLs!')
    return img_url_list

def download(img_url_list, pid_list, filename):
    headers = {
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, sdch, b',
        'accept-language':'zh-CN,zh;q=0.8,en;q=0.6',
        'referer':'',
        'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36'
    }
    # Download pics
    if os.path.exists('./'+filename+'/num'):
        with open('./'+filename+'/num', 'r') as f:
            continue_num = int(f.read())
    else:
        continue_num = 0
    pic_num = 0
    for each in img_url_list:
        headers['referer'] = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + pid_list[pic_num]
        res = rq.get(each, headers=headers)
        if res.status_code != 200:
            temp = each.replace('.jpg', '.png')
            res = rq.get(temp, headers=headers)
        # 写入文件
        with open('./'+filename+'/'+str(pic_num+continue_num)+'.jpg', 'wb') as f:
            f.write(res.content)
        print(pic_num+1, '/', len(img_url_list), 'are done!')
        pic_num += 1
    os.remove('./temp.txt')
    with open('./'+filename+'/num', 'w') as f:
        f.write(str(pic_num+continue_num))
    print('All done!')

# Login guide
print('---Sign in Pixiv---')
username = str(input('Username: '))
password = getpass.getpass('Password(invisible): ')

# Simulate login
res = login(username, password)
if res.status_code == 200:
    print('Login successfully!')
    print('-------------------')
    
    while True:
        # Search settings
        keyword = str(input('Search(ENG and Num only): '))
        page_num = int(input('To page: '))
        filename = str(input('Save to: '))
        headers = {
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, sdch, b',
            'accept-language':'zh-CN,zh;q=0.8,en;q=0.6',
            'referer':'https://www.pixiv.net/search.php?s_mode=s_tag&word=' + keyword,
            'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36'
        }
        img_url_list = searchPics(keyword, page_num, headers)

        # Create folder
        if not os.path.exists('./'+filename+'/'):
            os.mkdir('./'+filename+'/')
        
        # Extract PixivID
        pattern = r'/([0-9]*)[_|.]'
        matcher = re.compile(pattern)
        pid_list = []
        for each in img_url_list:
            temp = matcher.findall(each)
            pid_list.append(temp[0])
        with open('./'+filename+'/pid_list.txt', 'a') as f:
            for each in pid_list:
                f.write(each+'\n')

        # Download pics
        download(img_url_list, pid_list, filename)
else:
    print('Login failed!')
    os.system('pause')
    