from djitellopy import Tello
import time
import csv

# ===============================
# PARAMETROS DEL PID (AJUSTABLES)
# ===============================
Kp = 0.6
Ki = 0.04
Kd = 0.2

# Altura deseada
ALTURA_REF = 80    # cm

# Saturacion de velocidad
VZ_MAX = 30        # cm/s

# Muestreo
TS = 0.05          # 20 Hz
TIEMPO_TOTAL = 20  # s

ARCHIVO_CSV = "pid_altura_datos.csv"

# ===============================
# INICIALIZACION
# ===============================
tello = Tello()
tello.connect()

print(f"Bateria: {tello.get_battery()}%")

tello.takeoff()
time.sleep(2)

# Altura de referencia inicial
altura_ref_sensor = tello.get_height()
print(f"Referencia inicial: {altura_ref_sensor} cm")

# Variables PID
error_prev = 0.0
integral = 0.0

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
            # PID
            # ===============================
            error = ALTURA_REF - altura
            integral += error * TS
            derivada = (error - error_prev) / TS

            vz_cmd = (
                Kp * error +
                Ki * integral +
                Kd * derivada
            )

            error_prev = error

            # Saturacion
            vz_cmd = max(min(vz_cmd, VZ_MAX), -VZ_MAX)

            # Enviar solo velocidad vertical
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
                f"t={t:5.2f}s | h={altura:5.1f} cm | "
                f"e={error:5.1f} | vz={vz_cmd:5.1f}"
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
print("✅ Control PID finalizado")
print(f"📁 Datos guardados en {ARCHIVO_CSV}")
