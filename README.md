# spotify_etl
### Deskripsi
Goals dari project ini adalam membuat data pipeline dan warehouse untuk top song global di spotify. Data yang di akses meliputi Artist, Album, dan Song. Tools yang digunakan yaitu Python dan beberapa service di AWS, antara lain  S3, AWS lambda, AWS Glue, Cloud Watch dan AWS Athena. Data yang di ekstrak dalam bentuk json dan disimpan dalam datawarehouse dalam bentuk table relational.

### Tujuan
1. Mengekstrak data top song, artist dan album lewat API spotify
2. Membuat Data Warehouse berbasis Cloud

### Workflow
![alt text](https://github.com/Muhammadfaizaladdi/spotify_etl/blob/main/pictures/workflow.png?raw=true)

### Tools
1. Amazon S3
    Amazon S3 ( Simple Storage Service) adalah servis object storage yang scalable. S3 dapat digunakan untuk menyimpan dan mengakses data dalam jumlah banyak dan berasal dari web mana saja. Biasanya digunakan untuk mendistribusikan file dengan size yang cukup besar, penyimpanan data backup dan/atau file-file website statis.
    
2. AWS Lambda
    AWS lambda merupakan servis komputasi yang bersifat serverles. Memungkinkan pengguna untuk menjalankan kode tanpa harus mengelola server. Lambda dapat digunakan untuk menjalankan kode yang dapat memberikan perubahan di S3, DynamoDB, ataupun servis lainnya di AWS.
    
3. Amazon Cloud Watch
    Cloud Watch adalah service untuk memonitoring resources dan aplikasi yang dijalankan di Cloud AWS. Servis ini dapat digunakan untuk tracking metrics, mengumpulkan dan memonitor log files, serta dapat digunakan untuk membuat alarm.
    
4. Data Crawler
    AWS Glue Crawler merupakan servis yang dapat mengakses data secara otomatis, identifikasi format data, dan membuat/menduga schema yang akan dibuat di AWS Glue Data Catalog
    
5. AWS Glue Data Catalog
    Glue Data Catalog servis yang disediakan untuk mengelola repositori metadata. Servis ini memudahkan pengguna untuk mencari dan mengelola data di AWS.
    
6. AWS Athena
    Amazon Athena adalah servis query interaktif yang memungkinkan pengguna untuk menganalisa data di Amzon S3 dengan menggunakan SQL. Servis ini dapat digunakan pada data yang ada di Glue data Catalog maupun bucket S3.

### Kesimpulan dan Hasil
Project ini mengimplementasikan proses Extract, Transform dan Load (ETL) dari sebuah data warehouse berbasis cloud. Skill yang diimplementasikan dan didapatkan dari project ini antara lain:

- Mengakses data spotify menggunakan API
- Memahami beberapa produk AWS yang digunakan dalam proses pembuatan pipeline data.
- Mengembangkan pipeline ETL menggunakan aws lambda, membuat trigger pada aws lambda agar berjalan secara otomatis. Membuat staging area dengan menggunakan layanan S3, membuat table dan schema menggunakan crawler, serta mengakses database lewat Amazon Athena
- Mengubah data dari semi-structured (json file) menjadi structured data (tabel).

**Note**: Langkah pengerjaan project dapat di baca di [tautan berikut](https://faizaladdi.notion.site/faizaladdi/ETL-of-Spotify-Top-Global-Song-a6c8dc61e62f48d891354fd9f6be355b).
