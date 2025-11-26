## 🩺 Sistema de Prediagnóstico de Síndrome de Ovario Poliquístico (SOP)

Este proyecto implementa un **sistema interactivo de prediagnóstico de SOP (Síndrome de Ovario Poliquístico)** usando **Programación Orientada a Objetos** en Python.  
Incluye herencia, polimorfismo, clases abstractas y estrategias de combinación de reglas de evaluación.

---

## Descripción del Problema

Uno de los trastornos endocrinos más comunes entre las mujeres en edad fértil es el Síndrome de Ovario Poliquístico (SOP).  Aunque su prevalencia es alta, no es fácil diagnosticarla.  Las pacientes no muestran un único patrón clínico, en cambio, presentan una mezcla variable de trastornos hormonales, desbalances metabólicos, ciclos menstruales irregulares, cambios de peso y resistencia a la insulina, así como hiperandrogenismo, entre otros.  Esto quiere decir que no hay un solo indicador que pueda, por sí mismo, confirmar o descartar la enfermedad.

En situaciones donde no se cuenta con estudios especializados o con un monitoreo clínico constante, la complejidad aumenta.  El tiempo requerido para procesar análisis, cotejar criterios médicos y evaluar cómo evolucionan los síntomas hace que muchos diagnósticos se retrasen durante años o meses.  Por lo tanto, miles de mujeres sufren efectos que se podrían haber prevenido con una detección temprana: diabetes tipo 2, resistencia grave a la insulina, infertilidad, deterioro en la calidad de vida y riesgos cardiovasculares.

Dada esta situación, es necesario contar con un sistema que facilite el proceso de detección temprana a través de un análisis completo, que combine diferentes criterios hormonales y clínicos para calcular el riesgo probable de SOP.  No pretende reemplazar al médico, sino actuar como soporte para acelerar la interpretación de indicadores, simplificar la toma de decisiones y fomentar un seguimiento más accesible y organizado.  Este proyecto proporciona una base firme para experimentación, ampliación futura, integración con conjuntos de datos reales y aplicación en contextos educativos y clínicos. Se ha desarrollado utilizando un modelo programado en Python y Programación Orientada a Objetos.

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
