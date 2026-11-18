"""Modelos adicionales (M9-M18) de la guía Demuestro U1. Ejecutar: python3 generar_figuras_2.py"""
import json, math
import numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

AZ, AZ2, DO, GR, RO, VE = '#0A3B66', '#1E5A8E', '#C9A227', '#8A96A3', '#C0392B', '#1E7E34'
PAL = [AZ, DO, RO, VE, '#7D3C98', '#E67E22', GR]
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.titleweight': 'bold', 'axes.titlesize': 10, 'figure.dpi': 150})
def save(name):
    plt.tight_layout(rect=[0, 0.06, 1, 1]); plt.savefig(f'fig/{name}.pdf'); plt.close()
def fuente(ax, txt): ax.figure.text(0.01, 0.012, txt, fontsize=7, color='#555')

b1 = pd.read_excel('../BD1_Incidentes_Delictivos_Bogota.xlsx', sheet_name='Incidentes Delictivos')
b2 = pd.read_excel('../BD2_Gestion_Cuadrantes_Colombia.xlsx', sheet_name='Gestión Cuadrantes')
b3 = pd.read_excel('../BD3_Perfil_Criminal_Reincidencia.xlsx', sheet_name='Perfil y Reincidencia')
R = {}

# M9 Binomial
p = b1.Captura.mean(); n = 10
pmf = stats.binom.pmf(range(n+1), n, p)
R['binom'] = dict(p=p, n=n, pmf=[round(x, 4) for x in pmf], p0=pmf[0], p_ge3=1-stats.binom.cdf(2, n, p), esp=n*p, p_ge1=1-pmf[0])
fig, ax = plt.subplots(figsize=(5.6, 2.6))
ax.bar(range(n+1), pmf, color=[AZ if k < 3 else DO for k in range(n+1)])
for k, v in enumerate(pmf[:6]): ax.text(k, v+0.005, f'{v:.3f}', ha='center', fontsize=7)
ax.set_xticks(range(n+1)); ax.set_xlabel('Capturas en 10 incidentes (k)'); ax.set_ylabel('P(X = k)')
ax.set_title('Binomial (n = 10, p = 0,188): lo usual es 1 o 2 capturas')
fuente(ax, 'Fuente: elaboración propia con la tasa de captura de BD1. Dorado: 3 o más capturas.')
save('f8_binomial')

# M10 Intervalos de confianza
tr = b1.Tiempo_Respuesta_Min; nn = len(tr)
se_p = math.sqrt(p*(1-p)/nn); tcrit = stats.t.ppf(.975, nn-1); se_m = tr.std()/math.sqrt(nn)
R['ic'] = dict(p=p, se_p=se_p, lo_p=p-1.96*se_p, hi_p=p+1.96*se_p, media=tr.mean(), se_m=se_m, t=tcrit,
               lo_m=tr.mean()-tcrit*se_m, hi_m=tr.mean()+tcrit*se_m)

# M11 Chi-cuadrado de independencia (BD3)
ct = pd.crosstab(b3['Programa_Resocialización'], b3['Reincidió'])
chi2, pv, dof, exp = stats.chi2_contingency(ct, correction=False)
R['chi2'] = dict(tabla=ct.values.tolist(), esperadas=np.round(exp, 2).tolist(), chi2=chi2, p=pv, gl=dof,
                 tasa_sin=ct.loc[0, 1]/ct.loc[0].sum(), tasa_con=ct.loc[1, 1]/ct.loc[1].sum())

# M12 ANOVA TR por ciudad (BD2)
grupos = {c: g.Tiempo_Respuesta_Prom_Min.values for c, g in b2.groupby('Ciudad')}
F, pa = stats.f_oneway(*grupos.values())
R['anova'] = dict(F=F, p=pa, medias={c: round(v.mean(), 2) for c, v in grupos.items()}, n={c: len(v) for c, v in grupos.items()},
                  de={c: round(v.std(ddof=1), 2) for c, v in grupos.items()})
