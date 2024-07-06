import requests
from bs4 import BeautifulSoup

def get_text():

    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    url = "https://itvdn.com/ru/blog/article/interview-questions-python-developer"
    req = requests.get(url=url)
    soup = BeautifulSoup(req.text, "lxml")
    texts = soup.find("div", class_= "article-text dont-break-out base-font").find_all("p")

    res = [text.text.strip() for text in texts if text.text[0].isdigit()]

    for i in res:
        print(i)

def main():
    get_text()

if __name__ == "__main__":
    main()