SHAGGY26K -> MODO 100K ENEMIGO / 4K BF
======================================

Este parche agrega un modo nuevo sin eliminar los modos originales.

MODO NUEVO
----------
mania = 9
- Enemigo: 100 keys/receptores.
- Boyfriend: 4 keys/receptores normales.
- Las 100 flechas del enemigo caben en la mitad izquierda del HUD.
- Para las apariencias del enemigo se reutilizan/ciclan los 26 gráficos del modo 26K.
- BF usa las cuatro direcciones normales LEFT/DOWN/UP/RIGHT.

ARCHIVOS A REEMPLAZAR
---------------------
Copia los archivos de la carpeta source/ de este parche sobre la carpeta source/ del proyecto SHAGGY26K:
- Main.hx
- Note.hx
- StrumNote.hx
- PlayState.hx
- PauseSubState.hx

CÓMO FUNCIONA EL CHART EN mania=9
---------------------------------
Cada sección dispone de 104 índices posibles en total.

Si mustHitSection = false (turno del enemigo):
- 0..99   = enemigo, lanes 0..99
- 100..103 = BF, lanes 0..3

Si mustHitSection = true (turno de BF):
- 0..3    = BF, lanes 0..3
- 4..103  = enemigo, lanes 0..99

CONVERTIR UN CHART 26K EXISTENTE
--------------------------------
El parche incluye:
tools/convert_26k_to_100x4.py

Ejemplo:
python tools/convert_26k_to_100x4.py song-hard.json song-100k4k.json

El conversor:
- cambia mania de 5 a 9;
- conserva tiempos, sustains y tipos de nota;
- reduce las notas de BF a 4 lanes;
- distribuye las antiguas 26 lanes del enemigo entre las 100 lanes nuevas.

IMPORTANTE
----------
El Chart Editor original de este engine no fue diseñado para una cuadrícula asimétrica 100K/4K.
Para editar cómodamente, crea primero el chart como 26K (mania=5) y luego ejecuta el conversor.
No vuelvas a guardar el chart mania=9 con el Chart Editor original porque puede reinterpretar los carriles.

RENDIMIENTO
-----------
100 receptores simultáneos son mucho más pesados que 26. El parche evita las animaciones de entrada de los 100 receptores del enemigo para reducir carga. Si se usa una gran cantidad de notas/sustains al mismo tiempo, puede ser necesario optimizar más el engine.
