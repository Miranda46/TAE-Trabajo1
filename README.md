# Universingreso: Trabajo de Técnicas en Aprendizaje Estadístico de la UNAL-med 

## A cargo de:

- Esteban García Carmona
- Emilio Porras Mejía
- Felipe Miranda Arboleda
- José Luis Suárez Ledesma

## Introducción
Trabajamos con la base de datos College Scoreboard, la cual expone datos importantes de la universidades estadounidenses indicando costos, deudas, ingresos, número de egresados, entre otros. Se conoce que hay muchas razones por las cuales los estudiantes desertan sus estudios universitarios. Una de las principales es la inestabilidad económica y la presión que generan las deudas sobre cada individuo. Por esto, en vez de segregar universidades por su calidad académica o por gusto individual y pasión al arte, buscamos generar un medio para ayudar a descartar opciones que no sean viables para un estudiante con base en sus capacidades económicas. Se sabe que en EEUU el dinero genera estatus, por lo que muchos se hacen a la idea de que _deben_ ir a la universidad más cara en la medida de lo posible. Sin embargo, es justamente esta mentalidad la que termina afectándolos. El hecho de terminar los estudios inside en sí lo suficiente, aumentando salarios en \$17500 USD (entre _Millennials_ de 25-32 años) y disminuyendo valiosamente la tasa de desempleo (3.8% vs. 12.2%) [1].

## Objetivo
Buscamos agrupar las universidades según el riesgo económico que representan para un estudiante y la consecuente deuda con la que terminarán para poder pagar sus estudios universitarios. Estas decisiones afectarán tanto el futuro profesional como económico del estudiante. El producto de datos está dirigido a los aspirantes y estudiantes dependientes o independientes que buscan seleccionar (o descartar) universidades según sus capacidades económicas, de tal manera que puedan asegurar una estabilidad económica hacia el futuro sin recaer en grandes deudas que, por lo general, toman décadas en poderse pagar y afectan, especialmente, a estudiantes independientes y/o de bajos recursos.

## Variables
Utilizamos las siguientes columnas:

| Columna       | Descripción | Unidad |
| ------------- |-------------- | ------------- |
| DEP_INC_AVG   | Salario promedio de la familia de estudiantes dependientes (valores monetarios del 2014).   | USD |
| IND_INC_AVG   | Salario promedio de la familia de estudiantes independientes (valores monetarios del 2014). | USD |
| UNITID        | Identificador único de la institución Universitaria.   | --- |
| INSTNM        | Nombre del instituto. | --- |
| LATITUDE      | latitud (relativa a la localización geográfica de la sede).    | Grados sexagesimales |
| LONGITUDE     | longitud (relativa a la localización geográfica de la sede).  | Grados sexagesimales |
| GRAD_DEBT_MDN | la media de la deuda de los estudiantes que completan sus estudios. | USD |
| CONTROL       | Identificador de la estructura de gobierno de la institución. 0: Pública. 1: Privada sin ánimo de lucro. 2: Privada con ánimo de lucro.     | --- |

**Tabla 1:** *Columnas utilizadas.*

\
La selección de variables que se observa en la *Tabla 1* se hizo a partir de los salarios actuales del estudiante o su familia, teniendo en cuenta si este es dependiente en los ingresos familiares. Se conoce que un estudiantes independiente no tendrá la misma fluidez financiera que un estudiante dependiente, dado que, este primero debe costearse su comida, vivienda y estudios. Para ver cómo influyen estos datos al finalizar los estudios universitarios se utiliza la media de la deuda de los estudiantes que completan sus estudios.  Se usan los datos de las universidades para ubicarlos geográficamente en el mapa y enunciarlos según su nombre, de manera que cada quien pueda ubicar y seleccionar universidades cerca de su área. También se desea ver transversalmente si la estructura de gobierno de la institución afecta en el endeudamiento. Se podría pensar que las universidades públicas son más baratas y afectan menos financieramente a sus estudiantes. 

Demás decisiones de la elección de las columnas se pueden observar a continuación en el procedimiento. 

