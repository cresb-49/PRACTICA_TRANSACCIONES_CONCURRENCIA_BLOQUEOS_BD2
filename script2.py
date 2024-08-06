import threading
import time
import mysql.connector
import logging

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '201931012',
    'database': 'tcbDB2',
    'port': 3306
}

# Configurar el logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s')


class MovimientoDB:
    def __init__(self, config):
        self.config = config

    def connect(self):
        return mysql.connector.connect(**self.config)
    
    def test_db_update(self, initial_value=0):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            logging.info("Probando la conexión a la base de datos")
            cursor.execute("SELECT valor FROM movimiento WHERE id = 1")
            current_value = cursor.fetchone()[0]
            logging.info("Valor actual: %s", current_value)
            logging.info("Get exitoso")
            cursor.execute(
                "UPDATE movimiento SET valor = %s WHERE id = 1", (initial_value,))
            cursor.execute("COMMIT")
            cursor.execute("SELECT valor FROM movimiento WHERE id = 1")
            current_value = cursor.fetchone()[0]
            logging.info("Valor actual: %s", current_value)
            logging.info("Update exitoso")
            cursor.close()
            conn.close()
        except Exception as e:
            logging.error("Error al conectar a la base de datos: %s", e)

    def update_value(self, conn, increment):
        try:
            cursor = conn.cursor()
            logging.info("Obteniendo el valor actual de la base de datos")
            cursor.execute("START TRANSACTION")
            cursor.execute(
                "SELECT valor FROM movimiento WHERE id = 1 FOR UPDATE")
            current_value = cursor.fetchone()[0]
            new_value = current_value + increment
            logging.info("new_value = current_value + increment -> %s = %s + %s", new_value, current_value, increment)
            cursor.execute(
                "UPDATE movimiento SET valor = %s WHERE id = 1", (new_value,))
            cursor.execute("COMMIT")
            logging.info(
                "Valor actualizado. Incremento: %s, Nuevo Valor: %s", increment, new_value)
            cursor.close()
        except Exception as e:
            logging.error("Error al actualizar el valor: %s", e)
            
    def get_final_value(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT valor FROM movimiento WHERE id = 1")
        final_value = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return final_value


def increment(db_config, amount, interval, duration):
    logging.info("Hilo de incremento iniciado")
    conn = mysql.connector.connect(**db_config)
    start_time = time.time()
    end_time = start_time + duration
    while time.time() < end_time:
        db = MovimientoDB(db_config)
        db.update_value(conn, amount)
        time.sleep(interval)
    conn.close()
    logging.info("Hilo de incremento finalizado. Duración: %.4f segundos",
                 time.time() - start_time)


def decrement(db_config, amount, interval, duration):
    logging.info("Hilo de decremento iniciado")
    conn = mysql.connector.connect(**db_config)
    start_time = time.time()
    end_time = start_time + duration
    while time.time() < end_time:
        db = MovimientoDB(db_config)
        db.update_value(conn, -amount)
        time.sleep(interval)
    conn.close()
    logging.info("Hilo de decremento finalizado. Duración: %.4f segundos",
                 time.time() - start_time)


if __name__ == "__main__":
    # Parámetros
    valor_incremento = 5
    valor_decremento = 3
    intervalo_incremento = 1  # Segundos de espera de ejecución
    intervalo_decremento = 2  # Segundos de espera de ejecución
    duracion = 10  # Duración del experimento

    db = MovimientoDB(db_config)
    db.test_db_update()
    
    logging.info("Iniciando hilos")

    # Hilos de ejecución
    increment_thread = threading.Thread(target=increment, args=(
        db_config, valor_incremento, intervalo_incremento, duracion), name="IncrementThread")
    decrement_thread = threading.Thread(target=decrement, args=(
        db_config, valor_decremento, intervalo_decremento, duracion), name="DecrementThread")

    # Registrar el tiempo de inicio de toda la operación
    total_start_time = time.time()

    increment_thread.start()
    decrement_thread.start()

    increment_thread.join()
    decrement_thread.join()

    # Registrar el tiempo de finalización de toda la operación
    total_end_time = time.time()

    logging.info("Todos los hilos finalizados. Tiempo total de ejecución: %.4f segundos",
                 total_end_time - total_start_time)
    logging.info("Valor final: %s", MovimientoDB(db_config).get_final_value())
