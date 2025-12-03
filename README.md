# Tietoliikenteen sovellusprojekti

Oamkin tieto- ja viestintätekniikan 2. vuosikurssin opiskelijoiden "Tietoliikenteen sovellusprojekti" syksyllä 2025.

## Projektin kuvaus

Kehitysalusta nRF5340DK mittaa GY-61-kiihtyvyysanturilla dataa ja välittää datan langattomasti IoT-reitittimelle (Raspberry Pi). Raspberry Pi välittää dataa omalle MySQL-palvelimelle.

Tietokantaan tallentuvaan dataan on TCP-sokettirajapinta ja yksinkertainen HTTP API. Kerättyä dataa haetaan HTTP-rajanpinnasta omaan kannettavaan koodatulla Python-ohjelmalla ja käsitellään koneoppimistarkoituksiin.

## Projektin vaiheet

1. Mitataan GY-61-kiihdytysanturin XYZ-suuntadataa nRF5340DK-kehitysalustalla.
2. Data lähetetään BLE-yhteyden kautta IoT-reitittimenä toimivalle Raspberry Pi -alustalle.
3. Raspberry Pi välittää datan TCP-sokettirajapinnan kautta Oamkin MySQL-palvelimelle.
4. Tietokantaan tallennettu data haetaan HTTP-rajapinnan kautta tietokoneelle.
5. Haettu data käsitellään KMeans-luokittelualgoritmilla.

## Arkkitehtuuri

### Projektin arkkitehtuurikaavio:

![Arkkitehtuurikaavio](docs/projektin_arkkitehtuuri_ver1.png)

### Käytetyt teknologiat

- Alustat

  - Raspberry Pi 3 Model B
  - Nordic nRF5340DK
  - Ubuntu server
  - MySQL

- Kehitysalustat

  - Visual Studio Code
  - nRF Connect
  - GitHub

- Ohjelmointikielet

  - Python
  - C
  - PHP
  - Bash
  - SQL
  - Git

- Protokollat

  - Bluetooth LE
  - HTTP
  - TCP

## Komponentit

### nRF5430DK + GY-61-kiihtyvyysanturi

- ADC-ohjelma
  - kesken
- BLE GATT Server -ohjelma

  - Ohjelman tarkoitus on yhdistää Raspberry Pi -alustaan, mainostaa olemassaoloaan (advertising) ja yhteyden muodostaessaan lähettää mitattua anturidataa ilmoituksien (notifications) kautta.
  - GAP-yhteysrooli on Peripheral.

- KMeans

### Raspberry Pi 3 Model B

- BLE GATT Client -ohjelma
  - Ohjelma skannaa laitteita, yhdistää nRF5340DK-kehitysalustaan ja tilaa (subscribes) BLE ilmoituksia.
  - GAP-yhteysrooli on Central.

### Ubuntu serveri

- MySQL-tietokanta
  - Sisältää tietokantaan lähetettyä GY-61-kiihtyvyysanturin XYZ- ja suuntadataa.
- firewall.bash
  - Suodattaa Oamkin verkon ulkopuolelta tulevaa liikennettä.

### Kannettava tietokone

- KMeans-algoritmi

## Projektin tekijät

Veikka Kemppainen - [VolatileKoffee](https://github.com/VolatileKoffee)  
Taavetti Konttila - [Tappi868](https://github.com/Tappi868)

### Lisenssi

- in progress
