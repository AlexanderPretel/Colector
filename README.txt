Esta es una aplicación basada en la API "PyQGIS" que corre en las versiones de QGIS superiores a 3.0 como un complemento adicional. La función principal es la recolección de información espacial y alfanumérica con ayuda de un receptor GNSS monofrecuencia de la marca u-blox (ublox M8T) y de la clase QgsGpsConnection, así comoo la recolección de los datos de observación y navegación GNSS que el receptor está generando a partir de su operación.

Contenido
Información general

Instalación

Librerías y programas requeridos
PyQGIS
RTKLIB
Descarga
Desde el Advanced Packaging Tool (recomendado)
Desde la página oficial
Preparativos
Habilitar puerto serial
Instalación del plugin
Interfaz

Proyecto
Creación de un nuevo proyecto
Apertura de un proyecto existente
Colectar
Contacto

Información general
El complemento de QGIS "Colector" es una aplicación que funciona incrustada en QGIS y que fué programado para ser usado en distribuciones basadaos en Linux como Ubuntu y Ubuntu Mate y distribuciones basadas en Debian como Raspberry Pi OS y está principalmente creado para ser usado en arquitecturas ARM aunque funciona perfectamente en AMD64. El legunaje de programación utilizado es python en su versión 3.6 y funciona para versiones de QGIS que sean iguales o superiores a la versión 3.0. En términos generales el complemento funciona haciendo uso de la clase QgsGpsConnection que viene dentro de la API de QGIS para utilizar la información que el receptor envía en formato NMEA a través del puerto serial, conetandose al receptor, decodificando y extrayendo la información correspondinete a la ubicación geográfica que está siendo estimada en tiempo real por el receptor. Con el fin de mejorar la precisión de esta estimación se realiza la recolección de los datos crudos de la observación GNSS que fueron recepcionados y calculados por el receptor y se almacenan en un formato binario proporcionado por la casa fabricante del receptor (en este caso ubx), todo es esto con ayuda del software RTKLIB.

Con respecto al receptor, el complemento fué programado para ser usado con el receptor u-blox M8T pero puede funcionar con cualquier receptor de esta marca que tenga la capacidad de colectar los datos crudos de la observación GNSS. El receptor debe conectarse al dispositivo en el cual se esté corriendo el sistema operativo a través del puerto serial.

Instalación
Librerías y programas requeridos
PyQGIS
PyQGIS es la API de QGIS que ha sido transformado e interpretado de su lenguaje original C++ a Python, un lenguaje de programación interpretado cuyas carácteristicas principales son la legibilidad de su sintaxis, la orientación a objetos y una amplia comunidad de desarrollo e investigación a lo largo del mundo. Para tener esta API, es necesario tener instalado QGIS, que como lo muestra en su página de instalación se realiza de la siguiente manera: Primero es necesario instalar algunas herramientas que se necesitan:

sudo apt install gnupg software-properties-common
luego es necesario instalar la clave de firma QGIS, de modo que el software QGIS del repositorio QGIS será verificado e instalado:

wget -qO - https://qgis.org/downloads/qgis-2020.gpg.key | sudo gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/qgis-archive.gpg --import
sudo chmod a+r /etc/apt/trusted.gpg.d/qgis-archive.gpg
Lo siguiente es agregar el repositorio de QGIS de la última versión estable para el sistema operativo en la arquitectura utilizada

Nota: «lsb_release -c -s» en esas líneas devolverá su nombre de distribución:

sudo add-apt-repository "deb https://qgis.org/ubuntu $(lsb_release -c -s) main"
Por último se debe actualizar la información del repositorio y ejecutar el comando de instalación:

sudo apt update && sudo apt install qgis qgis-plugin-grass
RTKLIB
RTKLIB es un software de código abierto para el procesamiento y la recolección de datos crudos provenientes de observaciones GNSS. Éste software provee herramientas GUI y CUI con los que, que permite realizar posicionamientos con las constelaciones GPS, GLONASS, GALILEO, QZSS, BeiDoy y SBAS y con los métodos de posicionamiento Single, Static, Kinematic, Fixed, entre otros. Soporta múltiples versiones del formato intercambiable RINEX y puede leer, decodificar y almacenar los mensajes de los principales receptores GNSS propietarios tales como:

