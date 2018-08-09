import requests as rq
import re
import time
import os
'''未来考虑加入多关键词筛选'''

keyword = input('Safebooru Search: ')
keyword = str(keyword)
pages = input('How many pages do you want to search?(About 40p per-page): ')
pages = int(pages)
folder_name = input('Save to: ')
folder_name = str(folder_name)
url = 'http://safebooru.org/index.php?page=post&s=list'
page_index = 1
img_url = []
while page_index <= pages:
    # Create data pack
    data = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection':'keep-alive',
        'Host':'safebooru.org',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36',
        'page':'post',
        's':'list',
        'tags':keyword,
        'pid':(page_index-1)*40
    }
    try:
        # Get response
        res = rq.get(url, data, timeout=30)
        res.encoding = 'utf-8'
        # Match images
        match_patter = r'src="//safebooru.org/thumbnails/([a-zA-Z0-9_/:.-?]*)"'
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

# Preprocessing of pic URLs
new_img_url = []
for each in img_url:
    new_each = each.replace('thumbnail', 'sample')
    new_each = 'http://safebooru.org//samples/' + new_each
    new_img_url.append(new_each)

# Create image folder
if not os.path.exists('./'+folder_name+'/'):
    os.mkdir('./'+folder_name+'/')

# Download pics
img_counter = 0
for each in new_img_url:
    try:
        img_page = rq.get(each, timeout=30)
        if img_page.status_code == 404: # Check URL's validation for pics in safebooru
            new_url = each.replace('sample_', '')
            new_url = new_url.replace('samples', 'images')
            img_page = rq.get(new_url, timeout=30)
        with open('./'+folder_name+'/'+str(img_counter)+'.jpg', 'wb') as img:
            img.write(img_page.content)
        print(str(img_counter+1)+' of '+str(len(new_img_url))+' pics'+' are done!')
    except rq.exceptions.ConnectionError as e:
        e_str = str(e)
        print('Error type: %s! Jump to next image URL!' %e_str)
    finally:
        img_counter += 1
print('---------------------------------')
print('Done with %d pics!' %img_counter)
os.system('pause')