# -*- coding: utf-8 -*-
"""validate_folder_name の単体テスト（wx / Pillow 不要）"""
import sys
import types
import unittest

# clipfile_saver を import できるように依存をモックする
for name in ("wx", "wx.xrc", "wx.adv", "clipframe", "PIL", "PIL.ImageGrab", "PIL.Image", "winsound"):
    sys.modules.setdefault(name, types.ModuleType(name))

wx = sys.modules["wx"]
wx.MOD_CONTROL = 1
wx.MOD_ALT = 2
wx.ID_ANY = -1
wx.OK = 4
wx.ICON_ERROR = 512
wx.NewId = lambda: 1
wx.Frame = type("Frame", (), {})
wx.Menu = type("Menu", (), {})
wx.Icon = type("Icon", (), {})
wx.ArtProvider = type("ArtProvider", (), {"GetBitmap": staticmethod(lambda *a, **k: None)})
wx.ART_INFORMATION = 0
wx.ART_OTHER = 0
wx.StaticText = type("StaticText", (), {})
wx.MessageDialog = type("MessageDialog", (), {})
wx.EVT_HOTKEY = object()
wx.EVT_ICONIZE = object()
wx.EVT_MENU = object()
wx.CallAfter = lambda *a, **k: None

wxadv = sys.modules["wx.adv"]
wxadv.TaskBarIcon = type("TaskBarIcon", (), {})
wxadv.EVT_TASKBAR_LEFT_DCLICK = object()

sys.modules["clipframe"].MyFrame1 = type("MyFrame1", (), {})
sys.modules["PIL.ImageGrab"].grabclipboard = lambda: None
sys.modules["PIL.Image"].Image = type("Image", (), {})
sys.modules["PIL.Image"].new = lambda *a, **k: None

from clipfile_saver import validate_folder_name  # noqa: E402


class TestValidateFolderName(unittest.TestCase):
    def test_ok_names(self):
        for name in ("normal", "スペース入り", "日本語フォルダ", "shot_01", "  trim_me  "):
            cleaned, err = validate_folder_name(name)
            self.assertIsNone(err, name)
            self.assertEqual(cleaned, name.strip())

    def test_empty(self):
        for name in ("", "   ", None):
            cleaned, err = validate_folder_name(name)
            self.assertIsNone(cleaned)
            self.assertIn("入力", err)

    def test_dot_dirs(self):
        for name in (".", ".."):
            cleaned, err = validate_folder_name(name)
            self.assertIsNone(cleaned)
            self.assertIn(".", err)

    def test_invalid_chars(self):
        for name in ("a/b", "a\\b", "foo:bar", "foo*bar", "foo?bar",
                     'foo"bar', "foo<bar>", "foo|bar"):
            cleaned, err = validate_folder_name(name)
            self.assertIsNone(cleaned, name)
            self.assertIn("使えない文字", err)

    def test_trailing(self):
        for name in ("trailing.", "trailing "):
            # strip 後 trailing space は空扱いではなく、末尾スペースは strip で消える
            # 「trailing.」は末尾ドットで拒否
            cleaned, err = validate_folder_name(name)
            if name == "trailing ":
                # strip されて "trailing" になり許可される
                self.assertEqual(cleaned, "trailing")
                self.assertIsNone(err)
            else:
                self.assertIsNone(cleaned)
                self.assertIn("末尾", err)

    def test_reserved(self):
        for name in ("CON", "con", "NUL", "COM1", "LPT9", "AUX.txt"):
            cleaned, err = validate_folder_name(name)
            self.assertIsNone(cleaned, name)
            self.assertIn("予約名", err)

    def test_too_long(self):
        cleaned, err = validate_folder_name("a" * 201)
        self.assertIsNone(cleaned)
        self.assertIn("長すぎ", err)


if __name__ == "__main__":
    unittest.main()
