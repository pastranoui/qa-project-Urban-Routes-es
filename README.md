**qa-project-Urban-Routes-es**


Descripción del proyecto

Este proyecto contiene pruebas automatizadas para la aplicación Urban Routes. El objetivo es comprobar que las principales funciones para solicitar un taxi funcionan correctamente.

Las pruebas verifican diferentes acciones que puede realizar un usuario, como introducir las direcciones de origen y destino, seleccionar la tarifa Comfort, agregar un número de teléfono y una tarjeta de pago, escribir un mensaje para el conductor y seleccionar servicios adicionales.

También se incluye una prueba completa en la que se realizan varias de estas acciones y finalmente se solicita el taxi.

Tecnologías utilizadas
Para realizar este proyecto utilicé Python, Selenium WebDriver y Pytest.

Selenium se utiliza para abrir el navegador y realizar las acciones dentro de la aplicación. Pytest se utiliza para ejecutar las pruebas y comprobar los resultados.

También utilicé WebDriverWait y Expected Conditions para esperar a que los elementos de la página estén disponibles antes de interactuar con ellos.

Para organizar mejor el código utilicé el patrón Page Object Model. Los elementos y acciones de la página están organizados dentro de la clase UrbanRoutesPage.

Los datos utilizados durante las pruebas, como las direcciones, el número de teléfono, los datos de la tarjeta y el mensaje para el conductor, están guardados en el archivo data.py.

Pruebas realizadas
Las pruebas comprueban las siguientes funciones:

Introducir correctamente la dirección de origen y la dirección de destino.

Seleccionar la tarifa Comfort.

Agregar y confirmar un número de teléfono.

Agregar una tarjeta de pago.

Escribir un mensaje para el conductor.

Solicitar una manta y pañuelos.

Agregar dos helados al pedido.

Realizar un pedido completo de taxi y comprobar que aparece la ventana de búsqueda de automóvil.

Cómo ejecutar las pruebas
Primero es necesario tener instalado Python y Google Chrome.

Después se deben instalar las dependencias necesarias para ejecutar las pruebas. Para esto se puede utilizar el siguiente comando:

pip install selenium pytest

También es necesario tener un controlador compatible con la versión de Google Chrome instalada.

Antes de ejecutar las pruebas, hay que comprobar que los datos del archivo data.py sean correctos, especialmente la URL de Urban Routes y los datos utilizados en las pruebas.

Para ejecutar todas las pruebas, hay que abrir la terminal desde el directorio raíz del proyecto y utilizar el comando:

pytest

Si se quiere obtener más información sobre cada prueba durante la ejecución, se puede utilizar:

pytest -v

Pytest ejecutará automáticamente las funciones que comienzan con test_ y mostrará en la terminal cuáles pruebas pasaron y cuáles tuvieron algún error.

Nota
La función retrieve_phone_code() permite obtener el código de confirmación del teléfono durante la ejecución de las pruebas. Esta función y la configuración relacionada con los registros de rendimiento de Chrome no deben modificarse, ya que son necesarias para que la prueba de confirmación del teléfono funcione correctamente.