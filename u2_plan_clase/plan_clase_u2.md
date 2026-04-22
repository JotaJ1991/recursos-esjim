# Plan de clase — Unidad 2
## "Operaciones Básicas para la Gestión Efectiva en la Administración Policial"

| Dato | Detalle |
|---|---|
| **Docente** | IT. José Javier Mercado Reyes |
| **Asignatura** | Matemática aplicada a la profesión (338-ADMI-MATE-2) |
| **Secciones** | 008227 · 008228 · 008229 · 008230 |
| **Nivel** | Suboficiales y Nivel Ejecutivo — ESJIM |
| **Duración** | 4 horas (1 sesión) |
| **Modalidad** | Clase magistral activa + taller en equipos + plenaria |
| **Prerrequisitos** | U1 completada (estadística descriptiva + BD Bogotá) |

---

## 1. Resultado de aprendizaje y conexión institucional

> **RA-U2**: Realiza cálculos y operaciones matemáticas fundamentales (porcentajes, proporciones, manejo de datos cuantitativos) en el contexto policial para tomar decisiones informadas que fortalezcan la eficiencia operativa.

**Aporte al perfil profesional (IT/ST)**: cualquier comandante de CAI, de cuadrante o de grupo especializado toma decisiones cada turno sobre dónde poner el recurso y cómo medir impacto. Esta unidad entrega el **lenguaje técnico** para defender esas decisiones ante mandos y ante la ciudadanía.

---

## 2. Objetivos específicos de la sesión

Al finalizar, el estudiante estará en capacidad de:

1. **Modelar** una red criminal como un grafo y calcular métricas simples (grado, centralidad).
2. **Plantear** un problema de programación lineal (PL) con función objetivo y restricciones en contexto policial.
3. **Interpretar** la distribución de Poisson para predecir ocurrencia de delitos en un CAI.
4. **Evaluar** el impacto de una estrategia de intervención usando indicadores antes/después.
5. **Aplicar** análisis costo-beneficio (B/C, VPN) a una inversión policial (cámaras, motos, inteligencia).
6. **Justificar** una decisión operativa con base en los cinco puntos anteriores.

---

## 3. Estructura pedagógica (4 h = 240 min)

| Momento | Tiempo | Actividad |
|---|---|---|
| **Apertura** | 15 min | Saludo, encuadre, presentación del reto del día |
| **Bloque 1** | 35 min | Análisis de Redes Criminales |
| **Bloque 2** | 40 min | Programación Lineal aplicada |
| *Receso* | *15 min* | — |
| **Bloque 3** | 30 min | Modelos Matemáticos en Criminología |
| **Bloque 4** | 25 min | Evaluación de Estrategias de Intervención |
| **Bloque 5** | 35 min | Análisis Costo-Beneficio |
| **Bloque 6** | 30 min | Estudio de caso integrador |
| **Cierre** | 15 min | Síntesis + puente con la tarea Demuestro |

---

## APERTURA (15 min)

### Pregunta detonadora

> *"Como comandante de CAI usted tiene 8 patrulleros y 3 motos para cubrir un cuadrante de 1,5 km² con 12 000 habitantes y un promedio de 9 delitos reportados por día. Su jefe le pide que presente mañana un plan para reducir el delito un 20 % en tres meses, sin recursos adicionales. ¿Por dónde empieza?"*

Recoger ideas en el tablero (5 min). Agruparlas en:
- Intuición experiencial
- Distribución de recurso
- Medición del impacto
- Costo de la solución

**Transición**: "Estas cuatro columnas son justamente las herramientas de hoy."

### Presentación de temáticas

Mostrar el mapa de la unidad con las 6 temáticas y marcar **qué decisión operativa resuelve cada una**.

---

## BLOQUE 1 — Análisis de Redes Criminales (35 min)

### Concepto clave

Una **red criminal** es un conjunto de individuos (nodos) conectados por vínculos (aristas) que representan actividades, parentesco, comunicaciones o cadenas de mando. Tratarla como grafo permite preguntas como:

- ¿Quién es el "cabecilla" aunque no aparezca como tal?
- ¿Qué captura desarticula más rápido la organización?
- ¿Quién es el "puente" entre dos células?

### Métricas esenciales

