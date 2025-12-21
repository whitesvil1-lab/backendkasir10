# Sistem Kasir Sederhana seperti Indomaret
# Dibuat berdasarkan deskripsi kebutuhan fungsional (FR-01 hingga FR-06)
# Menggunakan Python OOP untuk simulasi. Data disimpan dalam memory (tidak persistent).

import datetime
import re
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
    def __init__(self, name, sku, harga, category, expired_date, stok = 0):
        self.name = name
        self.sku = sku
        self.harga = harga 
        self.category = category  # 'produk_biasa', 'produk_lelang'
        self.stok = stok
        self.expired_date = expired_date  # datetime.date
        self.status = 'Normal'  # 'Normal', 'Rusak Kemasan', 'Mendekati Expired'

    def is_near_expiry(self):
        today = datetime.date.today()
        selisih = (self.expired_date - today).days
        return selisih <= 10 and selisih >= 0   # kalau sisa ≤ 10 hari
    
    def mark_defect(self, status):
        if Produk.is_near_expiry(self):
            self.mark_defect('Mendekati Expired')
        self.status = status
        if status in ['Rusak Kemasan', 'Mendekati Expired']:
            self.category = 'produk_lelang'
            self.harga *= 0.5  # Auto-discount 50%

# Kelas untuk Inventory (Manajemen Stok)
class Inventory:
    def __init__(self):
        self.produk = {}  # key: SKU (string), value: Produk

    def add_produk(self, produk):
        self.produk[produk.sku] = produk

    def load_produk_from_db(self):
        self.produk = {}

        cursor = conn.cursor()
        cursor.execute(
            "SELECT no_SKU, Name_product, expired_date, Price, stok FROM produk_biasa"
        )

        for sku, name, expired_date, harga, stok in cursor.fetchall():
            sku = str(sku)  # SERAGAMKAN STRING

            p = Produk(
                name=name,
                sku=sku,
                harga=harga,
                category='Etalase Utama',
                expired_date=expired_date,
                stok=stok
            )
            self.produk[sku] = p

    def restock(self, sku, quantity):
        sku = str(sku)

        if sku in self.produk:
            self.produk[sku].stok += quantity

            cursor = conn.cursor()
            cursor.execute(
                "UPDATE produk_biasa SET stok = stok + %s WHERE no_SKU = %s",
                (quantity, sku)
            )
            conn.commit()

            print(f"Stok {self.produk[sku].name} berhasil ditambah.")
        else:
            print("Produk tidak ditemukan.")

    def reduce_stock(self, sku, quantity):
        sku = str(sku)
        if sku in self.produk and self.produk[sku].stok >= quantity:
            self.produk[sku].stok -= quantity
            print(
                f"Stok {self.produk[sku].name} dikurangi {quantity}. "
                f"Sisa: {self.produk[sku].stok}"
            )
        else:
            print("Stok tidak cukup atau produk tidak ditemukan.")

    def search_produk(self, query, is_lelang=False):
        results = []
        for sku, produk in self.produk.items():
            if query.lower() in produk.name.lower() or query == sku:
                if is_lelang and produk.category == 'produk_lelang':
                    results.append(produk)
                elif not is_lelang and produk.category == 'produk_biasa':
                    results.append(produk)
                    return results
    
    def move_to_lelang(self, sku, status):
        sku = str(sku)

        if sku not in self.produk:
            print("Produk tidak ditemukan.")
            return

        produk = self.produk[sku]

        if status not in ['Rusak Kemasan', 'Mendekati Expired']:
            print("Status tidak valid.")
            return

        harga_diskon = produk.harga * 0.5

        cursor = conn.cursor()

        # INSERT ke produk_lelang
        cursor.execute(
            "INSERT INTO produk_lelang (no_SKU, Name_product, expired_date, Price) "
            "VALUES (%s, %s, %s, %s)",
            (sku, produk.name, produk.expired_date, harga_diskon)
        )

        # DELETE dari produk_biasa
        cursor.execute(
            "DELETE FROM produk_biasa WHERE no_SKU = %s",
            (sku,)
        )

        conn.commit()

        # Update memory
        produk.category = 'produk Lelang'
        produk.harga = harga_diskon
        produk.status = status
        del self.produk[sku]

        print("Produk berhasil dipindahkan ke produk_lelang.")
    


# Kelas Utama Sistem
class CashierSystem:
    def __init__(self):
        self.users = {
            'admin': User('admin', 'admin123', 'admin'),
            'kasir': User('kasir', 'kasir123', 'kasir'),
            'staff': User('staff', 'staff123', 'staff')
        }
        self.inventory = Inventory()
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
        self.inventory.load_produk_from_db()

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
                expired_str = input("Tanggal expired (YYYY-MM-DD): ")

                try:
                    expired_date = datetime.datetime.strptime(
                        expired_str, "%Y-%m-%d"
                    ).date()
                except ValueError:
                    print("Format tanggal salah.")
                    continue

                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO produk_biasa (no_SKU, Name_product, Price, expired_date, stok) "
                    "VALUES (%s,%s,%s,%s,%s)",
                    (sku, name, harga, expired_date, 0)
                )
                conn.commit()

                self.inventory.load_produk_from_db()
                print("Produk berhasil disimpan.")

            elif choice == '2':
                sku = input("SKU produk: ")
                qty = int(input("Jumlah restock: "))
                self.inventory.restock(sku, qty)

            elif choice == '3':
                sku = input("SKU produk: ")
                status = input("Status (Rusak Kemasan/Mendekati Expired): ")

                self.inventory.move_to_lelang(sku, status)


            elif choice == '4':
                self.current_user = None
                break

            else:
                print("Pilihan tidak valid.")


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
