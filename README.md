# Trabajo de Técnicas en Aprendizaje Estadístico de la UNAL-med 

## A cargo de:

- Esteban García Carmona
- Emilio Porras Mejía
- Felipe Miranda Arboleda
- Jose Luis Suarez Ledesma

Trabajamos con la base de datos College Scoreboard, buscando analizarla y crear una solución basada en la información que esta dispone. Nuestro objetivo era crear un producto de datos de utilidad.

Utilizamos las siguientes variables:
- DEP_INC_AVG = Salario promedio de la familia de estudiantes dependientes (valores monetarios del 2014).
- IND_INC_AVG = Salario promedio de la familia de estudiantes independientes (valores monetarios del 2014).
- UNITID = Identificador único de la institución Universitaria.
- INSTNM = Nombre del instituto.
- LATITUDE = latitud (relativa a la localización geográfica de la sede).
- LONGITUDE = longitud (relativa a la localización geográfica de la sede).
- GRAD_DEBT_MDN = la media de la deuda de los estudiantes que completan sus estudios.
- CONTROL = Identificador de la estructura de gobierno de la institución. 0: Pública. 1: Privada sin ánimo de lucro. 2: Privada con ánimo de lucro. 

Con esto, buscamos analizar las universidades según el riesgo que representan para un estudiante y la consecuente deuda con la que terminarán para poder pagar sus estudios universitarios. 

Hicimos el siguiente procedimiento:
1. Obtuvimos y montamos la base de datos College Scoreboard de la página [data.world](https://data.world/exercises/cluster-analysis-exercise-2).
2. Reemplazamos los espacios vacíos por nulos. Con esto, removimos todas las columnas en las que TODOS los datos fueran nulos. Inicialmente, la base de datos tenía 7804 filas (universidades) y 1725 columnas (dato específico referente a las universidades). Después de este proceso, quedamos con 551 columnas. 
3. Se utilizó el método de la correlación y revisión manual para seguir descartando columnas. Tras esto, terminamos con 45 columnas.A
4. Se decidió trabajar con datos financieros. Se descartaron múltiples variables como, por ejemplo, el puntaje promedio del SAT, dado que tenía grandes cantidades de valores nulos. También se debe de tener en cuenta que muchos datos fueron suprimidos por privacidad, por lo que estos valores, al no poder observarse, también se reemplazaron por nulos.
5. Se eligieron las variables que se describieron más arriba, con estas trabajamos para llegar a nuestro producto de datos.