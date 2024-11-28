import cv2

# Haar Cascade modellerini yükle
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Video akışı başlat
cap = cv2.VideoCapture(0)  # Kamera ID'si (0 varsayılan kamerayı açar)

def is_glasses_present(roi_gray):
    """
    Gözlük tespiti için göz bölgesindeki kenarları ve pikselleri analiz eder.
    """
    edges = cv2.Canny(roi_gray, 50, 150)  # Kenar tespiti
    # Kenar piksel sayısını analiz et
    edge_density = (edges > 0).sum() / edges.size
    return edge_density > 0.13  # Belirli bir kenar yoğunluğunu aşarsa gözlük var diyelim

while True:
    ret, frame = cap.read()  # Video akışından bir kare oku
    if not ret:
        print("Kamera akışı okunamadı!")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Grayscale dönüştürme
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)  # Yüzleri tespit et

    for (x, y, w, h) in faces:
        # Yüz bölgesini çerçeve içine al
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Gözleri tespit et
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:  # En az iki göz tespit edilmişse
            glasses_detected = False
            for (ex, ey, ew, eh) in eyes:
                eye_region_gray = roi_gray[ey:ey + eh, ex:ex + ew]
                if is_glasses_present(eye_region_gray):
                    glasses_detected = True
                    break  # Bir gözlük bulunduğunda kontrolü bırak

            if glasses_detected:
                cv2.putText(frame, "Gozluk Var", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Gozluk Yok", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        else:
            # Göz tespit edilemezse
            cv2.putText(frame, "Gozluk Yok", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Çıktıyı göster
    cv2.imshow("Video Akisi - Gozluk Tespiti", frame)

    # Çıkış için 'q' tuşuna bas
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak ve pencereleri kapat
cap.release()
cv2.destroyAllWindows()
