Pokémon HM Compatibility Checker (Generations 1–3)

Este repositorio contiene un script en Python que consulta PokéAPI v2 para identificar qué Pokémon pueden aprender todos los HM relevantes en distintos juegos de las generaciones 1, 2 y 3, restringiendo el análisis al moveset propio de cada juego.

El objetivo es ofrecer un chequeo sistemático y reproducible, evitando mezclar generaciones, versiones o métodos de aprendizaje.

¿Qué hace el script?

Para cada juego clásico (Red/Blue, Yellow, Gold/Silver, Crystal, Ruby/Sapphire, Emerald, FireRed/LeafGreen), el script:

Define un pool de Pokémon según la generación del juego:

Gen 1 → Pokémon de Gen 1

Gen 2 → Pokémon de Gen 1 + 2

Gen 3 → Pokémon de Gen 1 + 2 + 3

Define el conjunto de HM relevantes para ese juego, respetando las diferencias históricas entre generaciones y versiones:

Gen 1: cut, surf, strength

Gen 2: cut, surf, strength, waterfall, whirlpool

Gen 3 (Ruby/Sapphire/Emerald): surf, strength, rock-smash, waterfall, dive

Gen 3 (FireRed/LeafGreen): cut, surf, strength, rock-smash, waterfall

Consulta PokéAPI y verifica, para cada Pokémon del pool:

si puede aprender cada HM en ese juego específico

usando exclusivamente el método de aprendizaje machine (TM/HM en PokéAPI)

filtrando explícitamente por version_group (el identificador del juego)

Aplica una condición fuerte:

Un Pokémon es considerado válido solo si puede aprender todos los HM exigidos en ese juego.

Si un HM no existe como movimiento aprendible por máquina en ese juego, se ignora automáticamente para evitar falsos negativos.

Exporta los resultados como un archivo CSV por juego, conteniendo únicamente la lista de Pokémon que cumplen la condición.

Qué NO hace (decisiones conscientes)

El script no:

distingue entre HM y TM dentro de machine (PokéAPI no los separa)

modela restricciones narrativas del juego (medallas, progreso, etc.)

considera en qué momento del juego se obtiene el HM

mezcla datos entre juegos o generaciones

Estas exclusiones son deliberadas para mantener un modelo claro, verificable y alineado con la estructura real de PokéAPI.

Detalle técnico clave: species vs. Pokémon

PokéAPI distingue entre:

pokemon-species (ej. deoxys)

pokemon (ej. deoxys-normal)

Para evitar errores (HTTP 404), el script:

resuelve cada especie a su variedad por defecto

y usa ese identificador para consultar el moveset

Este paso es fundamental para la compatibilidad completa del análisis.

Requisitos

Python 3.9 o superior

Dependencias:

pip install requests


No se utilizan librerías externas para el export CSV.

Salida

El script genera un archivo CSV por juego, por ejemplo:

red-blue.csv

yellow.csv

gold-silver.csv

crystal.csv

ruby-sapphire.csv

emerald.csv

firered-leafgreen.csv

Cada archivo contiene una sola columna:

pokemon
kingler
krabby
lickitung
mew

Fuente de datos

Todos los datos provienen de PokéAPI v2:
https://pokeapi.co/

Uso esperado

Este script está pensado para:

análisis comparativo entre juegos y generaciones

estudios de diseño y balance histórico

investigación sobre restricciones de progresión

generación de datasets reproducibles

Licencia

Este texto y el código fueron realizados mayoritariamente en la interacción con una versión premium de ChatGPT 5.2 de uso personal.
Es por lo tanto libre para uso académico, educativo y personal, sin atribución necesaria.
Si reutilizás el código o los datos procesados, es necesario referenciar PokeAPI.