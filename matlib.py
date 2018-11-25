#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Libreria destinada al manejo de matrices. """

from errores import *

###############################################################################
# ZONA DE COMENTARIOS
###############################################################################


def version():
    '''Version del modulo "matlib.py"
    v1.0
    Autor: Martin S. Lopez Paglione
    Octubre de 2014'''
    return "1.0"


def info_versiones(ver):
    '''Informacion de las versiones como historial de cambios y actualizaciones, fecha, y
    autor y colaboradores.
    El parametro "ver" es un string con la version a devolver, compatible con el valor 
    devuelto por la funcion version(). La variable de retorno es
    una tupla con descripcion de la version, fecha de creacion, y autor.
    Si ver = "todo" se devuelve un diccionario con todas las versiones.'''

    h = {'1.0': ('''Primera version del modulo.
    Las clases definidas son:
        matriz
    Las funciones disponibles son:
        calcular
        cofactor
        determinante
        diagonal
        diagonal2
        dimension
        elemento
        esdiag
        essimetrica
        estriinf
        estrisup
        identidad
        lup
        movcol
        movfil
        submatriz
        sustad
        sustat
        transpuesta''', 'Octubre 2014', 'Martin S. Lopez Paglione')}

    if ver in h:
        return h[ver]
    elif ver == "todo":
        return h
    else:
        raise ExcepcionVersion(ver)


