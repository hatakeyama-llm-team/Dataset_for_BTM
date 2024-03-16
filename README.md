# 日本語のwebデータなどを統合するパイプラインのテスト

- とりあえず､畠山の方でBTMの練習が必要なので､たたき台のscriptを書いていきます｡

# Scripts
- [setup.sh](./setup.sh)
    - minicondaで環境構築するためのscript
- [0_download_dataset.py](./codes/0_download_dataset.py)
    - huggingfaceのdatasetsをdata folderにcacheとして保存しておきます for 高速処理
        - mc4, oscar, cc100, shisa
    - 1 TBくらいは容量を使うと思います｡