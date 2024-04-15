import streamlit as st
import qrcode
import json
from PIL import Image
import io
import firebase_admin
from firebase_admin import credentials, db

if not firebase_admin._apps:
    cred = credentials.Certificate("path_firebase/firebase_credentials.json")
    firebase_admin.initialize_app(
        cred, {"databaseURL": "https://trueguide-846cb-default-rtdb.firebaseio.com/"}
    )


def display_data(data):
    num_items = len(data)
    num_columns = min(num_items, 5)  # Atur jumlah kolom maksimum di sini

    # Hitung jumlah baris per kolom
    rows_per_column = num_items // num_columns + (num_items % num_columns > 0)

    for i in range(rows_per_column):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            idx = i + j * rows_per_column
            if idx < num_items:
                key, value = list(data.items())[idx]
                cols[j].write(f"Kategori: {value['category']}")
                cols[j].write(f"Judul Aktivitas: {value['judul_aktivitas']}")
                cols[j].write(f"Deskripsi Aktivitas: {value['deskripsi_aktivitas']}")
                cols[j].write(f"Hari Aktivitas: {value['hari_aktivitas']}")
                cols[j].image(
                    value["gambar_aktivitas"],
                    caption="Gambar Aktivitas",
                    use_column_width=True,
                )
                cols[j].write(f"Body Aktivitas: {value['body_aktivitas']}")
                cols[j].markdown("---")


def get_data(path):
    ref = db.reference(path)
    data = ref.get()
    return data


def add_data(path, new_data):
    ref = db.reference(path)
    ref.push(new_data)


def update_data(path, data_key, updated_data):
    ref = db.reference(path)
    ref.child(data_key).update(updated_data)


def delete_data(path, data_key):
    ref = db.reference(path)
    ref.child(data_key).delete()


def create_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((250, 250))
    return img


