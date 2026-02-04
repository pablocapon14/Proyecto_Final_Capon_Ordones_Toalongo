import pandas as pd

# ===============================
# ========= LEER CSV ============
# ===============================
df = pd.read_csv(r"dron_datos_K5.csv")

# ===============================
# ========= PARÁMETROS ==========
# ===============================
ALTURA_OBJETIVO = 100
TOLERANCIA = 0.5       #por si hay ruido

ALTURA_130 = 130
ALTURA_90  = 90
ALTURA_110 = 110


df["en_100"] = (df["altura_cm"] >= ALTURA_OBJETIVO - TOLERANCIA) & \
               (df["altura_cm"] <= ALTURA_OBJETIVO + TOLERANCIA)

df["en_130"] = (df["altura_cm"] >= ALTURA_130 - TOLERANCIA) & \
               (df["altura_cm"] <= ALTURA_130 + TOLERANCIA)

df["en_90"] = (df["altura_cm"] >= ALTURA_90 - TOLERANCIA) & \
              (df["altura_cm"] <= ALTURA_90 + TOLERANCIA)

df["en_110"] = (df["altura_cm"] >= ALTURA_110 - TOLERANCIA) & \
               (df["altura_cm"] <= ALTURA_110 + TOLERANCIA)

# ===============================
# = PRIMERA VEZ QUE LLEGA A 100 =
# ===============================
idx_primera = df.index[df["en_100"]].min()

if pd.isna(idx_primera):
    print("Nunca llega a 100 cm")
    exit()

tiempo_primera = df.loc[idx_primera, "tiempo_s"]

# ===============================
# ===== CUANDO SALE DE 100 ======
# ===============================

idx_salida = None
for i in range(idx_primera + 1, len(df)):
    if not df.loc[i, "en_100"]:
        idx_salida = i
        break

if idx_salida is None:
    print("Nunca sale de 100 cm")
    exit()

# ===============================
# ==== CUANDO REGRESA A 100 =====
# ===============================

idx_regreso = None
for i in range(idx_salida + 1, len(df)):
    if df.loc[i, "en_100"]:
        idx_regreso = i
        break

if idx_regreso is None:
    print("Nunca regresa a 100 cm")
    exit()

# ========= CALCULO t1 =========
tiempo_regreso = df.loc[idx_regreso, "tiempo_s"]

# ========= CALCULO t2 =========
tiempo_sobreimpulso = tiempo_regreso - tiempo_primera

# ==============================
# = LLEGA A 130 DESPUÉS DE 100 =
# ==============================

idx_130 = None
for i in range(idx_primera + 1, len(df)):
    if df.loc[i, "en_130"]:
        idx_130 = i
        break

if idx_130 is None:
    print("Nunca llega a 130 cm")
    exit()

tiempo_130 = df.loc[idx_130, "tiempo_s"]

# ===============================
# ==== CUANDO REGRESA A 100 =====
# ===============================

idx_100_post_130 = None
for i in range(idx_130 + 1, len(df)):
    if df.loc[i, "en_100"]:
        idx_100_post_130 = i
        break

if idx_100_post_130 is None:
    print("No regresa a 100 después de 130")
    exit()

# ================================
# ===== ENSEGUIDA BAJA A 90 ======
# ================================

idx_90 = None
for i in range(idx_100_post_130 + 1, len(df)):
    if df.loc[i, "en_90"]:
        idx_90 = i
        break

if idx_90 is None:
    print("Nunca baja a 90 cm")
    exit()

# ===============================
# ==== CUANDO REGRESA A 100 =====
# ===============================

idx_100_final = None
for i in range(idx_90 + 1, len(df)):
    if df.loc[i, "en_100"]:
        idx_100_final = i
        break

if idx_100_final is None:
    print("No regresa a 100 después de bajar a 90")
    exit()

tiempo_100_final = df.loc[idx_100_final, "tiempo_s"]

# ========= CALCULO t3 =========
tiempo_ref1 = tiempo_100_final - tiempo_130

# ===============================
# ====== CUANDO BAJA A 90 =======
# ===============================

idx_90_2 = None
for i in range(idx_100_final + 1, len(df)):
    if df.loc[i, "en_90"]:
        idx_90_2 = i
        break

