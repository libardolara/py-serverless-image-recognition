# Función serverless para clasificar imagenes desde Cloudant
> Inspirado en el repositorio [Serverless Image Recognition with Cloud Functions](https://github.com/IBM/ibm-cloud-functions-refarch-serverless-image-recognition)

> Presentación de [Introducción a OpenWhisk - Serverless](https://ibm.box.com/v/wsk-ppt)

La aplicación demuestra una IBM Cloud Functions (basado en Apache OpenWhisk) que obtiene una imagen desde una base de datos en Cloudant y la clasifica a traves de Watson Visual Recognition. El caso de uso demustra como funcionals las acciones con servicios de datos y ejecuta un codigo en respuesta a un evento en Cloudant.

Una función, o acción, es disparada por cambios (en este caso de uso porque se sube un documento) en una base de datos Cloudant. Estos documentos son redirigidos a una acción que envia la imagen a Watson Visual recognition and sube un nuevo documento en Cloudant con los tags producidos por Watson.

Cuando termines este Code Pattern, entenderas como:

* Crear y desplegar Cloud Functions
* Disparar Cloud Functions con cambios en Cloudant
* Usar Watson Visual Recognition con Cloud Functions

![](docs/architecture.png)

## Flujo

1. El usuario escoge una imagen.
2. La imagen es almacenada en la base de datos Cloudant.
3. Una Cloud Function es disparada cuando hay una nueva imagen en la base de datos.
4. Una Cloud Function obtiene la imagen y ysa Watson Visual Recognition para procesar la imagen.
5. La Cloud Function guarda el resultada (tags con scores) del Visual Recognition en la base de datos.
6. El usuario puede ver los nuevos tags o clases en la imagen que subio.

## Componentes Incluidos

* [IBM Cloud Functions](https://console.ng.bluemix.net/openwhisk) (basado en Apache OpenWhisk): Ejecuta codigo bajo demand en un ambiente serverless y altamente escalable.
* [Cloudant](https://console.ng.bluemix.net/catalog/services/cloudant-nosql-db): Una base de datos completamente manejada diseñada para aplicaciones web y mobile modernas que usan documentos como JSON.
* [Watson Visual Recognition](https://www.ibm.com/watson/developercloud/visual-recognition): Visual Recognition usa algoritmos de deep learning para identificar escenas, objetos y rostros en una imagen. Pudes crear y entrenar clasificadores customizados para identificar patrones para tus necesidades.

## Tecnologias Importantes

* [Watson](https://www.ibm.com/watson/developer/): Watson en IBM Cloud permite integrar herramientas de AI en tu aplicación y guardar, entrenar y manejar tu data en una nube segura.
* [Serverless](https://www.ibm.com/cloud-computing/bluemix/openwhisk): Una plataforma basada en eventos que permite ejecutra codigo como respuesta a un evento.

# Prerequisitos

* [IBM Cloud Functions CLI](https://console.bluemix.net/openwhisk/learn/cli) para crear cloud functions desde la terminal. Haz una prueba de una acción `ibmcloud wsk action invoke /whisk.system/utils/echo -p message hello --result` para que tu `~/.wskprops` apunte a la cuenta correcta.

* [Whisk Deploy _(wskdeploy)_](https://github.com/apache/incubator-openwhisk-wskdeploy) es una herramienta que ayuda a describir y desplegar cualquier componente de OpenWhisk usando un archivo Manifest escirto en YAML. Lo usuaras si deseas hacer el despliege despliegue de todos los recursos de Cloud Functions en una sola linea de comandos. Puedes descargar en [releases page](https://github.com/apache/incubator-openwhisk-wskdeploy/releases) y seleccionar el archivo correcto para tu sistema operativo.

* Instala [Python](https://www.python.org/downloads/) para instalar las dependencias en tu computador. `Python >= 3.5`

* Instala [Node.js](https://nodejs.org/) si quiere usar Electron.

# Paso a Paso

### 1. Clonar el repo

Descarga o clona el repositorio `py-serverless-image-recognition` localmente. En una terminal, ejecuta:

```
$ git clone https://github.com/libardolara/py-serverless-image-recognition
```

### 2. Crea los servicio de IBM Cloud

Crea el servicio [**Cloudant**](https://console.bluemix.net/catalog/services/cloudant) escogiendo `Use both legacy credentials and IAM` para la opción _Available authentication method_.
* Crea las credenciales para la instacia y copia el username y password en el archivo `local.env` en el valor de `CLOUDANT_USERNAME` y `CLOUDANT_PASSWORD`.
* Copia las mismas credenciales del punto anterior en el archivo `actions/params.json`
* Lanza la consola web de y crea una base de dato llamada `images` y otra llamada `tags`. 
> Modifica el archivo `local.env` si planeas usar nombres de bases de datos diferentes.

Crea un servicio de [Watson Visual Recognition](https://console.bluemix.net/catalog/services/visual-recognition).
* Copia el API Key de la seccion de Credentials y pegala en el archivo `local.env` en el valor de `WATSON_VISUAL_APIKEY`
* Copia el mismo API Key en el archivo `actions/params.json`

### 3. Desplegar Cloud Functions
> Escoge un mentodo de despliegue

#### Desplegar a través del CLI de IBM Cloud Functions

Una vez completo los calores del archivo `local.env`, abre una terminal.

* Inicia sesión en IBM Cloud según la región que desees usando CLI, para ello utiliza uno de los siguientes comandos y sigue las instrucciones: 

```
$ ibmcloud login
```
> Sigue las instrucciones interactivas del CLI

Si deseas cambiar la región puedes usar alguna de los siguientes comandos:

```
$ ibmcloud login -a https://api.ng.bluemix.net            // US South
$ ibmcloud login -a https://api.us-east.bluemix.net       // US East
$ ibmcloud login -a https://api.eu-gb.bluemix.net         // UK
$ ibmcloud login -a https://api.eu-de.bluemix.net         // Germany
$ ibmcloud login -a https://api.au-syd.bluemix.net        // Sydney
```
> Donde `-a` indica que se va a seleccionar una región de API específica.

*	Observa el resultado del proceso anterior, tu organización y espacio están vacíos. Para configurar la organización y espacio que deseas usar en Cloud Foundry debes ejecutar el siguiente comando.

```
$ ibmcloud target -–cf
```
> Selecciona usando los menús, la organización y espacio que deseas utilizar.

Si deseas cambiar de Organización y de espacio puedes usar el comando

```
$ ibmcloud target -o <organization name> -s <spacename>
```

* Posicionate en la carpeta `/actions` 
* Aplica las variables locales sobre tu terminal. (Si usas Windows tendrás que reemplazar cada valor en los comandos que se usaran)

```
$ source local.env
```

* Instanciar el Package de Cloudant en tu cuenta. Llamaremos el paquete `serverless-python-cloudant-pkg`.

```
$ ibmcloud wsk package bind /whisk.system/cloudant serverless-python-cloudant-pkg -p username $CLOUDANT_USERNAME -p password $CLOUDANT_PASSWORD -p host ${CLOUDANT_USERNAME}.cloudant.com
```

* Crear el _Trigger_ que leera el evento de documentos subidos a la base de datos. Llamaremos el Trigger `update-trigger`

```
$ ibmcloud wsk trigger create update-trigger --feed serverless-python-cloudant-pkg/changes --param dbname $CLOUDANT_IMAGE_DATABASE
```

> TODO Colocar un link a documentación del uso de librerias propias

* Sube la función, o acción, usando el ambiente en IBM Cloud Function `python:3.7`. Llamaremos la acción `update-document`

```
$ ibmcloud wsk action update update-document __main__.py --kind python:3.7 --param-file params.json
```

* Crea una Regla que une la acción y el Trigger. Llamaremos la regla `update-trigger-rule`

```
$ ibmcloud wsk rule create update-trigger-rule update-trigger update-document
```

### 4. Lanzar Aplicación

Configura `electron/web/scripts/upload.js`. Modifica las lineas con las credenciales de Cloudant.

```js
let usernameCloudant = "YOUR_CLOUDANT_USERNAME"
let passwordCloudant = "YOUR_CLOUDANT_PASSWORD"
```

Ejecuta la aplicación Electron o abre el html.

* Electron:
```
$ npm install
$ npm start
```

* _(o) Doble-click `web/index.html`_

#### Ejemplo

![sample-output](docs/screenshot.png)
