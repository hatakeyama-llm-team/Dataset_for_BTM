# https://github.com/lighttransport/japanese-llama-experiment/blob/main/03_clean_step1/clean_text.py

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
アクセスマップ
お問い合わせ
周辺施設
会社概要
プライバシーポリシー
利用規約
All Rights Reserved.
スタッフブログ
賃貸ホームページ
物件カタログ
ホーム
メニュー
仲介手数料最大無料
詳細情報
ようこそゲストさん
中古マンション
一覧へ
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
[お問い合わせ]
[利用規約]
[個人情報保護方針]
/RSS
もっと読む
コメントを書く
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
新聞広告ガイド
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
