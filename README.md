# 🚀 LinkScanner 🚀

### Apreciaria que entren a mi comunidad.
#### ➜ https://discord.gg/programadores (Add me on discord plz -> SerLink04#1345)

![linkscanner](https://media.discordapp.net/attachments/811334964293140501/814578698577379348/lsq_cmd.PNG)

## ⚙️➜ Instalación
```
apt-get install python3
apt-get install python3-pip
pip3 install shodan
pip3 install colorama
git clone https://github.com/SerLink04/LinkScanner
cd LinkScanner
python3 LinkScanner.py
```
## 🪐➜ Opciones
Las opciones dentro de la tool
```
1) Escanear ips
2) Escanear list ip
3) Escanear semirangos
```
## 🌪➜ Funcionamiento
Funcionamiento de las distintas opciones dentro de la tool
```
(1) Con esta opción podrás escanear un montón de ips al mismo tiempo, en un rango totalmente configurable, escribe las ips que quieras escanear seguidas de 
espacios (si pones los datos incorrectamente la script te lo notificará y te impedirá seguir), seguidamente puedes optar por guardar los resultados en un 
txt, el archivo siempre tiene que ser .txt, puedes poner solamente el nombre que quieras darle al archivo (puedes añadir espacios, los cuales serán sustituidos 
por un _) y la propia script te lo guardará en extensión .txt, si añades el .txt al final del nombre no pasará nada, y los resultados se guardaran igualmente 
en un txt (si no pones nada se pondrá como n automáticamente) , a continuación podeis insertar un timeout, que es el tiempo que quereis que la script este 
intentando comprobar por cada puerto si este se encuentra abierto, de tal manera que si pongo 5 seg de timeout , la script intentará verificar si dicho puerto 
con dicha ip esta open durante un máximo tiempo de 5 seg (Esto se debe a que a veces puede tardar 20 seg como 1 seg en verificar si un puerto esta o no open), 
finalmente poneis el rango de puertos a escanear, el cual es totalmente configurable, podeis escanear un solo rango de puertos o varios a la vez (Ejemplo: 25530-25580 
(Escanearia un total de 50 puertos [comprendidos en ese rango]) o 25530-25580.25600-25650 (Escanearia los puertos comprendidos entre 25530-25580 y 25600-25650))
```
```
(2) Primero tienes que poner el nombre del archivo donde generaste las ips, sino lo tienes pulsa enter o pon cualquier nombre al archivo, en el caso de que detecte 
de que no hay ips en dicho archivo, simplemente agrega entre comillas simples las versiones / motds que te gustaría que fueran dichos servidores, y la script buscará 
servidores y obtendrá sus ips para posteriormente poder escanearlas a partir de esos parámetros. En el caso de que si detecta las ips (RECORDAD VERIFICAR QUE EL 
ARCHIVO ES EL CORRECTO) os pedirá a continuación si os gustaría ver las ips que se escanearan, esto os dará el número de ips totales que se escanearan y te mostará 
dichas ips. Luego te preguntará si deseas guardar los resultados en un txt, más adelante te pregunta si te gustaría agregar más ips para escanear (sería hacer que 
haciamos cuando no detectaba ips, si añadis más versiones las ips que encuentre la script se agregarán al txt), luego introduces el timeout y el rango de puertos y 
finalmente nos preguntará si deseamos iniciar el escaneo, escribimos s y pulsamos enter.
```
```
(3) Introduces los semirangos a escanear separados por espacios, indica si quieres que se guarden el escaneo en un txt, inserta un timeout y finalmente introduce el 
rango de puertos a escanear.
```

###### Hecho con ❤️ Necesitas ayuda? contactame por (``SerLink04#1345``) o contactame en Twitter: [@Link04Ser](https://twitter.com/Link04Ser)
