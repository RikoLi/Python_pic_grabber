import requests as rq
import re
'''用来扒百度图片'''
'''需要做连接超时错误捕捉与修正，使用try...except'''
'''正则表达式的写法要改进'''

# Get response
keyword = input('Input keyword to search: ')
keyword = str(keyword)
pages = input('How many pages do you want to search?(About 60p per-page): ')
pages = int(pages)
save_dir = input('Save to (Folder must exist!): ')
save_dir = str(save_dir)
print('Busy...')
url = 'http://image.baidu.com/search/flip'
page_index = 1
objURL_list = []
while page_index <= pages:
    # Create data pack
    data = {
        'tn': 'baiduimage',
        'word': keyword,
        'ie': 'utf-8',
        'pn': (page_index-1) * 20
    }
    try:
        # Get response
        response = rq.get(url, data, timeout=30)
        response.encoding = 'utf-8'
        # Match URLs
        match_pattern = r'"objURL":"([a-zA-Z0-9:_/.-]*)"'
        matcher = re.compile(match_pattern)
        objURL_list += matcher.findall(response.text)
    except rq.exceptions.ConnectionError as e:
        e_str = str(e)
        print('Error type: %s! Jump to next page!' %e_str)
    finally:
        page_index += 1    
print('---------------------------------')
print('Totally find %d pics!' %len(objURL_list))
print('---------------------------------')
# Save pics
print('Busy...')
img_counter = 0
for each in objURL_list:
    try:
        img_page = rq.get(each, timeout=30)
        with open('./catch_pics/'+save_dir+'/'+str(img_counter)+'.jpg', 'wb') as img:
            img.write(img_page.content)
        print(str(img_counter+1)+' of '+str(len(objURL_list))+' pics'+' are done!')
    except rq.exceptions.ConnectionError as e:
        e_str = str(e)
        print('Error type: %s! Jump to next image URL!' %e_str)
    finally:
        img_counter += 1
print('---------------------------------')
print('Done with %d pics!' %img_counter)