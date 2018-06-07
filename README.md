# clipfile_saver
クリップボードをリアルタイムで監視して、画像が貼られたら任意のフォルダに連番保存するソフト

clipframe.pyとclipfile_saver.pyを同じフォルダに置いてください。
clipfile_saver.pyを実行すると起動します。

clipfile_saver.exeは単体で動作します。

最初に親フォルダを選択してから、サブフォルダを指定、または作成してください。
クリップボードの画像を保存を押すと、今現在クリップボードにある画像をサブフォルダに保存します。
クリップボード監視ではスクリーンショットや、web上の画像のコピーを検知して自動的に保存します。

OSのエクスプローラでのコピーはファイルのパスがクリップボードに貼られる仕組みなので動作しません。

動作確認
windows7, 10 64bit
python3 32bit 3.5.4

起動に必要なライブラリ
・Pillow
・wxpython

制作者 suezo

HP http://blog.livedoor.jp/pythonsuezo/