| Métrica | Qué mide | Fórmula rápida |
|---|---|---|
| **Grado (degree)** | Nº de vínculos directos de un nodo | `deg(v) = nº aristas que tocan v` |
| **Centralidad de intermediación (betweenness)** | Cuánto pasa por él el flujo de la red | `∑ σst(v) / σst` — camino corto que lo cruza |
| **Densidad** | Qué tan "conectada" es la red | `D = 2E / [N(N−1)]` con N nodos, E aristas |

### Ejemplo aplicado — Célula de microtráfico en localidad Kennedy (Bogotá)

Supongamos una red de 7 individuos capturados. Inteligencia documenta estos vínculos (llamadas interceptadas, avistamientos):

```
           A
          /|\
         / | \
        B  C  D
        |  |  |
        E--F  G
            |
            H
```

**Matriz de adyacencia** (simplificada):

| | A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|---|
| A | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| B | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| C | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| D | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| E | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| F | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| G | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| H | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

**Cálculos en clase**:
- Grado de A = 3 (vínculos con B, C, D) — sospechoso de ser el cabecilla
- Grado de F = 3 (C, E, H) — posible "puente" operativo
- Densidad: `D = 2(8) / [8×7] = 16/56 = 0,286` → red poco densa

**Ejercicio en equipos (5 min)**: "Si capturan solo a un individuo, ¿a quién conviene capturar primero para fragmentar más la red? Justifique con cálculos."

**Respuesta esperada**: capturar a **A** (cabecilla) desconecta la red en 3 componentes; capturar a **F** desconecta H y deja E-B aislados del flujo con C. Se prefiere capturar a **A o F** según el objetivo (descabezar vs cortar canal).

### Dato real de contexto

- Caso Clan del Golfo: más de 2 000 capturas desde 2018, pero la estructura se mantuvo por reemplazo; ejemplo de red **resiliente** por alta conectividad (Fiscalía General 2023).
- Policía Metropolitana de Bogotá publica mensualmente "mapas de estructuras" que usan exactamente estas métricas.

---

## BLOQUE 2 — Programación Lineal aplicada (40 min)

### Concepto clave

La **programación lineal (PL)** resuelve problemas del tipo:

> **Maximizar** (o **minimizar**) una cantidad, sujeto a restricciones.

Tres ingredientes:
- **Variables de decisión** (¿qué decido?)
- **Función objetivo** (¿qué quiero optimizar?)
- **Restricciones** (¿qué limita mi decisión?)

### Ejemplo aplicado — Asignación de patrullas en comando Suroccidente (Cali)

**Situación**: El comando tiene 20 patrullas disponibles. Debe cubrir 3 zonas prioritarias:

| Zona | Prioridad | Costo operativo/patrulla-día | Demanda mínima (patrullas) |
|---|---|---|---|
| Z1 Aguablanca | Alta | $180 000 | ≥ 6 |
| Z2 Ladera | Media | $150 000 | ≥ 4 |
| Z3 Centro | Media | $130 000 | ≥ 3 |

Presupuesto diario: **$3 200 000**.
Objetivo: maximizar **cobertura ponderada por prioridad** (Z1=3, Z2=2, Z3=1).

**Formulación PL**:

- Variables: `x₁, x₂, x₃` = patrullas asignadas a Z1, Z2, Z3
- **Función objetivo**: `Max Z = 3x₁ + 2x₂ + x₃`
- **Restricciones**:
  - Total de patrullas: `x₁ + x₂ + x₃ ≤ 20`
  - Presupuesto: `180 000 x₁ + 150 000 x₂ + 130 000 x₃ ≤ 3 200 000`
  - Demanda mínima: `x₁ ≥ 6`, `x₂ ≥ 4`, `x₃ ≥ 3`
  - No-negatividad: `xᵢ ≥ 0`

**Resolución gráfica/Excel Solver**: solución óptima `x₁=12, x₂=4, x₃=4` → **Z = 48**. Presupuesto usado: `$2 680 000` (queda margen). Total patrullas: 20.

**Interpretación operativa**: asignar 12 patrullas a Aguablanca, 4 a Ladera, 4 al Centro maximiza la cobertura ponderada cumpliendo todos los mínimos y el presupuesto.

### Demo práctica (10 min)

Abrir **Excel** en pantalla proyectada y resolver con Solver:

1. `Datos → Solver` (si no está, instalarlo desde complementos)
2. Celda objetivo: Z (maximizar)
3. Cambiar celdas: x₁, x₂, x₃
4. Restricciones: presupuesto, total, mínimos
5. Método: Simplex LP
6. Resolver

