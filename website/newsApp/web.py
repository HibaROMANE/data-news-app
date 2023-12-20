from bs4 import BeautifulSoup
import requests
from .models import article
from datetime import datetime
from django.db import IntegrityError

# Fonction pour transformer le format de date
# Du Francais en anglais exemple : 19 aout 2023 a August 19,2023
def transform_date_format(date_str):
    # Dictionnaire pour la conversion des mois
    month_conversion = {
        'janvier': 'January',
        'février': 'February',
        'mars': 'March',
        'avril': 'April',
        'mai': 'May',
        'juin': 'June',
        'juillet': 'July',
        'août': 'August',
        'septembre': 'September',
        'octobre': 'October',
        'novembre': 'November',
        'décembre': 'December'
    }
    for month_fr, month_en in month_conversion.items():
        if month_fr in date_str:
            date_str = date_str.replace(month_fr, month_en)
            break

    date = datetime.strptime(date_str, "%d %B %Y")
    transformed_date = date.strftime("%B %d, %Y")
    return transformed_date

# transformet la frome de la date de : Nov 18, 2021 en November 18, 2021
def transform_date(date_string):
    # Dictionnaire associant les abréviations des mois à leurs noms complets
    months = {
        'Jan': 'January',
        'Feb': 'February',
        'Mar': 'March',
        'Apr': 'April',
        'May': 'May',
        'Jun': 'June',
        'Jul': 'July',
        'Aug': 'August',
        'Sep': 'September',
        'Oct': 'October',
        'Nov': 'November',
        'Dec': 'December'
    }

    # Sépare la date en jour, mois et année
    parts = date_string.split(' ')
    month = months[parts[0]]
    day = parts[1].replace(',', '')
    year = parts[2]

    # Construit la nouvelle date au format "Month day, year"
    transformed_date = f"{month} {day}, {year}"

    return transformed_date


def site1():
    def get_article_info(article):
        title = article.find("h2").text.strip()
        article_url = base_url + article.find("a")["href"]
        paragraph = article.find("p").text.strip()
        date = article.find("time").text.strip()
        image = article.find('img')['src']
        date = transform_date(date)
        return title, article_url, paragraph, image, date

    def create_article_dict(article_info):
        title, article_url, paragraph, image, date = article_info
        article_dict = {
            "Title": title,
            "URL": article_url,
            "Paragraph": paragraph,
            "Image_URL": image,
            "Date": date

        }
        return article_dict

    def print_article_info(article_dict):
        print("Title:", article_dict["Title"])
        print("URL:", article_dict["URL"])
        print("Paragraph:", article_dict["Paragraph"])
        print("Image:", article_dict["Image_URL"])
        print("Date:", article_dict["Date"])
        print("---")

    base_url = "https://www.data-blogger.com"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all("article")

    article_list = []  # Liste pour stocker les dictionnaires d'informations des articles

    for article in articles:
        article_info = get_article_info(article)
        article_dict = create_article_dict(article_info)
        article_list.append(article_dict)

    # Afficher les informations des articles
    '''for article_dict in article_list:
        print_article_info(article_dict)
        print_article_info(article_dict)'''

    return article_list