## Procedimiento
Hicimos el siguiente procedimiento:
1. Obtuvimos y montamos la base de datos College Scoreboard de la página [data.world](https://data.world/exercises/cluster-analysis-exercise-2).
2. Reemplazamos los espacios vacíos por nulos. Con esto, removimos todas las columnas en las que TODOS los datos fueran nulos. Inicialmente, la base de datos tenía 7804 filas (universidades) y 1725 columnas (dato específico referente a las universidades). Después de este proceso, quedamos con 551 columnas.
3. Se utilizó revisión manual para seguir descartando columnas. Tras esto, terminamos con 45 columnas.
4. Se decidió trabajar con datos financieros. Se descartaron múltiples variables como, por ejemplo, el puntaje promedio del SAT, dado que tenía grandes cantidades de valores nulos. También se debe de tener en cuenta que muchos datos fueron suprimidos por privacidad, por lo que estos valores, al no poder observarse, también se reemplazaron por nulos.
5. Se eligieron las variables que se describieron más arriba, con estas trabajamos para llegar a nuestro producto de datos. Son 8 columnas relacionadas con las universidades y las deudas que le dejan a los estudiantes.
6. Las variables "DEP_INC_AVG", "IND_INC_AVG" y "GRAD_DEBT_MDN" se convierten, debidamente, a tipo flotante, para poderle hacer un análisis.
7. Posteriormente, se descartaron las universidades a las que les hiciera falta por lo menos un valor de las columnas descritas anteriormente. Con esto, terminamos con 5703 filas.
8. Se separa en dos DataFrames los datos. Se utiliza el código (UNITID). El primer Dataframe (dfFinal) guarda los datos de las variables financieras continuas, es decir, los ingresos y las deudas y también guarda el dato del tipo de gobierno en la institución académica. En el segundo Dataframe (dfUbicacion), se guardan los datos relacionados con la ubicación y el nombre de la institución.
9. Se normalizan las 3 columnas continuas utilizando el método de MinMax y se prosigue con el análisis.
10. Se efectúa el análisis del codo para decidir el número de clusters a utilizar utilizando KMeans.

# Curva de codo
<img src="/Graficas/codo.png" alt="Análisis Codo" title="Análisis Codo">

**Imagen 1:** *Análisis de curva de codo.*

\
11. Con base en la curva de codo, observada en la *Imagen 1*, se determina el uso de 3 clusters. Con esto, se trabajará con las etiquetas 1, 2 y 3, que representarán cada uno de los clusters. 
12. Se procede con el análisis de los diferentes clústers. Se observa lo siguiente en la *Imagen 2*:

## Visualización de los clusters
![Clusters](https://github.com/Miranda46/TAE-Trabajo1/blob/main/Graficas/clusters.png "Clusters")

**Imagen 2:** *Visualización 3D de los clusters.*

\
Los color Cian representan el cluster 1; los naranja, el cluster 2; los verdes, el cluster 3. 
A continuación, se enuncia la caracterización de cada clúster según sus características. 

# Caracterización

## Cluster 1
- Es el cluster con mayor cantidad de universidades, con un total de 3174 universidades.
- Se caracteriza por tener las deudas más bajas, donde la media de la deuda se encuentra en \$10 201 USD y el 75% de los estudiantes tienen una deuda menor a \$12 000 USD. 
- El salario promedio de los estudiantes dependientes es de \$39 530 USD y de \$17 255 USD en independientes. Estos salarios son similares a los del cluster 3 y menores a los del cluster 2.

## Cluster 2
- Tiene 1409 universidades.
- Se destacan los salarios altos, con una media de \$80 211 USD, donde tan solo el 25\% de los estudiantes gana menos de \$68 000 USD en estudiantes dependientes, y con una media de \$27 233 USD en estudiantes independientes. 
- Se caracteriza por tener una gran cantidad de universidades privadas sin ánimo de lucro. Tiene 868 de 1301 universidades con esta estructura de gobierno de la institución, es decir, un 67%.

## Cluster 3
- Tiene 1120 universidades, lo que lo hace el cluster más pequeño.
- Como se puede observar en la *Imagen 2* y los datos, el cluster es semejante al cluster 1 pero las deudas son, en general, más altas. Véase que los salarios son más bajos que en cluster 2, con una media de \$40 701 USD en estudiantes dependientes y \$19 174 USD en estudiantes dependientes. Sin embargo, la deuda haciende a una media de \$26 499 USD, más alta que la de los estudiantes del cluster 2, que es, en promedio, de \$23 251 USD.
- El 75% de los estudiantes tiene una deuda superior a \$21 599.0 USD que es mayor a la deuda máxima entre los estudiantes de las universidades del cluster 2, que es de \$18 833 USD. 

Veamos los datos en gráficas:
<img src="/Graficas/deuda_mediana.png" alt="deuda mediana en los 3 clusters" title="Deuda mediana">

**Imagen 3:** *Deuda mediana de los 3 clusters.*

\
Se pueden observar en la *Imagen 3* deudas monetarias especialmente altas en el tercer cluster, es decir, en el de la derecha en la imagen. 
<img src="/Graficas/salario_dependientes.png" alt="salario de estudiantes dependientes en los 3 clusters" title="Deuda mediana">

**Imagen 4:** *Salario estudiantes dependientes de los 3 clusters.*

\
Según la *Imagen 4*, entre universidades con datos de estudiantes dependientes, se ven salarios similares en el cluster 1 y 3, el cluster 2 pueden observarse salarios más altos. 
<img src="/Graficas/salario_independientes.png" alt="salario de estudiantes independientes en los 3 clusters" title="Deuda mediana">

**Imagen 5:** *Salario estudiantes independientes de los 3 clusters.*


# Mapa
| Cluster | Color |
| --- | --- |
| 1 | Rojo |
| 2 | Verde |
| 3 | Azul | 

**Tabla 2:** *Clusters y sus respectivos colores en el mapa.*

\
Con la *Tabla 2* podemos identificar cada clúster en la siguiente imagen:

\
<img src="/Graficas/mapa_clusters.png" alt="mapa de los 3 clusters" title="Mapa USA">

**Imagen 6:** *Mapa de representación de los 3 clusters con sus respectivos colores.*

\
Se puede observar con ayuda de la *Imagen 6* que en cualquier sitio de EEUU se puede acceder a universidades de cualquier tipo de los clústers. 

# Conclusiones
+ Las universidades pertenecientes al cluster 1 representan la mejor opción para el ciudadano independiente o de bajos ingresos. La falta de capital puede llevar a la deserción y son justamente estos estudiantes los que mayor deuda se imponen. Sin embargo, terminar un "Associate Degree" o "Bachelor's Degree" puede implicar un aumento de más del 100% del salario [2]. Estar en la capacidad de poder estudiar y, además, no quedar con una deuda que perdurará más de 20 años [3] y tomará decenas de miles de dólares del bolsillo es un lujo [4]. 
+ En el cluster 2 hallamos universidades que se recomiendan principalmente para ciudadanos estadounidenses con mayor capacidad adquisitiva. Nótese que sus deudas llegan a ser relativamente altas a pesar de tener salarios mayores. Esto muestra que muchas de estas familias prefieren invertir mayores cantidades de dinero en el estudio. 
+ Se conoce que el la deuda promedio por préstamos para estudios Universitarios en Estados Unidos es de \$32 731 [3] y entre las universidades analizadas, de \$16 626. Esto puede afectar gravemente su puntaje crediticio. En un país donde reina la individualidad y las personas buscan emanciparse rápidamente, esto puede representar un peligro en cuanto a la posterior obtención de vivienda. 

# Propuesta para Colombia

Para poder desarrollar un análisis similar en Colombia, primero se requiere obtener la información económica en cuanto a los préstamos del ICETEX y préstamos a través de entidades privadas. Estos datos se deben discretizar por universidad, estructura de gobierno de la institución académica e independencia económica del estudiante, además de tener la ubicación geográfica de cada universidad. Cade destacar que estos datos económicos (Deuda luego de graduarse, salario de estudiante independiente, y salario de familia de estudiante pendendiente) pueden no estar disponibles, o no estar agrupados por universidad o colegios para el público en Colombia. Por último, se conoce que las universidades públicas y privadas de Colombia funcionan de manera diferente que en Estados Unidos. 

# Página web
Los invitamos cordialmente a visitar nuestra página [Universingreso](https://miranda46-tae-trabajo1-tae-streamlit-8b4qee.streamlitapp.com/) para que puedan analizar qué clase de universidad les beneficia según sus capacidades económicas.
¡Gracias!
# Referencias

[1] "Pew Research Center" (2014, Febrero 11). The Rising Cost of Not Going to College [Online]. Available: https://www.pewresearch.org/social-trends/2014/02/11/the-rising-cost-of-not-going-to-college/

[2] T. Stobierski (2020, Junio 2). 2022 Student Loan Statistics: Impact Of Student Debt On Job Market [Online]. Available: https://www.northeastern.edu/bachelors-completion/news/average-salary-by-education-level/ 

[3] K. Morris (2022, Junio 27). Average Salary by Education Level [Online]. Available: https://www.zippia.com/advice/student-loan-statistics/ 

[4] B. McGurran, A. Hahn (2022, Marzo 9). Average Student Loan Payment: Estimate How Much You’ll Owe [Online]. Available: https://www.forbes.com/advisor/student-loans/average-student-loan-payment/ 

Todas las imágenes y las tablas son de propia autoría. 
# Lecturas Recomendadas relacionadas

"National Center for Education Statistics" (2022, Mayo). Annual Earnings by Educational Attainment [Online]. Available: https://nces.ed.gov/programs/coe/indicator/cba 

Johnstone, Bruce. (2006). Financiación de la educación superior en Estados Unidos: cuestiones actuales  [Online]. Available: http://hdl.handle.net/2099/7264

Gutter, M., Copur, Z. (2011, April). Financial Behaviors and Financial Well-Being of College Students: Evidence from a National Survey [Online]. Available: https://doi.org/10.1007/s10834-011-9255-2
