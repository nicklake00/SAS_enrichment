from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

def clear(line):
    line = re.sub(r'</div>', '', line)
    line = re.sub(r'<div>', '', line)
    line = re.sub(r'<br/>', '', line)
    line = re.sub(r'</a>', '', line)
    line = re.sub(r'<a href=', '', line)
    line = re.sub(r'<b>', '', line)
    line = re.sub(r'</b>', '', line)
    line = re.sub(r'title', '', line)
    line = re.sub(r'target', '', line)

    #cood = line.find('Верховный суд р')
    func = line.find('function')
    line = line[:func]
    line = line[5000:]
    return line

def get_html(url):
    response = requests.get(url)
    return response.text
 
def get_all_links(html): #, state, news):
    file = open("gasprom.txt", "w") # запись лога страницы в файл
    soup = BeautifulSoup(html, 'lxml')
    page = "https://sudact.ru/"
    nextpage = "https://sudact.ru/vsrf/doc/"

    # text = soup.find('div', id = 'docListContainer', class_ = 'h-col2-inner2')
    str_ = str(soup)
    a = [i for i in range(len(str_)) if str_.startswith('<a href', i)] #начало всех ссылок (доков на странице)
    b = [i for i in range(len(str_)) if str_.startswith('target', i)] #конец всех доков на странице

    for i in range(10): # 10 - максимум, если меньше, обработать исключением
        #print(str_[a[i]])
        newl = str(str_[a[i] + 12:b[i] - 2])
        newpage = str(page + newl)
        #print(newpage, '\n\n')

        document(get_html(newpage), file)
    return 0
    #print(str_)
    file.close()


def document(html, file):
    soup = BeautifulSoup(html, 'lxml')
    print(str(soup)[50:300])
    new_soup = clear(str(soup))
    file.write(str(new_soup))
    file.write("\n\n\n\n\n\n\n\n\n##############################\n\n\n\n\n\n\n")

 
def main():
    page0 = "https://sudact.ru/vsrf/doc_ajax/?"
    page1 = "vsrf-txt="

    page2 = "Газпром" #имя организации должно вводиться
    page3 = "&vsrf-case_doc=&vsrf-lawchunkinfo=&vsrf-doc_type=&vsrf-date_from=&vsrf-date_to=&vsrf-judge=#searchResult"
    #page = str(page0 + page1 + page2 + page3)

    page_next = "page="
    number = str(1) #номер страницы на которую хотим попасть, могут перечисляться
    page_next_again = "&vsrf-doc_type=&vsrf-judge=&vsrf-case_doc=&"

    for i in range(1, 5): #количество страниц, которые выдаются
        number = str(i);
        page = str(page0 + page_next + number + page_next_again + page1 + page2 + page3)
        all_links = get_all_links(get_html(page))

 
if __name__ == '__main__':
    main()

