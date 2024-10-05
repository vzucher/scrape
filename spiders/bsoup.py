import requests
from bs4 import BeautifulSoup

# get the HTML content

url = "https://www.google.com/search?q=tattoo+artists+%22%40gmail.com%22+%22Brazil%22+site%3Ainstagram.com&sxsrf=AB5stBgqqB5FgT9F0GkwZ2oWusCJ1YcOcQ%3A1688918856776&ei=SNuqZIL4Ls6b1sQP5ZyziAg&ved=0ahUKEwiCvIyEgYKAAxXOjZUCHWXODIEQ4dUDCBA&uact=5&oq=tattoo+artists+%22%40gmail.com%22+%22Brazil%22+site%3Ainstagram.com&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQA0oECEEYAVAAWABgnQJoAXAAeACAAQCIAQCSAQCYAQDAAQE&sclient=gws-wiz-serp"
response = requests.get(url)
html_doc = response.text

# instantiate the soup object

soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.prettify())