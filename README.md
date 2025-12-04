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

<!-- ![Arkkitehtuurikaavio](docs/projektin_arkkitehtuuri_ver1.png) -->
<img src="https://github.com/VolatileKoffee/tietoliikenteen_sovellusprojekti_s25g1/blob/READMEupdate/docs/projektin_arkkitehtuuri_ver1.png" alt="Projektin arkkitehtuurikaavio" style="width:auto; height:auto;">

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

| Protokollat  | Kuvaus                                          |
| ------------ | ----------------------------------------------- |
| Bluetooth LE | Käytetään nRF5340DK:n ja Raspberry Pi:n välillä |
| HTTP         | desc                                            |
| TCP          | desc                                            |

## Komponentit

### nRF5430DK + GY-61-kiihtyvyysanturi

- adc.c -ohjelma

  - Alustaa ADC-kanavat, mittaa kiihtyvyysanturin jännitearvoja ja tallentaa ne tietueeseen (struct) lähettämistä varten.

- BLE GATT Server -ohjelma

  - Ohjelman tarkoitus on yhdistää Raspberry Pi -alustaan, mainostaa olemassaoloaan (advertising) ja yhteyden muodostaessaan lähettää mitattua anturidataa ilmoituksien (notifications) kautta.
  - GAP-yhteysrooli on Peripheral.

KUVA: nRF5340DK ja GY-61-kiihtyvyysanturi. Kuvassa alusta ja sensori ovat valmiita mittaukseen:

<!-- ![nRF5340DK ja GY-61-kiihtyvyysanturi](docs/nrf5340dk_and_sensor.jpg) -->
<img src="https://github.com/VolatileKoffee/tietoliikenteen_sovellusprojekti_s25g1/blob/READMEupdate/docs/nrf5340dk_and_sensor.jpg" alt="nRF5340DK ja GY-61-kiihtyvyysanturi" style="width:75%; height:auto;">

KUVA: GY-61-kiihtyvyysanturi ja XYZ-akselit. Arvot akselinimien vieressä ovat sensorisuuntia:

<!-- ![GY-61-kiihtyvyysanturi ja XYZ-akselit](docs/3axis_with_orientations_ver1.png) -->
<img src="https://github.com/VolatileKoffee/tietoliikenteen_sovellusprojekti_s25g1/blob/READMEupdate/docs/3axis_with_orientations_ver1.png" alt="GY-61-kiihtyvyysanturi ja XYZ-akselit" style="width:75%; height:auto;">

### Raspberry Pi 3 Model B

- BLE GATT Client -ohjelma
  - Ohjelma skannaa laitteita, yhdistää nRF5340DK-kehitysalustaan ja tilaa (subscribes) BLE ilmoituksia.
  - GAP-yhteysrooli on Central.

### Ubuntu serveri

- MySQL-tietokanta
  - Sisältää tietokantaan lähetettyä GY-61-kiihtyvyysanturin XYZ-dataa ja suunta-arvot.
- firewall.bash
  - Suodattaa Oamkin verkon ulkopuolelta tulevaa liikennettä.

### Kannettava tietokone

- tcp_datafetcher -ohjelma

  - Hakee TCP-protokollan avulla mittausdataa MySQL-tietokannasta ja tallentaa sen measurementdata.csv tiedostoksi.

- kmeans_algorithm -ohjelma

  - Lukee measurementdata.csv tiedoston ja piirtää XYZ-datapisteet 3D-taulukkoon. Tämän jälkeen ohjelma asettaa keskipisteille (centroids) omat datajoukot (clusters) ja laskee jokaiselle keskipisteelle etäisyyden datajoukon pisteisiin. Keskipiste "voittaa" lyhyimmällä etäisyydellä olevan datapisteen itselleen. Etäisyyslaskun ja "voitettujen" datapisteiden perusteella keskipiste saa omat XYZ-koordinaatit.
  - Kuuden keskipisteen XYZ-koordinaatit tallennetaan centroid_coords -taulukkoon centroid_data.h-tiedoston sisälle.

- confusion_matrix -ohjelma

  - Ohjelma käyttää kmeans_algorithm -ohjelman tuottamaa centroid_data.h-tiedostoa ja nRF5340DK-kehitysalustalla mitattuja XYZ-arvoja. Tuloksena syntyy 6x6 kokoinen "confusion matriisi", jonka avulla kmeans_algorithm -ohjelman luokittelukykyä voidaan arvioida.

<!-- ![measurement](docs/confusion_matrix_program_output.png) -->
<img src="https://github.com/VolatileKoffee/tietoliikenteen_sovellusprojekti_s25g1/blob/READMEupdate/docs/confusion_matrix_program_output.png" alt="Confusion Matrix ohjelman tulostus" style="width:50%; height:auto;">

## Projektin tekijät

Veikka Kemppainen - [VolatileKoffee](https://github.com/VolatileKoffee)  
Taavetti Konttila - [Tappi868](https://github.com/Tappi868)

### Lisenssi

- in progress
