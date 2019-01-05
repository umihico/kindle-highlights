---
layout: default
title: スマートPythonプログラミング: Pythonのより良い書き方を学ぶ by もみじあめ、Sonoko Asano
---

[![cover_img](http://images-jp.amazon.com/images/P/B01CX2AVUG.09.MZZZZZZZ.jpg)](https://www.amazon.co.jp/dp/B01CX2AVUG)  
## Author:もみじあめ、Sonoko Asano  
## Title:スマートPythonプログラミング: Pythonのより良い書き方を学ぶ  
## Last highlight:日曜日 5月 20, 2018,Total highlights:11  
```
  
@553  
pip install pudb  
  
@571  
pudb の最もシンプルな使い方は、普段スクリプトを実行するのに python コマンドを使っているところを、代わりに pudb (または pudb3) コマンドにするというものです。 $ pudb3 sample.py  
  
@594  
pudb のもうひとつの使い方は、既存のソースコードにブレークポイントとして動作するコードを挿入するというものです。 具体的には次のスニペットを使います。 from pudb import set_trace; set_trace()  
  
@640  
今から積極的に「%」演算子を使うことは避けたほうがよいでしょ  
  
@798  
外部からアクセスしてほしくないオブジェクトの名前には先頭にアンダースコアをつけ  
  
@833  
変更を許さない変数についてはクラスに部分的なサポートがあります。 これは @property  
  
@957  
実は docstring を書くときには慣例として """ を使うことになってい  
  
@967  
__doc__ という名前の特殊属性に格納され  
  
@970  
__doc__ に格納されている内容は組み込み関数 help() を使って読むことができ  
  
@979  
docstring は公開されているモジュール、関数、クラス、メソッドについてはすべて書くことが望ましいとされてい  
  
@2254  
この is 演算子は、左辺と右辺のオブジェクトが全く同じものかを比較するためのものです。 つまり、左辺と右辺のオブジェクトがメモリ上の同じ場所に配置されているかの比較になり  