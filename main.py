import requests
import lxml.html as html
import os
import datetime


HOME_URL = 'https://www.larepublica.co/'
ARTICLE_LINK = '//div[contains(@class, "V")]/a[contains(@class, "kicker")]/@href'
TITLE = '//div[@class="mb-auto"]//span/text()'
ABSTRACT = '//div[@class="lead"]/p/text()'
CONTENT = '//div[@class="html-content"]/p/text()'


def parse_news(someLink, someDate):
    try: 
        response = requests.get(someLink)
        if response.status_code == 200:
            new = response.content.decode('utf-8')
            parsed = html.fromstring(new)
            try: 
                title = parsed.xpath(TITLE)[1]
                title = title.replace('\"', "")
                abstract = parsed.xpath(ABSTRACT)[0]
                content = parsed.xpath(CONTENT)
            except IndexError:
                return
            with open(f'{someDate}/{title}', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(abstract)
                f.write('\n\n')
                for p in content:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try: 
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            news_links = parsed.xpath(ARTICLE_LINK)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in news_links:
                parse_news(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve :
        print(ve)


def run():
    parse_home()


if __name__ == "__main__":
    run()