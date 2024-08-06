import threading
import time
import mysql.connector
import logging

# Configurar el logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s')


class MovimientoDB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='201931012',
            database='tcbDB2',
            port=3306
        )
        self.cursor = self.conn.cursor()

    def test_db_update(self, initial_value=0):
        try:
            logging.info("Probando la conexión a la base de datos")
            self.cursor.execute("SELECT valor FROM movimiento WHERE id = 1")
            current_value = self.cursor.fetchone()[0]
            logging.info("Valor actual: %s", current_value)
            logging.info("Get exitoso")
            self.cursor.execute(
                "UPDATE movimiento SET valor = %s WHERE id = 1", (initial_value,))
            self.cursor.execute("SELECT valor FROM movimiento WHERE id = 1")
            current_value = self.cursor.fetchone()[0]
            logging.info("Valor actual: %s", current_value)
            logging.info("Update exitoso")
        except Exception as e:
            logging.error("Error al conectar a la base de datos: %s", e)

    def update_value(self, increment):
        try:
            logging.info("Obteniendo el valor actual de la base de datos")
            self.cursor.execute("SELECT valor FROM movimiento WHERE id = 1")
            current_value = self.cursor.fetchone()[0]
            logging.info("Valor actual: %s", current_value)
            new_value = current_value + increment
            logging.info("Nuevo valor: %s", new_value)
            self.cursor.execute(
                "UPDATE movimiento SET valor = %s WHERE id = 1", (new_value,))
            logging.info(
                "Valor actualizado. Incremento: %s, Nuevo Valor: %s", increment, new_value)
        except Exception as e:
            logging.error("Error al actualizar el valor: %s", e)

    def close(self):
        self.cursor.close()
        self.conn.close()


def increment(db, amount, interval, duration):
    logging.info("Hilo de incremento iniciado")
    start_time = time.time()
    end_time = start_time + duration
    while time.time() < end_time:
        db.update_value(amount)
        time.sleep(interval)
    logging.info("Hilo de incremento finalizado. Duración: %.4f segundos",
                 time.time() - start_time)


def decrement(db, amount, interval, duration):
    logging.info("Hilo de decremento iniciado")
    start_time = time.time()
    end_time = start_time + duration
    while time.time() < end_time:
        db.update_value(-amount)
        time.sleep(interval)
    logging.info("Hilo de decremento finalizado. Duración: %.4f segundos",
                 time.time() - start_time)


if __name__ == "__main__":
    db = MovimientoDB()

    # Parámetros
    valor_incremento = 5
    valor_decremento = 3
    intervalo_incremento = 1  # Segundos de espera de ejecución
    intervalo_decremento = 2  # Segundos de espera de ejecución
    duracion = 10  # Duración del experimento

    logging.info("Iniciando hilos")

    db.test_db_update()

    # Hilos de ejecución
    increment_thread = threading.Thread(target=increment, args=(
        db, valor_incremento, intervalo_incremento, duracion), name="IncrementThread")
    decrement_thread = threading.Thread(target=decrement, args=(
        db, valor_decremento, intervalo_decremento, duracion), name="DecrementThread")

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

    db.close()
