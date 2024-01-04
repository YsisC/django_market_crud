# django_market_crud
Estae es un repositorio de una API REST con Django y SQLLITE


# Variables de entorno

VITE_BACKEND_URL, esto es necesario para produccin

# Requisitos prueba tecnica

1. Mediante una query SQL, obtener los productos indicando su último menor precio activo, EAN, SKU y su mercado (market).
2. Teniendo en cuenta el modelo de la imagen 1, describa con palabras un proceso que tenga que ser ejecutado cada cierto tiempo (automatización) y que obtenga información “relevante” diferente a la pedida en la pregunta 1.
3. Basándose en los datos obtenidos en la respuesta de la pregunta 1.
Escribir una función en Python que recorra los datos y agrupe los productos mediante su Ean en el siguiente diccionario 
{
	“Ean”: {
			“nombre producto (asumir que los productos con mismo Ean tienen el mismo nombre)”,
			“datos de la query”:[“listado de los datos que vienen en la query”,],
			“cantidad de markets diferentes”,
			“rango de precios (Mayor precio - Menor precio)”
},
}


1. http://127.0.0.1:8000/markets/api/products/last_active_price
2. Objetivo: Obtener estadísticas mensuales de ventas.
Pasos:
Conectar a la Base de Datos:

Establecer una conexión con la base de datos que contiene la información de los pedidos.
Filtrar Pedidos por Mes:

Obtener todos los pedidos realizados en el último mes.
Calcular Estadísticas:

Calcular estadísticas relevantes, como el total de ventas, el número de pedidos realizados, los productos más vendidos, etc.
Guardar Resultados:

Almacenar los resultados de las estadísticas en una base de datos o archivo para su referencia futura.
Notificar:

Enviar notificaciones por correo electrónico o mensajes internos a los interesados, como los administradores del sistema.
Programar la Ejecución Automática:

Configurar un sistema de tareas programadas para que este proceso se ejecute automáticamente cada fin de mes.
Este proceso de automatización proporciona información relevante sobre las ventas mensuales, lo cual es valioso para la toma de decisiones empresariales. Puedes adaptar este ejemplo a tu propio contexto y modelos específicos.

3. Basándose en los datos obtenidos en la respuesta de la pregunta 1.
Escribir una función en Python que recorra los datos y agrupe los productos mediante su Ean en el siguiente diccionario 
{
	“Ean”: {
			“nombre producto (asumir que los productos con mismo Ean tienen el mismo nombre)”,
			“datos de la query”:[“listado de los datos que vienen en la query”,],
			“cantidad de markets diferentes”,
			“rango de precios (Mayor precio - Menor precio)”
},
}
El diccionario anterior debe ser recorrido mediante React, en donde se debe crear componentes HTML que contendrán el nombre del producto, el rango de precios y en cuántos mercados diferentes se encuentra. Poner un input en donde se puede filtrar los productos que se ven por su nombre y utilizando hooks (useEffect) hacer que los productos que no se deben ver vayan desapareciendo 1 a 1 cada segundo.
	Consideraciones:
No es necesario que el HTML tenga CSS o algún tipo de estilo.
El arreglo de diccionarios puede estar definido como constante dentro de React y su data debe ser inventada, al menos 3 Eans diferentes.
Al cargar la página se debe poder ver el HTML creado


