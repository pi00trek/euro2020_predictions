from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re

# GETTING ALL MATCH LINKS
url = 'https://www.betclic.pl/pilka-nozna-s1/euro-2020-c122'

source = requests.get(url)

soup = BeautifulSoup(source.text, 'lxml')


game_links = []
for i in soup.find_all('a'):
    link = i.get('href')
    if link is not None:
        if '/euro-2020' in link:
            game_links.append(link)
# print(game_links)

game_url = urljoin('https://www.betclic.pl', game_links[5])

# print(game_url)

# ITERATING OVER PAGES AND GETTING PREDICTIONS
for game in game_links[:3]:


    game_url = urljoin('https://www.betclic.pl', game)
    print(game_url)

    source = requests.get(game_url)

    soup = BeautifulSoup(source.text, 'lxml')

    # too many -> 9 big boxes
    # for i in soup.find_all('div', 'marketBox is-table ng-star-inserted'):
    for i in soup.find_all('h2', 'marketBox_headTitle'):

        # print(i.prettify())
        if i.text.strip() == 'Dokładny wynik':
            results_odds_section = i.parent.parent
            scores_list = [i.text for i in results_odds_section.find_all('p')]
            odds_list = [float(i.text.replace(',', '.')) for i in results_odds_section.find_all('span') if bool(re.search('\d', i.text))]

            score_odds_list = [i for i in zip(scores_list, odds_list)]

    print(score_odds_list)
    base_odds_for_comparison = 999
    most_prob_result = ''
    for i, j in score_odds_list:
        if j < base_odds_for_comparison:
            most_prob_result = i
            base_odds_for_comparison = j

    print(f'Mój typ: {most_prob_result}')
    print('-----------')
