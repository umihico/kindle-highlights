import os
from umihico.io_ import load_from_txt
import re
import codecs


def gen_header(html_title):
    src = '''---
layout: default
title: html_title
---

'''
    return src.replace('html_title', html_title)


def _write_md(filename, md_text):
    with codecs.open(filename, 'w', 'utf-8', 'ignore')as f:
        f.write(md_text)


def _beautify_date(raw_date):
     # '水曜日 7月 15, 2015','2015年7月15日'

    nums = re.findall(r'[0-9]+', raw_date)
    # print(nums)
    if '年' in raw_date:
        return int(nums[0] + nums[1].zfill(2) + nums[2].zfill(2))
    else:
        return int(nums[2] + nums[0].zfill(2) + nums[1].zfill(2))


def _test_bautify_date():
    tests = ['水曜日 7月 15, 2015', '2015年7月15日']
    for test in tests:
        print(_beautify_date(test))


# _test_bautify_date()
# raise


def _gen_index(txt_dirname, filenames):
    asins_imgurls_dates = []
    dicts = [load_from_txt(txt_dirname + '/' + filename)
             for filename in filenames]
    dicts.sort(key=lambda d: _beautify_date(d['date']), reverse=True)
    md_text = gen_header("my kindle-highlights")
    md_text += "|book|date|\n"
    md_text += "|---|---|\n"
    for d in dicts:
        url = f"http://umihi.co/kindle-highlights/md/{d['asin']}.html"
        imgurl = d['amazon_image_url']
        image = f"[![]({imgurl})]({url})"
        date = _beautify_date(d['date'])
        title_author = d['booktitle'] + "\n" + d['author']
        md_text += f"|{image}|{date}|\n"
    _write_md('index.md', md_text)


def _each_txt2md(dirname, filename):
    # print(filename)
    d = load_from_txt(dirname + '/' + filename)
    # print(d.keys())
    asin = d['asin']
    amazon_url = d.get('amazon_url', "https://www.amazon.co.jp/dp/" + asin)
    amazon_image_url = d['amazon_image_url']
    author = d['author']
    # print(d)
    title = d['booktitle']
    date = d['date']
    highlights = d['highlights']
    cover = f"[![cover_img]({amazon_image_url})]({amazon_url})"
    md_texts = [cover + '  ']
    md_texts.append(f"## Author:{author}  ")
    md_texts.append(f"## Title:{title}  ")
    md_texts.append(
        f"## Last highlight:{date},Total highlights:{len(highlights)}  ")
    tupled_highlights = [x for x in highlights.items() if x[0] != '']
    md_texts.append('```')
    for page_pos, text in sorted(tupled_highlights, key=lambda x: int(x[0])):
        md_texts.append('  ')
        md_texts.append(f'@{page_pos}  ')
        md_texts.append('```')
        md_texts.append(f'> {text}  ')
        md_texts.append('```')
    md_text = gen_header(
        title + ' by ' + author)
    md_text += '\n'.join(md_texts)
    _write_md('md/' + filename.replace('.txt', '.md'), md_text)


def txt2md():
    txt_dirname = 'txt'
    filenames = os.listdir(txt_dirname)
    for filename in filenames:
        _each_txt2md(txt_dirname, filename)
    _gen_index(txt_dirname, filenames)


if __name__ == '__main__':
    txt2md()
