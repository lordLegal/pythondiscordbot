
import time
jahr_st = 2021
monat_st = 4
Tag_st = 9
sek_st = 50
min_st = 56
stun_st = 13

jahr = jahr_st * 365
jahr = jahr * 86400
print(f"jahr: {jahr}")

if monat_st == 1:
    monat = 31
    monat = monat * 86400
if monat_st == 2:
    monat = 28
    monat = monat * 86400
if monat_st == 3:
    monat = 31
    monat = monat * 86400
if monat_st == 4:
    monat = 30
    monat = monat * 86400
if monat_st == 5:
    monat = 31
    monat = monat * 86400
if monat_st == 6:
    monat = 30
    monat = monat * 86400
if monat_st == 7:
    monat = 31
    monat = monat * 86400
if monat_st == 8:
    monat = 31
    monat = monat * 86400
if monat_st == 9:
    monat = 30
    monat = monat * 86400
if monat_st == 10:
    monat = 31
    monat = monat * 86400
if monat_st == 11:
    monat = 30
    monat = monat * 86400
if monat_st == 12:
    monat = 31
    monat = monat * 86400
print(f"monat: {monat}")

tag = Tag_st * 86400
print(f"tage: {tag}")

sek = sek_st
min = min_st * 60
print(f"min: {min}")

stunde = stun_st * 3600
print(f"H: {stunde}")

date = jahr + monat + tag + sek + min + stunde
print(f"Date in sekunden {date}")

t = int(time.strftime("%Y"))
t = int(time.strftime("%m"))
t = int(time.strftime("%d"))
t = int(time.strftime("%S"))
t = int(time.strftime("%M"))
t = int(time.strftime("%H"))
print(t)