class matriz(object):
    """Clase principal de la libreria. Esta clase define on objeto llamado 'matriz' y que
    esta destinado a almacenar de forma correcta las matrices que posteriormente se
    usaran en los distintos metodos y funciones."""

    def __init__(self, mat):
        """Rutina de inicializacion de la clase. La variable mat contiene una lista de
        listas haciendo referencia a las filas y columnas. Los elementos de estas listas
        deben ser numeros reales."""

        #Convierto los elementos de la matriz en float. Si alguno no se puede lanzo la
        #excepcion. Ademas aprovecho para conocer la dimension.
        cantfil = len(mat)
        cantcol = len(mat[0])
        mataux = []
        for i in range(0, len(mat)):
            f = mat[i]
            if len(f) != cantcol:
                raise NoEsMatriz()

            filaux = []
            for j in range(0, cantcol):
                l = f[j]
                if isinstance(l, (int, float, long)):
                    filaux.append(float(l))
                else:
                    raise NoEsReal()

            mataux.append(filaux)

        self._mat = mataux
        self.cantfilas = cantfil
        self.cantcolumnas = cantcol

    def __repr__(self):
        """Imprime la matriz con solo llamarla desde el interprete."""
        return self.__str__()

    def __str__(self):
        """Representacion de la matriz con formato string"""

        a = ''
        for b in self._mat:
            for c in b:
                a = a + '{0:.4f}'.format(c) + '   '
            a = a + '\n'

        return a

    def __add__(self, otro):
        """Suma de matrices."""
        if self.dimension()[0] != otro.dimension()[0] or self.dimension()[1] != \
        otro.dimension()[1]:
            raise DimensionesNoValidas()

        suma = []
        for fs, fo in zip(self.filas(), otro.filas()):
            fil = []
            for i, j in zip(fs, fo):
                fil.append(i + j)
            suma.append(fil)
        return matriz(suma)

    __radd__ = __add__

    def __sub__(self, otro):
        """Resta de matrices"""
        return (self + (-otro))

    def __rsub__(self, otro):
        """Resta de matrices"""
        return (otro + (-self))

    def __mul__(self, otro):
        """Multiplicacion de matrices"""
        if isinstance(otro, (int, float, long)):
            multip = []
            for f in self.filas():
                fila = []
                for c in f:
                    fila.append(otro * c)
                multip.append(fila)
        else:
            if self.dimension()[1] != otro.dimension()[0]:
                raise DimensionesNoValidas()

            multip = []
            for fil in self.filas():
                fila = []
                for col in otro.columnas():
                    elem = 0
                    for i, j in zip(fil, col):
                        elem += i * j
                    fila.append(elem)
                multip.append(fila)

        return matriz(multip)

    def __rmul__(self, otro):
        """Multiplicacion de matrices"""
        if isinstance(otro, (int, float, long)):
            multip = []
            for f in self.filas():
                fila = []
                for c in f:
                    fila.append(otro * c)
                multip.append(fila)
        else:
            multip = []
            for fil in otro.filas():
                fila = []
                for col in self.columnas():
                    elem = 0
                    for i, j in zip(fil, col):
                        elem += i * j
                    fila.append(elem)
                multip.append(fila)

        return matriz(multip)

    def __neg__(self):
        """Devuelve la matriz negativa"""
        neg = []
        for f in self.filas():
            fila = []
            for c in f:
                fila.append(-c)
            neg.append(fila)
        return matriz(neg)

    def __len__(self):
        """Devuelve la longitud de la matriz. Solo matrices cuadradas o vectores."""
        if self.cantcolumnas == self.cantfilas or self.cantcolumnas == 1:
            return self.cantfilas
        elif self.cantfilas == 1:
            return self.cantcolumnas
        else:
            raise NoEsCuadrada()

    def __getitem__(self, p):
        """Devuelve el item indicado mediante el uso de corchetes.
        Ejemplo: Si tenemos una matriz A como la siguiente

                1  2  3
            A = 4  5  6
                7  8  9

        El elemento de la fila 3 columna 1 se puede obtener de la siguiente forma

            A31 = A[3,1]

        El valor resultante de A31 es 7
        """
        i, j = p
        if i <= self.cantfilas and j <= self.cantcolumnas:
            return self._mat[i - 1][j - 1]
        else:
            raise IndiceDesbordado()

    def __setitem__(self, p, v):
        """Asigna al elemento indicado mediante corchetes en el lado izquierdo de una
        asignacion el valor que se encuentra al lado derecho de la asignacion.
       Ejemplo: Si tenemos una matriz A como la siguiente

                1  2  3
            A = 4  5  6
                7  8  9

        El elemento de la fila 3 columna 1 se puede modificar de la siguiente forma

            A[3,1] = v

        El valor resultante de A[3,1] es lo que contiene la variable v."""

        i, j = p
        if i > self.cantfilas or j > self.cantcolumnas:
            raise IndiceDesbordado()
        if not isinstance(v, (int, long, float)):
            raise NoEsReal()

        self._mat[i - 1][j - 1] = float(v)
        return matriz(self._mat)

    def dimension(self):
        """Devuelve una tupla con las dimensiones de la matriz."""
        return dimension(self)

    def elemento(self, i, j):
        """Devuelve el elemento (i,j) de la matriz. Es lo mismo que hacer A[i,j].
        Ejemplo:
            ej1 = A.elemento(i, j)
            es lo mismo que hacer
            ej2 = A[i,j]
            Las variables ej1 y ej2 son iguales."""
        return self[i, j]

    def fila(self, i):
        """Devuelve en una lista la i-esima fila."""
        if i <= self.cantfilas:
            return self._mat[i - 1]
        else:
            raise IndiceDesbordado()

    def filas(self):
        """Devuelve un generador con las filas de la matriz."""
        for i in self._mat:
            yield i

    def columna(self, j):
        """Devuelve en una lista la j-esima columna."""
        if j <= self.cantcolumnas:

            col = []
            for fila in self.filas():
                col.append(fila[j - 1])
            return col
        else:
            raise IndiceDesbordado()

    def columnas(self):
        """Devuelve un generador con las columnas de la matriz."""
        for j in range(1, self.cantcolumnas + 1):
            yield self.columna(j)

    def diagonal(self):
        """Devuelve en una lista los elementos de la diagonal principal."""
        return diagonal(self)

    def diagonal2(self):
        """Devuelve en una lista los elementos de la diagonal secundaria."""
        return diagonal2(self)

    def transpuesta(self):
        """Devuelve la matriz transpuesta."""
        return transpuesta(self)

    def submatriz(self, fil, col):
        """Devuelve la submatriz compuesta por las filas y columnas indicadas. Los
        parametros fil y col son tuplas donde en fil se colocan desde cual hasta cual
        fila de M extraer y en col lo mismo para las columnas. Si los valores son
        negativos, entonces es la matriz resultante de eliminar esas filas."""
        return submatriz(self, fil, col)

    def cofactor(self, i, j):
        """Devuelve el cofactor i, j de la matriz."""
        return cofactor(self, i, j)

    def determinante(self):
        """Determinante de una matriz."""
        return determinante(self)

    def menor(self, i, j):
        """Devuelve el determinante de la matriz resultante al eliminar la fila i y
        columna j. """
        subm = submatriz(self, (-i, -i), (-j, -j))
        return subm.determinante()


def elemento(M, i, j):
    """Devuelve el elemento (i,j) de la matriz M."""
    return M[i, j]


