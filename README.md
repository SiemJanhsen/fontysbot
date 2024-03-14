**ROS installatie**

__1: ROS2 setup__
Om ROS2 te installeren zal er eerst een operating system op de pc geïnstalleerd moeten zijn op de PC en de operating system dient geschikt te zijn voor de gekozen distributie van ROS2. 
In dit project is er gekozen voor ROS2 Humble en deze versie van ROS2 is gemaakt voor Ubuntu 22.04(Jammy). Deze kan gedownload worden via de onderstaande link:
https://releases.ubuntu.com/jammy/ 

Vervolgens zal het .iso bestand geschreven moeten worden naar een USB stick via een van de vele beschikbare OS-flashers. Balena Etcher is er een van en is te downloaden via onderstaande link:
https://etcher.balena.io/ 

Vervolgens kan Ubuntu geïnstalleerd worden zoals elk anders operating system en als dit gedaan is kan er over worden gegaan naar het installeren van ROS2.
De volgende stappen zijn afgeleid van de officiele ROS2 pagina: https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html  
In de onderstaande uitleg wordt het $ teken gebruikt, dit geeft een regel code weer die ingevuld kan worden in een terminal.  

Stap  1: Locale instellen:
Locale het format waarin de tekst en tijd wordt weergegeven in een operating system. Deze moet juist staan voordat ROS2 geïnstalleerd wordt. Opent de terminal niet? Zie troubleshooting en problemen in bijlage. Geef in de terminal van Ubuntu onderstaande regels code in regel voor regel.
$sudo apt update && sudo apt install locales
$sudo locale-gen en_US en_US.UTF-8
$sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
$export LANG=en_US.UTF-8
Nu zijn alle locale’s instellingen goed ingesteld.

Stap  2: Setup Sources:
Vervolgens moeten  de juiste paden worden gezet zodat ROS2 geïnstalleerd kan worden vanuit github.
$sudo apt install software-properties-common
$sudo add-apt-repository universe
$sudo apt update && sudo apt install curl -y
$sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null  

Stap  3: ROS2 installeren:
Voor dat ROS2 geïnstalleerd kan worden moeten alle packages in Ubuntu up to date zijn. Dit kan gedaan worden met onderstaande regels code:
$sudo apt update
$sudo apt upgrade
Altijd update voor upgrade doen!
ROS2 heeft 2 verschillende versies; één voor desktop met een grafische interface en de andere is voor een niet-grafische. Desktop dient geïnstalleerd te worden indien er een scherm aanwezig is, bijvoorbeeld bij de PC waarop RVIZ draait en het HMI. De niet grafische ‘bare-bones’ versie is in dit geval voor de Raspberry pi. Deze heeft geen scherm aangesloten en draait daarbij ook Ubuntu 22.04 Server edition. Deze versie van Ubuntu kan geen GUI projecteren op een scherm. 
De desktop versie voor de DEV-PC:
$sudo apt install ros-humble-desktop
De Bare-bones versie voor de Raspberry PI:
$sudo apt install ros-humble-ros-base
Voor beide is het verstandig om de dev-tools package te installeren. Deze package bevat de benodigde onderdelen voor het bouwen en debuggen van een ROS2 package:
	$sudo apt install ros-dev-tools

Stap  4: Package aanmaken en github ophalen:
Nu ROS2 volledig is geïnstalleerd kan de workspace aangemaakt worden:
Dit kan doormiddel van: 
$mkdir [naam van workspace]
In dit geval is er dev_ws als naam gebruikt
Vervolgens moet er in deze map een /src map gemaakt worden:
$cd dev_ws 
Hiermee spring je in de map.
	$mkdir src
Nu kan er ook in deze map gesprongen worden:
$cd src
Vervolgens kan de github in deze map gecloned worden:
$sudo apt install git
	$git clone https://github.com/SiemJanhsen/fontysbot.git
Ga vervolgens terug naar de dev_ws map en doe colcon build –symlink-install.
Als alles goed is doorlopen bouwt de package en kan deze ook gebruikt worden.
Als er een package mist zoals wordt er vaak aangegeven welke er mist en hoe deze te installeren is in de error melding.

Extra Tip:
Voordat een package gebruikt kan worden moet er elke keer wanneer een terminal geopent wordt de ROS2 versie en de install folder gesourced worden. Om dit te automatiseren kan dit in de bashrc geplaatst worden. Dit script wordt altijd bij het openen van een terminal uitgevoerd. Aanpassen kan als volgt:
$nano ~/.bashrc
Plaats onder de 4e regel: 
source /opt/ros/humble/setup.bash
cd ~/dev_ws
source install/setup.bash
Om dit op te slaan druk ctrl + s om op te slaan en daarna ctrl + x om het scherm te sluiten.
Eventuele verdere of bijgewerkte uitleg is te vinden in de readme onderaan de fontysbot repository in de Github van Siem Janhsen.

De mappenstructuur binnen de fontysbot  package ziet er als volgt uit:
In de config map staan alle parameter files. Deze zorgen ervoor dat bijvoorbeeld de NAV2 package altijd met dezelfde  parameters wordt opgestart. Aangezien er meer 300 regels aan instellingen beschikbaar is, is dit verwerkt in een .yaml-bestand. Dit geldt ook voor de SLAM parameters. 
In het description mapje staan de URDF’s van de robot zoals deze zijn beschreven in hoofdstuk 3.2.1. 
Het Fontysbot mapje met daarin een lege __init__.py is een vereiste voor het compile van en pythonpackage. Deze package bestaat uit zowel C als Python. Dit is mogelijk doordat in de CMakeLists.txt eerst alle C executables worden aangemaakt en vervolgens de Python executables. Meer hierover is te vinden op de volgende webpagina: https://roboticsbackend.com/ros2-package-for-both-python-and-cpp-nodes/ 



