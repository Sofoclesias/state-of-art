# Devlog
-----

# 22 de abril, 2025
Debí haber estudiado ciencias de la computación, probablemente. Creo que habría sido más feliz y estaría más satisfecho con la base teórica.
Actualmente estoy enfocándome demasiado en la recolección de datos, pero debería 

Prof mostró interés en MongoDB para el manejo de datos NoSQL. Puedo darle un vistazo, idealmente para la presentación parcial (pero no debo perder de vista primero lograr el mínimo indispensable para la presentación.)
También en HBase, pero dice que es duro. Idk, ya veré.

IMPORTANTE BISETTI: NO PIERDAS DE VISTA LOGRAR EL MÍNIMO INDISPENSABLE PARA LA PRESENTACIÓN PARCIAL.

Las solicitudes http enrutadas con Tor han demostrado 1. ser efectivas en explotar la recolección de recursos de la API, 2. ser eficientes en recursos y 3. muy escalables. Podría utilizar 23 enrutamientos para los 23 campos de estudio, pero soy un poco bobo o le temo al éxito (en realidad es porque en Tor son lentas de huevos). 
De todas formas, en términos de escalabilidad, debería indagar en potenciales mejores opciones (como desplegar servidores proxy o algo de IPs rotativas) y en métricas de escabilidad o control. Después de todo, no quiero saturarme yo con 1000 daemons de Tor o a Semantic Scholar.
   * PARA MÁS ADELANTE (o en un rato): empezar a estudiar network engineering + servers o algo lmao.
   * OCULTAR IP PARA ESCALABILIDAD DE HTTP REQUESTS.

También, pucha, me preocupa el tema del almacenamiento. Los .txt son controlables de momento, pero es que actualmente en realidad no tengo data, solo potencial de data xd. Los .json pueden irse en yara, puede que incluso más cuando lo pase a un modelo relacional o gráfico. Si ya eso es preocupante, imagina la adición de los .pdfs lmao.
   * Ponderar invertir en un NAS y HDDs para escalar espacio y chance con eso desplegar un HDFS. 
   * Ver si consigo cotizar una reparación para la laptop vieja (de ser posible) o pedirle a alguien alguna laptop que ya no usen o esté por morir. Necesito un homelab urgente ya donde hostear servidores y servicios; para Big Data se ha vuelto una necesidad.
   * Quiero recuperar mi pc pe

REQUERIMIENTOS FUNCIONALES DE LA SIGUIENTE RECOLECCIÓN

La extracción de las IDs funciona bien, pero está demorando mucho. Considerando que prof quiere prácticamente ya toda la BD en la presentación parcial, debo apresurar.

1) El crawler de los detalles debe hacerse ante la disponibilidad de nuevos IDs que extraer.
   * Un programa con agenda para concatenar todos los IDs, comparar con los que ya hay registrados, y buscar los que no se tengan.
   * De momento enrutar con Tor (probablemente sería mejor ip rotation(?)).
   * Como el .sh (aunque no necesariamente se hará con ello, no sé), que pueda crear y eliminar los proxies Tor.
2) ¿Apache Beam o Apache Spark? Uno de los dos en principio maneja datos en stream, en tiempo real. Investigar si es cierto (sería un puntazo tener ya una tecnología de Big Data en esta entrega parcial. Un wildcard, eso es lo que soy.)
   * Revisar papers O aplicaciones de cosas on demand.
   * Particularmente deseable si son capaces de gestionar la escalabilidad de los pipelines.
   * Probablemente una palabra clave acá sea concurrencia con paralelismo integrado.
3) Se debe estructurar en forma de base de datos relacional, en principio, y debe ser mandado a postgresql o mongodb.
   * Mapear modelo relacional.
   * Mapear cada query que se transformará en tabla.
   * Los requests a la API para cada query del db deben ser procesados en paralelo, pero deben esperar a que todo termine para recién proseguir.
   * ¿Base de datos SQL con la ruta del paper, NoSQL? ¿Qué chucha es una base de datos gráfica, acaso serviría acá?
   * La subida a la db tiene que ser al toque.
