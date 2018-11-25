#! /usr/bin/env python
#*-* encoding: utf-8 *-*
"""Modulo con distintos metodos numericos para busqueda de raices.
El modulo contiene variables de configuracion general que son usadas por varios de los
metodos implementados en este modulo. Estas variables tienen un valor por defecto y para
que un metodo utilice otro valor hay que cambiar el valor por defecto por el valor
deseado. Las variables y sus valores son:

  N = 100
    Es la cantidad de iteraciones maximas que utilizaran los metodos iterativos. Si las
    iteraciones del metodo superan este valor sale del bucle de iteracion, devolviendo lo
    correspondiente en cada caso.

  TOL = 1e-10
    Es la tolerancia permitida en el error relativo aproximado porcentual. Este sera el
    criterio de parada en los metodos iterativos. Si la cantidad de iteraciones supera el
    valor permitido, aumentar la tolerancia puede ayudar, aunque se pierde precision en
    el resultado obtenido.

  CANTSUBINT = 1000
    Es la cantidad de subintervalos en los que se divide el intervalo principal en los
    metodos por inspeccion.
    """

from errores import *
from math import *


def version():
    '''Version del modulo "raices.py"
    v1.0
    Autor: Martin S. Lopez Paglione
    Septiembre de 2014'''
    return "1.1"


def info_versiones(ver):
    '''Informacion de las versiones como historial de cambios y actualizaciones, fecha, y
    autor y colaboradores.
    El parametro "ver" es un string con la version a devolver. Si ver = "todo" se
    devuelve un diccionario con todas las versiones'''

    h = {'1.0': ('''Primera version del modulo.
    Los atributos globales son:
        CANTSUBINT
        N
        TOL
    Las funciones disponibles son:
        biseccion
        err
        evalx
        falsapos
        historial_versiones
        incremental
        newtonraphson
        puntofijo
        secante
        version''', 'Septiembre 2014', 'Martin S. Lopez Paglione'),
        '1.1': ('Se modifico la funcion evalx para poder evaluar sistemas de ecuaciones',
                'Octubre 2014', 'Martin S. Lopez Paglione')}

    if ver in h:
        return h[ver]
    elif ver == "todo":
        return h
    else:
        raise ExcepcionVersion(ver)


#Parametros generales de configuracion de los metodos
N = 100
TOL = 1e-10
CANTSUBINT = 1000


#Funciones utilizadas en los metodos
def evalx(fun, x):
    """Evalua la funcion fun en el valor x y retorna el resultado.
    Si x es un numero, se evaluara ese valor en donde exista la variable x en fun. Para
    evaluar otra variable, o pasar mas valores de variables x debe ser un diccionario con
    el nombre de variable y su valor.
    Si fun es una lista o tupla de funciones se evalua x para cada funcion. El resultado
    sera una lista de la misma longitud que fun con la evaluacion correspondiente a cada
    funcion.
    Esta funcion es util para evaluar sistemas de ecuaciones.
    Para mejor comprension ver el ejemplo siguiente:

        >>> f = ('x ** 2 + y', 'y ** 2 + z', 'z ** 2 + x')
        >>> valores = {'x': 3, 'y': 4, 'z': 5}
        >>> result = evalx(f, valores)
        >>> print result
        [13, 21, 28]

    Como se puede apreciar las variables 'x', 'y' y 'z' adoptaron los valores indicados
    en el diccionario 'valores' y luego se evaluaron las expresiones en 'f'.
    Si las ecuaciones de 'f' solo dependen de x se puede obviar el diccionario, pasando
    directamente el valor de x.

        >>> f = ('x ** 2', 'x ** 3', 'x ** 4')
        >>> result = evalx(f, 2)
        >>> print result
        [4, 8, 16]

    La variable x tomo el valor 2 sin indicar en la llamada a que variable asignar ese
    valor. Notar que la expresion
        >>> evalx(f, {'x':2})
    es equivalente a hacer
        >>> evalx(f, 2)
        """

    if isinstance(x, dict):
        if isinstance(fun, str):
            res = eval(fun, x)
            return res
        else:
            res = []
            for f in fun:
                res.append(evalx(f, x))
            return res
    else:
        if isinstance(fun, str):
            res = eval(fun)
            return res
        else:
            res = []
            for f in fun:
                res.append(eval(f))
            return res


