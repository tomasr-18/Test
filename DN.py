from bs4 import BeautifulSoup
import requests
import datetime
import webbrowser as wb


def scrape_dn():
    # Hämtar hemsidan
    url = 'https://dn.se'
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    # Plockar ut den del av sidan som ska skrapas
    a = soup.select(
        'div.ds-teaser-list-vertical__content')
    nyheter = a[0].select('a,href')

    # Plockar ut länkarna och rubrikerna
    # link_str = nyheter[0].get('href')
    rubrik = nyheter[0].get('data-label')

    return nyheter, rubrik

# Packeterar output i lista innehållande dicts med rubrik:länk


def get_latest_news(nyheter, rubrik) -> list:
    news_list = []
    for i in range(len(nyheter)):
        link = nyheter[i].get('href')
        rubrik = nyheter[i].get('data-label')
        news_list.append({rubrik: 'https://dn.se'+link})
    return news_list


def print_news(news_list):
    print(f'Senaste nytt {datetime.datetime.now()}')
    for index, i in enumerate(news_list):
        for items in i:
            print(f'{index+1} - {items}')


def get_link(news_list, index) -> str:
    link = news_list[index-1]
    for rubrik, url in link.items():
        return url


def open_url_in_browser(url, news_list, usr_input, browser='chrome'):
    url = get_link(news_list, usr_input)
    browser = wb.get(browser)
    browser.open(url)


def usr_input():
    while True:
        usr_input = input(
            'Välj en nyhet (1-20) för att öppna i webbläsare. Tryck enter för att avsluta ')
        if usr_input == '':
            return False
        try:
            usr_input = int(usr_input)
        except:
            print('Ange ett heltal mellan 1-20')
        else:
            if usr_input > 0 and usr_input < 21:
                return usr_input
            else:
                print('Felaktigt värde, ange ett tal mellan 1-20')


def main(url='https://dn.se'):
    nyheter, rubrik = scrape_dn()
    news_list = get_latest_news(nyheter, rubrik)
    print_news(news_list)
    while True:
        usr_input_index = usr_input()
        if usr_input_index is False:
            break
        else:
            print('Öppnar webläsaren')
            open_url_in_browser(url, news_list, usr_input_index)


if __name__ == '__main__':
    main()
