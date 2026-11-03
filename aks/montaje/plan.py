# Plan del montaje: cada tramo es (id, visual, texto de la locucion).
# visual: ("img", "00-portada") | ("vid", "bloque1", inicio, fin)   (fin None = hasta el final de la toma)
# En los bloques, ("paso", k) es el segundo en que aparece el comentario verde numero k (marcas.json, OCR); 0 = inicio de la toma.
# Cada texto de terminal esta escrito para llenar su tramo: primero explica que se hace y por que, y cierra con el resultado.

TRAMOS = [
 ("s01", ("img", "00-portada"),
  "Hola. En este video vamos a conocer Azure Kubernetes Service, o AKS, el servicio de Kubernetes administrado de Microsoft Azure. Veremos cómo funciona, qué lo diferencia, sus ventajas y desventajas, y al final lo pondremos a prueba desplegando dos aplicaciones distintas en un clúster real."),
 ("s02", ("img", "01-que-es-kubernetes"),
  "Empecemos por Kubernetes. Es una plataforma que automatiza el despliegue, el escalado y la operación de contenedores. La idea central es sencilla: uno declara el estado deseado, por ejemplo tres réplicas de una aplicación, y Kubernetes trabaja todo el tiempo para que la realidad coincida con esa declaración. Nació en Google, a partir de su experiencia con el sistema Borg. Un clúster tiene dos partes: el plano de control, con el API server, etcd, el scheduler y los controladores, que toma las decisiones; y los nodos, que ejecutan los pods donde viven nuestros contenedores."),
 ("s03", ("img", "02-que-hace-azure"),
  "Operar ese plano de control no es trivial: hay que mantenerlo disponible, actualizarlo y aplicarle parches de seguridad. En AKS todo eso lo hace Azure. A nosotros nos queda decidir cuántos nodos y de qué tamaño, construir las imágenes, escribir los manifiestos de las aplicaciones y, muy importante, vigilar los costos."),
 ("s04", ("img", "03-caracteristicas"),
  "¿Qué distingue a AKS de otras opciones? Primero, sus niveles de servicio: en el nivel Free el plano de control no cuesta y solo se pagan las máquinas de los nodos; los niveles Standard y Premium agregan un acuerdo de nivel de servicio pensado para producción. Segundo, la integración con el resto de Azure: Container Registry para guardar las imágenes, Microsoft Entra ID para la identidad, discos administrados para los datos, balanceadores de carga y Azure Monitor. Tercero, la sencillez: el clúster se crea con un solo comando, con el registro de imágenes ya conectado. Y cuarto, la automatización: el escalado automático de nodos y la modalidad AKS Automatic, que configura el clúster con buenas prácticas desde el inicio."),
 ("s05", ("img", "04-ventajas-desventajas"),
  "Hagamos el balance. Entre las ventajas: hay mucha menos carga operativa, porque Azure se encarga del plano de control; la integración con identidad, monitoreo y almacenamiento es nativa; y los manifiestos son estándar de Kubernetes, así que sirven en otros proveedores. Entre las desventajas: el nivel Free no tiene acuerdo de nivel de servicio, así que no es para producción; los nodos, los discos, las IP públicas y los registros se pagan aunque estén ociosos; los servicios integrados generan dependencia del proveedor; y la complejidad de Kubernetes no desaparece, solo se reduce. Lo vivimos en carne propia: la cuenta de estudiante tiene pocas regiones y cupos bajos de CPU, por eso usamos dos nodos pequeños en North Central US."),
 ("s06", ("img", "06-dos-aplicaciones"),
  "Pasemos a la práctica. En un mismo clúster vamos a desplegar dos aplicaciones con necesidades muy diferentes: la tienda de la unidad anterior, que guarda datos en MySQL, y whoami, un servicio sencillo sin estado. Antes de grabar, un script creó el grupo de recursos y el registro de contenedores, subió allí nuestras imágenes y creó el clúster con un solo comando. Veamos qué quedó."),
 # Bloque 1
 ("b1a", ("vid", "bloque1", ("paso", 0), ("paso", 1)), "Cada paso de la terminal tiene un comentario en verde que explica lo que vamos a hacer. Empezamos revisando el clúster."),
 ("b1b", ("vid", "bloque1", ("paso", 1), ("paso", 2)), "Con la CLI de Azure consultamos el clúster que creamos. Pedimos solo cuatro datos: el nombre, la versión de Kubernetes, el nivel y la región. Ahí está: aks tienda, con Kubernetes uno punto treinta y seis, en el nivel Free, que no cobra el plano de control, y en North Central US."),
 ("b1c", ("vid", "bloque1", ("paso", 2), ("paso", 3)), "Ahora le preguntamos a Kubernetes por sus nodos. Son dos máquinas virtuales de Azure con Ubuntu, ambas en estado Ready, listas para recibir pods."),
 ("b1d", ("vid", "bloque1", ("paso", 3), ("paso", 4)), "En el espacio kube system están los componentes que Azure instala y mantiene por nosotros: el DNS interno, el proxy de red, los controladores de discos y el servidor de métricas."),
 ("b1e", ("vid", "bloque1", ("paso", 4), ("paso", 5)), "Las clases de almacenamiento son el puente entre Kubernetes y los discos de Azure. Cuando una aplicación pide un volumen, la clase decide qué tipo de disco crear. Hay opciones con Azure Files y con discos administrados; la base de datos de la tienda usará managed csi, un disco administrado estándar."),
 ("b1f", ("vid", "bloque1", ("paso", 5), None), "Por último, el registro de contenedores. Ahí están nuestras dos imágenes, tienda web y tienda MySQL, construidas desde el código de la unidad anterior."),
 # Equivalencias y manifiestos
 ("s07", ("img", "05-compose-a-kubernetes"),
  "La primera aplicación es la tienda, hecha con Node.js y MySQL. En la unidad anterior la levantábamos con Docker Compose, y cada pieza tiene su equivalente en Kubernetes. El servicio web pasa a ser un Deployment con dos réplicas. La base de datos, un StatefulSet, que le da a cada pod un nombre y un disco estables. El volumen se convierte en un PersistentVolumeClaim, que Azure respalda con un disco administrado. Las variables de entorno van a un ConfigMap y las contraseñas a un Secret. El healthcheck se vuelve una sonda de disponibilidad, y los puertos publicados, un servicio LoadBalancer con IP pública."),
 ("vsa", ("vid", "vscode-manifiestos", 0, 22), "Así se ve en los manifiestos. En el de MySQL, un servicio sin IP le da a la base de datos un nombre estable, db, y el StatefulSet incluye una plantilla de volumen que pide un disco de cuatro gigas."),
 ("vsb", ("vid", "vscode-manifiestos", 22, None), "En el del servidor web, el Deployment pide dos réplicas, toma la configuración del ConfigMap y las claves del Secret, limita la CPU y la memoria, y solo envía tráfico a un pod cuando la ruta salud responde."),
 # Bloque 2
 ("b2a", ("vid", "bloque2", ("paso", 0), ("paso", 1)), "Ahora sí, desplegamos la tienda. Vamos a aplicar los manifiestos uno por uno, en orden, para ver qué crea cada uno."),
 ("b2b", ("vid", "bloque2", ("paso", 1), ("paso", 2)), "Primero, dos namespaces, tienda y whoami. Son como carpetas dentro del clúster que mantienen separados los objetos de cada aplicación."),
 ("b2c", ("vid", "bloque2", ("paso", 2), ("paso", 3)), "Luego, la configuración. El ConfigMap guarda datos como el nombre de la base de datos y el Secret guarda las contraseñas, así no quedan escritas dentro de la imagen."),
 ("b2d", ("vid", "bloque2", ("paso", 3), ("paso", 4)), "Aplicamos MySQL. Se crean el servicio db y el StatefulSet, que a su vez le pedirá a Azure un disco persistente para guardar los datos."),
 ("b2e", ("vid", "bloque2", ("paso", 4), ("paso", 5)), "Y el servidor web: un Deployment de dos réplicas y un servicio de tipo LoadBalancer, que le pedirá a Azure una IP pública."),
 ("b2f", ("vid", "bloque2", ("paso", 5), ("paso", 7)), "Ahora esperamos a que todo esté listo. Mientras tanto, Azure trabaja por debajo: crea el disco administrado, lo conecta al nodo donde corre MySQL y arranca la base de datos. El servidor web espera a que la sonda de salud responda antes de recibir tráfico. Primero queda lista la base de datos, y luego las dos réplicas del servidor web."),
 ("b2g", ("vid", "bloque2", ("paso", 7), ("paso", 8)), "Revisemos lo creado. Hay tres pods corriendo, repartidos entre los dos nodos. El servicio web ya tiene IP externa, y el volumen persistente está enlazado a un disco de cuatro gigas de la clase managed csi."),
 ("b2h", ("vid", "bloque2", ("paso", 8), ("paso", 9)), "El script detecta la IP pública del balanceador. Con kubectl exec entramos al pod de MySQL y cargamos los quince productos de prueba, los mismos de la unidad anterior."),
 ("b2i", ("vid", "bloque2", ("paso", 9), None), "Y probamos la API desde internet con curl. Responde el pod que atendió la petición, y un total de quince productos. La tienda ya está funcionando en Azure."),
 ("nta", ("vid", "navegador-tienda", 11, None), "Lo mismo en el navegador. La tienda carga desde la IP pública de Azure. La tarjeta del contenedor web muestra qué pod atendió la petición, y abajo aparecen las cuatro categorías y los quince productos, leídos de MySQL. La API devuelve la misma información en formato JSON."),
 # Bloque 3
 ("b3a", ("vid", "bloque3", ("paso", 0), ("paso", 1)), "Vamos con la segunda aplicación: whoami, un servicio que no guarda datos y responde con el nombre del pod que atiende cada petición."),
 ("b3b", ("vid", "bloque3", ("paso", 1), ("paso", 2)), "Un solo manifiesto crea tres objetos: el Deployment con tres réplicas, el servicio LoadBalancer y un autoescalador horizontal, que veremos en acción más adelante."),
 ("b3c", ("vid", "bloque3", ("paso", 2), ("paso", 3)), "Esperamos a que las tres réplicas estén listas y a que Azure asigne la IP pública. Al no tener disco, esta aplicación arranca mucho más rápido que la tienda."),
 ("b3d", ("vid", "bloque3", ("paso", 3), ("paso", 4)), "Ahora hacemos seis peticiones seguidas y mostramos solo la línea del hostname. Fíjense que no siempre responde el mismo pod: el servicio reparte las peticiones entre las réplicas. Eso es el balanceo de carga."),
 ("b3e", ("vid", "bloque3", ("paso", 4), None), "Y con la opción wide vemos que Kubernetes repartió los tres pods entre los dos nodos, para que la caída de uno no tumbe el servicio."),
 ("nwa", ("vid", "navegador-whoami", 10, None), "En el navegador se ve igual de claro. Con cada recarga, el hostname puede cambiar: unas veces responde un pod y otras veces otro, aunque la dirección es la misma."),
 # Bloque 4
 ("b4a", ("vid", "bloque4", ("paso", 0), ("paso", 1)), "Ahora veamos la operación del día a día, que es donde Kubernetes realmente ahorra trabajo."),
 ("b4b", ("vid", "bloque4", ("paso", 1), ("paso", 2)), "Supongamos que llega más tráfico. Con un solo comando escalamos whoami de tres a cinco réplicas. Kubernetes compara el estado actual con el deseado, ve que faltan dos pods y los crea. En pocos segundos las cinco réplicas están disponibles."),
 ("b4c", ("vid", "bloque4", ("paso", 2), ("paso", 3)), "Ahora simulemos una falla. Borramos a propósito uno de los pods, como si su proceso se hubiera caído o su nodo hubiera tenido un problema."),
 ("b4d", ("vid", "bloque4", ("paso", 3), ("paso", 4)), "Al listar los pods vemos que siguen siendo cinco. Kubernetes detectó que faltaba uno y creó otro para volver al estado deseado: es el que tiene la edad más corta. A esto se le llama autorreparación, y no tuvimos que hacer nada."),
 ("b4e", ("vid", "bloque4", ("paso", 4), ("paso", 5)), "Ahora una actualización. Cambiamos la imagen a una versión nueva. La actualización es progresiva: Kubernetes crea pods nuevos y retira los viejos de a poco, así que el servicio nunca se cae."),
 ("b4f", ("vid", "bloque4", ("paso", 5), ("paso", 6)), "El historial del Deployment guarda cada versión desplegada. Aquí aparecen dos revisiones: la original y la actualización."),
 ("b4g", ("vid", "bloque4", ("paso", 6), ("paso", 7)), "Si la versión nueva fallara, volvemos atrás con rollout undo. Kubernetes hace el mismo reemplazo progresivo, pero hacia la versión anterior, también sin caída del servicio."),
 ("b4h", ("vid", "bloque4", ("paso", 7), None), "Por último, el autoescalador. Vigila el uso de CPU y mantiene entre tres y ocho réplicas. Como es recién creado, todavía no tiene métricas."),
 # Bloque 5
 ("b5a", ("vid", "bloque5", ("paso", 0), ("paso", 1)), "Para terminar, la prueba más importante para la tienda: que los datos sobrevivan aunque el pod de la base de datos desaparezca."),
 ("b5b", ("vid", "bloque5", ("paso", 1), ("paso", 2)), "Primero contamos los productos directamente en MySQL, entrando al pod con kubectl exec. El resultado es quince, los que cargamos hace un momento."),
 ("b5c", ("vid", "bloque5", ("paso", 2), ("paso", 4)), "Ahora borramos el pod de MySQL, sin aviso. Con un contenedor normal, perderíamos los datos. Pero el StatefulSet lo recrea con el mismo nombre, mysql cero, y Azure vuelve a conectar el mismo disco administrado al nodo donde arranca el pod nuevo. Esperamos a que la base de datos vuelva a estar disponible."),
 ("b5d", ("vid", "bloque5", ("paso", 4), ("paso", 5)), "Volvemos a contar los productos, y el resultado es otra vez quince. Los datos no vivían en el pod, sino en el disco persistente, así que siguen ahí."),
 ("b5e", ("vid", "bloque5", ("paso", 5), None), "Lo confirma el volumen persistente: sigue enlazado al mismo disco, porque en Azure es un recurso independiente del pod."),
 # Cierre
 ("s08", ("img", "07-conclusiones"),
  "En conclusión: AKS reduce mucho el trabajo de operar Kubernetes, porque Azure se encarga del plano de control, y se integra de forma natural con el registro de imágenes, los discos, la red y la identidad de Azure. En la demostración vimos balanceo de carga, escalado, autorreparación, actualizaciones sin caída y datos persistentes. A cambio, exige vigilar los costos y entender bien los objetos de Kubernetes. Por eso, al terminar la grabación borramos el grupo de recursos para no consumir crédito. Los manifiestos y los scripts están en el repositorio del proyecto. Muchas gracias."),
 ("s09", ("img", "08-referencias"), "Estas son las referencias que usamos para preparar el video."),
]

# Pronunciacion para la voz (solo en el texto que se envia a ElevenLabs)
FONETICA = [("Azure", "Áshur"), ("MySQL", "mai ese cu ele"), ("whoami", "hu ami"), ("AKS", "a ka ese"), ("JSON", "yeison"),
            ("CPU", "ce pe u"), ("IP", "i pe"), ("DNS", "de ene ese"), ("CLI", "ce ele i"), ("Node.js", "Node ye ese"),
            ("rollout undo", "rol aut undu"), ("kubectl exec", "cube control exec"), ("curl", "curl"), ("etcd", "et ce de")]
