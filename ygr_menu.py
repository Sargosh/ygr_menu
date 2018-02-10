"""
-->> work in progress <<--
ygr_menu.py - Lädt die Mittagsmenüs von den 'Restaurants' und speicher sie als PDF
Installation von WKHTMLTOPDF ist notwendig! -> https://wkhtmltopdf.org/downloads.html
"""
import datetime
from string import Template
import sys
import csv
import urllib
from urllib.request import urlopen
import pdfkit
from bs4 import BeautifulSoup

CSVLIST = ("")
PATH_WKHTMLTOPDF = ("")
OPTIONS = {}
CONFIG = ("")


def main():
    """ Main Funktion - startet den ganzen Quatsch :)"""
    
    load_settings() # Lade einige Einstellungen
    
    # Lade eine .csv mit Restaurants in eine Liste[ ... , ... , ... , ... ]
    restaurants = read_restaurant(CSVLIST)                    
    
    for restaurant in restaurants:  # Druchläuft die Restaurants in der geladenen CSV-Liste "restaurants"
        for wday in range(1,6): # Durchläuft die Wochentage Montag(1) bis Freitag(5)
            open_days = restaurant[4].replace(";",",")   # Öffnungszeiten
            menuday = get_weekday(wday)
            print(restaurant[0])
            print(menuday)
            print(open_days)
            print(wday)
            if str(wday) in open_days:  # Falls an dem Wochentag geöffnet, dann ...
                pdf_filename = restaurant[0] + " - " + menuday + ".pdf"
                if int(restaurant[3]) == 1:   # 1 = extract aus HTML-Code
                    menu = prepare_menu(restaurant, wday)
                    html_menu = create_html_menu(menu, wday)
                    
                    html_filename = restaurant[0] + " - " + menuday + ".html"
                    pdf_filename = restaurant[0] + " - " + menuday + ".pdf"
                    save_str_as_html(html_menu, html_filename)

                    pdfkit.from_string(html_menu, pdf_filename, options=OPTIONS, configuration=CONFIG)
                
                elif int(restaurant[3]) == 2:   # 2 = Download PDF
                    
                    download_pdf(restaurant[2], pdf_filename)
                elif int(restaurant[3]) == 3:   # 3 = PDF aus HTML
                    save_html_as_pdf(restaurant[3], pdf_filename)

def load_settings():
    
    global CSVLIST
    global PATH_WKHTMLTOPDF
    global OPTIONS
    global CONFIG
    
    # CSV-Liste der Restaurants
    # Restaurant-Name, Homepage-URL, Menu-URL, int - ohne Kopfzeile
    CSVLIST = r'D:\Daten\GitHub\ygr_menu\Restaurants.csv'

    # PDFKIT Configuration
    PATH_WKHTMLTOPDF = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    CONFIG = pdfkit.configuration(wkhtmltopdf=PATH_WKHTMLTOPDF)
    OPTIONS = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
        } 

def get_weekday(day = None):

    week = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

    if day != None:
        return week[int(day) - 1]
    else:
        day = datetime.datetime.now().weekday()
        return week[day]

def prepare_menu(restaurant, wday):
    """ 
    
    """
    if int(restaurant[3]) == 1:   # 1 = extract aus HTML-Code
        if restaurant[0] == "August Wolhusen":
            parsed_html = BeautifulSoup()
            html = load_html(restaurant[2])
            return extract_remimag_menu(html,wday)
        else:
            pass
            #print("{} = {}".format(rest[0], rest[3]))

def check_url(testurl):
    """ Testet ob die URL verfügbar ist """
    try:
        print("Testing " + testurl + " ...")
        return bool((urlopen(testurl).getcode()) == 200)

    except urllib.error.URLError as exeption:
        print(exeption.reason)

def read_restaurant(csv_list):
    """
    Liste ein CSV (UTF-8) mit der Restaurant-Liste
    und gibt den Namen und die URL zurück
    """
    try:
        with open(csv_list, 'r') as csvfile:
            rest = csv.reader(csvfile, delimiter=',')
            r = []
            for row in rest:
                r.append(row)
            return r                
                
    except ValueError:
        print('ERROR ValueError')
        print('Die Datei {} konnte nicht geladen werden'.format(csv_list))

def load_html(url):
    """   Lese und gebe url als htmlstring zurück   """
    html_to_read = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    return urlopen(html_to_read)