def err(xold, xnew):
    """Calcula el error aproximado porcentual entre xnueva y xvieja"""
    e = abs(float(xnew - xold) / xnew) * 100
    return e


#Distintos metodos para busqueda de raices
def incremental(fun, lim):
    """Busqueda de raices por el metodo incremental. En este metodo se debe pasar un
    intervalo donde estaran la o las raices a buscar.
    Los parametros de entrada son:
      fun: funcion a la cual se le debe encontrar las raices. Debe ser pasada como string
      lim: es una tupla que contiene el intervalo donde buscar

    La salida de la funcion es una lista que contiene tuplas con los intervalos
    encontrados. En cada intervalo solo habra una sola raiz.

    El subintervalo inicial se particiona en 1000 subintervalos donde buscara las raices.
    Para cambiar este valor usar la variable a nivel de modulo CANTSUBINT"""

    #Particiono el intervalo inicial en n subintervalos
    xl, xu = lim
    delta = xu - xl
    minidelta = float(delta) / CANTSUBINT
    subint = []
    for i in range(CANTSUBINT):
        subint.append([xl + minidelta * i, xl + (minidelta * (i + 1))])

    #Variable para almacenar el resultado
    res = []

    #Recorrido incremental
    for interv in subint:
        fxl = evalx(fun, interv[0])
        fxu = evalx(fun, interv[1])
        if fxl * fxu < 0 or fxl == 0:
            res.append(interv)

    return res


def biseccion(fun, lim):
    """Metodo de la biseccion para encontrar las raices de una funcion. Es importante que
    exista una y solo una raiz en cada intervalo pasado, de lo contrario el metodo falla.
    El metodo tambien falla si la funcion tiene raices multiples en algun intervalo, o si
    no es continua en el intervalo pasado.

    Los parametros son:
      fun: funcion a la cual se le debe encontrar la raiz.
      lim: es una tupla que contiene tuplas con los inervalos donde buscar

    La salida de la funcion es una lista que contiene tuplas. Cada tupla sera un
    resultado con la raiz correspondiente y otros datos. Estas estan formadas como sigue:
      res[0] : La raiz buscada
      res[1] : El valor de la funcion evaluada en esa raiz (dado que es una aproximacion)
      res[2] : El error relativo aproximado porcentual
      res[3] : La cantidad de iteraciones usadas hasta llegar al resultado

    Si se superan la cantidad de iteraciones permitidas los valores [0] y [1] contendran
    None, mientras que [2] y [3] tendran el valor de error alcanzado y la cantidad de
    iteraciones usadas."""

    res = []
    for inter in lim:
        #Inicializacion
        e = 100
        xl, xu = inter
        xr = xl
        fxl = evalx(fun, xl)
        n = 0

        #Procedo con el metodo
        while e > TOL and n <= N:
            xrant = xr

            #estimacion de la raiz
            xr = float(xu + xl) / 2
            fxr = evalx(fun, xr)
            n = n + 1
            if xr != 0:
                e = err(xrant, xr)

            test = fxl * fxr
            if test < 0:
                xu = xr
            elif test > 0:
                xl = xr
                fxl = fxr
            else:
                e = 0

            r = xr
            n = n + 1

        #Armo la tupla de resultado individual
        if n > N:
            raux = (None, None, e, n)
        else:
            raux = (r, fxr, e, n)

        #Agrego la tupla de resultado individual a la de resultado general
        res.append(raux)

    #Devuelvo el resultado general
    return res


