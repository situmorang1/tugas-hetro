import csv
import os
from collections import deque

# Kapasitas maksimal parkiran
MAKS_PARKIR = 5

# File CSV
FILE_PARKIR = "parkiran.csv"
FILE_ANTREAN = "antrean.csv"

# Fungsi bantu: membaca CSV ke list
def baca_csv_ke_list(nama_file):
    if not os.path.exists(nama_file):
        return []
    with open(nama_file, mode='r', newline='') as file:
        return [row[0] for row in csv.reader(file)]

# Fungsi bantu: menyimpan list ke CSV
def simpan_list_ke_csv(nama_file, data_list):
    with open(nama_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        for item in data_list:
            writer.writerow([item])

# Fungsi menampilkan menu
def tampilkan_menu():
    print("\n=== SISTEM PARKIR (QUEUE & STACK via CSV) ===")
    print("1. Tambah Kendaraan ke Antrean Masuk")
    print("2. Proses Masuk Kendaraan ke Parkiran")
    print("3. Keluarkan Kendaraan dari Parkiran")
    print("4. Lihat Status Parkiran dan Antrean")
    print("5. Keluar")

# Fungsi untuk menambah kendaraan ke antrean masuk
def tambah_antrean():
    antrean = deque(baca_csv_ke_list(FILE_ANTREAN))
    plat = input("Masukkan plat nomor kendaraan: ")
    antrean.append(plat)
    simpan_list_ke_csv(FILE_ANTREAN, antrean)
    print(f"Kendaraan {plat} ditambahkan ke antrean.")

# Fungsi untuk memproses kendaraan masuk ke parkiran
def proses_masuk():
    antrean = deque(baca_csv_ke_list(FILE_ANTREAN))
    parkiran = baca_csv_ke_list(FILE_PARKIR)

    if len(parkiran) >= MAKS_PARKIR:
        print("Parkiran penuh.")
    elif not antrean:
        print("Tidak ada kendaraan dalam antrean.")
    else:
        kendaraan = antrean.popleft()
        parkiran.append(kendaraan)
        simpan_list_ke_csv(FILE_ANTREAN, antrean)
        simpan_list_ke_csv(FILE_PARKIR, parkiran)
        print(f"Kendaraan {kendaraan} masuk ke parkiran.")

# Fungsi untuk mengeluarkan kendaraan dari parkiran
def keluarkan_kendaraan():
    parkiran = baca_csv_ke_list(FILE_PARKIR)
    plat = input("Masukkan plat nomor kendaraan yang ingin keluar: ")

    if plat not in parkiran:
        print(f"Kendaraan {plat} tidak ditemukan di parkiran.")
        return

    temp_stack = []
    # Mengeluarkan kendaraan sampai menemukan yang dicari
    while parkiran:
        kendaraan = parkiran.pop()
        if kendaraan == plat:
            print(f"Kendaraan {plat} telah keluar dari parkiran.")
            break
        else:
            temp_stack.append(kendaraan)

    # Masukkan kembali kendaraan lainnya
    while temp_stack:
        parkiran.append(temp_stack.pop())

    simpan_list_ke_csv(FILE_PARKIR, parkiran)

# Fungsi untuk menampilkan status parkiran dan antrean
def tampilkan_status():
    parkiran = baca_csv_ke_list(FILE_PARKIR)
    antrean = baca_csv_ke_list(FILE_ANTREAN)

    print("\n--- STATUS PARKIRAN ---")
    if parkiran:
        print("Parkiran (dari pintu masuk ke dalam):")
        for kendaraan in reversed(parkiran):
            print(f"-> {kendaraan}")
    else:
        print("Parkiran kosong.")

    print("\nAntrean masuk:")
    if antrean:
        for kendaraan in antrean:
            print(f"-> {kendaraan}")
    else:
        print("Tidak ada kendaraan dalam antrean.")

# Program utama
while True:
    tampilkan_menu()
    pilihan = input("Pilih menu (1-5): ")

    if pilihan == '1':
        tambah_antrean()
    elif pilihan == '2':
        proses_masuk()
    elif pilihan == '3':
        keluarkan_kendaraan()
    elif pilihan == '4':
        tampilkan_status()
    elif pilihan == '5':
        print("Terima kasih. Program selesai.")
        break
    else:
        print("Pilihan tidak valid.")