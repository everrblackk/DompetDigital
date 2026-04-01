from webui import webui
import json

# Manajemen State Data
state = {"total_saldo": 0, "riwayat": [], "agregasi": {}}
DATA_FILE = "data.json"

KATEGORI_BY_JENIS = {
    "Pemasukan": ["Gaji", "Uang Bulanan", "Bonus", "Lainnya"],
    "Pengeluaran": ["Makanan", "Transportasi", "Tagihan", "Belanja", "Lainnya"],
}


def _state_default():
    return {"total_saldo": 0, "riwayat": [], "agregasi": {}}


def _normalisasi_state(raw_state):
    if not isinstance(raw_state, dict):
        return _state_default()

    total_saldo = raw_state.get("total_saldo", 0)
    riwayat = raw_state.get("riwayat", [])
    agregasi = raw_state.get("agregasi", {})

    if not isinstance(total_saldo, int):
        total_saldo = 0
    if not isinstance(riwayat, list):
        riwayat = []
    if not isinstance(agregasi, dict):
        agregasi = {}

    return {"total_saldo": total_saldo, "riwayat": riwayat[:20], "agregasi": agregasi}


def load_state():
    global state
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            state = _normalisasi_state(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        state = _state_default()


def save_state():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def _validasi_transaksi(data_transaksi):
    keterangan = str(data_transaksi.get("keterangan", "")).strip()
    nominal = data_transaksi.get("nominal", 0)
    jenis = data_transaksi.get("jenis")
    kategori_detail = data_transaksi.get("kategori_detail")

    if not keterangan:
        raise ValueError("Keterangan tidak boleh kosong")

    if not isinstance(nominal, int) or nominal <= 0:
        raise ValueError("Nominal harus berupa angka bulat positif")

    if jenis not in KATEGORI_BY_JENIS:
        raise ValueError("Jenis transaksi tidak valid")

    if kategori_detail not in KATEGORI_BY_JENIS[jenis]:
        raise ValueError("Kategori detail tidak valid untuk jenis transaksi")

    return keterangan, nominal, jenis, kategori_detail


def simpan_transaksi(e: webui.event):
    # Tangkap data sebagai satu kesatuan string JSON dari frontend
    payload_str = e.get_string()
    try:
        data_transaksi = json.loads(payload_str)
    except json.JSONDecodeError:
        e.window.run(f"alert({json.dumps('Format data tidak valid')})")
        return

    try:
        keterangan, nominal, jenis, kategori_detail = _validasi_transaksi(
            data_transaksi
        )
    except ValueError as err:
        e.window.run(f"alert({json.dumps(str(err))})")
        return

    # Komputasi Aritmatika & Agregasi Data Kategori
    if jenis == "Pemasukan":
        state["total_saldo"] += nominal
    elif jenis == "Pengeluaran":
        state["total_saldo"] -= nominal

    agregasi_key = f"{jenis} - {kategori_detail}"
    state["agregasi"][agregasi_key] = state["agregasi"].get(agregasi_key, 0) + nominal

    # Simpan ke riwayat transaksi terbaru
    state["riwayat"].insert(
        0,
        {
            "keterangan": keterangan,
            "nominal": nominal,
            "jenis": jenis,
            "kategori_detail": kategori_detail,
        },
    )

    # Batasi riwayat agar ringan
    state["riwayat"] = state["riwayat"][:20]
    save_state()

    # Integrasi Data Binding (IPC) - Memompa payload JSON kembali ke HTML
    payload_update = json.dumps(state)
    e.window.run(f"updateUI({json.dumps(payload_update)})")


# Inisialisasi jendela WebUI (gunakan webui.window() huruf kecil)
MyWindow = webui.window()

# Muat data lokal saat aplikasi dimulai
load_state()

# Mengikat (Bind) fungsi Python agar bisa dipanggil oleh JavaScript
MyWindow.bind("simpan_transaksi", simpan_transaksi)

# Menampilkan antarmuka HTML
MyWindow.show("index.html")

# Jalankan loop aplikasi agar tetap terbuka
webui.wait()
