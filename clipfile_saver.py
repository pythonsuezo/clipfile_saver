import clipframe        # wxFormBuilderのソース
import wx
import os, sys, re
import datetime
import subprocess
import configparser
from PIL import ImageGrab, Image
from threading import Event, Thread
from time import sleep
import copy
import winsound

"""----------------------------------------------
クリップ画像保存器
グローバル定数
path    : 実行ファイルのディレクトリ
today   : 今日の日付
now     : 今の時間
INI     : 設定ファイルの場所
設定ファイルに最後に保存したディレクトリの情報を記載する
----------------------------------------------"""

path = os.path.dirname( sys.argv[0] )
INI = path + "/INI.conf"
# Python 3.12 で削除された SafeConfigParser の代わりに ConfigParser を使う
conf = configparser.ConfigParser()

now = datetime.datetime.now()
today = now.strftime( "%Y/%m/%d" )          # 日付 YYYY/MM/DD
now = now.strftime( "%H:%M:%S" )            # 時刻 HH:MM:SS

# Windowsでフォルダ名に使えない文字・予約名
INVALID_FOLDER_CHARS = '<>:"/\\|?*'
WINDOWS_RESERVED_NAMES = frozenset([
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
])

def validate_folder_name( name ):
    """サブフォルダ名を検証する。問題なければ正規化した名前、ダメなら (None, 理由)。"""
    if name is None:
        return None, "サブフォルダ名を入力してください。"

    name = name.strip()
    if not name:
        return None, "サブフォルダ名を入力してください。"

    if name in ( ".", ".." ):
        return None, "「.」や「..」はフォルダ名に使えません。"

    bad = sorted( set( c for c in name if c in INVALID_FOLDER_CHARS or ord( c ) < 32 ) )
    if bad:
        shown = " ".join( repr( c )[1:-1] for c in bad )
        return None, (
            "フォルダ名に使えない文字が含まれています。\n"
            "使えない文字: < > : \" / \\ | ? * および制御文字\n"
            "検出: " + shown
        )

    if name.endswith( "." ) or name.endswith( " " ):
        return None, "フォルダ名の末尾にスペースや「.」は使えません。"

    # CON.txt のような予約名も弾く
    stem = name.split( "." )[0].upper()
    if name.upper() in WINDOWS_RESERVED_NAMES or stem in WINDOWS_RESERVED_NAMES:
        return None, "「%s」はWindowsの予約名のため使えません。" % name

    if len( name ) > 200:
        return None, "フォルダ名が長すぎます（200文字以内）。"

    return name, None

