# 🩺 Sistema de Prediagnóstico de Síndrome de Ovario Poliquístico (SOP)

Este proyecto implementa un **sistema interactivo de prediagnóstico de SOP (Síndrome de Ovario Poliquístico)** usando **Programación Orientada a Objetos** en Python.  
Incluye herencia, polimorfismo, clases abstractas y estrategias de combinación de reglas de evaluación.

---

## 📌 Descripción general

El sistema permite:

- Registrar pacientes con información clínica y hormonal.
- Calcular automáticamente indicadores relevantes como:
  - IMC
  - Razón LH/FSH
- Aplicar reglas diagnósticas mediante polimorfismo:
  - Regla IMC  
  - Regla Hormonal  
  - Regla Ciclo Menstrual  
- Combinar estas reglas usando diferentes estrategias:
  - **Promedio Ponderado**
  - **Bayes Simple**
- Generar un diagnóstico preliminar con:
  - Probabilidad estimada de SOP  
  - Nivel de riesgo  
  - Explicación detallada de los criterios evaluados

El programa opera mediante un **menú interactivo en consola**.

---

## 🧬 Conceptos de POO aplicados

Este proyecto demuestra de forma práctica los pilares de la Programación Orientada a Objetos:

### **Herencia**
- `Persona`
- `Paciente`
- `Medico`

### **Polimorfismo**
- Reglas de diagnóstico:
  - `ReglaIMC`
  - `ReglaHormonal`
  - `ReglaCiclo`
- Estrategias de combinación:
  - `PromedioPonderado`
  - `BayesSimple`

### **Clases abstractas**
- `ReglaDiagnostico`
- `EstrategiaCombinacion`

### **Composición**
- `MotorDiagnostico` utiliza internamente una regla compuesta.

---


## 📦 Requisitos
Este proyecto no necesita librerías adicionales.
Utiliza únicamente módulos estándar de Python:

abc

datetime

## 👩‍💻 Autoras

Nombres: 
- Iris Alina Pérez Rivera
- Fernanda Garcia Rodriguez
- Diana García Trujillo
- Karol Paola Rosales Miranda

Materia: 
- Programación Orientada a Objetos
  
Profesor:
- GUADALUPE JEANETTE GONZALEZ DIAZ

---

## ▶️ Cómo ejecutar el programa

Asegúrate de tener **Python 3** instalado.

Ejecuta el archivo principal:

```bash
python sistema-sop.py