tt = stats.ttest_ind(grupos['Bogotá'], np.concatenate([grupos[c] for c in grupos if c != 'Bogotá']), equal_var=False)
R['ttest'] = dict(t=tt.statistic, p=tt.pvalue)
fig, ax = plt.subplots(figsize=(5.6, 2.8)); orden = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla']
bp = ax.boxplot([grupos[c] for c in orden], patch_artist=True, widths=.5, medianprops=dict(color=DO, lw=2))
for b in bp['boxes']: b.set_facecolor('#D6E4F0'); b.set_edgecolor(AZ)
ax.plot(range(1, 5), [grupos[c].mean() for c in orden], 'D', color=RO, ms=5, label='Media')
ax.set_xticks(range(1, 5)); ax.set_xticklabels(orden); ax.set_ylabel('Tiempo de respuesta (min)')
ax.set_title(f'Bogotá responde más lento (ANOVA: F = {F:.2f}, p = {pa:.3f})'); ax.legend(frameon=False)
fuente(ax, 'Fuente: elaboración propia con BD2 (n = 250).')
save('f9_anova')

# M13 Regresión logística (BD3)
X = pd.DataFrame({'Antecedentes_Previos': b3.Antecedentes_Previos, 'Pertenece_Banda': b3.Pertenece_Banda,
                  'Programa_Resocializacion': b3['Programa_Resocialización'], 'Consumo_Sustancias': (b3.Consumo_Sustancias == 'Sí').astype(int),
                  'Empleo_Pre_Captura': b3.Empleo_Pre_Captura})
mod = sm.Logit(b3.Reincidió, sm.add_constant(X)).fit(disp=0)
orr = np.exp(mod.params); ci = np.exp(mod.conf_int())
pred = (mod.predict(sm.add_constant(X)) >= 0.5).astype(int); acc = (pred == b3.Reincidió).mean()
R['logit'] = dict(coef=mod.params.round(4).to_dict(), OR=orr.round(3).to_dict(), p=mod.pvalues.round(4).to_dict(),
                  ci_lo=ci[0].round(3).to_dict(), ci_hi=ci[1].round(3).to_dict(), acc=acc, pseudoR2=mod.prsquared,
                  base=b3.Reincidió.mean())
# perfil ejemplo
perfil = dict(const=1, Antecedentes_Previos=3, Pertenece_Banda=1, Programa_Resocializacion=0, Consumo_Sustancias=1, Empleo_Pre_Captura=0)
z = sum(mod.params[k]*v for k, v in perfil.items()); R['logit']['p_perfil'] = 1/(1+math.exp(-z))
perfil2 = dict(perfil, Programa_Resocializacion=1); z2 = sum(mod.params[k]*v for k, v in perfil2.items()); R['logit']['p_perfil2'] = 1/(1+math.exp(-z2))
lab = {'Antecedentes_Previos': 'Cada antecedente previo', 'Pertenece_Banda': 'Pertenece a banda', 'Programa_Resocializacion': 'Participó en resocialización',
       'Consumo_Sustancias': 'Consume sustancias', 'Empleo_Pre_Captura': 'Tenía empleo'}
ks = list(lab); fig, ax = plt.subplots(figsize=(5.8, 2.6))
y = np.arange(len(ks))[::-1]
ax.errorbar(orr[ks], y, xerr=[orr[ks]-ci[0][ks], ci[1][ks]-orr[ks]], fmt='o', color=AZ, ecolor=AZ2, capsize=3)
ax.axvline(1, color=RO, ls=':'); ax.set_yticks(y); ax.set_yticklabels([lab[k] for k in ks]); ax.set_xscale('log'); ax.set_xticks([0.3, 0.5, 1, 2, 3]); ax.set_xticklabels(['0,3', '0,5', '1', '2', '3']); ax.minorticks_off()
ax.set_xlabel('Razón de probabilidades (OR), escala log, IC 95 %'); ax.set_title('Factores asociados con la reincidencia')
fuente(ax, 'Fuente: elaboración propia con BD3 (n = 250). OR > 1 aumenta y OR < 1 reduce la probabilidad.')
save('f10_logistica')

