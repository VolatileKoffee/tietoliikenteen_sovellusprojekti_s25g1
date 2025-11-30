# Tietoliikenteen sovellusprojekti

Kurssin "Tietoliikenteen sovellusprojekti" projektirepositori syksyllä 2025.

## Johdanto

Projektin kulku:
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

- Ohjelmointikielet
  - Python
  - C
  - PHP
  - Bash
  - SQL
  
- Protokollat
  - Bluetooth LE
  - HTTP
  - TCP

### Projektin arkkitehtuurikaavio:

![Arkkitehtuurikaavio](docs/projektin_arkkitehtuuri_ver1.png)

### Projektin tekijät

Veikka Kemppainen - [VolatileKoffee](https://github.com/VolatileKoffee)  
Taavetti Konttila - [Tappi868](https://github.com/Tappi868)

### Lisenssi