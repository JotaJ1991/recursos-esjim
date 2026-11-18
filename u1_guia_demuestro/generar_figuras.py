"""Figuras y cifras de la guía Demuestro U1 (BD1 y BD2). Ejecutar: python3 generar_figuras.py"""
import json, math
import numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import milp, LinearConstraint, Bounds

AZ, AZ2, DO, GR, RO, VE = '#0A3B66', '#1E5A8E', '#C9A227', '#8A96A3', '#C0392B', '#1E7E34'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.titleweight': 'bold', 'axes.titlesize': 10,
                     'axes.edgecolor': '#555', 'figure.dpi': 150})
b1 = pd.read_excel('../BD1_Incidentes_Delictivos_Bogota.xlsx', sheet_name='Incidentes Delictivos')
b2 = pd.read_excel('../BD2_Gestion_Cuadrantes_Colombia.xlsx', sheet_name='Gestión Cuadrantes')
R = {}
def save(name):
    plt.tight_layout(rect=[0, 0.06, 1, 1]); plt.savefig(f'fig/{name}.pdf'); plt.close()
def fuente(ax, txt):
    ax.figure.text(0.01, 0.012, txt, fontsize=7, color='#555')

# ---------- M1/M2: tiempo de respuesta BD1 ----------
tr = b1.Tiempo_Respuesta_Min
R['tr'] = dict(n=len(tr), media=tr.mean(), mediana=tr.median(), moda=float(tr.mode()[0]), de=tr.std(),
               cv=tr.std()/tr.mean()*100, q1=tr.quantile(.25), q3=tr.quantile(.75), min=tr.min(), max=tr.max(),
               asim=tr.skew())
bins = np.arange(2, 22.1, 2.5)
fr, _ = np.histogram(tr, bins=bins)
R['tabla_frec'] = [[f'{a:.1f}--{b:.1f}', (a+b)/2, int(f)] for a, b, f in zip(bins[:-1], bins[1:], fr)]
fig, ax = plt.subplots(figsize=(6.2, 3.0))
ax.hist(tr, bins=bins, color=AZ2, edgecolor='white')
ax.axvline(tr.mean(), color=DO, lw=2, label=f'Media = {tr.mean():.2f} min')
ax.axvline(tr.median(), color=RO, lw=2, ls='--', label=f'Mediana = {tr.median():.2f} min')
ax.set_xlabel('Tiempo de respuesta (minutos)'); ax.set_ylabel('Número de incidentes')
ax.set_title('La mayoría de incidentes se atiende entre 7 y 17 minutos')
ax.legend(frameon=False); fuente(ax, 'Fuente: elaboración propia con BD1 (n = 250), ESJIM.')
save('f1_histograma_tr')

# ---------- M3: Pareto tipo de delito ----------
vc = b1.Tipo_Delito.value_counts(); acum = vc.cumsum()/vc.sum()*100
R['pareto'] = [[k, int(v), round(a, 1)] for k, v, a in zip(vc.index, vc.values, acum.values)]
fig, ax = plt.subplots(figsize=(6.4, 3.3))
ax.bar(range(len(vc)), vc.values, color=[AZ if a <= 80.5 else GR for a in acum.values])
ax.set_xticks(range(len(vc))); ax.set_xticklabels(vc.index, rotation=55, ha='right', fontsize=7)
ax.set_ylabel('Incidentes'); ax2 = ax.twinx(); ax2.plot(range(len(vc)), acum.values, color=DO, marker='o', ms=3)
ax2.axhline(80, color=RO, ls=':', lw=1); ax2.set_ylim(0, 105); ax2.set_ylabel('% acumulado')
ax2.spines['top'].set_visible(False)
ax.set_title('Diagrama de Pareto: tipos de delito registrados')
fuente(ax, 'Fuente: elaboración propia con BD1 (n = 250). Barras azules: delitos que suman hasta el 80 %.')
save('f2_pareto_delitos')

# ---------- M4: probabilidad condicional ----------
ct = pd.crosstab(b1.Arma_Medio, b1.Captura)
pc = (ct[1]/ct.sum(axis=1)).sort_values(ascending=False)
R['pcond'] = {k: [int(ct.loc[k].sum()), int(ct.loc[k, 1]), round(v, 3)] for k, v in pc.items()}
R['pcaptura'] = b1.Captura.mean()
top = [k for k in pc.index if ct.loc[k].sum() >= 15]
fig, ax = plt.subplots(figsize=(6.0, 2.7))
vals = [pc[k]*100 for k in top]
ax.barh(top[::-1], vals[::-1], color=AZ2)
ax.axvline(b1.Captura.mean()*100, color=DO, lw=2, label='Promedio general: 18,8 %')
for i, v in enumerate(vals[::-1]): ax.text(v+0.5, i, f'{v:.1f} %', va='center', fontsize=8)
ax.set_xlabel('P(captura | medio empleado), en %'); ax.legend(frameon=False, loc='lower right')
ax.set_title('La probabilidad de captura cambia según el medio empleado')
fuente(ax, 'Fuente: elaboración propia con BD1. Solo medios con 15 o más registros.')
save('f3_prob_condicional')

