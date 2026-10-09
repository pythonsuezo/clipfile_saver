# -*- coding: utf-8 -*-
"""to_jpeg_compatible の単体テスト（Pillow 必要）"""
import io
import sys
import types
import unittest

for name in ("wx", "wx.xrc", "wx.adv", "clipframe", "winsound"):
    sys.modules.setdefault(name, types.ModuleType(name))

wx = sys.modules["wx"]
wx.MOD_CONTROL = 1
wx.MOD_ALT = 2
sys.modules["wx.adv"].TaskBarIcon = type("TaskBarIcon", (), {})
sys.modules["wx.adv"].EVT_TASKBAR_LEFT_DCLICK = object()
sys.modules["clipframe"].MyFrame1 = type("MyFrame1", (), {})

from PIL import Image  # noqa: E402
from clipfile_saver import (  # noqa: E402
    to_jpeg_compatible,
    prepare_image_for_format,
    normalize_save_ext,
    save_image,
)


class TestToJpegCompatible(unittest.TestCase):
    def test_rgba_saves_as_jpeg(self):
        im = Image.new("RGBA", (8, 8), (255, 0, 0, 128))
        out = to_jpeg_compatible(im)
        self.assertEqual(out.mode, "RGB")
        buf = io.BytesIO()
        out.save(buf, "JPEG")
        self.assertGreater(len(buf.getvalue()), 0)

    def test_rgb_passthrough(self):
        im = Image.new("RGB", (4, 4), (1, 2, 3))
        self.assertIs(to_jpeg_compatible(im), im)

    def test_la(self):
        im = Image.new("LA", (4, 4), (100, 200))
        self.assertEqual(to_jpeg_compatible(im).mode, "RGB")


class TestSaveFormats(unittest.TestCase):
    def test_normalize_ext(self):
        self.assertEqual(normalize_save_ext("PNG"), ".png")
        self.assertEqual(normalize_save_ext(".jpeg"), ".jpg")
        self.assertEqual(normalize_save_ext("nope"), ".png")

    def test_png_keeps_alpha(self):
        im = Image.new("RGBA", (8, 8), (255, 0, 0, 128))
        out = prepare_image_for_format(im, "PNG")
        self.assertEqual(out.mode, "RGBA")

    def test_save_image_png_and_jpg(self):
        import tempfile
        import os

        im = Image.new("RGBA", (8, 8), (0, 255, 0, 200))
        td = tempfile.mkdtemp()
        try:
            png_path = os.path.join(td, "a.png")
            save_image(im, png_path, ".png")
            loaded = Image.open(png_path)
            self.assertEqual(loaded.mode, "RGBA")

            jpg_path = os.path.join(td, "a.jpg")
            save_image(im, jpg_path, ".jpg")
            loaded_jpg = Image.open(jpg_path)
            self.assertEqual(loaded_jpg.mode, "RGB")
        finally:
            for name in os.listdir(td):
                os.remove(os.path.join(td, name))
            os.rmdir(td)


if __name__ == "__main__":
    unittest.main()
