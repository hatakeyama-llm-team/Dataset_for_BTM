# https://github.com/lighttransport/japanese-llama-experiment/blob/main/03_clean_step1/clean_text.py

# TODO: hard codeしない

import unicodedata
import re
broken_sentence_endings = """
...
... 
...　
\"
'
[…]
詳細を見る
すべて表示する
するまとめ
にアクセス!
お​問​い​合​わ​せ​
アクセスマップ
送料無料!
お問い合わせ
,?
周辺施設
続きを表示
音楽出版社求人
Check
マップMAP
未入力項目があります
SNS
●facebook→
●twitter→
ABOUT US
求人情報
1件中1～1件を表示
事業内容
トップページ
特集
賃貸情報
条件を選ぶ
現在の選択エリア
沿線から選ぶ
エリアを選びなおす
さらにエリアを絞る
△ページTOP
公式
About
search
プロフィール
更新情報をチェックする
検索:
関連記事
ブックマークする
友達に教える
お問い合せ
CLOSE
My account
Contact Us
ご利用方法
会員規約
特定商取引法に基づく表記
組織概要
<前の20件1次の20件>
官公庁臨時職員
湘南国際村仕事
タイアップ広告掲載
広告を掲載しませんか?
会社概要
Pocket
目次
TOP
から見つける
プライバシーポリシー
利用規約
All Rights Reserved.
スタッフブログ
賃貸ホームページ
物件カタログ
ホーム
メニュー
仲介手数料最大無料
口コミをもっと
詳細情報
ツイート
メルマガ
登録商標です。
ようこそゲストさん
→
[...]
の先頭へ
個人情報の取り扱いについて
中古マンション
»
パスワードをお忘れの方
上部へ
JavaScriptを有効にしてご利用下さい.
ログインできない時は?
運営会社
企業情報
問い合わせ
一覧へ
ヘルプ
物件
もっと見る
を探す
マンション
検索
店
検索のヒント:
新規の表示
Vths
Id
見出し語
Yomi
大分類1
小分類2
Pos
Actions
メールアドレス
パスワード
次回から自動ログインをする
パスワードを忘れた方はこちら
不動産無料査定
住まい紹介ブログ
🗣naamal
⋆。* ⋆。* ⋆
122投稿
サイトは?
トップ
ニュース
日程
著作権
記事・写真・動画の利用申込
採用情報
サイト一覧
関連情報
の投稿
ページトップへ
記事を読む
運営者情報
Twitter公式
もっとみる
投稿する
店舗TOP
スタッフ・開発者募集
ヘルプページ
最近のコメント
カレンダー
の情報:
の情報
いいね
キャンペーン
|BOOKED
HOME
よくある質問
BLOG
...
問い合わせください。
休診日
木曜日・日曜日・祝日
all rights reserved.
</tr>
</div>
浮気調査
カテゴリー
お知らせ
新着アイテム
アーカイブ
月
Search
TOPへ
TOPページへ
Menu
Return Top
携帯版はこちら
会社情報
初めての方へ
ダウンロード
アクセス
IR情報
一覧
採用サイト
マイページ
研究会会員
専用ページ
はこちら
相談する
相談
探す
事例を見る
お客様からの声(成功事例)
書籍
メタ情報
の詳細
Home
ログイン
投稿フィード
コメントフィード
船井総研のサービス
お客様からの声(成功事例)
レポート
サービス
船井総研のサービス概要
セミナー
経営研究会
コンサルティング
業種・テーマ
住宅・不動産
リフォーム
不動産
賃貸
建設
病院・クリニック
歯科医院
特定商取引法
はじめてお越しの方へ
LINE
menu
免責事項
閉じる
読者になる
リンク
Tweet
方法はコチラ
トップへ戻る
[ヘルプ]
のプロフィール
ランキング】
更新しました
アーカイヴ
未分類
お問合せ
シェア
[お問い合わせ]
[利用規約]
[個人情報保護方針]
/RSS
もっと読む
の検索結果
通販ショップ
フォローする
シェアする
MENU
このブログについて
コメントを書く
twitter
facebook
line
コメント
arrowup
読まれている記事
のビュー
質問箱
コメントをキャンセル
down
Website
more
Name
Email
home
新着情報
First
のQ&A
サイトへ
Previous
上へ
更新
Twitter
拡大
ランキング
Next
会員登録
Last
スタッフ紹介
1階層ページ
タイトル
この記事を削除する
2階層ページ
サイド見出し
送信する
イメージナビ
お客様の声・対策事例
ページ次のページ »
こちらから
役立つ文例集
お客様の声
個人情報保護ポリシー
特定商取引について
必須お名前
申込
フォーム
FAQ
電話する
ページ先頭へ
送信する
天気予報
ロフィールを表示
リンク集
上部へ戻る
へスキップ
Category
ご質問
ヤミ金の電話番号
最新記事
インフォメーション
コラム
事務所案内
サービス料金
リストナビ
掲示板BBS
地図ページ
メールフォーム
ケータイサイト
サンプルです
これはテストです
ホーム>
"""

broken_ending_list = broken_sentence_endings.split("\n")
broken_ending_list = [x for x in broken_ending_list if len(x) > 0]

broken_ending_list += [
    '続きを読む', '[続きを読む]', '(続きを読む)', '続きを見る', '続きをみる', '(続く)', '(続きを表示)', '(続きをみる)', '[続きをみる]', '[続きを見る]',
]
broken_ending_list += ['...(続きを表示)', '[ 続きを見る ]',
                       '・・・続きを見る', '... 続きを読む',
                       "詳細はこちら »",
                       "詳細>>>",
                       "サイトマップ",
                       ]


noise_mid_list = """
Copyright(C)
デジタル広告ガイド
Copyright
HOME>
新聞広告ガイド
©
無断転載を禁止します
著作権
記事・写真・動画の利用申込
採用情報
Copyright © 
Copyright 
"""
noise_mid_list = noise_mid_list.split("\n")
noise_mid_list = [x for x in noise_mid_list if len(x) > 0]


def clean(sent: str):
    for broken_ending in broken_ending_list:
        # print("aa", broken_ending)
        if sent.endswith(broken_ending):
            return None
        if len(sent) < 2:
            return None

    for noise_mid in noise_mid_list:
        if noise_mid in sent:
            return None
    return sent