def extract_remimag_menu(html, wday):
    """   Suche in einem htmlstring von einem "Remimag AG"-Restaurant nach dem Mittagsmenü   """
    parsed_html = BeautifulSoup(html, 'html.parser')
    #print(html)
    #print(parsed_html)
    new_menu = []
    menu = str()
    s = str()
    line = 0
    new = True
    space = False
    
    # if str(wday) == str(3):
    #     pass
    # elif str(wday) == str(4):
    #     pass
    # elif str(wday) == str(5):
    #     pass
    # else:
    #     print("Geben Sie einen gültigen Wochentag an! (3,4,5)")

    
    
    #menu = 'Das Menü für das Restaurant August in Wolhusen:\n'
    #for n in range(3,6):    # Druchläuft die 3 Mittagsmenüs / Mittwoch "menu-3", Donnerstag "menu-4", Freitag "menu-5"
    
    for p in parsed_html.body.find('div', attrs={'id':'menu-{}'.format(wday)}).findAll('p'):   # Durchläuft alle Menüs (5) des Tages
        menu += p.text

    #print("Menu : " + menu)

    for char in menu: # Ersetzt mehrere Tap (9) und/oder Newline (10) durch einen einzelnen Newline
        if ord(char) == 9 or ord(char) == 10:
            if new == False:
                line += 1   # 
            new = True
        else:
            if new == True and line != 0:
                new_menu.append(str(s).replace("  "," "))
                s = ""
            if space == False or ord(char) != 32: # Prüft, dass nicht 2 Leerzeichen nacheinander kommen
                s += str(char)
            new = False
            if ord(char) == 32:
                space = True
            else:
                space = False
    if new == True and line != 0:
        new_menu.append(str(s).replace("  "," "))
        s = ""
    return new_menu

def create_html_menu(menu, wday):    
    # HTML-Template config
    weekday = get_weekday(wday)
    now_time_format = "%d %b %Y"
    last_update_format = "%d %b %H:%M %Y"
    date = datetime.datetime.now().strftime(now_time_format)
    last_update = datetime.datetime.now().strftime(last_update_format)

    cor_menu = []
    if len(menu) < 15:    #< Es sollten 5 Menüs a 3 Zeilen (=15) sein, falls nicht...
        row_menu = 0
        
        for row in menu:
            if row[0:3] == "CHF": # and row_menu % 3 != 0:  # Falls "CHF" und nicht in der 3. Zeile, dann ...
                while (len(cor_menu) + 1) % 3 != 0:
                    cor_menu.append(" ")
                cor_menu.append(menu[row_menu])
            else: # Falls "CHF" in der 3. Zeile des Menüs steht ist alles i.o.
                cor_menu.append(menu[row_menu])
            row_menu += 1 # Zähler für Reihe +1
    elif len(menu) > 15:
             print("es wurden mehr als 15 Zeilen Menü gefunden")
             sys.exit
    
    if not len(menu) == 15:
        menu = cor_menu 

    print(menu)

    # HTML-Template zusammenfügen
    t = Template("""<!DOCTYPE html>
        <html>
            <head>
                <style>
                    h1 {color:black; text-align:center; font-size:250%;}
                    h2 {color:black; text-align:center; font-size:160%;}
                    h3 {color:black; text-align:center; font-size:150%;}
                    h4 {color:black; text-align:center; font-size:120%;}
                    h5 {color:black; text-align:center; font-size:100%;}
                    p  {color:black; text-align:center; font-size:90%;}
                </style>
            </head>
            <meta http-equiv=Content-Type content="text/html; charset=utf-8">
            <body>
                <h1>Restaurant August, Wolhusen</h1>
                <h2>Mittagsmenüs - $weekday $datum</h2>
                <p>letzte Aktuallisierung: $update</p>
                <br>
                <h3>*** $menu31 ***</h3>
                <h4>$menu32</>
                <h5>$menu33</h5>
                <br>
                <h3>*** $menu41 ***</h3>
                <h4>$menu42</h4>
                <h5>$menu43</h5>
                <br>
                <h3>*** $menu51 ***</h3>
                <h4>$menu52</h4>
                <h5>$menu53</h5>
                <br>
                <h3>*** $menu61 ***</h3>
                <h4>$menu62</h4>
                <h5>$menu63</h5>
                <br>
                <h3>*** $menu71 ***</h3>
                <h4>$menu72</h4>
                <h5>$menu73</h5>
            </body>
        </html>""")
    
    print(len(menu))
    
    
    y=0
    for x in range(0,(len(menu))):
        print( str(y) + " = " + menu[y])
        y += 1
        
    menu = t.substitute(weekday=weekday, datum=date, update=last_update, 
        menu31=menu[0], menu32=menu[1], menu33=menu[2], 
        menu41=menu[3], menu42=menu[4], menu43=menu[5],
        menu51=menu[6], menu52=menu[7], menu53=menu[8],
        menu61=menu[9], menu62=menu[10], menu63=menu[11],
        menu71=menu[12], menu72=menu[13], menu73=menu[14],)

    return menu

def save_str_as_html(htmlstr, htmlfile):
    file = open(htmlfile, 'w')
    file.write(htmlstr)
    file.close()
    print(htmlfile + " - Completed")

def save_html_as_pdf(download_url, pdffile):
    """ speichert eine HTML-Seite 'download_url' als PDF-File 'pdffile' """
    try:
        print("Erstelle PDF von " + download_url + " ...")
        pdfkit.from_url(download_url, pdffile, options=OPTIONS, configuration=CONFIG)
        print(pdffile + " abgeschlossen.")

    except ValueError:
        print('ERROR ValueError')
        print('URL: ' + download_url, 'FileName: ' + pdffile)

def download_pdf(download_url, pdffile):
    """
    Lädt ein PDF von der URL download_url
    und speichert diese mit dem Filename pdffile
    """
    response = urlopen(download_url)
    file = open(pdffile, 'wb')
    file.write(response.read())
    file.close()
    print(pdffile + " - Completed")

if __name__ == "__main__":
    main()
