#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Libreria destinada a realizar graficas de funciones."""

from errores import *
import wx

###############################################################################
# ZONA DE COMENTARIOS
###############################################################################


def version():
    '''Version del modulo "graflib.py"
    v1.0
    Autor: Martin S. Lopez Paglione
    Octubre de 2014'''
    return "1.0"


def info_versiones(ver):
    '''Informacion de las versiones como historial de cambios y actualizaciones, fecha, y
    autor y colaboradores.
    El parametro "ver" es un string con la version a devolver. La variable de retorno es
    una tupla con descripcion de la version, fecha de creacion, y autor.
    Si ver = "todo" se devuelve un diccionario con todas las versiones'''

    h = {'1.0': ('''Primera version del modulo.
(todavia no hay nada)
''', 'Octubre 2014', 'Martin S. Lopez Paglione')}

    if ver in h:
        return h[ver]
    elif ver == "todo":
        return h
    else:
        raise ExcepcionVersion(ver)


ej = ((10, 9), (20, 22), (30, 21), (40, 30), (50, 41),
(60, 53), (70, 45), (80, 20), (90, 19), (100, 22),
(110, 42), (120, 62), (130, 43), (140, 71), (150, 89),
(160, 65), (170, 126), (180, 187), (190, 128), (200, 125),
(210, 150), (220, 129), (230, 133), (240, 134), (250, 165),
(260, 132), (270, 130), (280, 159), (290, 163), (300, 94))


class grafico(wx.Panel):
    def __init__(self, parent, datos):
        wx.Panel.__init__(self, parent)
        self.datos = datos
        self.grilla = grilla
        self.ejeX = ejex
        self.ejeY = ejey
        #self.SetBackgroundColour('WHITE')
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.SetDeviceOrigin(40, 400)
        dc.SetAxisOrientation(True, True)
        #dc.SetPen(wx.Pen('WHITE'))
        #dc.DrawRectangle(1, 1, 300, 200)
        self.dibujar_grilla(dc)
        self.dibujar_ejes(dc)
        self.dibujar_titulo(dc)
        self.dibujar_datos(dc)

    def dibujar_ejes(self, dc):
        '''Dibuja los ejes del grafico'''
        ejex = self.ejeX
        ejey = self.ejeY
        font = dc.GetFont()
        font.SetPointSize(8)
        dc.SetFont(font)
        #Dibujo el eje x
        dc.SetPen(wx.Pen(ejex.color, ejex.ancho, ejex.estilo))
        dc.DrawLine(0, 0, ejex.max + 1, 0)
        for i in range(ejex.min, ejex.max, ejex.marcas):
            dc.DrawLine(i, 1, i, -5)
            dc.DrawText(str(i), i - 5, -10)

        #Dibujo el eje y
        dc.SetPen(wx.Pen(ejey.color, ejey.ancho, ejey.estilo))
        dc.DrawLine(0, 0, 0, ejey.max + 1)
        for i in range(ejey.min, ejey.max, ejey.marcas):
            dc.DrawLine(1, i, -5, i)
            dc.DrawText(str(i), -30, i + 5)

    def dibujar_grilla(self, dc):
        '''Dibuja la grilla del grafico. Se deben pasar tambien los ejes para saber el
        tamaño de grilla que se necesita.'''
        grilla = self.grilla
        ejex = self.ejeX
        ejey = self.ejeY
        self.SetBackgroundColor = grilla.fondo
        #Dibujo las lineas horizontales
        if grilla.horizontal:
            dc.SetPen(wx.Pen(grilla.color_hor, grilla.ancho_hor, grilla.estilo_hor))
            for i in range(ejey.min, ejey.max, ejey.marcas):
                dc.DrawLine(1, i, ejex.max + 1, i)

        #Dibujo las lineas verticales
        if grilla.vertical:
            dc.SetPen(wx.Pen(grilla.color_ver, grilla.ancho_ver, grilla.estilo_ver))
            for i in range(ejex.min, ejex.max, ejex.marcas):
                dc.DrawLine(i, 1, i, ejey.max + 1)

    def dibujar_titulo(self, dc):
        '''Coloca el titulo del grafico.'''
        font = dc.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        dc.DrawText(self.datos.titulo, self.datos.pos_titulo[0], self.datos.pos_titulo[1])

    def dibujar_datos(self, dc):
        '''Dibuja los datos pasados.'''
        dc.SetPen(wx.Pen(self.datos.color, self.datos.ancho, self.datos.estilo))
        cant = len(self.datos.datos) - 1
        for i in range(cant):
            dc.DrawLine(self.datos.datos[i][0], self.datos.datos[i][1],
                        self.datos.datos[i + 1][0], self.datos.datos[i + 1][1])


class LineChartExample(wx.Frame):
    def __init__(self, parent, id, datos):
        wx.Frame.__init__(self, parent, id, size=(500, 500))
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('WHITE')
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        graf = grafico(panel, datos)
        hbox.Add(graf, 1, wx.EXPAND | wx.ALL, 15)
        panel.SetSizer(hbox)
        self.Centre()
        self.Show(True)


class eje(object):
    '''Define el estilo de un eje del grafico.'''
    def __init__(self):
        self.color = '#0AB1FF'
        self.ancho = 1
        self.estilo = wx.SOLID
        self.min = 0
        self.max = 500
        self.marcas = 50
        self.titulo = ''


class grilla(object):
    '''Define el estilo de la grilla.'''
    def __init__(self):
        self.horizontal = True
        self.vertical = True
        self.fondo = 'WHITE'
        self.color_hor = '#d5d5d5'
        self.ancho_hor = 1
        self.estilo_hor = wx.DOT
        self.color_ver = '#d5d5d5'
        self.ancho_ver = 1
        self.estilo_ver = wx.DOT


class datos(object):
    '''Define los datos a graficar y su estilo.'''
    def __init__(self, datos):
        self.color = '#0ab1ff'
        self.ancho = 2
        self.estilo = wx.SOLID
        self.datos = datos
        self.titulo = ''
        self.pos_titulo = (90, 235)


class leyenda(object):
    '''Define el estilo de la leyenda.'''
    pass


def mostrar(datos):
    app = wx.App()
    LineChartExample(None, -1, datos)
    app.MainLoop()
