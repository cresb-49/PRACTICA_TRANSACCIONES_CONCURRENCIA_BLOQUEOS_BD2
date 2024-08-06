# # Se implementa el algoritmo (sin bloqueos)

# import threading
# import time
# import mysql.connector

# class MovimientoDB:
#     def __init__(self):
#         self.conn = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='201931012',
#             database='tcbDB2'
#         )
#         self.cursor = self.conn.cursor()

#     def update_value(self, increment):
#         self.cursor.execute("SELECT valor FROM Movimiento WHERE id = 1")
#         current_value = self.cursor.fetchone()[0]
#         new_value = current_value + increment
#         self.cursor.execute("UPDATE Movimiento SET valor = %s WHERE id = 1", (new_value,))
#         self.conn.commit()

#     def close(self):
#         self.cursor.close()
#         self.conn.close()

# def increment(db, amount, interval, duration):
#     end_time = time.time() + duration
#     while time.time() < end_time:
#         db.update_value(amount)
#         time.sleep(interval)

# def decrement(db, amount, interval, duration):
#     end_time = time.time() + duration
#     while time.time() < end_time:
#         db.update_value(-amount)
#         time.sleep(interval)

# if __name__ == "__main__":
#     db = MovimientoDB()
    
#     # Parametros
#     valor_incremento = 5
#     valor_decremento = 3
#     intervalo_incremento = 1  # Segundos de espera de ejecucion
#     intervalo_decremento = 2  # Segundos de espera de ejecucion
#     duracion = 10  # Duracion del experimento

#     # Hilos de ejecucion
#     increment_thread = threading.Thread(target=increment, args=(db, valor_incremento, intervalo_incremento, duracion))
#     decrement_thread = threading.Thread(target=decrement, args=(db, valor_decremento, intervalo_decremento, duracion))

#     increment_thread.start()
#     decrement_thread.start()

#     increment_thread.join()
#     decrement_thread.join()

#     db.close()

import threading
import time
import mysql.connector
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s')

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
        try:
            logging.info("Fetching current value from database")
            self.cursor.execute("SELECT valor FROM Movimiento WHERE id = 1")
            current_value = self.cursor.fetchone()[0]
            new_value = current_value + increment
            self.cursor.execute("UPDATE Movimiento SET valor = %s WHERE id = 1", (new_value,))
            self.conn.commit()
            logging.info("Updated value. Increment: %s, New Value: %s", increment, new_value)
        except Exception as e:
            logging.error("Failed to update value: %s", e)

    def close(self):
        self.cursor.close()
        self.conn.close()

def increment(db, amount, interval, duration):
    logging.info("Increment thread started")
    start_time = time.time()
    end_time = start_time + duration
    while time.time() < end_time:
        db.update_value(amount)
        time.sleep(interval)
    logging.info("Increment thread finished. Duration: %.4f seconds", time.time() - start_time)

def decrement(db, amount, interval, duration):
    logging.info("Decrement thread started")
    start_time = time.time()
    end_time = start_time + duration
    while time.time() < end_time:
        db.update_value(-amount)
        time.sleep(interval)
    logging.info("Decrement thread finished. Duration: %.4f seconds", time.time() - start_time)

if __name__ == "__main__":
    db = MovimientoDB()
    
    # Parameters
    valor_incremento = 5
    valor_decremento = 3
    intervalo_incremento = 1  # Segundos de espera de ejecucion
    intervalo_decremento = 2  # Segundos de espera de ejecucion
    duracion = 10  # Duracion del experimento

    logging.info("Starting threads")
    
    # Hilos de ejecucion
    increment_thread = threading.Thread(target=increment, args=(db, valor_incremento, intervalo_incremento, duracion), name="IncrementThread")
    decrement_thread = threading.Thread(target=decrement, args=(db, valor_decremento, intervalo_decremento, duracion), name="DecrementThread")

    # Record the start time of the entire operation
    total_start_time = time.time()
    
    increment_thread.start()
    decrement_thread.start()

    increment_thread.join()
    decrement_thread.join()

    # Record the end time of the entire operation
    total_end_time = time.time()

    logging.info("All threads finished. Total execution time: %.4f seconds", total_end_time - total_start_time)

    db.close()