def diagonal(M):
    """Devuelve en una lista los elementos de la diagonal principal de M."""
    if M.cantfilas != M.cantcolumnas:
        raise NoEsCuadrada()

    col = 0
    diag = []
    for fil in M.filas():
        diag.append(fil[col])
        col += 1
    return diag


def diagonal2(M):
    """Devuelve en una lista los elementos de la diagonal secundaria de M."""
    if M.cantfilas != M.cantcolumnas:
        raise NoEsCuadrada()

    col = 0
    diag = []
    for fil in M.filas():
        col -= 1
        diag.append(fil[col])
    return diag


def submatriz(M, fil, col):
    """Devuelve la submatriz compuesta por las filas y columnas indicadas. Los parametros
    fil y col son tuplas donde en fil se colocan desde cual hasta cual fila de M extraer
    y en col lo mismo para las columnas. Si los valores son negativos, entonces es la
    matriz resultante de eliminar esas filas."""
    fi, ff = fil
    ci, cf = col

    if abs(fi) > M.cantfilas or abs(ff) > M.cantfilas or \
    abs(ci) > M.cantcolumnas or abs(cf) > M.cantcolumnas:
        raise IndiceDesbordado()

    #Extraigo las filas.
    filas = []
    #Indices positivos
    if fi > 0 and ff > 0:
        direccion = ff - fi
        if direccion >= 0:
            for i in range(fi, ff + 1):
                filas.append(M.fila(i))
        else:
            raise IndicesInvertidos()

    #Indices negativos. Quito las filas marcadas y me quedo con las otras.
    elif fi < 0 and ff < 0:
        direccion = ff - fi
        if direccion <= 0:
            rango = range(abs(fi), abs(ff) + 1)
            for i, v in enumerate(M.filas()):
                if i + 1 not in rango:
                    filas.append(v)
        else:
            raise IndicesInvertidos()
    else:
        raise IndiceDesbordado()

    #Columnas
    columnas = []
    #Indices positivos
    if ci > 0 and cf > 0:
        direccion = cf - ci
        if direccion >= 0:
            for i in filas:
                fils = []
                for j in range(ci - 1, cf):
                    fils.append(i[j])
                columnas.append(fils)
        else:
            raise IndicesInvertidos()

    #Indices negativos. Quito las filas marcadas y me quedo con las otras.
    elif ci < 0 and cf < 0:
        direccion = cf - ci
        if direccion <= 0:
            rango = range(abs(ci) - 1, abs(cf))
            maximo = len(filas[0])
            for i in filas:
                fils = []
                for j in range(0, maximo):
                    if j not in rango:
                        fils.append(i[j])
                columnas.append(fils)
        else:
            raise IndicesInvertidos()

    else:
        raise IndiceDesbordado()

    return matriz(columnas)


def transpuesta(M):
    """Devuelve la matriz transpuesta de M."""
    trans = []
    for col in M.columnas():
        trans.append(col)
    return matriz(trans)


def dimension(M):
    """Devuelve una tupla (filas, columnas) con las dimensiones de la matriz M."""
    return M.cantfilas, M.cantcolumnas


def cofactor(M, i, j):
    """Devuelve el cofactor i, j de la matriz M."""
    if i <= M.cantfilas and j <= M.cantcolumnas:
        #subm = submatriz(M, (-i, -i), (j, -j))
        cof = ((-1) ** (i + j)) * M.menor(i, j)
        return cof
    else:
        raise IndiceDesbordado()


def determinante(M):

    """Determinante de la matriz M."""

    dimension = len(M)

    #Si la matriz es triangular, por propiedad, det(A)=a11.a22.a33...ann
    det = 1
    if estrisup(M) or estriinf(M):
        for i in range(1, dimension + 1):
            det *= M[i, i]
        return det

    #Como no es triangular lo calculo por cofactores
    if dimension == 1:
        # Es un escalar
        return M[0, 0]
    else:
        # Es una matriz
        det = 0
        for j, n in enumerate(M.fila(1)):
            det = det + M[1, j + 1] * M.cofactor(1, j + 1)
        return det


def movfil(M, u, v):
    """Intercambia las filas u y v"""
    aux = []
    i = 1
    for f in M.filas():
        if i == u:
            aux.append(M.fila(v))
        elif i == v:
            aux.append(M.fila(u))
        else:
            aux.append(f)
        i += 1
    return matriz(aux)


