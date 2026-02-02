Pokémon HM Compatibility Checker (Generations 1–3)

Este repositorio presenta un script en Python que consulta PokéAPI v2 para identificar qué Pokémon pueden aprender todos los movimientos clave (HM) relevantes en distintos juegos de las generaciones 1, 2 y 3, restringiendo estrictamente el análisis al moveset propio de cada versión del juego.

El objetivo es ofrecer un chequeo sistemático, explícito y reproducible de compatibilidad mínima, evitando la mezcla entre generaciones, versiones o métodos de aprendizaje.

Descripción general del procedimiento

Para cada juego clásico —Red/Blue, Yellow, Gold/Silver, Crystal, Ruby/Sapphire, Emerald y FireRed/LeafGreen— el script implementa el siguiente procedimiento:

1. Definición del pool de Pokémon

Se construye un conjunto de Pokémon candidatos en función de la generación del juego analizado:

Generación 1 → Pokémon de Gen 1

Generación 2 → Pokémon de Gen 1 + 2

Generación 3 → Pokémon de Gen 1 + 2 + 3

Este criterio evita introducir especies no disponibles en el horizonte histórico de cada versión.

2. Definición del conjunto de HM por juego

Para cada juego se define un conjunto específico de movimientos clave, respetando las diferencias históricas entre generaciones y versiones:

Gen 1: cut, surf, strength

Gen 2: cut, surf, strength, waterfall, whirlpool

Gen 3 (Ruby/Sapphire/Emerald): surf, strength, rock-smash, waterfall, dive

Gen 3 (FireRed/LeafGreen): cut, surf, strength, rock-smash, waterfall

Estos conjuntos funcionan como requisitos mínimos de movilidad y progresión.

3. Consulta y verificación mediante PokéAPI

Para cada Pokémon del pool, el script consulta PokéAPI v2 y verifica, para cada movimiento requerido:

si el movimiento puede aprenderse en esa versión específica del juego,

utilizando exclusivamente el método de aprendizaje machine (TM/HM en PokéAPI),

filtrando explícitamente por version_group (identificador del juego).

Este filtrado impide que aprendizajes válidos en otras generaciones o versiones contaminen el análisis.

4. Criterio de inclusión (condición fuerte)

Un Pokémon es considerado válido únicamente si puede aprender todos los movimientos requeridos para ese juego.

Si alguno de los movimientos definidos no existe como movimiento aprendible por máquina en esa versión, se descarta automáticamente del conjunto de requisitos para evitar falsos negativos derivados de inconsistencias históricas o de modelado en la API.

5. Salida de resultados

El script genera un archivo CSV por juego, que contiene exclusivamente la lista de Pokémon que cumplen la condición fuerte de compatibilidad.

Ejemplos de archivos generados:

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

Decisiones metodológicas explícitas (qué NO hace el script)

El script no:

distingue entre HM y TM dentro del método machine (PokéAPI no los separa),

modela restricciones narrativas del juego (medallas, progresión, eventos),

considera el momento específico en que se obtiene cada movimiento,

mezcla datos entre juegos, generaciones o versiones.

Estas exclusiones son decisiones conscientes, orientadas a mantener un modelo claro, verificable y alineado con la estructura real de los datos disponibles.

Consideración técnica clave: species vs. Pokémon

PokéAPI distingue entre:

pokemon-species (por ejemplo, deoxys), y

pokemon (por ejemplo, deoxys-normal).

Para garantizar compatibilidad total y evitar errores (HTTP 404), el script:

resuelve cada especie a su variedad por defecto, y

utiliza ese identificador para consultar el moveset correspondiente.

Este paso es indispensable para asegurar la cobertura completa del pool de especies.

Requisitos técnicos

Python 3.9 o superior

Dependencias:

pip install requests


No se utilizan librerías externas para la exportación de archivos CSV.

Reproducibilidad

El procedimiento es completamente determinista dado:

el estado público de PokéAPI v2,

la definición explícita de pools, juegos y movimientos,

y la ausencia de muestreo o heurísticas no documentadas.

Los resultados pueden replicarse ejecutando el script en cualquier entorno compatible.

Fuente de datos

Todos los datos utilizados provienen de PokéAPI v2:
https://pokeapi.co/

Uso esperado

Este script está diseñado para:

análisis comparativos entre juegos y generaciones,

estudios históricos sobre diseño y restricciones de progresión,

investigación sobre condiciones mínimas de jugabilidad,

generación de datasets reproducibles para análisis académicos.

Licencia y atribución

El código y este texto fueron desarrollados en el marco de un uso personal y académico de una versión premium de ChatGPT (modelo 5.2), con edición y validación humana.

El proyecto es de uso libre con fines académicos, educativos y personales.
En caso de reutilización del código o de los datos procesados, debe citarse PokéAPI como fuente primaria.
