from djitellopy import Tello
import time
import csv

# ===============================
# PARAMETROS DEL CONTROLADOR P
# ===============================
Kp = 5              # Ganancia proporcional (ajustable)
ALTURA_REF = 100      # cm (referencia de altura)

VZ_MAX = 35           # cm/s (saturacion segura)
TS = 0.05             # 20 Hz
TIEMPO_TOTAL = 20     # s

ARCHIVO_CSV = "dron_datos_K5.csv"

# ===============================
# INICIALIZACION
# ===============================
tello = Tello()
tello.connect()

print(f"Bateria: {tello.get_battery()}%")

tello.takeoff()
time.sleep(2)

# Referencia del sensor (altura relativa)
altura_ref_sensor = 10
print(f"Altura inicial sensor: {altura_ref_sensor} cm")

t0 = time.time()

# ===============================
# CSV
# ===============================
with open(ARCHIVO_CSV, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        "tiempo_s",
        "altura_ref_cm",
        "altura_cm",
        "error_cm",
        "vz_cmd_cm_s"
    ])

    try:
        while True:
            t = time.time() - t0
            if t > TIEMPO_TOTAL:
                break

            # ===============================
            # MEDICION
            # ===============================
            altura_abs = tello.get_height()
            altura = altura_abs - altura_ref_sensor

            # ===============================
            # CONTROLADOR P
            # ===============================
            error = ALTURA_REF - altura
            vz_cmd = Kp * error

            # Saturacion
            vz_cmd = max(min(vz_cmd, VZ_MAX), -VZ_MAX)

            # Solo eje vertical
            tello.send_rc_control(0, 0, int(vz_cmd), 0)

            # ===============================
            # REGISTRO
            # ===============================
            writer.writerow([
                round(t, 3),
                ALTURA_REF,
                altura,
                error,
                vz_cmd
            ])

            print(
                f"t={t:5.2f}s | h={altura:6.1f} cm | "
                f"e={error:6.1f} | vz={vz_cmd:6.1f}"
            )

            time.sleep(TS)

    except KeyboardInterrupt:
        print("⛔ Interrumpido")

# ===============================
# FINALIZACION SEGURA
# ===============================
tello.send_rc_control(0, 0, 0, 0)
time.sleep(1)
tello.land()
print(f"Batería: {tello.get_battery()}%")
print("✅ Control P finalizado")
print(f"📁 Datos guardados en {ARCHIVO_CSV}")
