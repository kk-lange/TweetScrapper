from TweetScrapper import scrapper


url = "https://twitter.com/OculusSupport"

posts = scrapper(url)

for i in posts:
    print(i["date"])