# M14 Series de tiempo (BD1 mensual)
idx = pd.period_range('2024-01', '2025-06', freq='M')
s = b1.assign(per=pd.to_datetime(b1.Fecha).dt.to_period('M')).groupby('per').size().reindex(idx, fill_value=0)
t = np.arange(1, len(s)+1); lr = stats.linregress(t, s.values); mm3 = s.rolling(3).mean()
R['serie'] = dict(valores=s.tolist(), meses=[str(x) for x in idx], a=lr.intercept, b=lr.slope, r=lr.rvalue, p=lr.pvalue,
                  mm3=[None if np.isnan(v) else round(v, 2) for v in mm3], pron_mm=mm3.iloc[-1],
                  pron_tend=[lr.intercept+lr.slope*k for k in (19, 20, 21)], media=s.mean())
fig, ax = plt.subplots(figsize=(6.2, 2.8))
ax.plot(t, s.values, marker='o', color=AZ2, label='Incidentes por mes'); ax.plot(t, mm3.values, color=DO, lw=2, label='Promedio móvil (3 meses)')
tt2 = np.arange(1, 22); ax.plot(tt2, lr.intercept+lr.slope*tt2, color=RO, ls='--', label=f'Tendencia: ŷ = {lr.intercept:.2f} {lr.slope:+.2f}·t')
ax.axvspan(18.5, 21.5, color='#EEE'); ax.set_ylim(0, 25); ax.text(20, 23.5, 'pronóstico', ha='center', fontsize=7, color='#555')
ax.set_xticks([1, 4, 7, 10, 13, 16, 19]); ax.set_xticklabels(['ene-24', 'abr-24', 'jul-24', 'oct-24', 'ene-25', 'abr-25', 'jul-25'])
ax.set_ylabel('Incidentes'); ax.set_title('Serie mensual de incidentes: sin tendencia clara'); ax.legend(frameon=False, fontsize=7, loc='lower left')
fuente(ax, 'Fuente: elaboración propia con BD1 (ene-2024 a jun-2025).')
save('f11_serie')

# M15 Teoría de colas M/M/c (BD2 Bogotá, turno tarde)
bog = b2[b2.Ciudad == 'Bogotá']
lam_turno = bog[bog.Turno.str.startswith('Tarde')].Llamadas_123.mean(); lam = lam_turno/8   # llamadas por hora
mu = 60/45                                                      # supuesto: 45 min por atención
def erlang(c, lam, mu):
    a = lam/mu; rho = a/c
    if rho >= 1: return dict(c=c, rho=rho, pw=1, wq=float('inf'), lq=float('inf'))
    s0 = sum(a**k/math.factorial(k) for k in range(c)); last = a**c/(math.factorial(c)*(1-rho))
    pw = last/(s0+last); lq = pw*rho/(1-rho); wq = lq/lam
    return dict(c=c, rho=rho, pw=pw, wq=wq*60, lq=lq)
R['colas'] = dict(lam_turno=lam_turno, lam=lam, mu=mu, filas=[erlang(c, lam, mu) for c in (2, 3, 4, 5)])

# M16 Monte Carlo (BD2): demanda Poisson vs capacidad
rng = np.random.default_rng(2026)
cap_pat = (b2.Incidentes_Atendidos/b2.Patrullas_Disponibles).median()
lam_t = b2[b2.Turno.str.startswith('Tarde')].Llamadas_123.mean()
dem = rng.poisson(lam_t, 10000)
mc = {}
for c in (2, 3, 4):
    noat = np.maximum(dem - round(cap_pat*c), 0)
    mc[c] = dict(cap=round(cap_pat*c), pct_turnos=(noat > 0).mean()*100, media_noat=noat.mean(), pct_noat=noat.sum()/dem.sum()*100)
R['mc'] = dict(cap_pat=cap_pat, lam=lam_t, res=mc)
fig, ax = plt.subplots(figsize=(5.8, 2.7))
ax.hist(dem, bins=range(0, 30), color=AZ2, edgecolor='white', density=True, label='Demanda simulada (llamadas por turno)')
for c, col in zip((2, 3, 4), (RO, DO, VE)): ax.axvline(mc[c]['cap']+0.5, color=col, lw=2, label=f'Capacidad con {c} patrullas ({mc[c]["cap"]})')
ax.set_xlabel('Llamadas al 123 en el turno de tarde'); ax.set_ylabel('Proporción de turnos'); ax.legend(frameon=False, fontsize=7)
ax.set_title('Monte Carlo: 10.000 turnos de tarde simulados')
fuente(ax, 'Fuente: elaboración propia con BD2. Demanda Poisson; capacidad: 4 incidentes por patrulla y turno.')
save('f12_montecarlo')