4) A la vez, descargar los archivos .pdf o lo que sea
   * ¿Cómo agregaría los pdfs en la base de datos?
   * Aprovechar aquellos que son públicos, buscar los que sean pirateables y anotar los que no parecen estar para inspección posterior.
5) Agregar paneles de control o indicadores de salud
   * Tanto para indagar como para tomar decisiones de escalabilidad o algo.
   * PARTICULARMENTE IMPORTANTE CON EL TEMA DEL ALMACENAMIENTO.
   * Opciones de compresión y reducción de espacio (?)
6) Metaconsideraciones
   * Mi PC principal ya está teniendo sus malas noches solo con la extracción de los IDs. No quisiera aumentarle la carga con esta huevada. Ver si puedo abrir una red local, meterme desde mi laptop a mi compu y ejecutar con memoria compartida.

De forma ideal, esto ya quedaría como un algoritmo escalable para cualquier nueva id recabada.

Otra vez, wildcard effect que indica nuevamente no perder de vista lo mínimo presentable; pero sería bravazo poder mostrar ya una demostración gráfica de mi coso en funcionamiento. Como esa otra aplicación de spark que vi en github.

Entonces, para recapitular los pasos:

1) INVESTIGAR | Diferenciar y comparar PostgreSQL, MongoDB, Cassandra; alguna solución de graphdb(?). Ello implica desplegar también, crear dbs, hacer queries y todo todo todo para mandar nomás.

2) INVESTIGAR | Mejores prácticas para la escalabilidad de múltiples puertos tor.

3) PLANIFICAR | Modelo relacional y queries para la API

4) HACER | Mínimo código que abra un proxy tor, mande los requests necesarios a la API para una id, estructure la información para la dbms escogida y haga la recolección del .pdf. Poner log.

5) INVESTIGAR | Ver performance en papers de cosas con demand de Apache Beam o Apache Spark y cómo lo hacen; idealmente en scraping o crawling masivo con http requests. ASEGURAR CONCURRENCIA O PARALELISMO.

6) HACER | Si hay evidencia de eficiencia y escalabilidad para eventos a demand, a meterle ya una tecnología de Big Data ps :p. Ver cómo configurar la forma de prestar atención y activarse. Si no, tocó hacer manual ello y la forma de programar paralelismo (probablemente similar al .sh).

7) Loggear métricas y demás para gráficos después.

8) INVESTIGAR | Abrir red local y compartir memoria para el procesamiento paralelo entre la extracción de IDs y la preparación de la data.
   * Para mi compu principal, ya solo debo esperar que termine. Mucho tiempo ya pasó. Me conectaré allí mientras espero que termine. Cuando termine, ya podría derivar ese trabajo o a una laptop prestada (si eso funca) o a un NAS.

TODO ESTO PARA MÁXIMO EL JUEVES SI QUIERO TENER UN BUEN MARGEN DE TIEMPO ENTRE LA RECOLECCIÓN DE DATOS Y LA ENTREGA PARCIAL!!
IMPORTANTE!!
EL JUEVES O ME MORIRÉ!!
Chance hasta máximo el viernes, pero de ahí ya no puede pasar o lloraré.
Vamos, Bisetti, por nuestra salud mental y seguridad. Ya has vomitado todos tus pensamientos y sabes qué hacer. Considera que una vez acabes esto, podrás ya continuar chateando con ese ingeniero nuclear que te trae en un crush.
De todas formas, son bastantes tópicos nuevos de imprevisto. Será un reto enorme lograrlo para el jueves, pero alucina que sí estás en peligro de morir pues. Activa el hiperfoco.

