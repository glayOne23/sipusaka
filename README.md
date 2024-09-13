<h1 align="center">
    <img src="https://www.uinsalatiga.ac.id/wp-content/uploads/2022/12/2022-Web-UIN-Logo-1-1.png" alt="drawing" width="150"  />
    <br>
    SIPUSAKA
    <br>
</h1>

## Instalasi
### Ubuntu
1. Masuk pada direktori tempat ingin menyimpan code program
2. Clone code program dari repository. Ketik pada command line:
    ```bash
    $ git clone https://github.com/glayOne23/sipusaka.git
    ```
3. Buat environment python dan aktifkan enviroment python. Ketik pada command line:
    ```bash
    # membuat environment variable python
    $ python3 -m venv env

    # aktifkan environment variable python
    source env/bin/activate
    ```
4. Install library python yang dibutuhkan menggunakan command line berikut:
    ```bash
    # masuk ke direktory sipusaka
    $ cd sipusaka

    # install library
    $ pip install -r requirements.txt
    ```
5. Buat database mysql, download sql file pada tautan berikut: . Export sql file tersebut ke dalam database
6. Copy .env_dev dan rubah nama menjadi .env lalu sesuaikan DB_NAME, DB_USER, DB_PASSWORD,  DB_HOST, DB_PORT pada .env dengan database yang dibuat
    ```bash
    # copy .env_dev ke .env
    $ cp .env_dev .env
    ```
7. Jalankan command line berikut untuk meletakkan file static pada server:
    ```bash
    $ python manage.py collectstatic
    ```