def falsapos(fun, lim):
    """Metodo de la biseccion para encontrar las raices de una funcion. Es importante que
    exista una y solo una raiz en cada intervalo pasado, de lo contrario el metodo falla.
    El metodo tambien falla si la funcion tiene raices multiples en algun intervalo, o si
    no es continua en el intervalo pasado.

    Los parametros son:
      fun: funcion a la cual se le debe encontrar la raiz.
      lim: es una tupla que contiene tuplas con los inervalos donde buscar

    La salida de la funcion es una lista que contiene tuplas. Cada tupla sera un
    resultado con la raiz correspondiente y otros datos. Estas estan formadas como sigue:
      res[0] : La raiz buscada
      res[1] : El valor de la funcion evaluada en esa raiz (dado que es una aproximacion)
      res[2] : El error relativo aproximado porcentual
      res[3] : La cantidad de iteraciones usadas hasta llegar al resultado

    Si se superan la cantidad de iteraciones permitidas los valores [0] y [1] contendran
    None, mientras que [2] y [3] tendran el valor de error alcanzado y la cantidad de
    iteraciones usadas."""

    res = []
    for inter in lim:
        #Inicializacion
        e = 100
        xl, xu = inter
        xr = xl
        fxl = evalx(fun, xl)
        fxu = evalx(fun, xu)
        n = 0

        #Procedo con el metodo
        while e > TOL and n <= N:
            xrant = xr

            #estimacion de la raiz
            xr = xu - (fxu * (xl - xu) / (fxl - fxu))
            fxr = evalx(fun, xr)
            n = n + 1
            if xr != 0:
                e = err(xrant, xr)

            test = fxl * fxr
            if test < 0:
                xu = xr
                fxu = fxr
            elif test > 0:
                xl = xr
                fxl = fxr
            else:
                e = 0

        r = xr

        #Armo la tupla de resultado individual
        if n > N:
            raux = (None, None, e, n)
        else:
            raux = (r, fxr, e, n)

        #Agrego la tupla de resultado individual a la de resultado general
        res.append(raux)

    #Devuelvo el resultado general
    return res


def secante(fun, inis, ini2=0.5):
    """Metodo de la secante para la busqueda de raices. Devuelve una lista con las raices
    encontradas. La cantidad de raices encontradas no es exactamente la cantidad
    de raices que tenga la funcion.
    Los parametros son:
        fun: funcion a la cual se le debe encontrar las raices.
        inis: tupla con los valores iniciales. Para cada valor de la tupla se hara una
              busqueda.
        ini2: es un valor opcional y es el valor para tomar la secante de la primera
              iteracion. Si se omite este valor se toma 0.5 por defecto.

    La salida de la funcion es una lista que contiene tuplas. Cada tupla sera un
    resultado con la raiz correspondiente y otros datos. Estas estan formadas como sigue:
      res[0] : La raiz buscada
      res[1] : El valor de la funcion evaluada en esa raiz (dado que es una aproximacion)
      res[2] : El error relativo aproximado porcentual
      res[3] : La cantidad de iteraciones usadas hasta llegar al resultado

    Si dos valores iniciales dan raices cuya cercania es menor al error admitido se
    considerara que los resultados son dos aproximaciones distintas a la misma raiz y se
    devolvera solo la de menor error relativo aproximado.
    """

    res = []
    for ini in inis:
        #Inicializacion
        e = 100
        n = 0
        xi = float(ini)
        xold = xi - ini2
        fxi = evalx(fun, xi)
        fxold = evalx(fun, xold)

        #Procedo con el metodo
        while e > TOL and n <= N:
            n = n + 1

            #estimacion de la raiz
            if (fxold - fxi) != 0:
                xnew = xi - (fxi * (xold - xi) / (fxold - fxi))

            fxnew = evalx(fun, xnew)
            if xnew != 0:
                e = err(xi, xnew)

            #Preparo las variables para la iteracion siguiente. Si sale del while no va a
            #usarse pero las preparo igual
            xold = xi
            fxold = fxi
            xi = xnew
            fxi = fxnew

        #Armo la tupla de resultado individual
        if n < N:
            raux = (xi, fxi, e, n)

            #Agrego la tupla de resultado individual a la de resultado general
            #Para agregarla comparo los resultados anteriores
            ag = False  # Flag de raiz agregada
            for ant in range(0, len(res)):
                if raux[0] != 0:
                    e2 = err(res[ant][0], raux[0])
                else:
                    if res[ant][0] != 0:
                        e2 = err(raux[0], ant[0])
                    else:
                        e2 = 0

                if e2 < TOL:
                    if raux[2] < res[ant][2]:
                        res[ant] = raux
                    ag = True

            #Si no ha sido agregada es que es una raiz distinta y la agrego ahora
            if not ag:
                res.append(raux)

    #Devuelvo el resultado general
    return res


