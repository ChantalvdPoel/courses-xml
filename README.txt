In dit document staat informatie over alle bestanden die hierin staan en over de stand van zaken omtrent het hele project.

Het doel van het project is een centrale database opzetten waarvan uit gemakkelijk CSV of XML bestanden gegenereerd kunnen worden 
met de op dat moment benodigde informatie.

Hierbij gaat het eerst vooral om een aantal XML bestanden voor externe websites: Springest, Edubookers en Studytube.
Deze websites hebben alle drie ook het totale cursusaanbod op de website staan en door via XML bestanden te werken moet het
wijzigen en bijhouden van dit cursusaanbod vereenvoudigd worden.

Daarnaast moet het bijhouden van de eigen website ook makkelijker worden door het gebruik van een centrale database.
Op die manier hoeven wijzigingen alleen in de database doorgevoerd worden waarna het zowel op de eigen als de externe websites zichtbaar wordt.

##########################################################

Mapjes:

- info_external_websites
	bevat de informatie over de externe websites, voorbeelden van XML bestanden en evt XSD bestanden
	hier staat ook beschreven met wie er contact kan worden gezocht mochten er vragen zijn

- output
	in deze map wordt alle output weggeschreven van de scripts
	hier komt dan een CSV voor de eigen website (voor de tabel 'cursusdatums' in de website database),
	en drie XML bestanden voor de externe websites


Overige bestanden:

- Cursussen database
	de centrale database met zowel de cursusinformatie als de planning

- main
	het hoofdbestand waarvan uit de CSV en de XML bestanden worden gemaakt
	voer dit script uit om de bestanden te maken

- functions
	alle functies die gebruikt worden om de bestanden te maken, nodig om main.py uit te kunnen voeren

(- planning_to_db.py 	Dit script is gebruikt om de export vanuit de geo-ict website om te zetten naar de planning in de database
			zodat ik de meest recente versie van de planning in de database had staan. Toen best wat handmatige controles nog
			gedaan, dus is niet compleet geautomatiseerd, maar kan gebruikt worden mocht het nog een keer nodig zijn..)

(- voor geo-ict.nl xml	De data die nodig is voor de geo-ict website, notitie die is gebruikt bij het opzetten van de CSV voor de website
			Er is besloten dat de cursusinformatie in een aparte tabel opgeslagen kan worden in de website database, is niet handig
			dat te verwerken in de cursusdatums tabel)

(- wpgeo_cursusdatums_export_2019-08-28.csv 	De export van de cursudatums tabel van de geoict website die is gebruikt om de op dat moment
						meest recente versie van de planning te krijgen. Met de planning_to_db.py is deze vervolgens
						in de cursussen database gezet.

###############################################################

Stand van zaken

Wat moet er nog gebeuren:

- Op aanvraag	
	Nagaan hoe de websites de cursussen 'op aanvraag' verwerkt willen hebben. Op dit moment hebben die cursussen geen rooster toegevoegd
	en is de node in de xml leeg. Kan goed zijn om nog even na te vragen of ze dit nog op een speciale manier verwerkt willen zien.

- Websites koppeling
	Nakijken op welk onderwerp de XML met hun database wordt gekoppeld. Bij Springest gaat het om het SpringestID en onze eigen ID's. 
	Hiervan moet bij de eerste keer aanleveren via XML een koppeltabel worden aangeleverd, op de website staat hoe die eruit moet
	komen te zien.
	Bij Edubookers wordt het op cursusnaam gekoppeld, hierbij is het belangrijk om na te gaan of de cursusnamen die daar online staan 
	helemaal overeenkomen met de cursusnamen uit de database, anders gaat de koppeling niet goed.
	Bij Studytube is het niet bekend waarop zij koppelen, maar waarschijnlijk is dat ook op cursusnaam.

(geen prio, maar wel erg handig als die ook erin staat)
- De cursusomschrijvingen in de centrale database zetten
	Hierbij moet nog goed worden gekeken hoe dit wordt gedaan, in plain tekst of html
	Originele idee: omschrijvingen van de website in Word opslaan als html bestand 
	en dit vervolgend door Python in laten lezen en gebruiken voor de CSV en XML bestanden


Wat kan nog verbeterd/toegevoegd worden:

- Kortingsperiodes verwerken in de database
	Alle externe websites kunnen ook kortingsperiodes verwerken, moet nog worden gekeken of dit nodig is en 
	hoe dit in de centrale database gezet kan worden

- Minimaal aantal deelnemers, maximaal aantal deelnemers en startgarantie
	Dit was nog niet duidelijk hoe dit voor elke cursus ingevuld moet worden
	Niet standaard startgarantie, maar wel als er minimaal 2 deelnemers staan ingeschreven
	Bij 1 deelnemer kan de cursus soms niet doorgaan of op een ander moment

- Vaste waarden
	Er kan nog eens goed naar gekeken worden naar de vaste waarden die nu hardcoded erin worden gezet
	Misschien dat deze waarden bij een aantal cursussen kunnen afwijken.

- Controles toevoegen
	Er is al wel een begin gemaakt aan een aantal controles inbouwen in het Python script, maar dit kan ook nog verder uitgebouwd worden
	Hierdoor kan je nagaan dat het een betrouwbaar bestand is voordat het wordt geconverteerd naar de XML bestanden.



################################################################

Stappenplan voor het maken van de bestanden:

- Zet de planning in de Cursussen database.xlsx

- Zorg dat de meest recente versie van main.py, functions.py en cursussen database.xlsx lokaal staan opgeslagen

- Verander indien nodig de directories die staan ingesteld bij main.py (database directory en output directory)

- Run main.py - er wordt aangegeven wanneer het script klaar is

- Controleer de bestanden

- Upload het CSV bestand in de eigen website in de PHP omgeving (cursusdatums tabel)

- Neem contact op met de websites over het uploaden van de XML bestanden. Contactgegevens staan in de info_external_websites in de info <website>.txt bestanden

- Geef aan of er eventueel onderwerpen overgeslagen moeten worden waarbij niet zeker is dat die goed in de database verwerkt staan
	Bijvoorbeeld: omschrijving, prijs etc.

- Daarna gaat de website het oploaden en is het hopen op een goed resultaat :)




