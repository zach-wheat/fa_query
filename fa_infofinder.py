import requests
from bs4 import BeautifulSoup
from sub_pages import subpage_query


def main():
    
    """prints link to each advisor's webpage and builds an email address"""
    
    landingpage_query()
    names = get_name()
    urls = get_url()

    for i in range(len(names)):
        # ^ used as delimiter
        print(urls[i] + ' ^ ' + names[i].split()[0] + '.' + names[i].split()[-1] + '@xyz.com')
    return


def landingpage_query(attempts=3):
    
    """retrieves div elem containing webpage links and names for all financial advisors and saves them to a file in file_path specified"""

    url = 'https://www.xyz.com/department/financial-advisors/'
    file_path = 'filepath'

    headers = {'user-agent':
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
               'AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/95.0.4638.54 Safari/537.36'}

    while attempts != 0:
        try:
            r = requests.get(url, headers=headers, timeout=15)
            attempts = 0
        except Exception as Ex:
            print(f'Error when retrieving data: {Ex}')
            attempts -= 1
            print(f'Trying again. Number of attempts remaining: {attempts}')

    soup = BeautifulSoup(r.content, 'html.parser')
    advisors = soup.findAll('div', class_='container')
    
    with open(file_path, 'w') as file:
        file.write(str(advisors))
    
    return


def get_name():

    """reads data from file_path and extracts each advisor's name"""

    file_path = 'filepath'
    
    with open(file_path, 'r') as file:
        soup = BeautifulSoup(file.read(), features="html.parser")
        advisors = soup.findAll('div', class_='name-title')
        names = []
        for fa in advisors:
            names.append(fa.find('h4').text.split(',')[0])
    return names


def get_url():

    """reads data from file_path and extracts the link to each advisor's webpage"""

    file_path = 'filepath'

    with open(file_path, 'r') as file:
        soup = BeautifulSoup(file.read(), features="html.parser")
        advisors = soup.findAll('a', class_='btn adv-btn')
        urls = []
        for fa in advisors:
            urls.append(fa.get('href'))
    return urls


if __name__ == "__main__":
    main()
