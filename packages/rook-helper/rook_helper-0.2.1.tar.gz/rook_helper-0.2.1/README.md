# 📌 Proyecto: README

## 📖 Tabla de Contenidos
1. [Instrucciones para probar](#instrucciones-para-probar)
2. [Pruebas y análisis](#pruebas-y-análisis)
3. [Compilación y distribución](#compilación-y-distribución)
4. [Uso del paquete](#uso-del-paquete)
5. [Paquetes habilitados](#paquetes-habilitados)

---

## 🚀 Instrucciones para probar

### 🔹 Clonar el repositorio
```bash
# Clona el repositorio desde GitHub
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
```

### 🔹 Instalar dependencias
```bash
pip install -r requirements-dev.txt
```

---

## 🛠 Pruebas y análisis

### 🧪 Ejecutar pruebas
```bash
# Ejecuta todos los tests
python -m unittest discover

# Ejecuta un test específico
python -m unittest directory/test.py -k test_function
```

### ✅ Ejecutar el linter
```bash
tox -e lint
```

### 📊 Ejecutar test coverage
```bash
tox -e coverage
```

### 🔄 Ejecutar todas las pruebas y análisis
```bash
tox
```

### 🔍 Análisis de vulnerabilidades
```bash
tox -e security
```

---

## 📦 Compilación y distribución

### 🔹 Compilar el paquete
```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

### 🔹 Probar el paquete localmente
```bash
pip install -e .
```

---

## 📌 Uso del paquete

### 📂 Ruta para crear un JSON de un documento de un pilar
```python
from rook_helper.structure.body_health.blood_glucose_event import build_json
```

#### Ejemplo:
```python
from rook_helper.structure.pillar.data_structure import build_json
```

### 🛠 Ruta de un helper
```python
from rook_helper import package general
```

#### Ejemplo:
```python
from rook_helper import convert_to_type
```

### 🛠 Ruta para obtener el formato de la data granular
```python
from rook_helper.structure import GranularData

granular_data = GranularData.blood_glucose_granular_data(data, 'variable de extracción')

```

---

## 📚 Paquetes habilitados

### 🔹 Helpers generales
- `remove_client_uuid_from_user_id`
- `format_datetime`
- `convert_to_type`

### 🔹 Helpers de estructura

#### 🏥 Body Health
- `blood_glucose_event`
- `blood_pressure_event`
- `body_metrics_event`
- `heart_rate_event`
- `hydration_event`
- `menstruation_event`
- `mood_event`
- `nutrition_event`
- `oxygenation_event`
- `temperature_event`
- `summary`

#### 🏃 Physical Health
- `calories_event`
- `heart_rate_event`
- `oxygenation_event`
- `steps_event`
- `stress_event`
- `activity_event`
- `summary`

#### 🌙 Sleep Health
- `summary`

#### 👤 User Information
- `information`

#### 👤 Granular Data
- `activity_granular_data`
- `blood_glucose_granular_data`
- `blood_pressure_granular_data`
- `breathing_granular_data`
- `elevation_granular_data`
- `floors_climbed_granular_data`
- `menstruation_granular_data`
- `heart_rate_granular_data`
- `hydration_granular_data`
- `mood_granular_data`
- `temperature_granular_data`
- `saturation_granular_data`
- `snoring_granular_data`
- `steps_granular_data`
- `active_steps_granular_data`
- `stress_granular_data`
- `swimming_granular_data`
- `traveled_granular_data`
- `tss_granular_data`
- `vo2_granular_data`
- `cadence_granular_data`
- `lap_granular_data`
- `speed_granular_data`
- `torque_granular_data`
- `velocity_granular_data`
- `power_granular_data`
- `position_granular_data`