**Ejercicio en equipos (10 min)**: formular (NO resolver) la PL para este caso:

> *"Distrito Norte tiene 15 motos y 8 patrullas. Las motos cubren mejor el centro histórico por maniobrabilidad (peso 3), las patrullas mejor los corredores (peso 2). Tiene 120 horas-turno máximo por día entre todos. Plantee la PL para maximizar cobertura ponderada si la moto aporta 8 h/turno y la patrulla 12 h/turno."*

---

## RECESO (15 min)

---

## BLOQUE 3 — Modelos Matemáticos en Criminología (30 min)

### Concepto clave

La criminología aplicada usa **modelos probabilísticos** para anticipar la ocurrencia de eventos. Hoy veremos dos:

### a) Distribución de Poisson

> *¿Cuál es la probabilidad de que en la próxima hora entren k llamadas al 123 en un CAI, si el promedio histórico es λ llamadas/hora?*

Fórmula: `P(X = k) = (λᵏ · e⁻ᵏ) / k!`

### Ejemplo aplicado — CAI Kennedy-Castilla

Histórico (BD1 Bogotá): **λ = 3,2 llamadas críticas/hora** en franja 16:00-19:00.

| k | P(X=k) | Interpretación |
|---|---|---|
| 0 | 0.041 | 4 % de las horas NO entran llamadas críticas |
| 1 | 0.130 | 13 % |
| 2 | 0.209 | 21 % |
| 3 | 0.223 | 22 % (la más frecuente) |
| 4 | 0.178 | 18 % |
| 5 | 0.114 | 11 % |
| ≥6 | 0.105 | 10 % (saturación del CAI) |

**Decisión operativa**: hay **10 % de las horas pico** en que entran **6 o más llamadas** — si el CAI solo puede atender 4 simultáneas, ese 10 % del tiempo hay saturación → justifica una patrulla extra o un PSE (Punto de Salida Estratégico) en la franja.

### b) Regresión lineal simple (recordatorio de U1)

Predecir el tiempo de respuesta en función del número de patrullas. Fórmula clásica:

`T = a + b·P` (con T tiempo-respuesta, P nº patrullas)

Si `a = 18`, `b = -0,9` y asignamos 12 patrullas: `T = 18 - 0,9(12) = 7,2 minutos` estimados.

**Limitación**: el modelo extrapola mal fuera del rango histórico. Un comandante prudente usa regresión **solo dentro del rango observado**.

### Actividad flash (5 min)

"Con λ = 4,5 robos/día en un cuadrante, calcule la probabilidad de que mañana no ocurra ningún robo." → `P(X=0) = e⁻⁴·⁵ ≈ 0,011` (1,1 %).

---

## BLOQUE 4 — Evaluación de Estrategias de Intervención (25 min)

### Concepto clave

Una estrategia se evalúa comparando **indicadores antes / durante / después**. No basta con "bajó el delito" — hay que descontar tendencia, estacionalidad y causalidad.

### Indicadores base

| Indicador | Fórmula | Ejemplo |
|---|---|---|
| **Tasa delictiva** | delitos × 100 000 / habitantes | 320 /100 000 |
| **Tasa de captura** | capturas / delitos reportados | 18,8 % (BD1 Bogotá) |
| **Variación porcentual** | (final − inicial) / inicial × 100 | −22 % |
| **Tiempo de respuesta medio** | ∑ tᵢ / N | 12,49 min (BD1) |

### Ejemplo aplicado — Plan "Navidad Segura" en Chapinero

**Antes (nov 2025)**:
- Hurto a persona: 193 casos/mes
- Tiempo respuesta: 13,2 min
- Tasa captura: 16 %

**Durante (dic 2025 con plan)**:
- Hurto a persona: 83 casos/mes
- Tiempo respuesta: 9,8 min
- Tasa captura: 22 %

**Cálculos**:
- Reducción hurto: `(83−193)/193 = −57 %`
- Mejora tiempo: `(9,8−13,2)/13,2 = −26 %`
- Mejora captura: `(22−16)/16 = +37,5 %`

**Alerta metodológica** (muy importante para los IT):
- Diciembre suele tener más hurtos por comercio/turismo → el baseline de noviembre infla la reducción aparente.
- Solución: comparar con **diciembre del año anterior** (2024) o ajustar por estacionalidad.

### Ejercicio guiado (5 min)

