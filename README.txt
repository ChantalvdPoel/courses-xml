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

- database_to_outputfiles
	het hoofdbestand waarvan uit de CSV en de XML bestanden worden gemaakt

- xml_general
	python functies die op meerdere plekken gebruikt kunnen worden

- xml_springest
	python functies die specifiek zijn voor het maken van de Springest XML


###############################################################

Stand van zaken:

Wat moet er nog gebeuren:

- De cursusomschrijvingen in de centrale database zetten
	Hierbij moet nog goed worden gekeken hoe dit wordt gedaan, in plain tekst of html
	Originele idee: omschrijvingen van de website in Word opslaan als html bestand 
	en dit vervolgend door Python in laten lezen en gebruiken voor de CSV en XML bestanden

- Kortingsperiodes verwerken in de database
	Alle externe websites kunnen ook kortingsperiodes verwerken, moet nog worden gekeken of dit nodig is en 
	hoe dit in de centrale database gezet kan worden

- Minimaal aantal deelnemers, maximaal aantal deelnemers en startgarantie
	Dit was nog niet duidelijk hoe dit voor elke cursus ingevuld moet worden
	Niet standaard startgarantie, maar wel als er minimaal 2 deelnemers staan ingeschreven
	Bij 1 deelnemer kan de cursus soms niet doorgaan of op een ander moment