Considerar además que:
   * El viernes hay control de Big Data.
   * El martes siguiente hay PC de Big Data.
   * El viernes siguiente es la entrega de todo esto.
   * Preparar algoritmo de Map Reduce para la PC (idealmente mejor si lo tienes pal control)

Mientras antes tengas el API exploiter, más tiempo tendrás para redactar el paper y para estudiar bien para las cosas de Big Data (que justo se ha acumulado todo ahora xd).

Probablemente el manejo del proyecto de aquí hasta la entrega parcial será:
1) Terminar el API exploiter y dejar que trabaje hasta su fin (indefinido).
2) Trabajar estado del arte (knowledge graphs es lo más cercano a la visión general que tengo)
3) Finalizar descripción de la metodología, desde la recolección hasta la estructuración de los datos, así como el entrenamiento y evaluación del sistema de recomendación; pero dejar pendientes las estadísticas descriptivas y los gráficos de performance (si es que para entonces no ha terminado).
4) Realizar tres diseños descriptivos:
   * Uno para finalizar la introducción con un diagrama de funcionamiento.
   * El de los pasos de la metodología para el "study design".
   * El ecosistema de servidores, entre los grupos de workers y el maestro. PREVISTOS:
      * Master node o de monitorio (zookeeper? no sé). Yarn quizás por el resource management, pero creo que ya viene integrado.
      * Proxy servers: API-crawlers (el de ids como el de detalles)
      * Storage servers: potencialmente un HDFS en un NAS, o nada.
      * MongoDB o lo que sea server para la base de datos.
      * App server o Spark app para la interacción de la aplicación por cliente.
      * Nodo para procesamiento, extracción de datos, entrenamiento del modelo de deep learning
5) Terminar la introducción y la colocación de objetivos.
6) Por supuesto, las citas.
7) Preparar el PPT con toda la información condensada del paper para la exposición.
7) Idealmente, todo lo descrito hasta ahora, incluido la tarea del API exploiter, estaría terminado. Exagerando el menor tiempo, el domingo; a más tardar, el miércoles. Proceder con la realización de estadísticas descriptivas, análisis exploratorios y gráficos de monitoreo de recursos.
   * Si es así, me cubro de gloria (ignorando fuertísimo el peligro latente del espacio xd). No tendré que modificar lineas después, eficiencia.
   * Si no es así, pucha, copia un snippet de los papers tomados y realiza los gráficos y descripciones sobre ello nomás. Joda que luego habría que cambiarlas, pero no es lo peor del mundo.
8) Para este punto, el paper ya estaría técnicamente terminado. Agregar lo último en el ppt y preparar el conjunto de archivos para la entrega (paper en inglés, bibtex, tex y tal, ¿los datos? Preguntar al profesor cómo pasarle los datos de lo mío).
   * Probablemente pueda mandar una tabla plana de excel y los archivos, o si consigo desplegar el server en mi laptop o con conexión remota 
SI QUEDA TIEMPOOOOOO
9) Crear webapp que es como connected papers. No me apetece pensar en sus requerimientos funcionales ahora, pero básicamente necesito mostrar estas tres funciones:
   * Le indico papers o le meto .pdfs, y va funcionando como un mendeley o connected papers. Mostrará el grafo de los papers y, según las opciones, los papers que los que son referidos y los que refieren. 
   * Una interfaz de interacción con el server de MongoDB
   * Chance una visión general de todo. Lo más leve son las estadísticas descriptivas; lo más fuerte, un T-SNE o algo así.
   * Puede ser una demostración del sistema de recomendación frente a un conjunto de papers seleccionados, pero solo con las métricas cientométricas.
   * Como funcionalidad extra, dado que sería posible, agregar opción de exportar .bibtex lol.

En alguno de esos momentos ocurre que consigo una nueva laptop de la nada, le meto arch linux o algo, y lo hago un homeserver lol.
   * Hablando de eso, averiguar forma de acceso mediante red externa.
   * Probablemente tratar de agregar un firewall o DNS para que no sea tan malo (?).
