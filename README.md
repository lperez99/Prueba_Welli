# Prueba_Welli

## Instrucciones rápidas para ejecutar el proyecto

1. **Clona el repositorio:**
   ```sh
   git clone <URL_DEL_REPOSITORIO>
   cd Prueba_Welli
   ```

2. **Dale permisos de ejecución al script de inicio (solo la primera vez):**
   ```sh
   chmod +x start.sh
   ```

3. **Ejecuta el proyecto (esto instalará dependencias, poblará la base de datos y levantará el servidor):**
   ```sh
   ./start.sh
   ```

Esto instalará automáticamente los requirements, ejecutará el script para poblar la base de datos (`run.py`) y levantará el servidor FastAPI en modo desarrollo.

---

## Job automático de multas por préstamos atrasados

Este proyecto incluye un **job automático** que revisa diariamente todos los préstamos activos y aplica multas a los usuarios por días de retraso:

- **Primeros 30 días de retraso:** $2.000 por día.
- **A partir del día 31:** $4.000 por día.
- El sistema lleva el control de los días ya multados, por lo que **no se cobra dos veces la misma multa** aunque el job se ejecute todos los días.

### ¿Cómo funciona?

- El job revisa todos los préstamos activos cuyo `end_date` ya pasó.
- Calcula los días de retraso y aplica la multa correspondiente solo por los días nuevos de retraso.
- Suma la multa al campo `fines` del usuario.
- Actualiza el campo `days_fined` en el préstamo para llevar el control.

### ¿Cómo ejecutarlo manualmente?

Desde la raíz del proyecto, ejecuta:

```sh
python3 -m app.cronjobs.pending_transactions
```

Esto ejecutará el job una vez y mostrará en consola las multas aplicadas.

### ¿Cómo programar la ejecución automática?

El archivo `app/cronjobs/pending_transactions.py` está configurado para ejecutarse automáticamente todos los días a la 1:00 AM usando la librería `schedule`.  
Puedes dejarlo corriendo en segundo plano con:

```sh
python3 -m app.cronjobs.pending_transactions
```

o programar su ejecución diaria usando herramientas como **cron** en tu servidor.
