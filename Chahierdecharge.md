On doit faire un outil de nettoyage du fichier ./Data/ENEDIS.input.csv. Ce fichier est extraction du distrubuteur energetique de ma maison.  Les donnée sont presenter avec chaque ligne une heure de consomation. les donnée commence en 2023 et finisse en 2024. Mon objectif est verifier chaque jour de 2023 et 2024 si les donnée sont complete. Si il manque des donnée sur une heure on prend un les donnée de l'heure de l'année 2024 ou 2023 ou meêm 2025. Il faut que trouve la meilleur facon de traiter. le resultat finale est d'avoir un fichier 2023.csv et fichier 2024.csv. Avec deux colone 

Ayttention le fichier ENEDIS.input.csv contient x colone. Il nous faut la colone Horodate et la colone Valeur.

Les test et le programme dois prendre en compte que le fichier peut avoir plusier colones. Mais, il nous faut Horadate et la colone Valeur.

Il faut généer un fichier xlsx. pour cahque année avec ce format.

'
"Note:
 1. Do not delete this note or change the format, date & time column, or time interval in the template. Enter the load power for each time segment in each date. Do not leave any cell empty.
 2. The template contains all data from 0:00 on January 1 to the end of the year (365 days).
 3. Enter the unit of the load power (kW or W) in cell B3.
 4. Column A refers to ""Month/Day Hour:Minute"".
 5. Enter the load power at 0:00 on January 1 in cell B5, the load power at 1:00 on January 1 in cell B6, and so on.
 6. Each value must be greater than or equal to 0. If you set the unit to kW, you can enter a maximum of six decimal places for each value. If you set the unit to W, you can enter a maximum of two decimal places for each value."	"
"	"
"	"
"	"
"	"
"	"
"	"
"	"
"
Time Interval	60							
Unit	kW							
Month/Day Hour:Minute	Load Power							
1/1 0:00								
1/1 1:00								
1/1 2:00								
1/1 3:00								
1/1 4:00								
1/1 5:00								
1/1 6:00								
1/1 7:00								
1/1 8:00								
1/1 9:00								
1/1 10:00								
'

Coder en python.