if idx_90_2 is None:
    print("No vuelve a bajar a 90 cm")
    exit()

tiempo_90_2 = df.loc[idx_90_2, "tiempo_s"]

# ===============================
# ==== CUANDO REGRESA A 100 =====
# ===============================

idx_100_post_90_2 = None
for i in range(idx_90_2 + 1, len(df)):
    if df.loc[i, "en_100"]:
        idx_100_post_90_2 = i
        break

if idx_100_post_90_2 is None:
    print("No regresa a 100 después de bajar a 90 (segunda vez)")
    exit()

# =================================
# ===== ENSEGUIDA SUBE A 110 ======
# =================================
idx_110 = None
for i in range(idx_100_post_90_2 + 1, len(df)):
    if df.loc[i, "en_110"]:
        idx_110 = i
        break

if idx_110 is None:
    print("Nunca sube a 110 cm")
    exit()

# ===============================
# ==== CUANDO REGRESA A 100 =====
# ===============================

idx_100_post_110 = None
for i in range(idx_110 + 1, len(df)):
    if df.loc[i, "en_100"]:
        idx_100_post_110 = i
        break

if idx_100_post_110 is None:
    print("No regresa a 100 después de subir a 110")
    exit()

tiempo_100_post_110 = df.loc[idx_100_post_110, "tiempo_s"]

# ========= CALCULO t4 =========
tiempo_ref2 = tiempo_100_post_110 - tiempo_90_2

# ===============================
# ====== CUANDO BAJA A 90 =======
# ===============================

idx_90_3 = None
for i in range(idx_100_post_110 + 1, len(df)):
    if df.loc[i, "en_90"]:
        idx_90_3 = i
        break

if idx_90_3 is None:
    print("No ocurre el tercer evento: no baja a 90")
    exit()

tiempo_90_3 = df.loc[idx_90_3, "tiempo_s"]

# ===============================
# ==== CUANDO REGRESA A 100 =====
# ===============================

idx_100_post_90_3 = None
for i in range(idx_90_3 + 1, len(df)):
    if df.loc[i, "en_100"]:
        idx_100_post_90_3 = i
        break

if idx_100_post_90_3 is None:
    print("No regresa a 100 después del tercer 90")
    exit()

# =================================
# ===== ENSEGUIDA SUBE A 110 ======
# =================================

idx_110_2 = None
for i in range(idx_100_post_90_3 + 1, len(df)):
    if df.loc[i, "en_110"]:
        idx_110_2 = i
        break

if idx_110_2 is None:
    print("No sube a 110 en el tercer evento")
    exit()

# ===============================
# ==== CUANDO REGRESA A 100 =====
# ===============================

idx_100_post_110_2 = None
for i in range(idx_110_2 + 1, len(df)):
    if df.loc[i, "en_100"]:
        idx_100_post_110_2 = i
        break

if idx_100_post_110_2 is None:
    print("No regresa a 100 después del segundo 110")
    exit()

tiempo_100_post_110_2 = df.loc[idx_100_post_110_2, "tiempo_s"]

# ========= CALCULO t5 =========
tiempo_ref3 = tiempo_100_post_110_2 - tiempo_90_3


# ===============================
# RESULTADOS
# ===============================
print("==================================================================================")
print("=============================== RESULTADOS TIEMPOS ===============================")
print("==================================================================================")
print(f"       Tiempo de establecimiento:                      t1 = {tiempo_regreso:.3f} s")
print("----------------------------------------------------------------------------------")
print(f"       Tiempo de sobre impulso:                        t2 = {tiempo_sobreimpulso:.3f} s")
print("----------------------------------------------------------------------------------")
print(f"       Tiempo en regresar a la referencia caso 1:      t3 = {tiempo_ref1:.3f} s")
print("----------------------------------------------------------------------------------")
print(f"       Tiempo en regresar a la referencia caso 2:      t4 = {tiempo_ref2:.3f} s")
print("----------------------------------------------------------------------------------")
print(f"       Tiempo en regresar a la referencia caso 3:      t5 = {tiempo_ref3:.3f} s")
print("==================================================================================")