def site2():
    def get_article_info(article):
        title = article.find("h2").text.strip()
        article_url = base_url + article.find("h2").find("a")["href"]
        paragraph = article.find("p").text.strip()
        image_element = article.find("img")
        image_url = base_url + image_element["data-background-src"] if image_element else ""
        date = article.find("span", {"class": "timestamp"}).text.strip()
        return title, article_url, paragraph, image_url, date

    def create_article_dict(article_info):
        title, article_url, paragraph, image_url, date = article_info
        article_dict = {
            "Title": title,
            "URL": article_url,
            "Paragraph": paragraph,
            "Image_URL": image_url,
            "Date": date
        }
        return article_dict

    def print_article_info(article_dict):
        print("Title:", article_dict["Title"])
        print("URL:", article_dict["URL"])
        print("Paragraph:", article_dict["Paragraph"])
        print("Image_URL:", article_dict["Image_URL"])
        print("Date:", article_dict["Date"])
        print("---")

    base_url = "https://engineering.linkedin.com"
    initial_url = base_url + "/blog/topic/data-science"

    response = requests.get(initial_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all("li", {'class': 'post-li'})
    article_list = []  # Liste pour stocker les dictionnaires d'informations des articles

    for article in articles:
        article_info = get_article_info(article)
        article_dict = create_article_dict(article_info)
        article_list.append(article_dict)

    # Afficher les informations des articles
    '''for article_dict in article_list:
        print_article_info(article_dict)'''
    return article_list


def site3():
    def get_article_info(article):
        title = article.find("h2").text.strip()
        article_url = article.find("h2").find("a")["href"]
        paragraph = article.find("p").text.strip()
        image_element = article.find(class_='post-background-image')
        image_url = image_element['data-bg']
        return title, article_url, paragraph, image_url

    def create_article_dict(article_info):
        title, article_url, paragraph, image_url = article_info
        article_dict = {
            "Title": title,
            "URL": article_url,
            "Paragraph": paragraph,
            "Image_URL": image_url
        }
        return article_dict

    def get_article_date(article_url):
        response = requests.get(article_url)
        article_soup = BeautifulSoup(response.text, 'html.parser')
        date_element = article_soup.find('span', class_='tie-date')
        date = date_element.text.strip()
        # Transforme la date dans le nouveau format
        transformed_date = transform_date_format(date)

        return transformed_date

    def print_article_info(article_dict):
        print("Title:", article_dict["Title"])
        print("URL:", article_dict["URL"])
        print("Paragraph:", article_dict["Paragraph"])
        print("Image:", article_dict["Image_URL"])
        print("Date:", article_dict["Date"])
        print("---")

    base_url = "https://www.lebigdata.fr/intelligence-artificielle"

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all("article")

    article_list = []  # Liste pour stocker les dictionnaires d'informations des articles

    for article in articles:
        article_info = get_article_info(article)
        article_dict = create_article_dict(article_info)
        article_list.append(article_dict)

    for article_dict in article_list:
        article_url = article_dict["URL"]
        date = get_article_date(article_url)
        article_dict["Date"] = date

    # Afficher les informations des articles avec la date
    '''for article_dict in article_list:
        print_article_info(article_dict)'''

    return article_list


def site4():
    def get_article_info(article):
        title = article.find("h2").text.strip()
        article_url = article.find("h2").find("a")["href"]
        paragraph = article.find("div", {"class": "clz-post-text"}).text.strip()
        date = article.find("div", {"class": "clz-post-date"}).text.strip()
        image_element = article.find("img")["src"]
        date = transform_date_format(date)
        return title, article_url, paragraph, image_element, date

    def create_article_dict(article_info):
        title, article_url, paragraph, image, date = article_info
        article_dict = {
            "Title": title,
            "URL": article_url,
            "Paragraph": paragraph,
            "Image_URL": image,
            "Date": date

        }
        return article_dict

    def print_article_info(article_dict):
        print("Title:", article_dict["Title"])
        print("URL:", article_dict["URL"])
        print("Paragraph:", article_dict["Paragraph"])
        print("Image:", article_dict["Image_URL"])
        print("Date:", article_dict["Date"])
        print("---")

    base_url = "https://blog.cellenza.com/articles/data/"

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all("article")

    article_list = []  # Liste pour stocker les dictionnaires d'informations des articles

    for article in articles:
        article_info = get_article_info(article)
        article_dict = create_article_dict(article_info)
        article_list.append(article_dict)

    # Afficher les informations des articles
    '''for article_dict in article_list:
        print_article_info(article_dict)'''

    return article_list


def site5():
    def get_article_info(article):
        title = article.find("h3").text.strip()
        article_url = article.find("a")["href"]
        paragraph = article.find("div", {"class": "content-m"}).text.strip()
        image_element = article.find("img")
        image_url = image_element["src"] if image_element else ""
        date_element = article.find('span', class_='post-published-date content-s')
        date = date_element.text.strip()
        date = transform_date(date)
        return title, article_url, paragraph, image_url, date

    def create_article_dict(article_info):
        title, article_url, paragraph, image_url, date = article_info
        article_dict = {
            "Title": title,
            "URL": article_url,
            "Paragraph": paragraph,
            "Image_URL": image_url,
            "Date": date
        }
        return article_dict

    def print_article_info(article_dict):
        print("Title:", article_dict["Title"])
        print("URL:", article_dict["URL"])
        print("Paragraph:", article_dict["Paragraph"])
        print("Image:", article_dict["Image_URL"])
        print("Date:", article_dict["Date"])
        print("---")

    base_url = "https://developer.nvidia.com/blog/recent-posts/"

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all("div", {"class": "carousel-row-slide__inner"})

    article_list = []  # Liste pour stocker les dictionnaires d'informations des articles

    for article in articles:
        article_info = get_article_info(article)
        article_dict = create_article_dict(article_info)
        article_list.append(article_dict)

    # Afficher les informations des articles
    '''for article_dict in article_list:
        print_article_info(article_dict)'''

    return article_list


def main():
    MonsiteArticles =  site1()+site2()+site3()+site4()+site5()
    MonsiteArticles_tries = sorted(MonsiteArticles,
                                   key=lambda x: datetime.strptime(x['Date'],
                                                                   "%B %d, %Y"),
                                   reverse=True)
    for art in MonsiteArticles_tries:
        #print(article)
        try:
            article.objects.get(Title=art["Title"], URL=art["URL"])
            # L'article existe déjà dans la base de données
            continue  # Passe à l'article suivant
        except article.DoesNotExist:
            new_article = article(
                Title=art["Title"],
                URL=art["URL"],
                Paragraph=art["Paragraph"],
                Image_URL=art["Image_URL"],
                Date=art["Date"]
            )
            try:
                new_article.save()
            except IntegrityError:
                pass
    #article_list = MonsiteArticles_tries
    #return article_list


if __name__ == "__main__":
    main()

