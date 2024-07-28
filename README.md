# PRACTICA_TRANSACCIONES_CONCURRENCIA_BLOQUEOS_BD2
Pasos para levantar en local
1. Crear el entrono virtual
    ```sh
    python3 -m venv venv
    ```
2. Activacion del entorno
    ```sh
    source venv/bin/activate
    ```
3. Instalacion de los requerimientos
    ```sh
    pip3 install -r requirements.txt
    ```

Script de creacion del docker de MYSQL

1. Creacion del volumen
    ```sh
    docker volume create mysql_data
    ```
2. Creacion del docker
    ```sh
    docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=201931012 -e MYSQL_DATABASE=tcbDB2 -e MYSQL_USER=benjamin -e MYSQL_PASSWORD=201931012 -v mysql_data:/var/lib/mysql -p 3306:3306 -d mysql:latest
    ```