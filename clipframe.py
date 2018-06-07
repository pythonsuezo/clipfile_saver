# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Nov  6 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"クリップ画像保存器", pos = wx.DefaultPosition, size = wx.Size( 500,331 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_dirPicker1 = wx.DirPickerCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, u"親フォルダを選択", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_SMALL )
		bSizer7.Add( self.m_dirPicker1, 0, wx.ALL, 5 )
		
		self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"サブフォルダ：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer7.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_comboBox1Choices = []
		self.m_comboBox1 = wx.ComboBox( self.m_panel1, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_comboBox1Choices, 0 )
		bSizer7.Add( self.m_comboBox1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button1 = wx.Button( self.m_panel1, wx.ID_ANY, u"作成", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_button1, 0, wx.ALL, 5 )
		
		self.m_textCtrl1 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl1.SetToolTip( u"ファイル名" )
		
		bSizer7.Add( self.m_textCtrl1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer4.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"保存先：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer8.Add( self.m_staticText3, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl2 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"保存先フォルダ", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer8.Add( self.m_textCtrl2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		bSizer4.Add( bSizer8, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_button4 = wx.Button( self.m_panel1, wx.ID_ANY, u"フォルダを開く", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_button4, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_button5 = wx.Button( self.m_panel1, wx.ID_ANY, u"クリップボードの画像を保存", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_button5, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer9.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_toggleBtn2 = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"クリップボード監視", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_toggleBtn2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer6.Add( self.m_toggleBtn2, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer9.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		
		bSizer5.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		
		bSizer2.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		
		self.m_panel1.SetSizer( bSizer2 )
		self.m_panel1.Layout()
		bSizer2.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.ExitHandler )
		self.m_dirPicker1.Bind( wx.EVT_DIRPICKER_CHANGED, self.Dirset )
		self.m_button1.Bind( wx.EVT_BUTTON, self.Make_Dir )
		self.m_button4.Bind( wx.EVT_BUTTON, self.Opendir )
		self.m_button5.Bind( wx.EVT_BUTTON, self.Clipsave )
		self.m_toggleBtn2.Bind( wx.EVT_TOGGLEBUTTON, self.Monitoring_set )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def ExitHandler( self, event ):
		event.Skip()
	
	def Dirset( self, event ):
		event.Skip()
	
	def Make_Dir( self, event ):
		event.Skip()
	
	def Opendir( self, event ):
		event.Skip()
	
	def Clipsave( self, event ):
		event.Skip()
	
	def Monitoring_set( self, event ):
		event.Skip()
	

