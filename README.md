# Tietoliikenteen sovellusprojekti

Kurssin "Tietoliikenteen sovellusprojekti" projektirepositori syksyllä 2025.

## Projektin kuvaus (TLDR:mitä tuote tekee)

nRF5340 mittaa kiihtyvyysanturi ja välittää tietoa langattomasti IoT-reitittimelle (Raspberry Pi v2). Raspberry välittää dataa omalle MySQL-palvelimelle.

Tietokantaan tallentuvaan dataan on TCP-sokettirajapinta ja yksinkertainen HTTP API. Kerättyä dataa haetaan HTTP-rajanpinnasta omaan kannettavaan koodatulla Python-ohjelmalla ja käsitellään koneoppimistarkoituksiin.

## Johdanto

Projektin kulku/vaihe/prosessi:

1. Mitataan GY-61 kiihdytysanturin XYZ-suuntadataa nRF5340DK-kehitysalustalla.
2. Data lähetetään BLE-yhteyden kautta IoT-reitittimenä toimivalle Raspberry Pi -alustalle.
3. Raspberry Pi välittää datan TCP-sokettirajapinnan kautta OAMKin MySQL-palvelimelle.
4. Tietokantaan tallennettu data haetaan HTTP-rajapinnan kautta tietokoneelle.
5. Haettu data käsitellään Kmeans-luokittelualgoritmilla.

## Arkkitehtuuri

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

### Projektin arkkitehtuurikaavio:

![Arkkitehtuurikaavio](docs/projektin_arkkitehtuuri_ver1.png)

## Komponentit

### nRF5430DK + GY-61 kiihtyvyysanturi

### Raspberry Pi 3 Model B

- BLE GATT Client -ohjelma.
  - Ohjelma toimii keskuslaitteena (Central) eli se skannaa laitteita, yhdistää Nordic MCU ja tilaa BLE ilmoituksia (notifications).

### Ubuntu serveri

- MySQL-tietokanta
- firewall.bash

### Kannettava tietokone

- Kmeans-algoritmi

## Projektin tekijät

Veikka Kemppainen - [VolatileKoffee](https://github.com/VolatileKoffee)  
Taavetti Konttila - [Tappi868](https://github.com/Tappi868)

### Lisenssi
