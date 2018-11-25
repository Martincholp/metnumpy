#! /usr/bin/env python
# -*- coding: utf-8 -*-


class ExcepcionGeneral(Exception):
    """Clase base para todas las excepciones"""
    def __init__(self):
        """"""
        self.valor = 0
        self.descripcion = "Error general"

    def __str___(self):
        """"""
        return "[Error " + str(self.valor) + "] " + self.descripcion


class ExcepcionVersion(ExcepcionGeneral):
    """Error en la busqueda de versiones"""
    def __init__(self, ver):
        """"""
        self.valor = 0
        self.version = ver
        self.descripcion = "La version " + ver + " no existe."

    def __str__(self):
        """"""
        return "[Error " + str(self.valor) + "] " + self.descripcion


class ExcepcionMatlib(ExcepcionGeneral):
    """Clase base para las excepciones producidas por el modulo Matlib."""

    def __init__(self):
        """"""
        self.valor = 0
        self.descripcion = "Error de matlib"

    def __str___(self):
        """"""
        return "[Error " + str(self.valor) + "] " + self.descripcion


class ErrorIndice(ExcepcionMatlib):
    pass


class IndiceDesbordado(ErrorIndice):
    """Excepcion de indice desbordado"""

    def __init__(self):
        """"""
        self.valor = 1
        self.descripcion = "El indice este fuera de rango"

    def __str___(self):
        """"""
        return "[Error " + str(self.valor) + "] " + self.descripcion


class IndicesInvertidos(ErrorIndice):
    """Error debido a un mal orden en el paso de los indices"""

    def __init__(self):
        """"""
        self.valor = 0
        self.descripcion = "El indice superior no puede ser menor que el indice inferior"

    def __str__(self):
        return "[Error " + str(self.valor) + "] " + self.descripcion


class NoEsMatriz(ExcepcionMatlib):
    """La lista pasada como argumento no representa una matriz"""
    def __init__(self):
        """"""
        self.valor = 2
        self.descripcion = "La lista pasada como argumento no representa una matriz"

    def __str___(self):
        """"""
        return "[Error " + str(self.valor) + "] La cantidad de columnas no es la misma \
        en todas las filas\n"


class NoEsReal(ExcepcionMatlib):
    """El elemento de la lista no es un real."""
    def __init__(self):
        """"""
        self.valor = 3
        self.descripcion = "Un elemento de la lista no es de tipo numerico."

    def __str___(self):
        """"""
        return "[Error " + str(self.valor) + "] El elemento no se puede convertir a un \
        real."


class ErrorForma(ExcepcionMatlib):
    """Clase base para los errores de forma"""
    def __init__(self):
        """"""
        self.valor = 4
        self.descripcion = "La forma de la matriz no es adecuada."

    def __str___(self):
        """"""
        return "[Error " + str(self.valor) + "] " + self.descripcion


class NoEsCuadrada(ErrorForma):
    """La matriz no es cuadrada."""
    def __init__(self):
        """"""
        self.valor = 4
        self.descripcion = "La cantidad de filas y columnas de la matriz no es la misma."

    def __str___(self):
        """"""
        return "[Error " + str(self.valor) + "] La matriz no es una matriz cuadrada."


class NoEsTriInf(ErrorForma):
    """La matriz no es triangular inferior."""
    def __init__(self):
        """"""
        self.valor = 4
        self.descripcion = "La matriz no es triangular inferior."

    def __str___(self):
        """"""
        return "[Error " + str(self.valor) + "] " + self.descripcion


class NoEsTriSup(ErrorForma):
    """La matriz no es triangular superior."""
    def __init__(self):
        """"""
        self.valor = 4
        self.descripcion = "La matriz no es triangular superior."

    def __str___(self):
        """"""
        return "[Error " + str(self.valor) + "] " + self.descripcion


class NoEsDiagonal(ErrorForma):
    """La matriz no es diagonal."""
    def __init__(self):
        """"""
        self.valor = 4
        self.descripcion = "La matriz no es diagonal."

    def __str___(self):
        """"""
        return "[Error " + str(self.valor) + "] " + self.descripcion


class NoEsSimetrica(ErrorForma):
    """La matriz no es simetrica."""
    def __init__(self):
        """"""
        self.valor = 4
        self.descripcion = "La matriz no es simetrica."

    def __str___(self):
        """"""
        return "[Error " + str(self.valor) + "] " + self.descripcion


class DimensionesNoValidas(ExcepcionMatlib):
    """Las dimensiones involucradas no son adecuadas para la operacion deseada."""
    def __init__(self):
        """"""
        self.valor = 5
        self.descripcion = "La dimension no es correcta."

    def __str___(self):
        """"""
        return "[Error " + str(self.valor) + "] " + self.descripcion
