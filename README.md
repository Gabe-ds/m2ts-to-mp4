# m2ts-to-mp4

録画ファイルをmp4ファイルに変換する．

## 実行環境構築

本プロジェクトはpyenvとpoetryを使用する．

1. pythonダウンロード

    ```shell
    pyenv install $(cat .python-version)
    ```

1. ライブラリインストール

    ```shell
    poetry install
    ```

    ```shell
    brew install ffmpeg
    ```

1. 仮想環境起動

    ```shell
    poetry shell
    ```

1. 実行

    | 引数 | 説明 |
    | --- | --- |
    | 1 | Pythonファイル |
    | 2 | 録画ファイルの絶対パス |
    | 3 | 録画ファイルの時間 (※1)　|
    | 4 | 切り抜き開始時間 (※1) |
    | 5 | 切り抜き終了時間 (※1) |

    ※1: VLCのタイムラインで確認できる残り時間

    ![time]("docs/assets/time.drawio.png")

    ```shell
    python src/m2ts_to_mp4.py {録画ファイルの絶対パス} {録画ファイルの時間} {切り抜き開始時間} {切り抜き終了時間}
    ```

    <details>

    <summary>実行例</summary>

    ```shell
    python src/m2ts_to_mp4.py 'file/to/absolute/path/file_name.m2ts' 00:49:05 00:40:00 00:39:30
    ```

    </details>
