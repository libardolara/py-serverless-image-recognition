# Función serverless para clasificar imagenes desde Cloudant
> Inspirado en el repositorio [Serverless Image Recognition with Cloud Functions](https://github.com/IBM/ibm-cloud-functions-refarch-serverless-image-recognition)

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

* Instala [Node.js](https://nodejs.org/) si quiere usar Electron.