def newtonraphson(fun, dfun, inis):
    """Metodo de Newton-Raphson para la busqueda de raices. Devuelve una lista con las
    raices encontradas. La cantidad de raices encontradas no es exactamente la cantidad
    de raices que tenga la funcion.
    Los parametros son:
        fun: funcion a la cual se le debe encontrar las raices.
        dfun: derivada de la funcion fun.
        inis: tupla con los valores iniciales. Para cada valor de la tupla se hara una
              busqueda.

    La salida de la funcion es una lista que contiene tuplas. Cada tupla sera un
    resultado con la raiz correspondiente y otros datos. Estas estan formadas como sigue:
      res[0] : La raiz buscada
      res[1] : El valor de la funcion evaluada en esa raiz (dado que es una aproximacion)
      res[2] : El error relativo aproximado porcentual
      res[3] : La cantidad de iteraciones usadas hasta llegar al resultado

    Si dos valores iniciales dan raices cuya cercania es menor al error admitido se
    considerara que los resultados son dos aproximaciones distintas a la misma raiz y se
    devolvera solo la de menor error relativo aproximado.
    """

    res = []
    for ini in inis:
        #Inicializacion
        e = 100
        n = 0
        xi = float(ini)
        fxi = evalx(fun, xi)
        dfxi = evalx(dfun, xi)

        #Procedo con el metodo
        while e > TOL and n <= N:
            n = n + 1

            #estimacion de la raiz
            if dfxi != 0:
                xnew = xi - (fxi / dfxi)
            else:
                n = N + 1

            fxnew = evalx(fun, xnew)
            if xnew != 0:
                e = err(xi, xnew)

            #Preparo las variables para la iteracion siguiente. Si sale del while no va a
            #usarse pero las preparo igual
            xi = xnew
            fxi = fxnew
            dfxi = evalx(dfun, xnew)

        #Armo la tupla de resultado individual
        if n < N:
            raux = (xi, fxi, e, n)

            #Agrego la tupla de resultado individual a la de resultado general
            #Para agregarla comparo los resultados anteriores
            ag = False  # Flag de raiz agregada
            for ant in range(0, len(res)):
                if raux[0] != 0:
                    e2 = err(res[ant][0], raux[0])
                else:
                    if res[ant][0] != 0:
                        e2 = err(raux[0], ant[0])
                    else:
                        e2 = 0

                if e2 < TOL:
                    if raux[2] < res[ant][2]:
                        res[ant] = raux
                    ag = True

            #Si no ha sido agregada es que es una raiz distinta y la agrego ahora
            if not ag:
                res.append(raux)

    #Devuelvo el resultado general
    return res


def puntofijo(fun, inis):
    """Metodo de punto fijo para la busqueda de raices. Devuelve una lista con las
    raices encontradas. La cantidad de raices encontradas no es exactamente la cantidad
    de raices que tenga la funcion.
    Los parametros son:
        fun: funcion a la cual se le debe encontrar las raices.
        inis: tupla con los valores iniciales. Para cada valor de la tupla se hara una
              busqueda.

    La salida de la funcion es una lista que contiene tuplas. Cada tupla sera un
    resultado con la raiz correspondiente y otros datos. Estas estan formadas como sigue:
      res[0] : La raiz buscada
      res[1] : El valor de la funcion evaluada en esa raiz (dado que es una aproximacion)
      res[2] : El error relativo aproximado porcentual
      res[3] : La cantidad de iteraciones usadas hasta llegar al resultado

    Si dos valores iniciales dan raices cuya cercania es menor al error admitido se
    considerara que los resultados son dos aproximaciones distintas a la misma raiz y se
    devolvera solo la de menor error relativo aproximado.
    """

    res = []
    for ini in inis:
        #Inicializacion
        e = 100
        n = 0
        gx = '(' + fun + ') + x'  # gx sera la funcion auxiliar que se usa en el metodo
        xr = float(ini)

        #Procedo con el metodo
        while e > TOL and n <= N:
            n = n + 1

            xold = xr
            xr = evalx(gx, xold)
            if xr != 0:
                e = err(xold, xr)

        #Armo la tupla de resultado individual
        if n < N:
            raux = (xr, evalx(fun, xr), e, n)

            #Agrego la tupla de resultado individual a la de resultado general
            #Para agregarla comparo los resultados anteriores
            ag = False  # Flag de raiz agregada
            for ant in range(0, len(res)):
                if raux[0] != 0:
                    e2 = err(res[ant][0], raux[0])
                else:
                    if res[ant][0] != 0:
                        e2 = err(raux[0], ant[0])
                    else:
                        e2 = 0

                if e2 < TOL:
                    if raux[2] < res[ant][2]:
                        res[ant] = raux
                    ag = True

            #Si no ha sido agregada es que es una raiz distinta y la agrego ahora
            if not ag:
                res.append(raux)

    # Devuelvo el resultado general
    return res