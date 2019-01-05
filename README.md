# kindle-highlights
Scripts to share highlights in your kindle library in github pages

## How to build your own library
* this script requires selenium,chrome and chromedriver.

```
$ git clone https://github.com/umihico/kindle-highlights.git
$ git checkout gh-pages
$ python scraping.py
```

Then chrome will open and redirect to https://read.amazon.co.jp/notebook.  
Scraping will start after your logging in. Please type your e-mail and password.

```
$ python txt2md.py
```

Then import this local repository as yours in github.com!