NovAtel: OEM4/V/6, OEM3, OEMStar, Superstar II
Hemisphere: Eclipse, Crescent
u-blox: LEA-4T/5T/6T/8T
SkyTraq: S1315F
JAVAD: GRIL/GREIS
Furuno: GW-10 II/III y NVS NV08C BINR.
Además, soporta la comunicación externa con el receptor vía:

Serial
TCP/IP
NTRIP
Archivo local log (carga y recolección)
FTP/HTTP (descarga automática)
Descarga
Para descargar RTKLIB hay 2 opciones:

Desde el Advanced Packaging Tool (recomendado):
Haciendo uso de apt (Advanced Packaging Tool), es posible instalar en linux los binarios de RTKLIB, los cuales quedarán listos para ser usados desde una consola de comandos, sin modificar la estructura de la carpeta /usr/bin. El comando en bash es el siguiente:

sudo apt install rtklib
Desde la página oficial:
En la página oficial RTKLIB permite realizar la descarga tanto de las aplicación con GUI (que tienen interfaz gráfica de usuario) como los binarios que son losq ue realmente serán utilizados. Para hacer uso de estas, es necesario realizar un enlace simbólico, con el que se busca poder ejecutar estos binarios sin necesidad de llamar directamente la ruta en la que se encuentran los binarios.

Preparativos
Habilitar puerto serial
En linux, los dispositivos externos se tratan como si fueran archivos, por lo que para encontrar el puerto serial por el que se conecta el receptor habrá que navegar a la carpeta /dev. Normalmente este puerto serial tiene por nombre ttyACM0 y si intentamos acceder a él ya sea por un software de lectura y escritura de puertos serial o por una librería de algún lenguaje de programación como por ejemplo pyserial, el programa arrojará un error [Error #]: Access is Denied , que corresponde a un error al momento de acceder al archivo con ruta /dev/ttyACM0. Actualmente hay multiples soluciones para este problema, pero las dos principales son las siguientes:

Agregar el usuario actual al grupo dialout (recomendado):
sudo usermod -a -G dialout $USER
Agregar temporalmente permisos de lectura y escritura a todos los usuarios:
Nota: Como los permisos son temporales, cada que se reinicie el dispositivo será necesario volver a agregarlos:

sudo chmod a+rw /dev/ttyACM0
Instalación del plugin
Inicialmente, para la instalación del plugin es necesario descargar o clonar los archivos de este repositorio con git clone https://github.com/AlexanderPretel/Colector y copiar la carpeta Colector a la carpeta ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins. El paso a seguir es ejecutar QGIS (anteriormente instalado) y en la pestaña complementos -> Administrar e instalar complementos seleccionar la pestaña "instalados" como se ve en la siguiente imagen y posteriormente dar click en el checkbox hasta que aparezca como se muestra



Al realizar esto, aparecerá en la interfaz de QGIS un nuevo ícono que será el encargado de ejecutar la interfaz de la aplicación.

Nota: Sólo es necesario hacer click en él cuando se inicia QGIS o cuando la interfaz desaparezca del panel.

Interfaz


Proyecto


Creación de un nuevo proyecto
Al dar click en el botón "Crear" en la interfaz "Proyecto" se abré una ventana de diálogo que permite crear una nueva carpeta. El complemento automáticamente genera una estructura de carpetas como la siguiente:

Base
Export
Survey
Apertura de un proyecto existente
Para abir un proyecto existente, es necesario tener una estructura similar a la presentada en Creacioón de un nuevo proyecto y es recomendable tener dentro de la carpeta "Base" las capas que serán utilizadas al momento del levantamiento. Al momento de dar click en el botón "Cargar" en la interfaz "Proyecto" que permite realizar la apertura de un poryecto existente.

Colectar
 En la interfaz "Colectar" se presentan botones para "Ubicar" que realiza la localización actual y la muestra en el mapa con un círculo verde si el factor DOP es menor a 1 o un círculo rojo si el factor DOP es mayor que 1. También, se encuentra el botón "Colectar" que dependiendo el tipo de geometría que se ha seleccionado en el comboBox, permite realizar la recolección de atributos, localización y su posterior almacenamiento dentro de la capa como un nuevo Feature. Por útlimo, se encuentra el área para colectar vértices que se activa sí y solo sí, la geometría de la capa seleccionada es Linea o Polígono.

Contacto
Autor: Alexander Pretel Díaz

correo: alexander.pretel@correounivalle.edu.co , laboratorio.geoposicionamiento@correounivalle.edu.co
