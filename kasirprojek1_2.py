# Sistem Kasir Sederhana seperti Indomaret
# Dibuat berdasarkan deskripsi kebutuhan fungsional (FR-01 hingga FR-06)
# Menggunakan Python OOP untuk simulasi. Data disimpan dalam memory (tidak persistent).

import datetime
#membuat database
import mysql.connector

conn=mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    database='db_kasir1',
    password= ''
)
myconn=conn.cursor()

# Kelas untuk User (Admin, Kasir, Distributor)
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role  # 'admin', 'kasir', 'distributor'

# Kelas untuk Produk
class Produk:
    def __init__(self, name, sku, harga, category, stok = 0):
        self.name = name
        self.sku = sku
        self.harga = harga 
        self.category = category  # 'Etalase Utama', 'produk Lelang'
        self.stok = stok
        self.status = 'Normal'  # 'Normal', 'Rusak Kemasan', 'Mendekati Expired'

    def mark_defect(self, status):
        self.status = status
        if status in ['Rusak Kemasan', 'Mendekati Expired']:
            self.category = 'produk Lelang'
            self.harga *= 0.5  # Auto-discount 50%
# Kolom untuk koneksi table database
def load_produk_from_db(self):
    self.produk = {}

    # Produk Reguler
    myconn.execute("SELECT no_SKU, Name_product, Price FROM produk_reguler")
    for sku, name, price in myconn.fetchall():
        p = Produk(name, sku, price, 'Etalase Utama', stok=100)
        self.produk[sku] = p

    # Produk Lelang
    myconn.execute("SELECT no_SKU, Name_product, Price FROM produk_lelang")
    for sku, name, price in myconn.fetchall():
        p = Produk(name, sku, price, 'produk Lelang', stok=50)
        self.produk[sku] = p

# Kelas untuk Inventory (Manajemen Stok)
class Inventory:
    def __init__(self):
        self.produk = {}  # key: SKU, value: Product

    def add_produk(self, produk):
        self.produk[produk.sku ] = produk

    def restock(self, sku, quantity):
        if sku in self.produk:
            self.produk[sku].stok += quantity
            print(f"Stok {self.produk[sku].name} ditambah {quantity}. Stok sekarang: {self.produk[sku].stok}")
        else:
            print("Produk tidak ditemukan.")

    def reduce_stock(self, sku, quantity):
        if sku in self.produk and self.produk[sku].stok >= quantity:
            self.produk[sku].stok -= quantity
            print(f"Stok {self.produk[sku].name} dikurangi {quantity}. Stok sekarang: {self.produk[sku].stock}")
        else:
            print("Stok tidak cukup atau produk tidak ditemukan.")

    def search_produk(self, query, is_lelang=False):
        results = []
        for sku, Produk in self.produk.items():
            if query.lower() in Produk.name.lower() or query == sku:
                if is_lelang and Produk.category == 'produk Lelang':
                    results.append(Produk)
                elif not is_lelang and Produk.category == 'Etalase Utama':
                    results.append(Produk)
        return results

# Kelas Utama Sistem
class CashierSystem:
    def __init__(self):
        self.users = {
            'admin': User('admin', 'admin123', 'admin'),
            'kasir': User('kasir', 'kasir123', 'kasir'),
            'staff': User('staff', 'staff123', 'staff')
        }
        self.inventory = Inventory()
        self.inventory.load_produk_from_db()
        self.current_user = None

    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        if username in self.users and self.users[username].password == password:
            self.current_user = self.users[username]
            print(f"Login berhasil sebagai {self.current_user.role}")
            return True
        else:
            print("Login gagal.")
            return False
    def menu_admin(self):
        while True:
            print("\nMenu Admin:")
            print("1. Tambah Produk Baru")
            print("2. Restock Barang")
            print("3. Mark Barang Rusak/Expired")
            print("4. Logout")
            choice = input("Pilih: ")
            if choice == '1':
                name = input("Nama produk: ")
                sku = input("SKU: ")
                harga = float(input("Harga dasar: "))
                category = 'Etalase Utama'
                myconn.execute(
                    "INSERT INTO produk_reguler (no_SKU, Name_product, Price) VALUES (%s,%s,%s)",
                    (sku, name, harga)
                )
                conn.commit()

                self.inventory.load_produk_from_db()
                print("Produk ditambahkan.")
            elif choice == '2':
                sku = input("SKU produk: ")
                qty = int(input("Jumlah restock: "))
                self.inventory.restock(sku, qty)
            elif choice == '3':
                sku = input("SKU produk: ")
                status = input("Status (Rusak Kemasan/Mendekati Expired): ")
                if sku in self.inventory.produk:
                    self.inventory.produk[sku].mark_defect(status)
                    print("Barang dipindahkan ke Lelang dengan diskon 50%.")
            elif choice == '4':
                self.current_user = None
                break

    def menu_kasir(self):
        transaction = transaction(self.inventory)
        while True:
            print("\nMenu Kasir:")
            print("1. Cari Produk Reguler")
            print("2. Cari Produk Lelang")
            print("3. Tambah ke Keranjang")
            print("4. Checkout")
            print("5. Logout")
            choice = input("Pilih: ")
            if choice == '1':
                query = input("Cari produk: ")
                results = self.inventory.search_produk(query, is_lelang=False)
                for p in results:
                    print(f"{p.sku}: {p.name} - Rp{p.harga} (Stok: {p.stok})")
            elif choice == '2':
                query = input("Cari produk lelang: ")
                results = self.inventory.search_produk(query, is_lelang=True)
                for p in results:
                    print(f"{p.sku}: {p.name} - Rp{p.harga} (Stok: {p.stok})")
            elif choice == '3':
                sku = input("SKU: ")
                qty = int(input("Jumlah: "))
                transaction.add_to_cart(sku, qty)
                print("Ditambahkan ke keranjang.")
            elif choice == '4':
                transaction.checkout()
            elif choice == '5':
                self.current_user = None
                break

    def menu_staff(self):
        # staff bisa restock, mirip admin tapi terbatas
        while True:
            print("\nMenu Staff gudang:")
            print("1. Restock Barang")
            print("2. Logout")
            choice = input("Pilih: ")
            if choice == '1':
                sku = input("SKU produk: ")
                qty = int(input("Jumlah restock: "))
                self.inventory.restock(sku, qty)
            elif choice == '2':
                self.current_user = None
                break

    def run(self):
        while True:
            if not self.current_user:
                if not self.login():
                    continue
            if self.current_user.role == 'admin':
                self.menu_admin()
            elif self.current_user.role == 'kasir':
                self.menu_kasir()
            elif self.current_user.role == 'staff':
                self.menu_staff()
# Jalankan sistem
if __name__ == "__main__":
    system = CashierSystem()
    system.run()
