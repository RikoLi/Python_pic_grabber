import requests as rq
import re
import time
import os
'''未来考虑加入多关键词筛选'''

keyword = input('Search: ')
keyword = str(keyword)
pages = input('How many pages do you want to search?(About 20p per-page): ')
pages = int(pages)
url = 'https://danbooru.donmai.us/posts?tags='+keyword
page_index = 1
img_url = []
while page_index <= pages:
    # Create data pack
    data = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection':'keep-alive',
        'Host':'isshiki.donmai.us',
        'Origin':'https://danbooru.donmai.us',
        'Referer':'https://danbooru.donmai.us/posts?tags='+keyword,
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36',
        'page':page_index
    }
    try:
        # Get response
        res = rq.get(url, data, timeout=30)
        res.encoding = 'utf-8'
        # Match images
        match_patter = r'data-large-file-url="([a-zA-Z0-9_/:.-]*)"'
        matcher = re.compile(match_patter)
        img_url += matcher.findall(res.text)
        print('---------------------------------')
        print('Get page %d of %d!' %(page_index, pages))
        if page_index < pages:
            print('Next page starts in 3 secs...')
            time.sleep(3)
    except rq.exceptions.ConnectionError as e:
        e_str = str(e)
        print('Error type: %s! Jump to next page!' %e_str)
    finally:
        page_index += 1
print('Totally find %d pics!' %len(img_url))
print('---------------------------------')

# Create image folder
if not os.path.exists('./pic/'):
    os.mkdir('./pic/')

# Download pics
img_counter = 0
for each in img_url:
    try:
        img_page = rq.get(each, timeout=30)
        with open('./pic/'+str(img_counter)+'.jpg', 'wb') as img:
            img.write(img_page.content)
        print(str(img_counter+1)+' of '+str(len(img_url))+' pics'+' are done!')
    except rq.exceptions.ConnectionError as e:
        e_str = str(e)
        print('Error type: %s! Jump to next image URL!' %e_str)
    finally:
        img_counter += 1
print('---------------------------------')
print('Done with %d pics!' %img_counter)
os.system('pause')