def main():
    st.title("Data Kegiatan Mingguan")

    path = [
        "/SM7",
        "/SALES_SKILL",
        "/PRODUCT_&_KNOWLEDGE",
        "/PRU_SALES_ACADEMY",
        "/PERSONAL_EXCELLENT_MENTALITY_ATTITUDE",
    ]

    st.title("List Data:")
    selected_path = st.selectbox("Select path:", path)
    data = get_data(selected_path)
    # st.write(data)

    if data:
        display_data(data)
    else:
        st.write("Data tidak ditemukan.")

    # Form untuk menambahkan data baru
    st.title("Tambah Data")
    body_aktivitas = st.text_input("Body Aktivitas")
    category = st.text_input("Category")
    deskripsi_aktivitas = st.text_input("Deskripsi Aktivitas")
    gambar_aktivitas = st.text_input("Gambar Aktivitas")
    hari_aktivitas = st.text_input("Hari Aktivitas")
    judul_aktivitas = st.text_input("Judul Aktivitas")

    if st.button("Tambah Data"):
        new_data = {
            "body_aktivitas": body_aktivitas,
            "category": category,
            "deskripsi_aktivitas": deskripsi_aktivitas,
            "gambar_aktivitas": gambar_aktivitas,
            "hari_aktivitas": hari_aktivitas,
            "judul_aktivitas": judul_aktivitas,
        }
        add_data(selected_path, new_data)

    # Ambil data dari Firebase
    data = get_data(selected_path)

    # Periksa kembali apakah data kosong setelah menambahkan
    if not data:
        st.write("Data tidak ditemukan.")
        return

    # Form untuk mengubah data yang ada
    st.title("Update Existing Data")
    data_to_update = st.selectbox("Select data to update:", list(data.keys()))

    updated_body_aktivitas = st.text_input(
        "Updated Body Aktivitas", data[data_to_update]["body_aktivitas"]
    )
    updated_category = st.text_input(
        "Updated Category", data[data_to_update]["category"]
    )
    updated_deskripsi_aktivitas = st.text_input(
        "Updated Deskripsi Aktivitas", data[data_to_update]["deskripsi_aktivitas"]
    )
    updated_gambar_aktivitas = st.text_input(
        "Updated Gambar Aktivitas", data[data_to_update]["gambar_aktivitas"]
    )
    updated_hari_aktivitas = st.text_input(
        "Updated Hari Aktivitas", data[data_to_update]["hari_aktivitas"]
    )
    updated_judul_aktivitas = st.text_input(
        "Updated Judul Aktivitas", data[data_to_update]["judul_aktivitas"]
    )

    if st.button("Update"):
        updated_data = {
            "body_aktivitas": updated_body_aktivitas,
            "category": updated_category,
            "deskripsi_aktivitas": updated_deskripsi_aktivitas,
            "gambar_aktivitas": updated_gambar_aktivitas,
            "hari_aktivitas": updated_hari_aktivitas,
            "judul_aktivitas": updated_judul_aktivitas,
        }
        update_data(selected_path, data_to_update, updated_data)

    st.title("Hapus Data")
    data_to_delete = st.selectbox(
        "Pilih judul aktivitas untuk dihapus:",
        [value["judul_aktivitas"] for value in data.values()],
    )

    if st.button("Hapus"):
        key_to_delete = None
        for key, value in data.items():
            if value["judul_aktivitas"] == data_to_delete:
                key_to_delete = key
                break
        if key_to_delete:
            delete_data(selected_path, key_to_delete)
        else:
            st.error("Judul aktivitas tidak ditemukan.")

    st.title("QR Code Generator for Events TRUE AGENCY SM7")

    programs = [
        "Training SM7",
        "Training PRU SALES ACADEMY",
        "Training Product & Knowledge",
        "Personal Excellent Mentallity & Attitude",
        "Sales Skill",
    ]

    events = [
        "True Talk",
        "True Story",
        "True Gathering",
        "True Skill",
        "True WorkShop",
        "Pengenalan Sejarah Asuransi (Syariah), Tokoh dan Istilah didalam Asuransi Jiwa",
        "Peta Produk As. Tradisional & Kegunaan di Masyarakat",
        "Pru Cinta & Role Play Presentasi & Membuat + Menerangkan ilustrasi",
        "Pru Anugerah & Role Play Presentasi & Membuat + Menerangkan ilustrasi",
        "PCB 88 & Role Play Presentasi & Membuat + Menerangkan ilustrasi",
        "PKKS & Role Play Presentasi & Membuat + Menerangkan ilustrasi",
        "PSS Plus Pro & Role Play Presentasi & Membuat + Menerangkan ilustrasi",
        "Perbandingan antar Produk Asuransi, Kapan Menjual itu semua >> Role Play",
        "Mengisi SPAJ, CEKATAN & Pru PayLink >> Role Play",
        "Mengoperasikan Pru Force (Lisensi, Training, Income, %, Lapse) + PULSE",
        "Peraturan - peraturan KLAIM, Kode Etik (TTD, KTP, Edit Document, PEC)",
        "Hukum Dasar Penjualan As., Pola Ring 123, & Tehnik Canvassing",
        "Dream Book, Janji Temu, Daily Activity",
        "Membangun Hubungan, Perkenalan",
        "Fact Finding (Market Survey) & Tehnik Up Selling",
        "Tehnik Bertanya & Memberikan Solusi + Ide (Identifikasi Need)",
        "Presentasi Keranjang Batu (+ Role Play)",
        "Presentasi 28000 (+ Role Play)",
        "Presentasi Pak Hikmad (+ Role Play)",
        "Urutan Acara Prospek Lengkap (+ Role Play)",
        "Membaca Kebutuhan, Kemampuan & Kemauan Beli & Solusi",
        "Tehnik Handling Objection & Role Play",
        "SALES CLINIC & Perlengkapan Perang & Sales Tools",
        "Presentasi Bisnis (NBO), HO NBO, Hitung Komisi - OR",
        "Mentalitas Sales Asuransi Jiwa (Misi & Visi Asuransi, Aktifitas Rutin)",
        "Kemampuan Inisiasi (Menggerakkan Agen & Team)",
        "Pemantauan Target Mingguan - Tahunan, Pemantauan Aktifitas, Strategy",
        "Penampilan (Grooming), Buah Tangan / Hadiah, Pru Flyer (Referensi)",
        "Mengantar Polis, Etika dalam mengurus KLAIM, Servicing Klien Lama (Hadiah ultah, HWA)",
        "Kedisplinan, Komitmen, Mindset, Etika, Attitude",
        "Management Keuangan Agen & Leader, Investasi Seminar / Skill Upgrade dll",
        "3 Misi Mulia, 7 Penghambat, Visi dan Misi Agen Asuransi, 7 Pilar Kepercayaan",
    ]

    tab_items = [
        "Q1",
        "Q2",
        "Q3",
        "Mentality & Attitude",
        "PRU Sales Academy",
        "Product & Knowledge Academy",
        "Sales Skill",
    ]

    with st.form("event_form", clear_on_submit=True):
        selected_event = st.selectbox("Pilih Acara", events)
        selected_program = st.selectbox("Pilih Program", programs)
        selected_tab_item = st.selectbox("Pilih Tab Item", tab_items)
        tanggal_acara = st.date_input("Tanggal Acara")
        jam_mulai = st.time_input("Jam Mulai")
        jam_selesai = st.time_input("Jam Selesai")
        lokasi = st.text_input("Lokasi")
        submit_button = st.form_submit_button("Generate QR Code")

    if submit_button:
        event_data = {
            "namaAcara": selected_event,
            "program": selected_program,
            "tabName": selected_tab_item,
            "tanggalAcara": str(tanggal_acara),
            "jamMulai": str(jam_mulai),
            "jamSelesai": str(jam_selesai),
            "lokasi": lokasi,
            "kehadiran": "",
        }
        json_data = json.dumps(event_data)
        qr_code_img = create_qr_code(json_data)

        # Konversi PIL Image ke BytesIO
        buf = io.BytesIO()
        qr_code_img.save(buf, format="PNG")
        buf.seek(0)

        # Menampilkan QR code di UI
        st.image(buf, caption="QR Code for Event", use_column_width=True)

        # Opsi untuk mengunduh QR code sebagai gambar
        buf.seek(0)  # Reset buffer position
        st.download_button(
            label="Download QR Code",
            data=buf,
            file_name="event_qr_code.png",
            mime="image/png",
        )


if __name__ == "__main__":
    main()