In de launch directory bevinden zich alle launchfiles die met $ros2 launch kunnen worden uitgevoerd. De code van al deze launchfiles zijn niet in de bijlage verwerkt aangezien er vrij gemakkelijk via Github naar de code kan worden gekeken.
Het models en het world mapje zijn voor de simulatie geweest in het begin. Hierin staat de werelden met 3d objecten voor Gazebo beschreven. Indien er geen simulaties meer gebruikt worden zou deze map er tussen uit gehaald kunnen worden.
Als laatst het script mapje: Hierin staat de tfbroadcaster.py script die de transformatie regelt tussen de odometry en de base_footprint van de robot.
 
__2. PI setup: microROS en LiDAR__
Allereerst zal er verbinding gemaakt moeten worden met de PI. Dit kan via SSH of doormiddel van een beeldscherm en een toetsenbord aan te sluiten op de PI. 
Inloggen op pi kan alsvogt:
De PI verbindt automatisch met een netwerk genaamd ROS met als wachtwoord 12345678.
Deze kan gemaakt worden via telefoon of via netwerkrouter. 
Vervolgens kan er verbonden worden via ssh. Dit kan in ubuntu terminal of via windows cmd via: 
$ssh pi@[IP-adres]
Vervolgens wordt er gevraagd om een wachtwoord, dit is ‘pi’.

ROS dient geïnstalleerd te worden via dezelfde manier als op de laptop. Alleen dient niet de desktopversie geïnstalleerd te worden maar de server versie.

Vervolgens kan microros geïnstalleerd worden.
Allereerst voor de zekerheid sourcen:
$source /opt/ros/humble/setup.bash

Workspace aanmaken en hierin gaan
$mkdir microros_ws
$cd microros_ws
Bestanden clonen vanuit de microROS git:
$git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup

Vervolgens moeten de dependencies geüpdatet worden, dit kan met onderstaande commando’s:
$sudo apt update
$rosdep update
$rosdep install --from-paths src --ignore-src -y

Als laatst kan het project gebouwd worden:
$colcon build
$source install/local_setup.bash
Als alles goed is verlopen is MicroROS nu goed geïnstalleerd. 
Vervolgens kan de LiDAR package geïnstalleerd worden. Hiervoor moet er in de /src map van de fontysbot repository en de RPlidar package geïmporteerd worden:
$git clone https://github.com/SiemJanhsen/fontysbot.git
$git clone https://github.com/Slamtec/rplidar_ros.git 
En deze moet gebuild worden vanuit de microros_ws map:
	$cd ~/microros_ws
	$colcon build
Vervolgens dient de package opnieuw gesourced te worden vanuit de workspace map:
$source install/setup.bash
	(dit kan ook weer in de .bashrc van de pi worden geplaatst zodat dit automatisch gebeurd)
Nu alle packages geinstalleerd zijn kan als het goed is het volgende commando uitgevoerd worden:
	$ros2 launch fontysbot raspberry.launch.py
De usb van de LiDAR en van de STM moet ingestoken zijn. Als er geen toegang is tot de USB poort moet het volgende commando worden ingevoerd:
$sudo adduser $USER dialout		Na dit commando opnieuw opstarten!
Als de subscribers en publishers niet worden aangemaakt bij het starten van microROS dan moet de usb er uit worden gehaald en opnieuw erin gestoken worden. Hiervoor zal uiteindelijk een oplossing gezocht moeten worden in een later onderzoek.
Eventuele verdere of bijgewerkte uitleg is te vinden in de readme onderaan de fontysbot repository in de Github van Siem Janhsen.

__3: Simulink setup__
Het overzetten van een Simulink bestand naar een Keil project is een lastige klus. Dit komt doordat hier nog geen goede manier voor gevonden is. De huidig bekende manier is zeer gebruiksonvriendelijk en vereist verbetering. Daarnaast gaat deze manier om de een of andere reden niet altijd goed en vereist soms dat het gehele proces herhaald wordt. 
In Helixcore staat bevindt zich onder de software_tree/SimulinktestprojectsIDE twee mapjes:
Keil Projects en Simulink models.
Het model dat moet worden overgezet naar een simulink model moet hernoemd worden naar ‘Testprogram’ en moet in de ‘Simulink Models’  map gezet worden. 
Vervolgens moet de folder ‘testprogram_ert_rtw’ verwijderd worden
Daarna kan het model gebouwd worden in c code door middel van de embedded coder. 
Deze embedded coder compiled het model en zet de code in de ‘testprogram_ert_rtw’ map. Hieruit moeten alle .c files en .h files over gekopieerd worden naar het keilproject genaamd “Simulink_TestProgram_STM32_standalone.uvprojx in de keilProjets folder. 
Vervolgens kan als alles goed is verlopen dit project gebouwd worden en geflashed worden naar een STM32 bordje. 
Indien gewenst kan dit project worden samengevoegd met een ander Keil project zoals in de onderste afbeelding. 
Nogmaals, dit is geen gebruiksvriendelijke oplossing en om deze reden wordt er aanbevolen om hier een nieuwe manier voor te bedenken.
Het is belangrijk dat alle paden goed staan naar de header files en dat de juiste recentste versies van de MechVenlo toolbox wordt gebruikt.
 