Calcular las tres variaciones con datos 2024 vs 2025 que trae el docente en Excel. Discutir cuál es la interpretación correcta.

---

## BLOQUE 5 — Análisis Costo-Beneficio (35 min)

### Concepto clave

Una inversión policial (cámaras, motos, inteligencia) se justifica si los **beneficios netos** superan el **costo total**, idealmente en un horizonte definido.

### Indicadores clave

| Indicador | Fórmula | Criterio |
|---|---|---|
| **Relación Beneficio/Costo (B/C)** | ∑ Beneficios / ∑ Costos | B/C > 1 → viable |
| **Valor Presente Neto (VPN)** | ∑ [(Bₜ−Cₜ) / (1+i)ᵗ] | VPN > 0 → viable |
| **Tasa Interna de Retorno (TIR)** | i que hace VPN=0 | TIR > tasa referencia → viable |

### Ejemplo aplicado — ¿Invertir en 20 cámaras LPR o en 5 motos?

**Opción A — 20 cámaras LPR (lectoras de placa)**:
- Inversión inicial: $350 000 000
- Costo operativo anual: $40 000 000
- Beneficios estimados (reducción hurto vehículos recuperados + ahorro judicial): $180 000 000/año
- Horizonte: 5 años, tasa descuento: 10 %

**Opción B — 5 motos + 5 patrulleros adicionales**:
- Inversión inicial: $180 000 000
- Costo operativo anual: $240 000 000 (salarios + combustible)
- Beneficios estimados: $290 000 000/año
- Horizonte: 5 años, tasa descuento: 10 %

**Cálculos (VPN a 5 años)**:

Opción A:
```
VPN_A = −350 + ∑ₜ₌₁⁵ (180−40)/(1,1)ᵗ
      = −350 + 140 · [1/1,1 + 1/1,21 + 1/1,331 + 1/1,4641 + 1/1,6105]
      = −350 + 140 · 3,7908
      = −350 + 530,7
      = +180,7 millones  ✓
```

Opción B:
```
VPN_B = −180 + ∑ₜ₌₁⁵ (290−240)/(1,1)ᵗ
      = −180 + 50 · 3,7908
      = −180 + 189,5
      = +9,5 millones  (apenas viable)
```

**B/C**:
- A: Beneficios VPN / Costos VPN = 682,4 / 501,7 = **1,36**
- B: 1 099,3 / 1 089,8 = **1,01**

**Decisión**: **Opción A** domina en rentabilidad. Pero hay que considerar:
- **Tangibles no contemplados**: percepción ciudadana, disuasión
- **Riesgo operativo**: cámaras no capturan en flagrancia; motos sí
- **Sostenibilidad**: cámaras requieren mantenimiento técnico

### Mensaje clave

> "El número no decide solo. Un VPN positivo es **condición necesaria pero no suficiente**. El comandante aporta juicio operativo sobre lo que el modelo no ve."

### Ejercicio en equipos (10 min)

Caso simplificado: "Comando X evalúa comprar un dron ($60M inversión, $8M/año costos, $25M/año beneficios, 4 años, i=12%). ¿Es viable? Calcule VPN y B/C."

Respuesta: VPN = −60 + 17·3,037 = **+1,63 M** (marginalmente viable); B/C ≈ 1,03.

---

## BLOQUE 6 — Estudio de caso integrador (30 min)

### Caso "Patrulla Inteligente Rafael Uribe Uribe"

**Contexto** (basado en BD1 Bogotá 2024-2025):

La localidad Rafael Uribe Uribe pasó de **26 a 1 caso/mes** de hurto a persona (−96 %) entre 2024 y 2025. Los IT van a reconstruir el plan.

**Paso 1 — Red de la banda desarticulada (Análisis de redes)**
- Inteligencia mapeó 11 individuos, densidad 0,32, cabecilla con grado 5 → captura del cabecilla fragmentó la red en 3 componentes inviables.

**Paso 2 — Redistribución de patrullas (PL)**
- Se reasignaron 8 patrullas desde localidad con baja actividad → función objetivo: maximizar capturas ponderadas por riesgo; restricciones: mínimo 4 patrullas por cuadrante crítico.

**Paso 3 — Modelo predictivo (Poisson)**
- λ bajó de 4,8 a 0,5 incidentes/día → probabilidad de día sin incidentes subió de 0,8 % a 60,7 %.

**Paso 4 — Evaluación del impacto**
- Reducción delitos: −96 %
- Aumento tasa captura: +18 puntos
- Ajuste por estacionalidad: mantiene significancia estadística

