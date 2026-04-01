from webui import webui
import json

# Manajemen State Data
state = {
    "total_saldo": 0,
    "riwayat": [],
    "agregasi": {
        "Pemasukan": 0,
        "Pengeluaran": 0
    }
}

def simpan_transaksi(e: webui.event):
    # Tangkap data sebagai satu kesatuan string JSON dari frontend
    payload_str = e.get_string()
    data_transaksi = json.loads(payload_str)

    keterangan = data_transaksi["keterangan"]
    nominal = data_transaksi["nominal"]
    kategori = data_transaksi["kategori"]

    # Komputasi Aritmatika & Agregasi Data Kategori
    if kategori == "Pemasukan":
        state["total_saldo"] += nominal
        state["agregasi"]["Pemasukan"] += nominal
    elif kategori == "Pengeluaran":
        state["total_saldo"] -= nominal
        state["agregasi"]["Pengeluaran"] += nominal

    # Simpan ke riwayat transaksi terbaru
    state["riwayat"].insert(0, {
        "keterangan": keterangan,
        "nominal": nominal,
        "kategori": kategori
    })

    # Integrasi Data Binding (IPC) - Memompa payload JSON kembali ke HTML
    payload_update = json.dumps(state)
    e.window.run(f"updateUI('{payload_update}')")

# Inisialisasi jendela WebUI (gunakan webui.window() huruf kecil)
MyWindow = webui.window()

# Mengikat (Bind) fungsi Python agar bisa dipanggil oleh JavaScript
MyWindow.bind('simpan_transaksi', simpan_transaksi)

# Menampilkan antarmuka HTML
MyWindow.show('index.html')

# Jalankan loop aplikasi agar tetap terbuka
webui.wait()