# ---------- M5: Poisson hurto a persona ----------
hp = b1[b1.Tipo_Delito == 'Hurto a persona']
idx = pd.MultiIndex.from_product([[2024], range(1, 13)]).append(pd.MultiIndex.from_product([[2025], range(1, 7)]))
m = hp.groupby(['Año', 'Mes']).size().reindex(idx, fill_value=0)
lam = m.mean(); obs = np.bincount(m.values, minlength=9)[:9]
pk = stats.poisson.pmf(range(9), lam); esp = 18*pk
R['poisson'] = dict(lam=lam, var=m.var(), mensual=m.tolist(), pk=[round(p, 4) for p in pk],
                    pcum=[round(p, 4) for p in stats.poisson.cdf(range(9), lam)], obs=obs.tolist(), esp=[round(e, 2) for e in esp],
                    p5mas=1-stats.poisson.cdf(4, lam), p0=pk[0], q95=int(stats.poisson.ppf(0.95, lam)))
fig, ax = plt.subplots(figsize=(6.0, 2.8)); w = 0.38; k = np.arange(9)
ax.bar(k-w/2, obs, w, color=AZ2, label='Meses observados'); ax.bar(k+w/2, esp, w, color=DO, label='Meses esperados (Poisson, λ = 3)')
ax.set_xticks(k); ax.set_xlabel('Hurtos a persona en el mes (k)'); ax.set_ylabel('Número de meses')
ax.set_title('El conteo mensual se ajusta razonablemente a Poisson'); ax.legend(frameon=False)
fuente(ax, 'Fuente: elaboración propia con BD1, hurto a persona, 18 meses (ene-2024 a jun-2025).')
save('f4_poisson')

# ---------- M6: indicadores BD2 por ciudad ----------
g = b2.groupby('Ciudad').agg(registros=('ID_Registro', 'size'), llamadas=('Llamadas_123', 'sum'),
                             no_aten=('Incidentes_No_Atendidos', 'sum'), tr=('Tiempo_Respuesta_Prom_Min', 'mean'),
                             capturas=('Capturas', 'sum'), costo=('Costo_Operativo_COP', 'sum'))
g['pct_no_aten'] = g.no_aten/g.llamadas*100; g['costo_captura'] = g.costo/g.capturas
R['ciudades'] = g.round(2).reset_index().values.tolist()
R['turnos'] = b2.groupby('Turno')[['Llamadas_123', 'Tiempo_Respuesta_Prom_Min']].mean().round(2).reset_index().values.tolist()

# ---------- M7: regresión TR ~ patrullas (BD2) ----------
x, y = b2.Patrullas_Disponibles, b2.Tiempo_Respuesta_Prom_Min
lr = stats.linregress(x, y)
X = np.c_[np.ones(len(b2)), x, b2['Área_km2']]; beta = np.linalg.lstsq(X, y, rcond=None)[0]
yh = X@beta; r2m = 1-((y-yh)**2).sum()/((y-y.mean())**2).sum()
R['reg'] = dict(a=lr.intercept, b=lr.slope, r=lr.rvalue, r2=lr.rvalue**2, p=lr.pvalue,
                medias=b2.groupby('Patrullas_Disponibles').Tiempo_Respuesta_Prom_Min.mean().round(2).to_dict(),
                multi=[*beta], r2m=r2m)
rng = np.random.default_rng(7)
fig, ax = plt.subplots(figsize=(5.6, 3.0))
ax.scatter(x+rng.uniform(-.12, .12, len(x)), y, s=10, alpha=.45, color=AZ2, label='Registros (con leve dispersión horizontal)')
xx = np.array([0.8, 3.2]); ax.plot(xx, lr.intercept+lr.slope*xx, color=RO, lw=2,
                                   label=f'ŷ = {lr.intercept:.2f} − {abs(lr.slope):.2f}·x   (r = {lr.rvalue:.2f})')
ax.set_xticks([1, 2, 3]); ax.set_xlabel('Patrullas disponibles en el turno'); ax.set_ylabel('Tiempo de respuesta (min)')
ax.set_title('Más patrullas, menor tiempo de respuesta'); ax.legend(frameon=False, fontsize=7.5)
fuente(ax, 'Fuente: elaboración propia con BD2 (n = 250 registros de turno).')
save('f5_regresion')

