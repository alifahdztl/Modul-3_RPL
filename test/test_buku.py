from unittest.mock import MagicMock
from models.buku_model import BukuModel

def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Melakukan eksekusi fungsi
    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)

    # Memverifikasi apakah fungsi mengembalikan nilai True
    assert hasil is True

    # Memverifikasi apakah cursor.execute benar-benar dipanggil
    mock_cursor.execute.assert_called_once()

    # Memverifikasi apakah perintah commit (simpan) dipanggil
    model.conn.commit.assert_called_once()

def test_get_all_buku():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Simulasi hasil kembalian data dari database (fetchall)
    mock_cursor.fetchall.return_value = [
        (1, "Laut Bercerita", "Leila S. Chudori", 2017),
        (2, "Bumi Manusia", "Pramoedya Ananta Toer", 1980)
    ]

    # Melakukan eksekusi fungsi
    hasil = model.get_all_buku()

    # Memverifikasi apakah hasil kembalian berupa list data
    assert isinstance(hasil, list)
    assert len(hasil) == 2

    # Memverifikasi apakah cursor.execute benar-benar dipanggil
    mock_cursor.execute.assert_called_once()