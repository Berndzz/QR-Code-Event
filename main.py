import streamlit as st
import qrcode
import json
from PIL import Image
import io


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
    st.title("QR Code Generator for Events")

    programs = [
        "Training SM7",
        "Training PRU SALES ACADEMY",
        "Sertifikat Product & Knowledge",
        "Sales Skill & Product Knowledge",
    ]

    events = [
        "True Talk",
        "True Story",
        "True Gathering",
        "MFC",
        "AML",
        "PRULeads",
        "PRUFliks Series",
        "Ayo Kita Syariah",
        "Training PRUCinta",
        "Training PCB88",
        "Sertifikasi PRUWarisan",
        "Sertifikasi PKKS",
        "Sertifikasi PSS + Pro",
        "Sertifikasi PRUCerah",
        "Unit Link",
        "Basic Financial Planning",
        "Claim Update",
        "Operation Workshop",
        "PRUTop CCB61 & ESCC",
        "Prudential Financial Advisor",
        "PRUSales Builder",
        "Semua Bisa Menjual Syariah",
        "Upsell PRUCinta",
        "Semua Bisa Menjual PCB88",
    ]

    tab_items = [
        "Q1",
        "Q2",
        "Q3",
        "Material",
        "PRU Sales Academy",
        "Sertifikat & Knowledge Academy",
        "Sales Skill & Product",
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
