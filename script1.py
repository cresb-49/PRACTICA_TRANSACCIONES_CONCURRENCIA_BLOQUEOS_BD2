# Se implementa el algoritmo (sin bloqueos)

import threading
import time
import mysql.connector

class MovimientoDB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='201931012',
            database='tcbDB2'
        )
        self.cursor = self.conn.cursor()

    def update_value(self, increment):
        self.cursor.execute("SELECT valor FROM Movimiento WHERE id = 1")
        current_value = self.cursor.fetchone()[0]
        new_value = current_value + increment
        self.cursor.execute("UPDATE Movimiento SET valor = %s WHERE id = 1", (new_value,))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

def increment(db, amount, interval, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        db.update_value(amount)
        time.sleep(interval)

def decrement(db, amount, interval, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        db.update_value(-amount)
        time.sleep(interval)

if __name__ == "__main__":
    db = MovimientoDB()
    
    # Parametros
    valor_incremento = 5
    valor_decremento = 3
    intervalo_incremento = 1  # Segundos de espera de ejecucion
    intervalo_decremento = 2  # Segundos de espera de ejecucion
    duracion = 10  # Duracion del experimento

    # Hilos de ejecucion
    increment_thread = threading.Thread(target=increment, args=(db, valor_incremento, intervalo_incremento, duracion))
    decrement_thread = threading.Thread(target=decrement, args=(db, valor_decremento, intervalo_decremento, duracion))

    increment_thread.start()
    decrement_thread.start()

    increment_thread.join()
    decrement_thread.join()

    db.close()
