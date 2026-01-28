# どうぶつしょうぎ

## ゲームの概要
3*4マスで動物の駒を操作して対戦を行う「どうぶつしょうぎ」を作成した。2人で行う通常対戦モードとGemini API(モデル：gemini-2.5-flash)を用いたAI対戦モードの計2つのゲームモードを用意した。

## 操作方法
`python3 main.py`でゲームを起動すると、AI対戦モードと2人で行う通常対戦モードを選択するタイトル画面が表示される。AI対戦モードを選択すると、ターミナル上でGemini APIキーの入力が求められる。APIキーを入力すると、対戦が開始される。通常対戦モードを選択すると、2人でそれぞれ操作を行い対戦することができる。どちらのモードでも先攻と後攻はランダムで決定され、マウスで駒をクリックすることでハイライト表示された移動可能な升目に駒を動かすことができる。

### 「どうぶつしょうぎ」のルールについて
【ルール】
1. プレイヤーは交互に自分の駒を動かします。
2. 移動した先に相手の駒があった場合はそれを盤上から取り除いて自分の駒にすることができ、次回以降の自分の順番の時に空いている場所に自分の駒としておくことができます。
3. 相手のライオンをとれば勝ちで、この勝ち方をキャッチといいます。
4. どうぶつしょうぎでは、自分のライオンを相手の一段目まで移動させることができても勝ちで、この勝ち方をトライといいます。

#### 参考
*   [日本将棋連盟 3×4マスなのに奥深い・・・子どもも遊べる「どうぶつしょうぎ」の遊び方と魅力について](https://www.shogi.or.jp/column/2016/11/post_43.html)

## 工夫した点
第一に、プログラムの拡張性と可読性を考え、機能ごとにファイルを分割した。メインの処理を行う`main.py`、盤面とゲームロジックを管理する`board.py`、AIとの通信を行う`gemini_manager.py`、タイトル画面を表示する`title_screen.py`、そして設定値をまとめた`config.py`に分けることで、役割を明確化することができた。特に`config.py`で定数を一元で管理したことにより、盤面の変更や調整を容易にした。おそらくは、このconfig.pyを中心に軽微な変更を加えることによって、どうぶつしょうぎだけではなく実際の将棋も実装することができるだろう。
次に、Gemini APIを用いたAI対戦の実装である。`board.py`内に`get_board_state_as_text`等のメソッドを作成し、盤面の状態（各マスの駒の配置、持ち駒、現在の手番）をテキスト形式で表現してプロンプトに含めることで状況を把握できるようにした。また、`get_legal_moves`メソッドでルール上可能な手をすべてリストとして提示することで、AIが反則をするリスクを低減させた。

## 苦労した点
特に苦労したのは、AIの応答をゲーム内での動作に反映させる処理である。Geminiはテキストで手を返してくるため、それをプログラムが解釈可能な形式に変換する必要があった。文字列を解析し実際に駒を移動させる処理の実装において、座標のずれやフォーマットの不一致によるエラーに対し、調整を繰り返した。生成AIを用いた対戦AIの実装においては、ミニマックス法等を用いた方が計算コストを考えると間違いなく効率的ではあるだろう。しかし、生成AIのAPIを用いることで授業内で扱ったような文字列の処理を発展させるだけでこのような対戦AIを即座に実装できる点は、手軽かつ強力であり評価できるポイントだろう。
また、持ち駒を盤面に打つ処理の実装にも手間取った。盤上の駒の移動とは異なり、持ち駒リストから削除して盤面に配置するという処理の流れを`_execute_drop`等のメソッドを用い、移動可能な空きマスの判定ロジックと組み合わせる点に時間を要した。

### pylintのエラーについて
授業資料内で紹介された『DOOM-style-Game』や[Pygameのリファレンス翻訳ページ](https://westplain.sakura.ne.jp/translate/pygame/)を参考に記した"pg.init()"等の記述で、どうしてもpylintエラーが表示されてしまった。以下にエラー内容を記載する。

```pylint ./main.py
$ pylint ./main.py 
************* Module main
main.py:23:4: E1101: Module 'pygame' has no 'init' member (no-member)
main.py:50:29: E1101: Module 'pygame' has no 'QUIT' member (no-member)
main.py:51:16: E1101: Module 'pygame' has no 'quit' member (no-member)
main.py:55:29: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
main.py:21:0: R0912: Too many branches (13/12) (too-many-branches)

------------------------------------------------------------------
Your code has been rated at 6.25/10 (previous run: 6.25/10, +0.00)
```

```pylint ./title_screen.py 
$ pylint ./title_screen.py 
************* Module title_screen
title_screen.py:5:19: C0303: Trailing whitespace (trailing-whitespace)
title_screen.py:77:33: E1101: Module 'pygame' has no 'QUIT' member (no-member)
title_screen.py:78:20: E1101: Module 'pygame' has no 'quit' member (no-member)
title_screen.py:81:33: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
title_screen.py:8:0: R0903: Too few public methods (1/2) (too-few-public-methods)

------------------------------------------------------------------
Your code has been rated at 7.02/10 (previous run: 7.02/10, +0.00)
```

[Stack OverflowのQuestionsの投稿](https://stackoverflow.com/questions/53012461/imports-failing-in-vscode-for-pylint-when-importing-pygame)にて、"For E1101: The problem is that most of Pygame is implemented in C directly. Now, this is all well and dandy in terms of performance, however, pylint (the linter used by VSCode) is unable to scan these C files. Unfortunately, these same files define a bunch of useful things, namely QUIT and other constants, such as MOUSEBUTTONDOWN, K_SPACE, etc, as well as functions like init or quit."と回答されており、PygameがC言語で直接書かれていること起因しておりパフォーマンスには影響がないとのことである。しかし、確かな情報を元にしたエラーの解決には至れなかった。