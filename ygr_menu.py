"""
mittags_menu.py - Lädt die Mittagsmenüs von den 'Ygnis-Restaurants' und speicher sie als PDF

Installation von WKHTMLTOPDF ist notwendig! -> https://wkhtmltopdf.org/downloads.html
"""

import urllib
from urllib.request import urlopen
import csv
import pdfkit
from bs4 import BeautifulSoup
import datetime
from string import Template

# CSV-Liste der Restaurants
# Restaurant-Name, Homepage-URL, Menu-URL, int - ohne Kopfzeile
CSVLIST = r'C:\Users\baschwanden\Desktop\Scripts\YGR-Rest\Restaurants.csv'

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

def main():
    """ Main Funktion - startet den ganzen Quatsch :)"""
    rest_list = read_restaurant(CSVLIST)
    menu = prepare_restlist(rest_list, 3)
    
    #html_file = "August Wolhusen - " + weekday + ".html"
    #save_str_as_html(m, html_file)
    #pdfkit.from_string(m, rest[0] + " - " + weekday + ".pdf", options=OPTIONS, configuration=CONFIG)
    

def prepare_restlist(rest_list, wday):
    """ Wählt anhand des "Verarbeitungs-Codes" (rest[4]) die Methode zum erstellen des PDF fest.
        1 = extract aus HTML-Code / 2 = PDF-Download / 3 = HTML print as PDF """
    for rest in rest_list:
        if int(rest[3]) == 1:
           
            if rest[0] == "August Wolhusen":
                parsed_html = BeautifulSoup()
                weekday = str()
                
                html = load_html(rest[2])
                print(wday)
                    
                if str(wday) == str(3):
                    weekday = "Mittwoch"
                elif str(wday) == str(4):
                    weekday = "Donnerstag"
                elif str(wday) == str(5):
                    weekday = "Freitag"
                                        
                return extract_august_menu(html,wday)
                   
                    
                
            else:
                pass
                #print("{} = {}".format(rest[0], rest[3]))
        
        elif int(rest[3]) == 2:
            pass
            #print("{} = {}".format(rest[0], rest[3]))
        
        elif int(rest[3]) == 3:
            pass
            #print("{} = {}".format(rest[0], rest[3]))
        
        else:
            pass
            #print("Es wurde kein 'Verarbeitungs-Code' gefunden. (1,2,3)")

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

def extract_august_menu(html, wday):
    """   Suche in einem htmlstring nach dem Mittagsmenü   """
    parsed_html = BeautifulSoup(html, 'html.parser')
    print(html)
    print(parsed_html)
    new_menu = []
    menu = str()
    s = str()
    line = 0
    new = True
    space = False
    
    if str(wday) == str(3):
        pass
    elif str(wday) == str(4):
        pass
    elif str(wday) == str(5):
        pass
    else:
        print("Geben Sie einen gültigen Wochentag an! (3,4,5)")

    
    
    #menu = 'Das Menü für das Restaurant August in Wolhusen:\n'
    #for n in range(3,6):    # Druchläuft die 3 Mittagsmenüs / Mittwoch "menu-3", Donnerstag "menu-4", Freitag "menu-5"
    for p in parsed_html.body.find('div', attrs={'id':'menu-{}'.format(wday)}).findAll('p'):   # Durchläuft alle Menüs (5) des Tages
        menu += p.text

    print("Menu : " + menu)

    for char in menu: # Ersetzt mehrere Tap (9) und/oder Newline (10) durch einen einzelnen Newline
        if ord(char) == 9 or ord(char) == 10:
            if new == False:
                line += 1
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
    print(new_menu)

    # HTML-Template config
    now_time_format = "%A %b %d %Y"
    last_update_format = "%a %b %d %H:%M %Y"
    date = datetime.datetime.now().strftime(now_time_format)
    last_update = datetime.datetime.now().strftime(last_update_format)

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
                <h2>Mittagsmenüs - $datum</h2>
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
    y=0
    for x in new_menu:
        print( str(y) + " = " + new_menu[y])
        y += 1
    menu_mittwoch = t.substitute(datum=date, update=last_update, 
        menu31=new_menu[0], menu32=new_menu[1], menu33=new_menu[2], 
        menu41=new_menu[3], menu42=new_menu[4], menu43=new_menu[5],
        menu51=new_menu[6], menu52=new_menu[7], menu53=new_menu[8],
        menu61=new_menu[9], menu62=new_menu[10], menu63=new_menu[11],
        menu71=new_menu[12], menu72=new_menu[13], menu73=new_menu[14],)

    return menu_mittwoch

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


