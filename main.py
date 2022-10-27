import undetected_chromedriver
from bs4 import BeautifulSoup
import requests
import time
import os

MY_DEBUG = False

def main():
    driver = undetected_chromedriver.Chrome()
    print(driver)
    manga_url = input("Введіть URL манґи:")
    chapter_list_url = parsing_for_BS(get_manga_page(manga_url, driver))
    name = get_name(manga_url, driver)
    
    try:
        os.mkdir(name)
    except:
        print('Папка вже існує')

    i = 1
    for ch in chapter_list_url:
            path = os.path.join(name, str(i))
            try:
                os.mkdir(path)
            except:
                print('Папка вже існує')
            img_url = get_page_img_url(ch, driver)
            p = 1
            for img in img_url:
                ext = img.split(".")[-1]
                save_img(img, path, str(p) + '.' + ext, driver)
                time.sleep(0.5)
                p += 1
            p = 1
            i += 1
    driver.close()
    driver.quit()
    return print(manga_url)

def get_manga_page(url: str, driver):
    driver.get(url)
    time.sleep(1)
    page_raw = driver.page_source
    #driver.close()
    return page_raw

def get_name(url, driver):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    #driver.close()
    return soup.find(class_ = 'UAname').text


def parsing_for_BS(page_raw):
    soup_raw = BeautifulSoup(page_raw, 'lxml')
    ch_list = chapters_list(soup_raw)
    return ch_list

def chapters_list(page_raw):
    ch_list = []
    find_manga_chapters = page_raw.find_all(class_ = 'forfastnavigation')
    for ch_find in find_manga_chapters:
            ch_list.append(ch_find.get('href'))

    if MY_DEBUG:
        with open('debug_url.txt', 'w') as f:
            for line in ch_list:
                f.write(f'{line}\n')
    
    return ch_list

def get_page_img_url(ch_url, driver):
    img_url = []
    soup_raw = BeautifulSoup(get_manga_page(ch_url, driver), 'lxml')
    ul = soup_raw.find('ul', {'class': 'loadcomicsimages'})
    for li in ul.find_all('li'):
        img = li.find('img')
        img_url.append('https://manga.in.ua' + img.get('data-src'))

    if MY_DEBUG:
        with open('debug_page_url.txt', 'w') as f:
            for line in img_url:
                f.write(f'{line}\n')
    
    return img_url
def save_img(url_img, folder, file , driver):
    with open(folder+"/"+file, 'wb') as f:
        #driver.get(url_img)
        #res = driver.page_source
        res = requests.get(url_img).content
        #driver.close()
        f.write(res)





if __name__ == "__main__":
    main()