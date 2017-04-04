#!/usr/bin/python
# -*- coding: utf-8 -*-

from generator import Generator
from mysql import MySQL

import wx
import wx.html

class GUI(wx.Frame,Generator):
	
	Databases_selected = ''
	conn = MySQL()
	
	def __init__( self, parent ):
		wx.Frame.__init__(self,parent,title=u"Generador de datos",size=wx.Size(910,450))
		self.Show()
		self.Centre()
		favicon = wx.Icon('icons/logo_db_64x64.png',wx.BITMAP_TYPE_ICO, 16,16)
		self.SetIcon(favicon)
		self.menu()
		self.toolbar()
		self.initgui()

	def menu(self):
		self.menubar = wx.MenuBar()

		fileMenu = wx.Menu()
		quit = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+Q')
		fileMenu.AppendItem(quit)

		extensionesMenu = wx.Menu()
		newExtension = wx.MenuItem(extensionesMenu, wx.ID_NEW, '&Nueva\tCtrl+N')
		extensionesMenu.AppendItem(newExtension)
		listarExtensiones = wx.MenuItem(extensionesMenu, -1, '&Listar')
		extensionesMenu.AppendItem(listarExtensiones)

		databaseMenu = wx.Menu()
		connectionHelp = wx.MenuItem(databaseMenu, -1, '&Conectar')
		databaseMenu.AppendItem(connectionHelp)
		databasesHelp = wx.MenuItem(databaseMenu, -1, '&Databases')
		databaseMenu.AppendItem(databasesHelp)

		helpMenu = wx.Menu()
		ayudaHelp = wx.MenuItem(helpMenu, wx.ID_HELP, '&Ayuda')
		helpMenu.AppendItem(ayudaHelp)
		aboutHelp = wx.MenuItem(helpMenu, -1, '&Acerca de')
		helpMenu.AppendItem(aboutHelp)

		self.menubar.Append(fileMenu, '&Archivo')
		self.menubar.Append(extensionesMenu, '&Extensiones')
		self.menubar.Append(databaseMenu, '&Database')
		self.menubar.Append(helpMenu, '&Help')

		self.SetMenuBar(self.menubar)

		self.Bind(wx.EVT_MENU, self.OnAboutBox, aboutHelp)
		self.Bind(wx.EVT_MENU, self.OnShowHelpContents, ayudaHelp)
		self.Bind(wx.EVT_MENU, self.nuevaColeccion, newExtension)
		self.Bind(wx.EVT_MENU, self.nuevaConexion, connectionHelp)
		self.Bind(wx.EVT_MENU, self.salir, quit)
		self.Bind(wx.EVT_MENU,self.dialog_selection,databasesHelp)
		self.Bind(wx.EVT_MENU,self.listar_extensiones,listarExtensiones)
		self.InitHelp()

	def toolbar(self):
		self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY ) 
		self.toolDocumento = self.m_toolBar1.AddLabelTool( 101, u"tool", wx.Bitmap( u"icons/document.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Nuevo diccionario", wx.EmptyString, None ) 
		
		self.toolDatabase = self.m_toolBar1.AddLabelTool( 102, u"tool", wx.Bitmap( u"icons/databases.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Abrir base de datos", wx.EmptyString, None ) 

		self.m_toolBar1.Realize()

		self.Bind(wx.EVT_TOOL, self.nuevaColeccion, id=101)
		self.Bind(wx.EVT_TOOL, self.dialog_selection, id=102)

	def initgui(self):
		# Sizer para agregar los componentes
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		#=============================== Primera linea de botones ===============================#
		
		self.lblTabla = wx.StaticText( self, wx.ID_ANY, u"Tabla:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblTabla.Wrap( -1 )
		bSizer4.Add( self.lblTabla, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		cboTablasChoices = self.conn.tables_list(self.Databases_selected)
		self.cboTablas = wx.ComboBox( self, wx.ID_ANY, u"Seleccione", wx.DefaultPosition, wx.DefaultSize, cboTablasChoices, 0 )
		bSizer4.Add( self.cboTablas, 0, wx.ALL, 5 )

		self.spinRango = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 500, 10 )
		bSizer4.Add( self.spinRango, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.btnGenerarData = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"icons/triangle-right.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( self.btnGenerarData, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		#=============================== Segunda linea: campo de texto ===============================#
		
		self.txtCampossql = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.txtCampossql, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		#=============================== Tercera linea: Botones para generar datos ===============================#
		
		self.lblDato = wx.StaticText( self, wx.ID_ANY, u"Dato:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblDato.Wrap( -1 )
		bSizer3.Add( self.lblDato, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.array_opciones = ['Ninguno','Random','Personalizado','E-mail','Password','DATE']
		cboDatosChoices = self.array_opciones + self.lista_archivos()
		self.cboDatos = wx.ComboBox( self, wx.ID_ANY, u"Seleccione", wx.DefaultPosition, wx.DefaultSize, cboDatosChoices, 0 )
		bSizer3.Add( self.cboDatos, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.lblUnir = wx.StaticText( self, wx.ID_ANY, u"Unir con:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblUnir.Wrap( -1 )
		bSizer3.Add( self.lblUnir, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		cboDatosUnirChoices = self.array_opciones + self.lista_archivos()
		self.cboDatosUnir = wx.ComboBox( self, wx.ID_ANY, u"Seleccione", wx.DefaultPosition, wx.DefaultSize, cboDatosUnirChoices, 0 )
		bSizer3.Add( self.cboDatosUnir, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		cboTipoDatoChoices = ['String','Int','Date','Float']
		self.cboTipoDato = wx.ComboBox( self, wx.ID_ANY, u"Tipo", wx.DefaultPosition, wx.DefaultSize, cboTipoDatoChoices, 0 )
		bSizer3.Add( self.cboTipoDato, 0, wx.ALL, 5 )
		
		self.lblOpcion = wx.StaticText( self, wx.ID_ANY, u"Opcion:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblOpcion.Wrap( -1 )
		bSizer3.Add( self.lblOpcion, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		cboOpcionChoices = ['Ninguna','Unir','Retorna']
		self.cboOpcion = wx.ComboBox( self, wx.ID_ANY, u"Ninguna", wx.DefaultPosition, wx.DefaultSize, cboOpcionChoices, 0 )
		bSizer3.Add( self.cboOpcion, 0, wx.ALL, 5 )
		
		self.btnGeneraCadena = wx.Button( self, wx.ID_ANY, u"Generar", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.btnGeneraCadena, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer3, 0, wx.EXPAND, 5 )

		#=============================== Cuarta linea: caja de texto de la cadena de opciones ===============================#
		
		self.txtCadena = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.txtCadena, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_generarsql = wx.Button( self, wx.ID_ANY, u"Generar cadena", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.btn_generarsql, 0, wx.ALL, 5 )
		
		self.btnLimpiarCampos = wx.Button( self, wx.ID_ANY, u"Limpiar", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.btnLimpiarCampos, 0, wx.ALL, 5 )
		
		#self.btnInsertarBD = wx.Button( self, wx.ID_ANY, u"Insertar en bd", wx.DefaultPosition, wx.DefaultSize, 0 )
		#bSizer2.Add( self.btnInsertarBD, 0, wx.ALL, 5 )

		#self.btnEliminarRepetidos = wx.Button( self, wx.ID_ANY, u"Eliminar repetidos", wx.DefaultPosition, wx.DefaultSize, 0 )
		#bSizer2.Add( self.btnEliminarRepetidos, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
		
		#=============================== Quinta linea: caja de texto ===============================#
		
		self.txtSQLGenerado = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer1.Add( self.txtSQLGenerado, 1, wx.ALL|wx.EXPAND, 5 )
		self.SetSizer( bSizer1 )
		self.Layout()

		#=============> Eventos de botones
		self.btnGenerarData.Bind(wx.EVT_BUTTON,self.generaPosSQL)
		self.btnGeneraCadena.Bind(wx.EVT_BUTTON,self.genera_cadena)
		self.btn_generarsql.Bind(wx.EVT_BUTTON,self.obtener_datos_aleatorios)
		self.btnLimpiarCampos.Bind(wx.EVT_BUTTON,self.limpiarcajas)

	############################### Eventos ###############################
	def limpiarcajas(self,evt):
		self.txtCampossql.SetValue("")
		self.txtCadena.SetValue("")
		self.txtSQLGenerado.SetValue("")

	def nuevaColeccion(self,evt):
		dialog = NuevaColeccion(self)
		result = dialog.ShowModal()
		if result == wx.ID_OK:

			self.cboDatos.Clear()
			self.cboDatos.SetValue('Ninguno')
			array = self.array_opciones + self.lista_archivos()
			self.cboDatos.AppendItems(array)


			self.cboDatosUnir.Clear()
			self.cboDatosUnir.SetValue('Ninguno')
			array = self.array_opciones + self.lista_archivos()
			self.cboDatosUnir.AppendItems(array)

		else:
			self.cboDatos.Clear()
			self.cboDatos.SetValue('Ninguno')
			array = self.array_opciones + self.lista_archivos()
			self.cboDatos.AppendItems(array)


			self.cboDatosUnir.Clear()
			self.cboDatosUnir.SetValue('Ninguno')
			array = self.array_opciones + self.lista_archivos()
			self.cboDatosUnir.AppendItems(array)

		dialog.Destroy()

	def nuevaConexion(self,evt):
		dialog = NuevaConexion(self)
		result = dialog.ShowModal()
		if result == wx.ID_OK:
			print "OK"
		else:
			print "Cancel"
		dialog.Destroy()

	def OnAboutBox(self,evt):
		description = "Generador de datos megaprogrammer\nPermite generar datos en formato sql para\n"
		description = description + "llenar sus bases de datos de forma rapida"

		licence = "Esta biblioteca es software libre; puede redistribuirla\ny/o modificarla bajo los términos de la\n"
		licence = licence + "Licencia Pública General Reducida de GNU tal como la publica la\n"
		licence = licence + "Free SoftwareFoundation; ya sea la versión 2.1 de la licencia o \n"
		licence = licence + "(según su criterio) cualquier versión posterior."

		info = wx.AboutDialogInfo()

		info.SetIcon(wx.Icon('icons/logo_db_64x64.png', wx.BITMAP_TYPE_PNG))
		info.SetName('Generador')
		info.SetVersion('0.2')
		info.SetDescription(description)
		info.SetCopyright('(C) 2006 - 2016 JC')
		info.SetWebSite('http://www.pacpac1992.github.io')
		info.SetLicence(licence)
		info.AddDeveloper('JC')

		wx.AboutBox(info)

	def dialog_selection(self,evt):
		try:
			r = self.check_config()
			if r != 'False':
				self.conn.datos_preconstruidos(r[0],r[1],r[2])
				choices = self.conn.databases_list()
				if choices == False:
					wx.MessageBox("Datos incorrectos para iniciar sesion en mysq", "Message" ,wx.OK |wx.ICON_ERROR)
				else:
					dialog = wx.SingleChoiceDialog(None, "Seleccione una", "Databases",choices)

					if dialog.ShowModal() == wx.ID_OK:
						self.Databases_selected = dialog.GetStringSelection()
						self.cboTablas.Clear()
						self.cboTablas.SetValue('Tablas')
						self.array_tablas = self.conn.tables_list(self.Databases_selected)
						self.cboTablas.AppendItems(self.array_tablas)
					
						dialog.Destroy()
			else:
				wx.MessageBox("No hay datos para iniciar la conexion", "Message" ,wx.OK |wx.ICON_ERROR)
				
		except Exception as e:
			print e
	
	def check_config(self):
		array = self.return_data_file_array('config.txt','src/config/config/')
		if array[0] == '':
			return 'False'
		else:
			return array

	def listar_extensiones(self,evt):
		choices = self.lista_archivos()
		dialog = wx.SingleChoiceDialog(None, "Lista de archivos", "Archivos",choices)
		
		if dialog.ShowModal() == wx.ID_OK:
			pass
		
		dialog.Destroy()

	def generaPosSQL(self,evt):
		r = self.conn.columns_list(self.Databases_selected,self.cboTablas.GetValue())
		sql = self.crear_sql(self.cboTablas.GetValue(),r)
		self.txtCampossql.SetValue(sql)

	def genera_cadena(self,evt):
		datos = self.cboDatos.GetValue()
		union = self.cboDatosUnir.GetValue()
		tipo = self.cboTipoDato.GetValue()
		opcion = self.cboOpcion.GetValue()

		dato = ''

		if datos == 'Seleccione' or datos == 'Ninguno':
			print("Falta seleccionar")
		else:
			if union == 'Ninguno' or union == 'Seleccione':
				if datos == 'Random':
					dato = '[0:100]'
				elif datos == 'Personalizado':
					dato = '[1-2-3]'
				elif datos == 'DATE':
					dato = 'DATE(1990>2000)'
				else:
					dato = datos
			else:
				if opcion == 'Unir':
					dato = datos + ' ' + union
			
			if opcion == 'Retorna':
				dato = datos + '_()'

			if tipo == 'String' or tipo == 'Date':
				dato = '"' + dato + '"'

		self.txtCadena.AppendText(dato + ',')

	def obtener_datos_aleatorios(self,evt):
		data = self.txtCadena.GetValue()
		data = data.rstrip(',')
		
		numb = self.spinRango.GetValue()

		for x in xrange(0,numb):
			result = self.before_buil(data)
			sql = self.preparar_consulta(self.txtCampossql.GetValue(),result)
			self.txtSQLGenerado.AppendText(sql+'\n')

	def InitHelp(self):
		def _addBook(filename):
			if not self.help.AddBook(filename):
				wx.MessageBox("Unable to open: " + filename,"Error", wx.OK|wx.ICON_EXCLAMATION)

		self.help = wx.html.HtmlHelpController()
		_addBook("helpfiles/testing.hhp")

	def OnCloseWindow(self, evt):
		del self.help
		evt.Skip()

	def OnShowHelpContents(self, evt):
		self.help.DisplayContents()

	def salir(self,evt):
		self.Close()

###########################################################################
## Class NuevaColeccion
###########################################################################
class NuevaColeccion(wx.Dialog):
	
	def __init__( self, parent ):
		wx.Dialog.__init__(self,parent,id=wx.ID_ANY,title=u"Nuevo Archivo",pos=wx.DefaultPosition,size=wx.Size(190,300))
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btnGuardarArchivo = wx.Button( self, wx.ID_ANY, u"Guardar", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.btnGuardarArchivo, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer6, 0, wx.EXPAND, 5 )
		
		self.txtArchivo = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer5.Add( self.txtArchivo, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer5 )
		self.Layout()
		
		self.Centre( wx.BOTH )

		self.btnGuardarArchivo.Bind(wx.EVT_BUTTON,self.Guardar_archivo)

	def Guardar_archivo(self,evt):
		self.generator = Generator()
		dialog = wx.TextEntryDialog(None, "Escriba el nombre del archivo","Guardar", "", style=wx.OK|wx.CANCEL)
		if dialog.ShowModal() == wx.ID_OK:
			n = dialog.GetValue()
			self.generator.write_file(n.lower()+'.txt',self.txtArchivo.GetValue())
			self.Destroy()
		self.Destroy()

###########################################################################
## Class NuevaConeccion
###########################################################################

class NuevaConexion(wx.Dialog):
	
	def __init__( self, parent ):
		wx.Dialog.__init__(self,parent,id=wx.ID_ANY,title=wx.EmptyString,pos=wx.DefaultPosition,size=wx.Size(300,185))
		
		self.lblhostname = wx.StaticText(self, -1, u"HostName:", pos=(5,7))
		self.txtHostName = wx.TextCtrl(self, -1, pos=(105,5),size=(170,30))

		self.lblusername = wx.StaticText(self, -1, u"UserName:", pos=(5,47))
		self.txtUserName = wx.TextCtrl(self, -1, pos=(105,40),size=(170,30))

		self.lblpassword = wx.StaticText(self, -1, u"Password:",pos=(5,87))
		self.txtPassword = wx.TextCtrl(self, -1,style=wx.TE_PASSWORD,pos=(105,80),size=(170,30))

		self.btnGuardar = wx.Button( self, -1, u"Guardar", pos=(105,120))
		self.btnCerrar = wx.Button( self, -1, u"Cerrar", pos=(190,120))
		self.Centre( wx.BOTH )

		self.btnGuardar.Bind(wx.EVT_BUTTON,self.OnClicked)
		self.btnCerrar.Bind(wx.EVT_BUTTON,self.OnClose)

		self.generator = Generator()
		self.comprobar_datos()
	
	def comprobar_datos(self):
		
		a = self.generator.return_data_file_array("config.txt","src/config/config/")
		if len(a) > 1:
			self.txtHostName.SetValue(a[0])
			self.txtUserName.SetValue(a[1])
			self.txtPassword.SetValue(a[2])

	def OnClicked(self,evt):
		data = self.txtHostName.GetValue() + ',' + self.txtUserName.GetValue() + ',' + self.txtPassword.GetValue()
		r = self.generator.update_content_file('config.txt',data,'src/config/config/')
	
	def OnClose(self,evt):
		self.Destroy()

app = wx.App()
GUI(None)
app.MainLoop()