**Paso 5 — Costo-beneficio**
- Costo adicional: $420 M (reasignación + horas extra)
- Beneficios: reducción victimización + mejora imagen = estimado $680 M
- **B/C = 1,62** → plan ratificado para replicar

**Paso 6 — Decisión**: el comandante propone replicar el modelo en Bosa, Ciudad Bolívar y Usme, ajustando por tamaño poblacional.

### Discusión plenaria (10 min)

Preguntas guía:
1. ¿Qué técnica consideran más determinante en este éxito? ¿Por qué?
2. ¿Qué debilidades ven en el caso? (ej: ¿el efecto desplazamiento? ¿qué pasa con la localidad de donde se retiraron patrullas?)
3. ¿Cómo podrían medir el efecto desplazamiento matemáticamente?

---

## CIERRE (15 min)

### Síntesis: las 6 herramientas como un solo sistema

```
         ┌──────────────────┐
         │ DECISIÓN OPERATIVA│
         └──────────▲───────┘
                    │
   ┌────────────────┼────────────────┐
   │                │                │
   │  ANTES         │        DESPUÉS │
   │                │                │
  REDES           PL              COSTO
 (quién atacar) (cómo distribuir) BENEFICIO
   │                │                │
   └────POISSON───┴───EVALUACIÓN ────┘
      (cuánto        (funcionó?)
       esperar)
```

### Preparación de la tarea "Demuestro mi aprendizaje" U2

La tarea pide:
1. **Árbol de problemas** sobre gestión de recursos en operaciones policiales
2. **Programación lineal** — función objetivo + restricciones
3. **Análisis costo-beneficio** de la solución

Los tres puntos los vimos hoy. Recomendación:
- Elijan un problema **real de su jurisdicción** (hurto a persona, homicidio, microtráfico)
- Usen **BD1/BD2 del material de apoyo** para soportar los números
- Formulen la PL con **Excel Solver** y peguen el resultado
- Calculen **B/C o VPN** con supuestos transparentes
- Informe de **8-10 páginas** con 3-4 gráficos

### Indicaciones finales

- Lectura obligatoria previa a la próxima sesión: Villarreal-Satama et al. (2021), Pontón (2020)
- Herramienta sugerida: **Excel Solver** para PL. Alternativa libre: GeoGebra 3D para PL 2D
- Fecha de entrega: **jueves 14 de mayo 2026, 23:59**

### Invitación al cierre

> "La matemática aplicada no reemplaza su experiencia; la estructura. Les da el vocabulario para que sus decisiones no dependan de la intuición solitaria sino de un argumento que cualquier mando pueda auditar."

---

## 4. Recursos necesarios

| Recurso | Uso |
|---|---|
| Proyector / tablero digital | Explicar matrices, fórmulas, casos |
| Excel con Solver habilitado | Demo PL y ejercicios en equipos |
| BDs del material de apoyo | Datos reales para ejemplos (BD1 Bogotá, BD2 Cuadrantes) |
| Plantilla "Árbol de problemas" (tablero) | Ejercicio de Bloque 6 |
| Calculadora con función exponencial | Cálculos Poisson |

## 5. Evaluación formativa durante la sesión

| Momento | Actividad | Evidencia |
|---|---|---|
| Bloque 1 | Ejercicio captura para fragmentar red | Cálculo escrito en papel |
| Bloque 2 | Formulación PL por equipos | Planteo en hoja (revisar en plenaria) |
| Bloque 3 | Cálculo Poisson individual | Tarjeta rápida |
| Bloque 4 | Discusión caso Navidad Segura | Participación oral |
| Bloque 5 | VPN del dron en equipos | Número correcto + interpretación |
| Bloque 6 | Debate plenario | Calidad de argumento |

**Observación clave**: esta evaluación es formativa (no sumativa). La nota U2 Aprendo Haciendo se da por participación (política ESJIM: 5,00 automático).

## 6. Puente con U3 y evaluación final

Esta unidad es la base de la **Evaluación final del curso**. Los estudiantes ya tienen:
- **U1**: herramientas descriptivas (media, mediana, %, probabilidad clásica)
- **U2**: herramientas prescriptivas (optimización, predicción, evaluación económica)

La evaluación final integra ambas en un caso complejo. Avisar a los estudiantes que la Demuestro U2 es el ensayo general.