# ---------- M8: optimización (Bogotá, BD2) ----------
bog = b2[b2.Ciudad == 'Bogotá']
e = bog.groupby('Estación').agg(llam=('Llamadas_123', 'mean'), tr=('Tiempo_Respuesta_Prom_Min', 'mean'),
                                pat=('Patrullas_Disponibles', 'mean')).reindex(['Ciudad Bolívar', 'Kennedy', 'Engativá', 'Suba', 'Usaquén'])
# (a) reparto proporcional de 30 policías por demanda (método del mayor residuo)
cuota = e.llam/e.llam.sum()*30; base = np.floor(cuota); resto = int(30-base.sum())
base[(cuota-base).sort_values(ascending=False).index[:resto]] += 1
R['prop'] = [[k, round(e.llam[k], 2), round(cuota[k], 2), int(base[k])] for k in e.index]
# (b) PL entera: 6 patrullas adicionales por turno
b = abs(lr.slope); n = len(e); c = -(e.llam.values*b)          # minimizar sum llam*(tr - b x)  <=> max sum llam*b*x
A = [np.ones(n)]; lo = [6]; hi = [6]
lb = np.ceil(np.maximum(0, (e.tr.values-10)/b)); ub = np.full(n, 2)
res = milp(c, constraints=LinearConstraint(np.array(A), lo, hi), integrality=np.ones(n), bounds=Bounds(lb, ub))
xo = np.round(res.x).astype(int)
# referencia: reparto igual (redondeado a 6) y sin restricción de meta
tr_new = e.tr.values-b*xo
wtr0 = (e.llam*e.tr).sum()/e.llam.sum(); wtr1 = (e.llam.values*tr_new).sum()/e.llam.sum()
R['pl'] = dict(b=b, lb=lb.tolist(), x=xo.tolist(), tr0=e.tr.round(2).tolist(), tr1=np.round(tr_new, 2).tolist(),
               llam=e.llam.round(2).tolist(), est=list(e.index), wtr0=wtr0, wtr1=wtr1)
fig, ax = plt.subplots(figsize=(6.0, 2.9)); k = np.arange(n); w = .38
ax.bar(k-w/2, e.tr, w, color=GR, label='Situación actual'); ax.bar(k+w/2, tr_new, w, color=AZ, label='Con la solución óptima')
ax.axhline(10, color=RO, ls=':', lw=1.2, label='Meta: 10 min')
for i, v in enumerate(xo): ax.text(i+w/2, tr_new[i]+0.2, f'+{v}', ha='center', fontsize=8, color=AZ, fontweight='bold')
ax.set_xticks(k); ax.set_xticklabels(e.index); ax.set_ylabel('Tiempo de respuesta (min)'); ax.set_ylim(0, 13)
ax.set_title('Programación lineal: 6 patrullas adicionales en cinco estaciones', pad=22); ax.legend(frameon=False, fontsize=7.5, ncol=3, loc='lower center', bbox_to_anchor=(0.5, 1.0))
fuente(ax, 'Fuente: elaboración propia con BD2 (Bogotá). Etiqueta: patrullas adicionales asignadas.')
save('f6_programacion_lineal')

# ---------- Parte II: mapa de calor localidad × franja (BD1) ----------
b1['h'] = pd.to_datetime(b1.Hora.astype(str), format='%H:%M:%S').dt.hour
b1['Franja'] = pd.cut(b1.h, [-1, 5, 11, 17, 23], labels=['00–06', '06–12', '12–18', '18–24'])
hm = pd.crosstab(b1.Localidad, b1.Franja); hm = hm.loc[hm.sum(axis=1).sort_values(ascending=False).index]
R['franjas'] = b1.Franja.value_counts().sort_index().to_dict()
R['loc_tr'] = b1.groupby('Localidad').Tiempo_Respuesta_Min.agg(['count', 'mean']).round(2).sort_values('count', ascending=False).reset_index().values.tolist()
fig, ax = plt.subplots(figsize=(5.4, 3.8))
im = ax.imshow(hm.values, cmap='Blues', aspect='auto')
ax.set_xticks(range(4)); ax.set_xticklabels(hm.columns); ax.set_yticks(range(len(hm))); ax.set_yticklabels(hm.index, fontsize=8)
for i in range(hm.shape[0]):
    for j in range(4):
        v = hm.values[i, j]; ax.text(j, i, v, ha='center', va='center', fontsize=8, color='white' if v >= hm.values.max()*0.6 else '#222')
ax.set_xlabel('Franja horaria'); ax.set_title('Incidentes por localidad y franja horaria'); plt.colorbar(im, ax=ax, shrink=.8)
fuente(ax, 'Fuente: elaboración propia con BD1 (n = 250).')
save('f7_mapa_calor')

json.dump(R, open('cifras_guia.json', 'w'), ensure_ascii=False, indent=1, default=float)
print(json.dumps(R, ensure_ascii=False, default=float)[:6000])
