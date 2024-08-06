# import threading
# import time
# import mysql.connector

# class MovimientoDB:
#     def __init__(self):
#         self.conn = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='password',
#             database='Practica'
#         )
#         self.cursor = self.conn.cursor()
#         self.lock = threading.Lock()

#     def update_value(self, increment):
#         with self.lock:
#             self.cursor.execute("SELECT valor FROM Movimiento WHERE id = 1 FOR UPDATE")
#             current_value = self.cursor.fetchone()[0]
#             new_value = current_value + increment
#             self.cursor.execute("UPDATE Movimiento SET valor = %s WHERE id = 1", (new_value,))
#             self.conn.commit()

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
#     increment_amount = 5
#     decrement_amount = 3
#     increment_interval = 1  # seconds
#     decrement_interval = 2  # seconds
#     execution_duration = 10  # seconds

#     # Hilos
#     increment_thread = threading.Thread(target=increment, args=(db, increment_amount, increment_interval, execution_duration))
#     decrement_thread = threading.Thread(target=decrement, args=(db, decrement_amount, decrement_interval, execution_duration))

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
            password='password',
            database='Practica'
        )
        self.cursor = self.conn.cursor()
        self.lock = threading.Lock()

    def update_value(self, increment):
        with self.lock:
            try:
                logging.info("Acquiring lock and starting transaction for increment: %s", increment)
                start_time = time.time()
                self.cursor.execute("SELECT valor FROM Movimiento WHERE id = 1 FOR UPDATE")
                current_value = self.cursor.fetchone()[0]
                new_value = current_value + increment
                self.cursor.execute("UPDATE Movimiento SET valor = %s WHERE id = 1", (new_value,))
                self.conn.commit()
                end_time = time.time()
                logging.info("Transaction committed. Increment: %s, New Value: %s, Duration: %.4f seconds", increment, new_value, end_time - start_time)
            except Exception as e:
                self.conn.rollback()
                logging.error("Transaction failed: %s", e)

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
    increment_amount = 5
    decrement_amount = 3
    increment_interval = 1  # seconds
    decrement_interval = 2  # seconds
    execution_duration = 10  # seconds

    logging.info("Starting threads")
    
    # Threads
    increment_thread = threading.Thread(target=increment, args=(db, increment_amount, increment_interval, execution_duration), name="IncrementThread")
    decrement_thread = threading.Thread(target=decrement, args=(db, decrement_amount, decrement_interval, execution_duration), name="DecrementThread")

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