# M17 K-Means (BD1)
XY = b1[['Latitud', 'Longitud']].values
sil = {k: silhouette_score(XY, KMeans(k, n_init=20, random_state=1).fit_predict(XY)) for k in range(3, 9)}
kbest = max(sil, key=sil.get); km = KMeans(kbest, n_init=20, random_state=1).fit(XY); b1['cl'] = km.labels_
cl = b1.groupby('cl').agg(n=('ID_Caso', 'size'), tr=('Tiempo_Respuesta_Min', 'mean'), cap=('Captura', 'mean'),
                          loc=('Localidad', lambda s: s.value_counts().index[0]), lat=('Latitud', 'mean'), lon=('Longitud', 'mean')).sort_values('n', ascending=False)
R['kmeans'] = dict(sil={k: round(v, 3) for k, v in sil.items()}, k=kbest, clusters=cl.round(4).reset_index().values.tolist())
fig, ax = plt.subplots(figsize=(5.0, 4.0))
for i, c in enumerate(cl.index):
    d = b1[b1.cl == c]; ax.scatter(d.Longitud, d.Latitud, s=12, alpha=.7, color=PAL[i % len(PAL)], label=f'Foco {i+1}: {cl.loc[c, "loc"]} ({cl.loc[c, "n"]})')
    ax.scatter(cl.loc[c, 'lon'], cl.loc[c, 'lat'], marker='X', s=110, color=PAL[i % len(PAL)], edgecolor='k')
ax.set_xlabel('Longitud'); ax.set_ylabel('Latitud'); ax.set_title(f'K-Means: {kbest} focos geográficos de incidentes')
ax.legend(frameon=False, fontsize=6.5, loc='best'); fuente(ax, 'Fuente: elaboración propia con BD1. X: centroide de cada foco.')
save('f13_kmeans')

# M18 Cadena de Markov (BD3 hoja ejemplo)
est = ['Libre sin antecedentes', 'Capturado 1.ª vez', 'Libertad con antecedentes', 'Reincidente', 'Rehabilitado']
P = np.array([[.85, .15, 0, 0, 0], [0, 0, .7, .1, .2], [0, .25, .35, .25, .15], [0, .1, .3, .45, .15], [.6, .05, .15, .05, .15]])
v0 = np.array([0, 1, 0, 0, 0]); evo = [v0]
for _ in range(8): evo.append(evo[-1]@P)
w, V = np.linalg.eig(P.T); pi = np.real(V[:, np.argmin(abs(w-1))]); pi = pi/pi.sum()
R['markov'] = dict(P=P.tolist(), P2=np.round(np.linalg.matrix_power(P, 2), 4).tolist(), P3=np.round(np.linalg.matrix_power(P, 3), 4).tolist(),
                   evo=[np.round(e, 4).tolist() for e in evo], pi=np.round(pi, 4).tolist(), est=est)
fig, ax = plt.subplots(figsize=(6.0, 2.8)); E = np.array(evo)
for j in range(5): ax.plot(range(9), E[:, j], marker='o', ms=3, color=PAL[j], label=est[j])
ax.set_xlabel('Periodo'); ax.set_ylabel('Probabilidad'); ax.set_title('Markov: evolución de quien es capturado por primera vez')
ax.legend(frameon=False, fontsize=7, ncol=2); fuente(ax, 'Fuente: elaboración propia con la matriz de transición de BD3.')
save('f14_markov')

old = json.load(open('cifras_guia.json')); old.update(R)
json.dump(old, open('cifras_guia.json', 'w'), ensure_ascii=False, indent=1, default=float)
print(json.dumps(R, ensure_ascii=False, default=float))
