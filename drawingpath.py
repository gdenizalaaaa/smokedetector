import cv2

# -----------------------------
# 1. PATH (BFS sonucundan gelir)
# -----------------------------
room_path = [5, 6, 9, 19, 20, "exit"]

# -----------------------------
# 2. KOORDİNATLAR (MANUEL GİRİLİR)
# ⚠️ Bunları kendi planına göre ayarlamalısın
# -----------------------------
room_coords = {
    5: (520, 380),
    6: (470, 380),
    9: (420, 500),
    19: (520, 620),
    20: (520, 720),
    "exit": (460, 780)
}


# -----------------------------
# 3. PATH ÇİZME FONKSİYONU
# -----------------------------
def draw_path(image_path, output_path, room_path, room_coords):
    img = cv2.imread(image_path)

    if img is None:
        print("Görsel bulunamadı!")
        return

    # çizgi çiz
    for i in range(len(room_path) - 1):
        p1 = room_coords[room_path[i]]
        p2 = room_coords[room_path[i+1]]

        cv2.line(img, p1, p2, (0, 0, 255), 4)  # kırmızı çizgi

    # noktaları çiz
    for room in room_path:
        x, y = room_coords[room]
        cv2.circle(img, (x, y), 6, (255, 0, 0), -1)
        cv2.putText(img, str(room), (x+5, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 0), 1)

    # kaydet
    cv2.imwrite(output_path, img)
    print("Çıktı kaydedildi:", output_path)


# -----------------------------
# 4. ÇALIŞTIR
# -----------------------------
if __name__ == "__main__":
    input_image = "2d_kat_plani.png"     # kendi görselin
    output_image = "output.png"  # çıktı

    draw_path(input_image, output_image, room_path, room_coords)
