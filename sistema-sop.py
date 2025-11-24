from abc import ABC, abstractmethod
from datetime import datetime

class Persona:
    def __init__(self, nombre, apellido, edad, id):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.id = id
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    def __str__(self):
        return f"{self.nombre_completo()} (ID: {self.id}, Edad: {self.edad})"

class Paciente(Persona):
    def __init__(self, nombre, apellido, edad, id, peso, altura, ciclo_regular, lh, fsh, testosterona, insulina):
        super().__init__(nombre, apellido, edad, id)
        self.peso = peso
        self.altura = altura
        self.ciclo_regular = ciclo_regular
        self.lh = lh
        self.fsh = fsh
        self.testosterona = testosterona
        self.insulina = insulina
        self.diagnostico = None
        self.fecha_diagnostico = None
    
    def calcular_imc(self):
        return self.peso / (self.altura ** 2)
    
    def calcular_ratio_lh_fsh(self):
        if self.fsh == 0:
            return 0
        return self.lh / self.fsh
    
    def asignar_diagnostico(self, resultado):
        self.diagnostico = resultado
        self.fecha_diagnostico = datetime.now()
    
    def __str__(self):
        base = super().__str__()
        imc = self.calcular_imc()
        ratio = self.calcular_ratio_lh_fsh()
        return (f"{base}\n"
                f"  IMC: {imc:.2f} | Ciclo regular: {'Si' if self.ciclo_regular else 'No'}\n"
                f"  LH/FSH: {ratio:.2f} | Testosterona: {self.testosterona:.2f} ng/dL | "
                f"Insulina: {self.insulina:.2f} µU/mL")


class Medico(Persona):
    def __init__(self, nombre, apellido, edad, id, especialidad, cedula):
        super().__init__(nombre, apellido, edad, id)
        self.especialidad = especialidad
        self.cedula = cedula
        self.pacientes_atendidos = []
    
    def diagnosticar(self, paciente, motor_diagnostico):
        resultado = motor_diagnostico.evaluar(paciente)
        paciente.asignar_diagnostico(resultado)
        self.pacientes_atendidos.append(paciente)
        return resultado
    
    def __str__(self):
        base = super().__str__()
        return f"{base}\n  Especialidad: {self.especialidad} | Cedula: {self.cedula}"


class ReglaDiagnostico(ABC):
    def __init__(self, nombre, peso=1.0):
        self.nombre = nombre
        self.peso = peso
    
    @abstractmethod
    def evaluar(self, paciente):
        pass


class ReglaIMC(ReglaDiagnostico):
    def __init__(self, peso=1.0):
        super().__init__("Regla IMC", peso)
    
    def evaluar(self, paciente):
        imc = paciente.calcular_imc()
        cumple = imc >= 25
        probabilidad = min(1.0, (imc - 18.5) / 20) if imc >= 18.5 else 0
        
        return {
            'cumple': cumple,
            'probabilidad': probabilidad,
            'detalles': f"IMC: {imc:.2f} ({'Alto riesgo' if cumple else 'Normal'})"
        }