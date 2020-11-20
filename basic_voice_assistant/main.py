import speech_recognition as sr
from gtts import gTTS
from selenium import webdriver
import time
import os
import playsound
import subprocess
import datetime
import webbrowser
import random
from pyowm.owm import OWM
import wikipedia
from bs4 import BeautifulSoup as soup
import requests
import winshell
import ctypes
from ecapture import ecapture as ec #Kullanılan modül ve kütüphaneler

i = 0 #giriş sayısını tutan değer
while True: #biz isteyene kadar kapanmaması için oluşturulan sonsuz döngü


    def speak(text): #Google'ın api si sayesinde yazıları seslendiren method
        tts = gTTS(text=text, lang='tr')
        date = datetime.datetime.now()
        file_name = str(date).replace(":", "-") + ".mp3"
        tts.save(file_name)
        playsound.playsound(file_name)
        os.remove(file_name)

    def get_audio(): #mikrofon inputu ile aldığı sesi yazıya çeviren method
        r=sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source,timeout=1,phrase_time_limit=5)
            said = ""

            try:
                said = r.recognize_google(audio,language="tr-TR")

            except Exception as e:

                speak("Anlamadım tekrarlar mısın")
                get_audio()

        return said.lower() #yazıyı küçük harf yapıp gönderiyor


    def get_audio_en(): #uygulama adları için bir de ingilizce anlayan method oluşturduk
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=1, phrase_time_limit=5)
            said = ""

            try:
                said = r.recognize_google(audio, language="en-US")

            except Exception as e:
                speak("Anlamadım tekrarlar mısın")
                get_audio()
        return said.lower()  #yazıyı küçük harf yapıp gönderiyor

    def net_search(text): #google araması yapan fonksiyon
        url = "https://www.google.com.tr/search?q={}".format(text)
        webbrowser.open_new_tab(url)

    def note(text): #not defteri açıp söyleneni kaydeden method
        date = datetime.datetime.now()
        file_name = str(date).replace(":","-") + "-note.txt"
        with open(file_name,"w") as f:
            f.write(text)

        subprocess.Popen(["notepad.exe",file_name])

    def play_music(text): #youtube üzerinden şarkıları açan method
        driver = webdriver.Chrome()
        driver.get("https://www.youtube.com/")
        driver.find_element_by_name("search_query").send_keys(text)
        driver.find_element_by_id("search-icon-legacy").click()
        time.sleep(5)
        driver.find_element_by_id("description-text").click()
        time.sleep(300)
        driver.quit()

    def play_video(text): #play_music ile aynı şekilde youtube üzerinden videoları açan method
        driver = webdriver.Chrome()
        driver.get("https://www.youtube.com/")

        driver.find_element_by_name("search_query").send_keys(text)
        driver.find_element_by_id("search-icon-legacy").click()
        time.sleep(5)

        driver.find_element_by_id("description-text").click()
        time.sleep(500)
        driver.quit()

    def weather(): #hava durumlarını api üzerinden çekip anlık olarak söyleyen method
        owm = OWM('bbe1108552e97a288646c8be7b776acf')
        weather_mngr = owm.weather_manager()
        observation = weather_mngr.weather_at_place('Izmir,TR')
        weather = observation.weather
        temperature = weather.temperature("celsius")
        speak("Sıcaklık " + str(temperature["temp"]) + "derece")
        speak("Hissedilen sıcaklık "+ str(temperature["feels_like"]) + "derece")
        speak("Hava durumu " + str(weather.detailed_status))

    def flip_a_coin(): #yazı tura atan ve sonucu söyleyen method
        speak("Parayı atıyorum")
        flip = random.randint(1,2)
        if flip == 1:
            speak("Yazi")
        else:
            speak("Tura")

    def roll_a_dice(): #zar atıp sonucu söyleyen method
        speak("Zarı atıyorum")
        dice = random.randint(1,6)
        if dice == 1:
            speak("zar 1 geldi")
        elif dice == 2:
            speak("zar 2 geldi")
        elif dice == 3:
            speak("zar 3 geldi")
        elif dice == 4:
            speak("zar 4 geldi")
        elif dice == 5:
            speak("zar 5 geldi")
        else:
            speak("zar 6 geldi")

    def alarm_clock(text): #belli bir dakika sonrasına alarm kuran ve çalan method
        speak("Alarm kuruyorum")
        text.split(" ")
        text_int = int(text[0])
        time.sleep(text_int*60)
        speak("Alarm")
        playsound.playsound("C:\\Users\\brky-\\PycharmProjects\\sesli_asistan\\alarmsound.mp3")

    def international_clock(): # o anki saati söyleyen fonksiyon
        date = datetime.datetime.now()
        date_org = str(date).split(":")
        date_org_2 = str(date_org).split(" ")
        speak("Şu an saat "+ str(date_org_2[1]) +":"+ str(date_org_2[2]))

    def calculate(text): #basit matematik işlemlerini yapan method
        try:
            cal = str(text).split(" ")
            num1 = int(cal[0])
            num2 = int(cal[2])
            if cal[1] == "artı":
                sum = num1 + num2
                speak(cal[0]+cal[1]+cal[2]+" eşittir "+str(sum))
            elif cal[1] == "eksi":
                dec = num1 - num2
                speak(cal[0]+cal[1]+cal[2]+" eşittir "+str(dec))
            elif cal[1] == "x":
                mul = num1 * num2
                speak(cal[0] + cal[1] + cal[2] + " eşittir " + str(mul))
            else:
                speak("Benim matematiğim buna yetmiyor ne yazık ki")
        except:
            speak("İşlemi doğru anladığımdan emin değilim, tekrar söyler misin")
            cal_answ = get_audio()
            calculate(cal_answ)


    def count(text): #verilen sayı kadar saniye sayan method
        try:
            text_sp = text.split("'")
            text_int = int(text_sp[0])
            for i in range(text_int):
                speak(str(i+1))
            speak("Süre doldu")
        except:
            speak("Sayıyı tekrar söyleyebilir misin ?")
            num_answ = get_audio()
            count(num_answ)

    def who_am_i(): #asistanın kendini tanıttığı fonksiyon
        speak("Ben Ciri , Senin asistanınım")

    def wikipedia_def(text): #verilen konu hakkında wikipedia apisi ile ilk paragrafı çeken method
        wikipedia.set_lang("tr")
        speak("Lutfen bekleyiniz.")
        speak(wikipedia.summary(text))
        speak("Daha detaylı bilgi ister misin")
        answ = get_audio()
        if answ == "EVET":
            webbrowser.open_new_tab("https://tr.wikipedia.org/wiki/"+ text)


    def open_app(text): #dosya konumunu vererek girilen kelimeye göre uygun exe yi açan method
        try:
            if text in "spotify":
                file_path = "C:\\Users\\brky-\\AppData\\Roaming\\Spotify\\Spotify.exe"
                subprocess.Popen([file_path])
            elif text == "excel":
                file_path = "C:\\Program Files (x86)\Microsoft Office\\root\\Office16\\EXCEL.EXE"
                subprocess.Popen([file_path])
            elif text == "word":
                file_path = "C:\\Program Files (x86)\Microsoft Office\\root\\Office16\\WINWORD.EXE"
                subprocess.Popen([file_path])
            elif text == "powerpoint":
                file_path = "C:\\Program Files (x86)\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
                subprocess.Popen([file_path])
            elif text == "chrome":
                file_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
                subprocess.Popen([file_path])
            elif text == "onenote":
                file_path = "C:\\Program Files (x86)\Microsoft Office\\root\\Office16\\ONENOTE.EXE"
                subprocess.Popen([file_path])
            elif text == "steam":
                file_path = "C:\\Program Files (x86)\\Steam\\Steam.exe"
                subprocess.Popen([file_path])
            elif text == "telegram":
                file_path = "C:\\Users\\brky-\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe"
                subprocess.Popen([file_path])
            elif text == "whatsapp":
                file_path = "C:\\Users\\brky-\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
                subprocess.Popen([file_path])
            else:
                speak("Bu programı bilgisayarda bulamadım")
        except:
            speak("Bu program ismi tanıdık gelmiyor tekrar dener misin")
            app_answ = get_audio_en()
            open_app(app_answ)


    def are_you_a_robot(): #ufak bir espri
        speak("Robot da olsa insan insandır")

    def why_do_you_exist(): #asistanın neler yapabildiğini anlatığı method
        speak("Ben Berkay beyin küçük işleri için oluşturduğu asistanıyım. Ona pek çok konuda yardımcı oluyorum. Pek çok şey yapabilirim. İnternette gezinme, müzik,video ve uygulama açma, bilgisayarını kontrol etme, hatırlatıcı oluşturma ve alarm kurmak, kronometre oluşturmak gibi şeyler yapabildiğim bazı şeyler.")

    def news(): #google haberler üzerinden başlıkları scrap'leyen ve bunları tek tek çekip okuyan method.
        try:
            news_url = "https://news.google.com/rss?hl=tr&gl=TR&ceid=TR:tr"
            Client = requests.get(news_url)
            xml_page = Client.text
            soup_page = soup(xml_page, "lxml")
            news_list = soup_page.findAll("item")
            for news in news_list[:1]:
                speak(news.title.text)
            speak("Daha fazlasını ister misin")
            answ = get_audio()
            if answ == 'evet':
                webbrowser.open_new_tab("https://news.google.com/topstories?hl=tr&gl=TR&ceid=TR:tr")

        except Exception as e:
            speak("Haberlere ulaşamadım")

    def empty_recycle_bin(): #geri dönüşüm kutusunu temizleyen method
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        speak("Geri dönüşüm kutunu temizledim")

    def where_is(text): #google maps açıp verilen veriyi giren method
        webbrowser.open("https://www.google.com/maps/place/"+ text )

    def take_photo(): #webcam üzerinden fotoğraf çeken ve kaydeden method
        rand = random.randint(1,1000)
        speak("Gülümse çekiyorum")
        (ec.capture(0, "Ciri Camera", str(rand) +"img.jpg"))


    def social_media(text): #sosyal medya sitelerini açan method
        if text == "facebook":
            webbrowser.open("https://www.facebook.com/")
        elif text == "twitter":
            webbrowser.open("https://twitter.com/home")
        elif text == "instagram":
            webbrowser.open("https://www.instagram.com/")
        elif text == "reddit":
            webbrowser.open("https://www.reddit.com/")
        else:
            speak("Sitelere ulaşamıyorum")

    def lock_machine(): #bilgisayarı kilitleyen method
        speak("Bilgisayarı kilitliyorum")
        ctypes.windll.user32.LockWorkStation()

    def log_off(): #oturumu kapatan method
        speak("Oturumu kapatıyorum. Lütfen her şeyi kaydettiğinden emin ol.")
        time.sleep(5)
        subprocess.call(["shutdown", "/l"])

    def exit_ciri():
        speak("Görüşmek üzere") #programı bitiren method.
        exit(0)

    def jokes(): #rastgele şaka seslendiren method
        rand = random.randint(0,4)
        if rand == 0:
            speak("Temel'in eldivenle yazı yazdığını görenler sormuş, Niye eldivenli yazıyorsun zor olmuyor mu, Zorluğuna zor ama el yazımın tanınmasını istemiyorum. ")
        elif rand == 1:
            speak("Temel ve Fadime uzun yıllar nikahsız yaşamaktadır Bir gün Fadime ,Temel bu iş böyle olmuyor, evlenelim artık, demiş. Temel gayet sakin ,Bizi bu yaştan sonra kim alır Fadimem")
        elif rand == 2:
            speak("Temel araba sürerken kırmızı ışıkta geçmiş. Tabii bunu gören polis Temel'i durdurmuş. Polis , Ehliyet ve ruhsat beyefendi! Temel: verdiniz de sanki istiyorsunuz ")
        elif rand == 3:
            speak("Temel trene binmiş, bilet kontrol gelmiş, biletinin İstanbul'a, olduğunu, trenin Ankara'ya gittiğini söylemiş. Temel kendinden emin , peki makinist yanlış yere gittiğini biliyor mu")
        elif rand == 4:
            speak("Doktor Temel'e sormuş, Bacağın nasıl? Hala sekiyorum. Devamlı mı? Yok sadece yürürken.")

    def recommend_movie(): #rastgele film öneren method
        rand = random.randint(1,10)
        if rand == 1:
            speak("Yüzüklerin Efendisi bugün için muhteşem bir seçim")
        elif rand == 2:
            speak("Ucuz romana ne dersin? Ama biraz sert bir film.")
        elif rand == 3:
            speak("Biraz aksiyon için Terminatör'e ne dersin")
        elif rand == 4:
            speak("Belki de Aynı yıldızın altında ile biraz duygulanabiliriz.")
        elif rand == 5:
            speak("Nolan'ın bilimkurguları muhteşemdir. Yıldızlararasına ne dersin?")
        elif rand == 6:
            speak("Suç ve aksiyonun en iyisi Batman Şovalye Yükseliyordur.")
        elif rand == 7:
            speak("Aslan kral ile çocukluğumuza mı dönsek?")
        elif rand == 8:
            speak("Kült arıyorsan Baba serisine bakmalısın")
        elif rand == 9:
            speak("Ben kimim filmi baya baya kafa karıştırıyor.")
        elif rand == 10:
            speak("Kafa dağıtmak için yenilmezler'i izlemeliyiz.")

    def main(i): #tüm işlemleri yöneten main methodu

        hour = int(datetime.datetime.now().hour) #saate göre günaydın ya da iyi akşamlar gibi şekilde açılıyor.
        if i == 0:
            if hour >= 5 and hour < 12:
                speak("Günaydın nasıl yardımcı olabilirim")
            elif hour >= 12 and hour < 18:
                speak("İyi günler nasıl yardımcı olabilirim")
            else:
                speak("İyi akşamlar nasıl yardımcı olabilirim")
        else: #bir işlem yaptıktan sonra farklı bir şekilde sesleniyor
            speak("Başka ne yapabilirim senin için")
        command = get_audio()
        command.upper()
        i = i+1
        if 'ara' in command or 'bak' in command: #google da arama yapmak için aranan komutlar
            speak("Neyi aramamı istersin")
            search_answ = get_audio()  #neyi arayacağınızı burada giriyorsunuz
            speak("Arama sonuçlarını açıyorum")
            net_search(search_answ)

        elif 'not' in command or 'not al' in command or 'hatırlat' in command: #not almak için aranan komutlar
            speak("Not almamı istediğiniz şeyi söyler misin")
            note_answ = get_audio() #neyi kaydedileceği burada giriliyor
            speak("Yazıyorum")
            note(note_answ)

        elif 'müzik' in command : #müzik açmak için aranan komutlar
            speak("Hangi şarkıyı açmamı istersin")
            video_answ = get_audio() #hangi şarkıyı açacağını burada giriyorsunuz
            speak("Açıyorum iyi seyirler")
            play_music(video_answ)

        elif 'video' in command: #video açmak için aranan komutlar
            speak("Hangi videoyu açmamı istersin")
            video_answ = get_audio() #video adını burada giriyoruz
            speak("Açıyorum iyi seyirler")
            play_video(video_answ)

        elif 'hava' in command or 'sıcak' in command : #hava durumu çekip söyleyen kısım için aranan kelimeler
            speak("senin için hava durumunu buluyorum ")
            weather()

        elif 'yazı' in command or 'tura' in command : #yazı tura atılan kısım
            flip_a_coin()

        elif 'zar' in command or 'şans' in command : #zar atmak için kullanılan kısım
            roll_a_dice()

        elif 'alarm' in command: #alarm kurmak için kullanılan kısım
            speak("Kaç dakika sonraya alarm kurmak istersin?")
            alarm_answ = get_audio() #alarmın kaç dakika sonraya kurulacağını söylüyoruz
            alarm_clock(alarm_answ)

        elif 'saat' in command or 'zaman' in command : #anlık olarak saati söyler
            international_clock()

        elif 'hesap' in command or 'matematik' in command: #basit matematik işlemleri için aranan kelimeler
            speak('Hangi işlemi yapmak istersiniz')
            cal_answ = get_audio() #3 artı 3 ya da 5 çarpı 5 şeklinde girişler ile hesap yapar
            calculate(cal_answ)

        elif 'say' in command or 'kronometre' in command: #kronometre için aranan kelimeler
            speak('Kaça kadar sayayım')
            count_answ = get_audio() #kronometrenin süresini giriyoruz
            count(count_answ)

        elif 'sen kim' in command: #ciri kendini tanıtıyor
            who_am_i()

        elif 'wikipedia' in command or 'wiki' in command : #wikipedia da aramak için aranan kelimeler
            speak('neyi araştırmak istersiniz')
            wiki_answ = get_audio() #wiki de araştırılmak istenen kısımı giriyoruz
            wikipedia_def(wiki_answ)

        elif 'aç' in command or 'program' in command or 'uygulama' in command: #uygulama açmak için aranan kısımlar
            speak('hangi programı açmamı istersiniz') #açılmak istenen uygulama giriliyor
            app_answ = get_audio_en()
            open_app(app_answ)

        elif 'robot' in command:
            are_you_a_robot()

        elif 'ne işe' in command or 'ne yap' in command or 'neden var' in command: #cirinin neler yapabildiğini anlatan kısım
            why_do_you_exist()

        elif 'haber' in command or 'gündem' in command: #haberler için aranan kelimeler
            speak('Yeni haberler')
            news()

        elif 'geri dönüşüm' in command or 'boşalt' in command or 'kutu' in command: #geri dönüşüm kutusunu silen kısımda aranan kelimeler
            empty_recycle_bin()

        elif 'nerede' in command or 'bul' in command or 'en yakın' in command: #google mapsi açıp arayan kelimeler
            speak('nereyi arıyorsun')#nereyi aradığını giriyorsun
            location_answ = get_audio()
            where_is(location_answ)

        elif 'foto' in command or 'kamera' in command or 'resim' in command: #fotoğraf çekmek için aranan kesimler
            take_photo() #fotoğraf çeken kısım

        elif 'sosyal' in command or 'medya' in command or 'paylaş' in command: #sosyal medya için aranan kelimeler
            speak('Hangi mecraya gidelim')
            social_answ = get_audio_en() #hangi mecrayı açacağını seçtiğin kısım
            social_media(social_answ)

        elif 'uyku' in command: #uyku moduna geçmek için kullanılan kısım
            lock_machine()

        elif 'kilit' in command or 'oturum' in command: #oturumu kapatmak için seçilen kısım
            log_off()

        elif 'şaka' in command or 'espri' in command: #rastgele şaka yapılan kısım
            jokes()

        elif 'film' in command or 'izle' in command: #film seçmek için kullanılan kısım
            recommend_movie()

        elif 'çık' in command or 'kapa' in command: #programı kapatan kısım
            exit_ciri()

        else :
            speak('Benim bunu yapabilme şansım yok ne yazık ki') #eğer girilen anahtar kelimeler hiçbir şeyle uyuşmuyorsa bu seçenek
            main(i)

    if __name__ == '__main__': #main i başlatan kısım
        main(i)
        i = i+1