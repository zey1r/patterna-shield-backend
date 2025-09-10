"""
Patterna Shield Mini - Test Örnekleri
====================================

Bu dosya API'yi test etmek için örnek istekler içerir.
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_message_analysis():
    """Mesaj analizi testi"""
    print("🔍 Mesaj Analizi Testi")
    print("-" * 50)
    
    test_messages = [
        {
            "message": "Merhaba, nasılsın?",
            "sender_phone": "05551234567",
            "expected": "Güvenli"
        },
        {
            "message": "ACİL! Hesabınız bloke oldu. Şifrenizi girmek için tıklayın: http://sahte-site.com",
            "sender_phone": "08501234567",
            "expected": "Dolandırıcılık"
        },
        {
            "message": "Tebrikler! 10.000 TL kazandınız. Hemen bu linke tıklayın!",
            "sender_phone": "05559876543",
            "expected": "Dolandırıcılık"
        }
    ]
    
    for i, test in enumerate(test_messages, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/analyze/message",
                json={
                    "message": test["message"],
                    "sender_phone": test["sender_phone"]
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                status = "🔴 FRAUD" if result["is_fraud"] else "🟢 SAFE"
                
                print(f"\nTest {i}: {test['expected']}")
                print(f"Mesaj: {test['message'][:50]}...")
                print(f"Sonuç: {status} (Risk: {result['risk_score']}%)")
                print(f"Nedenler: {', '.join(result['reasons'][:2])}")
            else:
                print(f"❌ Test {i} başarısız: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Test {i} hatası: {e}")

def test_phone_analysis():
    """Telefon analizi testi"""
    print("\n📞 Telefon Analizi Testi")
    print("-" * 50)
    
    test_phones = [
        {"phone": "05551234567", "expected": "Normal"},
        {"phone": "08501234567", "expected": "Şüpheli"},
        {"phone": "invalid_phone", "expected": "Geçersiz"},
        {"phone": "+905551234567", "expected": "Normal"}
    ]
    
    for i, test in enumerate(test_phones, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/analyze/phone",
                json={"phone_number": test["phone"]}
            )
            
            if response.status_code == 200:
                result = response.json()
                status = "🔴 RISK" if result["is_fraud"] else "🟢 SAFE"
                
                print(f"\nTest {i}: {test['expected']}")
                print(f"Telefon: {test['phone']}")
                print(f"Sonuç: {status} (Risk: {result['risk_score']}%)")
                print(f"Nedenler: {', '.join(result['reasons'])}")
            else:
                print(f"❌ Test {i} başarısız: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Test {i} hatası: {e}")

def test_url_analysis():
    """URL analizi testi"""
    print("\n🔗 URL Analizi Testi")
    print("-" * 50)
    
    test_urls = [
        {"url": "https://www.google.com", "expected": "Güvenli"},
        {"url": "http://192.168.1.1/phishing", "expected": "Şüpheli"},
        {"url": "https://bit.ly/suspicious", "expected": "Şüpheli"},
        {"url": "https://bankam.com/login", "expected": "Şüpheli"}
    ]
    
    for i, test in enumerate(test_urls, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/analyze/url",
                json={"url": test["url"]}
            )
            
            if response.status_code == 200:
                result = response.json()
                status = "🔴 RISK" if result["is_fraud"] else "🟢 SAFE"
                
                print(f"\nTest {i}: {test['expected']}")
                print(f"URL: {test['url']}")
                print(f"Sonuç: {status} (Risk: {result['risk_score']}%)")
                print(f"Nedenler: {', '.join(result['reasons'])}")
            else:
                print(f"❌ Test {i} başarısız: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Test {i} hatası: {e}")

def test_health_check():
    """Sistem sağlık kontrolü"""
    print("\n💚 Sistem Sağlık Kontrolü")
    print("-" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Sistem Durumu: {result['status']}")
            print(f"🕐 Zaman: {result['timestamp']}")
            print(f"📦 Versiyon: {result['version']}")
        else:
            print(f"❌ Sağlık kontrolü başarısız: {response.status_code}")
    except Exception as e:
        print(f"❌ Sağlık kontrolü hatası: {e}")

if __name__ == "__main__":
    print("🛡️ Patterna Shield Mini - Test Suite")
    print("=" * 50)
    
    # API'nin çalıştığını kontrol et
    try:
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print("❌ API çalışmıyor! Önce 'python main.py' ile başlatın.")
            exit(1)
    except:
        print("❌ API'ye bağlanılamıyor! Önce 'python main.py' ile başlatın.")
        exit(1)
    
    print("✅ API çalışıyor, testler başlatılıyor...\n")
    
    # Testleri çalıştır
    test_health_check()
    test_message_analysis()
    test_phone_analysis()
    test_url_analysis()
    
    print("\n🎉 Tüm testler tamamlandı!")
    print("\n💡 Swagger UI için: http://localhost:8000/docs")
