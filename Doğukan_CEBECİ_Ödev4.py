import sqlite3  # SQLite veritabanı işlemleri için kütüphane
import json  # JSON işlemleri için kütüphane

# SQLite veritabanına bağlantı kuran fonksiyon
def create_connection(db_name):
    try:
        # Veritabanına bağlan ve bir bağlantı nesnesi döndür
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        print("Veritabanına bağlanırken hata:", e)
        return None

# SQLite tablosunu oluşturan fonksiyon
def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Texts (
            id INTEGER PRIMARY KEY,
            text_content TEXT
        )
    """)

# JSON dosyasına metinleri kaydeden fonksiyon
def save_texts_to_json(filename, texts):
    try:
        # JSON dosyasına yazmak için dosyayı aç
        with open(filename, "w") as f:
            # Metinleri JSON formatında kaydet
            json.dump({"texts": texts}, f)
    except Exception as e:
        print("JSON dosyasına yazma hatası:", e)

# Ortak karakter oranını hesaplayan fonksiyon
def common_character_ratio(text1, text2):
    # İki metin arasındaki ortak karakterleri bul
    common_chars = set(text1) & set(text2)
    # Toplam benzersiz karakter sayısını bul
    total_chars = len(set(text1) | set(text2))
    # Ortak karakter oranını hesapla
    if total_chars == 0:
        return 0
    ratio = (len(common_chars) / total_chars) * 100
    return ratio

# Veritabanına metinleri ekleyen fonksiyon
def insert_texts(cursor, texts):
    try:
        # Metinleri veritabanına ekle
        cursor.executemany("INSERT INTO Texts (text_content) VALUES (?)", [(text,) for text in texts])
    except Exception as e:
        print("Veritabanına metin ekleme hatası:", e)

# Raporu dosyaya yazan fonksiyon
def write_report(file_path, report):
    try:
        # Rapor dosyasını yazmak için aç
        with open(file_path, "w") as f:
            # Raporu dosyaya yaz
            f.write(report)
    except Exception as e:
        print("Rapor dosyasına yazma hatası:", e)

# Ana fonksiyon
def main():
    # Kullanıcıdan metin girdisi al
    text1 = input("İlk metni girin: ")
    text2 = input("İkinci metni girin: ")

    # SQLite veritabanına bağlan
    conn = create_connection("texts.db")
    if conn:
        with conn:
            # Cursor oluştur
            cursor = conn.cursor()
            # Tabloyu oluştur
            create_table(cursor)
            # Metinleri veritabanına ekle
            insert_texts(cursor, [text1, text2])
            # Değişiklikleri kaydet
            conn.commit()

    # JSON dosyasına metinleri kaydet
    save_texts_to_json("texts.json", [text1, text2])

    # Benzerlik oranını hesapla
    similarity_ratio = common_character_ratio(text1, text2)

    # Rapor oluştur
    report = f"İlk metin: {text1}\nİkinci metin: {text2}\nBenzerlik oranı: {similarity_ratio:.2f}%\n"

    # Raporu dosyaya yaz
    write_report("benzerlik_durumu.txt", report)

    # Konsolda raporu göster
    print(report)
    print("Benzerlik durumu 'benzerlik_durumu.txt' dosyasına yazıldı.")

# Programı çalıştır
if __name__ == "__main__":
    main()

#Bu kod girilen iki metin arasındaki benzerlik durumunu hesaplar