Haciendo ese paso a paso, he caído en la realización de que estoy declarando a todos los frameworks de Apache como servers, pero puede que sea incorrecto. No sé, dudo con algunos en particular; es preciso corroborar terminología después. 

Si es que llegara a cumplir con el punto 9 y todos los papers fueron recuperados, tendría ya 60% del trabajo. Restaría:
   * Realizar más extracción de datos con NLP (minería de más data).
   * Chance extraer las tablas de los papers (minería de másañadir más data).
   * Si es factible, realizar eso del objetivo-método-resultado (minería de másañadir más data).
   * El anticipado, temido y magno (o probablemente, por mi miedo) entrenamiento y despliegue del modelo de deep learning (¿o reinforcement?) (Bueno, esto ya es procesamiento duro).
   * Adición de los indicadores de similaridad al sistema de recomendación y perfeccionar si tal.

La interfaz última e ideal, que era el sistema de recomendación, potencialmente se podría mostrar en la primera entrega lmao. Si realmente es posible calcular las métricas esas con lo que hay, luego agregar NLP será fácil.
SERÍA UNA LOCURA EN TODA LA PALABRA SI LO CONSIGUIERA. También lo veo del todo improbable xddd, pero a ver si puedo aprovechar la ansiedad.
Eso sí, Bisetti, no te vayas a descuidar con las evaluaciones de Big Data ni actúes en detrimento de tu salud. Siendo realistas es imposible, pero por algo eres ambicioso.

Recordemos que hasta el mayor problema de la esquizofrenia que te da al enfrentar proyectos es que pierdes noción del tiempo, las responsabilidades y los exámenes; por lo que terminas con un nivel de preparación muy bajo y muy cansado. A pesar de que probablemente sea lo más valioso para demostrar la aplicación de los conceptos aprendidos, el proyecto sigue siendo una nota ínfima. No pierdas de vista lo importante.

Hablando de esquizofrenia, ya empecé a hablar en primera persona lmao.

Este proyecto es demasiado ambicioso, probablemente de los más ambiciosos de mi vida. Ya me alejé de cosas puramente pytónicas, incluso yendo más lejos que las arquitecturas de Big Data. Estoy configurando todos los malditos requerimientos funcionales de esta huevada y su funcionamiento como un servicio web open source, lmao.

Ícaro, volaste muy cerca del sol y te quemaste. Tengo miedo que el profesor me saque la mierda por la complicación sjjdsjdsjd auxilio, porfa no lo hagas.
Lowkey si llegara al punto 9, podría justificar que todo lo mapeado es recontra lograble.

Yo creo que lo clave para desplegar ya toda la arquitectura es conseguir esa computadora extra. Ya ahí se hacen los experimentos y huevadas.
EL almacenamiento sigue siendo una incógnita y motivo de estrés.

¿Cómo habrá funcionado SciHub en sí? Valdría la pena mirar.
Donar de nuevo al Anna's Archive.
Indagar modelo de Solow aplicado a Latam.

Ahora sí, Bisetti, buenas noches. Realmente necesitaba sacarme todos pensamientos de encima para no explotar. LO que no esperaba era que pasara tantísimo tiempo xd, pero es que tengo demasiadas cosas que decir, al parecer.

Empecé a escribir acá a las 10pm y ahora son las 2am. Yo supuestamente estaba cansadazo por haber dormido nada y me iba a tirar. 13,700~ palabras hasta ahora, dios, el aire el laburo.

Bueno, en fin. Pucha, a saber si llegaré a conseguir todo; pero al menos ya he vomitado todo. Dios mío, ¿cómo uno llega a decir tantas cosas?

Buenas noches a mis pensamientos y a quien sea que, por cualquier causal, se ha topado con este devlog.

Para tu información, esto es un trabajo grupal que estoy haciendo solo de un curso de pregrado. Habla de ambición.
