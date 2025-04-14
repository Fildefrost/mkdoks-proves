# Python Course

> Strings

```python
print("String_input")

# Para variables

nombre= "Jordi"
print(f"Hola, me llamo {nombre}")

Output: Hola me llamo Jordi
```

Entradas de texto, siempre en comillas

> Formats

```python
# Newline Character

print("\\n")

# backslash

print("\\\\")

# Comilla simple

print("\\'")

# Tabulador

print("\\t")

# Backspace

print("\\b")

```

> Tipos

Defineix el tipus de dada

```python
x = 10
print (type(x))
Output = <class 'ini'>

```

> Tipos de datos

```python
**Integer** = Numeros enteros > x = 4
**Float** = Numeros decimales > x = 2.5
```

> Listas

```python
example = [1,2,3]
example = [1,"prova", 10]

```

no mutable:

```python
example.append (4) > Attributte error

```

> Ordenar listas

```python
example = list{range(0,11)}
print (example)
Output: [0,1,2,3,4,5,6,7,8,9,10]

```

> Tuplas

```python
example = (1,2,3)
example1 = (("a","b","c") , (1,23))

mutable:

example.append (4) > 1,2,3,4

```

> Buscar funciones

```python
dir(__builtins__)
dir(list)
dir(str)
dir(dict)

```

> Ayuda funciones

```python
help (function)

```

> Diccionarios

```python
example = {'input1':value, 'input2':value, 'input3':value}

```

Ex:

```python
search_engines_users = {"google": 1000, "bing": 127000000, "duck duck go":12000000}

'google':Key
'1000': value key

```

> Añadir funciones

```python
example = [1,2,3,4]
plus = [5,6]
example.append (plus)
Output: [1,2,3,4,[5,6]]

```

> Extender funciones

<pre class="language-python"><code class="lang-python">example = [1,2,3,4]
plus = [5,6]
example.extend (plus)
Output: [1,2,3,4,5,6]
<strong>
</strong></code></pre>

#### INDEX

> Funciones de indice

```python
example = ['a','b','c','d']

print (example[1])
Output = ['b']
print example[0]
Output = ['a']
print example [1:3]
Output = ['b','c','d']

```

> Funciones de indice de numero

```python
example = ['hola',4,5,6]
print example [0]
Output: 'hola'

print example[0][2]
Output: 'l'

print example [1]
Output: 4

```

Para diccionarios

```python
Numbers:

example = {"Joan": 4, "Marta": 2, "Lluna": 8}
print ("Joan")
Output: 4

Strings:

example = {"mati": "Sol", "tarda": "nuvol", "nit": "pluja"}
print ("tarda")
Output = 'nuvol'

```

#### CONVERSION

> De tupla a lista

```python
1. >>> cool_tuple = (1, 2, 3)
2. >>> cool_list = list(cool_tuple)
3. >>> cool_list
4. [1, 2, 3]

```

> De lista a tupla

```python
1. >>> cool_list = [1, 2, 3]
2. >>> cool_tuple = tuple(cool_list)
3. >>> cool_tuple
4. (1, 2, 3)

```

> De string a lista

```python
1. >>> cool_string = "Hello"
2. >>> cool_list = list(cool_string)
3. >>> cool_list
4. ['H', 'e', 'l', 'l', 'o']

```

> De lista a string

```python
1. >>> cool_list = ['H', 'e', 'l', 'l', 'o']
2. >>> cool_string = str.join("", cool_list)
3. >>> cool_string
4. 'Hello'

```

> Definicion de funciones

```python
def nombre_funcion(parametro1, parametro2, ...):

		# Cuerpo de la función
		# Código que ejecutará la función

	return valor # Opcional, para devolver un resultado

'def':# Palabra clave que indica que estás definiendo una función
'nombre_funcion:'# El nombre que le das a la función.
'parametros:'# Valores que le puedes pasar a la función para que los use'
'return:'# (Opcional) La función puede devolver un valor utilizando `return`. Si no usas `return`, la función devuelve `None` por defecto.'

```

```python
Ex.1

def saludar(nombre="Amigo"):
	print(f"Hola, {nombre}!")

saludar() # Salida: Hola, Amigo!
saludar("Ana") # Salida: Hola, Ana!

```

> User Input

```python
#Opció 1

user_input = input("Posa el teu nom")
missatge = "Hola %s" % user_input
print (missatge)
# Posa en el %s el valor de user inmpu

# Per diferents variables:
nom = input ("Posa el teu nom:")
cognom = input ("Posa el teu cognom:")
message = "Hola %s %s" % (nom,cognom)
print(message)

------------------------------------------------------

# Opció 2
user_input = input("Posa el teu nom")
missatge = f"Hola {user_input}:"
print (missatge)

# Per diferents variables:
nom = input ("Posa el teu nom:")
cognom = input ("Posa el teu cognom:")

message = f"Hola {nom}{cognom}"

# Opció 3

1. name = "John"
2. surname = "Smith"

4. message = "Your name is {}. Your surname is {}".format(name, surname)
5. print(message)

```

#### **BUCLES**

> Bucle FOR

```python
values = [1,2,3,4,5]
for valor in values
	print (valor)

# Ex 1: Simple

colors = [1,2,3,4,5]
for color in colors:
	print (color)
# el color , representa los indices de la variable colors. El bucle seria : imprime cada indice (print color) que esta dentro de la variable colors

# Es 2: Usando operadores

colors = [11, 34.1, 98.2, 43, 45.1, 54, 54]

for color in colors:
    if isinstance (color,int) and color > 50 :
        print (color)

# Se pueden usar operadores para sumar condiciones (AND y OR)

# Ex 3: Llamando a funciones

def celsius_to_kelvin(cels):
return cels + 273.15 # esto es la formula que converite celsius a kelvin
for temperature in [9.1, 8.8, -270.15]: # se pasa una lista de temperaturas
	print(celsius_to_kelvin(temperature)) # imprime cada item de la lista, pasado por   la funcion celsius_to_kelvin

# Ex 4: Usando diccionarions

notas_estudiantes = {"Pol": 4, "Joan": 5, "Laia": 8}

for notas in notas_estudiantes.items():
	print (notas)

Output: ('Pol', 4) ('Joan', 5) ('Laia', 8)

# Para mostrar los nombres, usamos el valor "keys"
for notas in notas_estudiantes.keys():
Output: Pol ,Joan, Laia

# Para mostrar las notas, usamos el valor "values"
for notas in notas_estudiantes.values():
Output: 4,5,8

```

```python
Uso de FOR en diccionario formateando texto

# Ex 1: Iterando en los indices

phone_numbers = {"John": "+37682929928", "Marry": "+423998200919"}

for pair in phone_numbers.items():
	print(f"{pair[0]} has as phone number {pair[1]}")

# Ex 2: Iterando en las keys y values de la lista

phone_numbers = {"John": "+37682929928", "Marry": "+423998200919"}

for key, value in phone_numbers.items():
	print(f"{key} has as phone number {value}")

```

> Bucle WHILE

```python
a= 3

while a > 0:
	print(1)
	print(2)

Output:
1
2
1
2
1
2
.
.
.

# User INPUT example : Va demanant "Enter username" fins que coincideixi amb "marco"

username = ''

while username != "marco":
	username = input ("Enter username:")
```