def movcol(M, u, v):
    """Intercambia las columnas u y v"""
    aux = []
    j = 1
    for f in M.columnas():
        if j == u:
            aux.append(M.columna(v))
        elif j == v:
            aux.append(M.columna(u))
        else:
            aux.append(f)
        j += 1
    return transpuesta(matriz(aux))


def identidad(n):
    """Devuelve la matriz identidad de n x n."""
    aux = []
    for i in range(0, n):
        f = []
        for j in range(0, n):
            f.append(i == j)
        aux.append(f)
    return matriz(aux)


def lup(M):
    """Devuelve una tupla de 3 elementos, donde el primer y segundo elemento son las
    matrices resultantes de la descomposicion L-U de la matriz pasada y el tercer
    elemento es la matriz de pivoteo empleada por el metodo."""

    #Dimension de M
    n = len(M)

    #Copio una matriz U para no perder M
    U = []
    for f in M.filas():
        U.append(f)
    U = matriz(U)

    #Inicializo L y P
    L = identidad(n)
    P = identidad(n)

    #Repito para cada columna
    for k in range(1, n):
        #Pivoteo
        c = U.columna(k)
        auxc = c[k - 1:]
        m = auxc.index(max(auxc)) + k - 1
        piv = False
        if c[m] > c[k - 1]:
            U = movfil(U, m + 1, k)
            P = movfil(P, m + 1, k)
            piv = True
        #Fin pivoteo

        for i in range(k + 1, n + 1):
            factor = U[i, k] / U[k, k]
            L[i, k] = factor
            if piv:  # Si hay pivoteo cambio tambien las filas de L
                for li in range(1, k):
                    inter = L[k, li]
                    L[k, li] = L[m + 1, li]
                    L[m + 1, li] = inter

            U[i, k] = 0
            for j in range(k + 1, n + 1):
                U[i, j] = U[i, j] - factor * U[k, j]

    return (L, U, P)


def estriinf(M):
    """Verifica si la matriz pasada es triangular inferior. Deveuelve False o True"""
    n = len(M)
    res = True
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            if M[i, j] != 0:
                res = False

    return res


def estrisup(M):
    """Verifica si la matriz pasada es triangular superior. Deveuelve False o True"""
    n = len(M)
    res = True
    for j in range(1, n):
        for i in range(j + 1, n + 1):
            if M[i, j] != 0:
                res = False

    return res


def esdiag(M):
    """Verifica si la matriz pasada es diagonal. Devuelve False o True"""
    return estrisup(M) and estriinf(M)


def essimetrica(M):
    """Verifica si la matriz pasada es simetrica. Devuelve True o False"""
    n = len(M)
    res = True
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            if M[i, j] != M[j, i]:
                res = False

    return res


def sustad(L, b):
    """Realiza la sustitucion hacia adelante y devuelve el vector de resultados. La
    matriz L debe ser triangular inferior, y el vector b es el lado derecho del sistema
    y debe tener la misma dimension que la matriz."""

    if not estriinf(L):
        raise NoEsTriInf()

    n = len(L)
    if n != len(b):
        raise DimensionesNoValidas()

    x = []
    for i in range(1, n + 1):
        sumat = 0
        for j, val in enumerate(x):
            sumat += L[i, j + 1] * val
        x.append((float(b[i - 1]) - sumat) / L[i, i])

    return x


def sustat(U, b):
    """Realiza la sustitucion hacia atras y devuelve el vector de resultados. La
    matriz U debe ser triangular superior, y el vector b es el lado derecho del sistema
    y debe tener la misma dimension que la matriz."""

    if not estrisup(U):
        raise NoEsTriSup()

    n = len(U)
    if n != len(b):
        raise DimensionesNoValidas()

    x = []
    for i in range(n, 0, -1):
        sumat = 0
        for j, val in enumerate(x):
            sumat += U[i, n - j] * val
        x.append((float(b[i - 1]) - sumat) / U[i, i])

    x.reverse()
    return x


def calcular(A, b):
    """Calcula la solucion del sistema Ax = b. La matriz A debe ser no singular."""

    #Verifico si es triangular. Si es asi me ahorro la descomposicion
    if estrisup(A):
        x = sustat(A, b)

    elif estriinf(A):
        x = sustad(A, b)

    else:
        l, u, p = lup(A)
        b2 = (p * matriz([b]).transpuesta()).columna(1)
        c = sustad(l, b2)
        x = sustat(u, c)

    return x