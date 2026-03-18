Problema: Al tener 50 usuarios intentando reservar 10 cursos simultáneamente, ocurre una "condición de carrera". Varios hilos leen que queda 1 cupo antes de que el anterior lo descuente, resultando en sobreventa (cupos negativos).

Solución con Lock: Se utiliza un objeto Lock de Python para que la verificación y la resta sean una operación atómica. Esto garantiza que nunca se exceda el límite de 10.

Solución con Semáforo: Se implementa un Semaphore(3) para controlar el flujo, permitiendo que el servidor procese un máximo de 3 solicitudes en paralelo, optimizando el uso de recursos sin perder la integridad de los datos.

Resultados:

 * Sin Lock: Cupos finales inconsistentes, en mi caso -20.

 * Con Lock/Semáforo: Cupos finales siempre 0 todo trabajaba mejor.