class Mainframe( clipframe.MyFrame1 ):
    def __init__( self, parent ):
        clipframe.MyFrame1.__init__( self, parent )
        try:
            conf.read(INI)                  # 設定ファイルをロードする
            if conf.has_option("save","folder"):
                print("設定読み込み成功")
                m_folder = conf.get("save","folder")
                s_folder = conf.get("save","s_folder")
                name = conf.get("save","name")

                if os.path.exists( m_folder ):
                    self.m_textCtrl2.SetValue(m_folder)
                    self.SetCombo(m_folder)
                    self.m_textCtrl1.SetValue(name)
                    if os.path.exists(os.path.join(m_folder,s_folder)):
                        self.m_comboBox1.SetValue(s_folder)
                else:   # ディレクトリが無いならボタンを無効にする
                    print(m_folda,"\nディレクトリが存在しません")
                    self.m_textCtrl2.SetValue("親フォルダを選択してください")
                    self.m_button4.Disable()
                    self.m_button5.Disable()
                    self.m_toggleBtn2.Disable()
                    self.m_toggleBtn2.SetValue(False)
            else:
                print("設定がありません")
                conf.add_section("save")
                self.m_textCtrl2.SetValue("親フォルダを選択してください")
                self.m_button4.Disable()
                self.m_button5.Disable()
                self.m_toggleBtn2.Disable()
                self.m_toggleBtn2.SetValue(False)
        except:
            print("設定ファイルがありません")

    def Dirset( self, event ):              # ディレクトリ選択した時
        dir = self.m_dirPicker1.GetPath()
        print(dir)
        self.m_textCtrl2.SetValue(dir)      # 保存先をテキストコントロールにセット
        self.m_button4.Enable()
        self.m_button5.Enable()
        self.m_toggleBtn2.Enable()
        # INIに書き込み
        conf.set("save","folder",dir)
        f = open(INI,"w")
        conf.write(f)
        f.close()
        self.SetCombo(dir)
        return

    def Opendir( self, event ):
        dir = os.path.join(self.m_textCtrl2.GetValue(),self.m_comboBox1.GetValue())   # テキストコントロールから保存先を取得する
        if os.path.exists( dir ):           # ディレクトリが存在するか？
            subprocess.Popen(["explorer", dir])
        else:
            subprocess.Popen(["explorer", path])
        return

    def Clipsave( self, event ):
        im = ImageGrab.grabclipboard()   # クリップボードの画像を取得
        dir = self.m_textCtrl2.GetValue()
        manual_save = dir + "/manual"       # 手動保存のディレクトリ
        file_name = "pic_"

        if im == None:                      # クリップボード内に画像が無ければ何もしない
            return print("クリップボードに画像がありません")

        if os.path.exists( dir ):           # ディレクトリが存在するか？
            if not os.path.exists(manual_save): # 手動保存のディレクトリが存在するか？
                os.mkdir(manual_save)          # 無いなら作る
        else:
            return print("存在しないディレクトリ:",dir)

        save_file = self.New_file(manual_save, file_name)[0]

        im.save( save_file,"JPEG",quality=99,optimize=True )       # 画像を保存
        winsound.PlaySound('SystemAsterisk', winsound.SND_ASYNC)
        print(save_file)           # パスを表示
        return

    def Monitoring_set( self, event ):
        m_set = self.m_toggleBtn2.GetValue()   # トグルスイッチの状態を取得
        print(m_set)
        if m_set:
            thread = Thread(target=self.ssloop,name="loop",args=())
            thread.start()                                              # ssloopを別スレッドで処理
        else:
            threadevent.set()                                           # ssloopのイベントをセット
            self.m_dirPicker1.Enable()                                  # 監視終了でボタン類を有効に戻す
            # self.m_button1.Enable()

    def ssloop(self):                                                   # クリップボード監視ループ
        imdelta = Image.new("RGB", (512, 512), (128, 128, 128))         # imdelta=Noneにならないように適当なimageを設定
        print("監視開始")
        self.m_dirPicker1.Disable()                                     # ボタン類を無効にしておく
        # self.m_button1.Disable()
        while not threadevent.wait(0.5):
            im = ImageGrab.grabclipboard()
            dir = self.m_textCtrl2.GetValue() + "/" + self.m_comboBox1.GetValue()
            name = self.m_textCtrl1.GetValue()
            if im == None:
                continue

            else:
                if imdelta.histogram() != im.histogram() or imdelta == None:
                    if isinstance( im, Image.Image ):
                        save_file = self.New_file(dir,name)[0]
                        im.save(save_file,"JPEG",quality=99,optimize=True)
                        winsound.PlaySound('SystemAsterisk', winsound.SND_ASYNC)
                        print("saved")
                        print(save_file)
                        imdelta = im
                    else:
                       pass
                elif imdelta.histogram() == im.histogram() or im == None:
                    pass
                else:
                    pass
        print("監視終了")
        threadevent.clear()

    def New_file( self, dir, file_name ):
        # ディレクトリのパスを受け取って最高値+1のファイル名を返す
        # 同名ファイルのナンバリング最高値を求める
        dir_list = os.listdir(dir)     # フォルダの中身をリスト化

        if len(dir_list) == 0:          # ディレクトリ内にファイルがない場合は00000
            return dir + "/" + file_name + "00000" + ".jpg", "00000"

        if [s for s in dir_list if s.startswith(file_name)]:
            max_num =  max([s for s in dir_list if s.startswith(file_name)]).split(".")[0]
            max_num = re.sub(file_name, r"", max_num)  # ファイル名を削除
            new_file = "{0:05d}".format(int(max_num)+1)   # ファイル名に+1して５ケタでゼロサプレスする
        else:
            new_file = "00000"
        return dir + "/" + file_name + new_file + ".jpg", new_file

    def ShowError( self, message ):
        dlg = wx.MessageDialog( self, message, "クリップ画像保存器", style=wx.OK|wx.ICON_ERROR )
        dlg.ShowModal()
        dlg.Destroy()

    def Make_Dir(self, event):
        m_folder = self.m_textCtrl2.GetValue()
        new_folder, err = validate_folder_name( self.m_comboBox1.GetValue() )
        if err:
            self.ShowError( err )
            return

        if not os.path.isdir( m_folder ):
            self.ShowError( "親フォルダが存在しません。\n先に親フォルダを選択してください。" )
            return

        new_path = os.path.join( m_folder, new_folder )
        print( new_path )

        if os.path.isdir( new_path ):
            # 既存ならコンボを合わせるだけ
            self.m_comboBox1.SetValue( new_folder )
            return

        try:
            os.mkdir( new_path )
        except OSError as e:
            self.ShowError( "フォルダを作成できませんでした。\n%s" % e )
            return

        self.SetCombo( m_folder )
        self.m_comboBox1.SetValue( new_folder )

    def SetCombo(self, dir):
        files = os.listdir(dir)
        s_folder = [f for f in files if os.path.isdir(os.path.join(dir, f))]
        print(s_folder)

        self.m_comboBox1.SetItems(s_folder)  # 対象.SetItems(リスト)で項目を与える
        return

    def ExitHandler( self, event ):
        # dlg = wx.MessageDialog( None, 'クリップ画像保存器を終了します。\nよろしいですか？',
        #                     "クリップ画像保存器", style = wx.YES_NO )
        # result = dlg.ShowModal()        #ダイアログの表示

        result = wx.ID_YES                      # 閉じる時の確認要らない

        if result == wx.ID_YES:              #はいを押した時終了
            threadevent.set()
            conf.set("save","name",self.m_textCtrl1.GetValue())
            conf.set("save","s_folder",self.m_comboBox1.GetValue())
            conf.set("save","toggle",str(self.m_toggleBtn2.GetValue()))
            f = open(INI,"w")
            conf.write(f)
            f.close()
            sys.exit()                      #プログラム終了
        else:                           #いいえの時は何もしない
            return

threadevent = Event()

if __name__ == "__main__":
    app = wx.App( False )
    frame = Mainframe( None )
    frame.Show( True )
    app.MainLoop()
