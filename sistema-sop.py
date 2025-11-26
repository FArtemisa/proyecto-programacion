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

class ReglaHormonal(ReglaDiagnostico):
    def __init__(self, peso=1.5):
        super().__init__("Regla Hormonal", peso)
    
    def evaluar(self, paciente):
        ratio_lh_fsh = paciente.calcular_ratio_lh_fsh()
        
        puntos = 0
        if ratio_lh_fsh > 2:
            puntos += 1
        if paciente.testosterona > 50:
            puntos += 1
        if paciente.insulina > 20:
            puntos += 1
        
        cumple = puntos >= 2
        probabilidad = puntos / 3
        
        return {
            'cumple': cumple,
            'probabilidad': probabilidad,
            'detalles': (f"LH/FSH: {ratio_lh_fsh:.2f}, Testosterona: {paciente.testosterona:.2f} ng/dL, "
                        f"Insulina: {paciente.insulina:.2f} µU/mL ({puntos}/3 criterios)")
        }


class ReglaCiclo(ReglaDiagnostico):
    def __init__(self, peso=1.2):
        super().__init__("Regla Ciclo Menstrual", peso)
    
    def evaluar(self, paciente):
        cumple = not paciente.ciclo_regular
        probabilidad = 0.8 if cumple else 0.2
        
        return {
            'cumple': cumple,
            'probabilidad': probabilidad,
            'detalles': f"Ciclo {'irregular (riesgo)' if cumple else 'regular (normal)'}"
        }


class EstrategiaCombinacion(ABC):
    @abstractmethod
    def combinar(self, resultados, pesos):
        pass


class PromedioPonderado(EstrategiaCombinacion):
    def combinar(self, resultados, pesos):
        if not resultados:
            return 0.0
        
        suma_ponderada = sum(r['probabilidad'] * p for r, p in zip(resultados, pesos))
        suma_pesos = sum(pesos)
        
        return suma_ponderada / suma_pesos if suma_pesos > 0 else 0.0


class BayesSimple(EstrategiaCombinacion):
    def combinar(self, resultados, pesos):
        if not resultados:
            return 0.0
        
        suma_pesos = sum(pesos)
        probabilidad_no_sop = 1.0
        
        for resultado, peso in zip(resultados, pesos):
            peso_norm = peso / suma_pesos if suma_pesos > 0 else 0
            probabilidad_no_sop *= (1 - resultado['probabilidad'] * peso_norm)
        
        return 1 - probabilidad_no_sop


class ReglaCompuesta(ReglaDiagnostico):
    def __init__(self, reglas, estrategia, nombre="Regla Compuesta"):
        super().__init__(nombre, peso=1.0)
        self.reglas = reglas
        self.estrategia = estrategia
    
    def evaluar(self, paciente):
        resultados = [regla.evaluar(paciente) for regla in self.reglas]
        pesos = [regla.peso for regla in self.reglas]
        
        probabilidad_final = self.estrategia.combinar(resultados, pesos)
        cumple = probabilidad_final >= 0.5
        
        detalles = "\n    ".join([f"- {r['detalles']}" for r in resultados])
        
        return {
            'cumple': cumple,
            'probabilidad': probabilidad_final,
            'detalles': f"Combinacion de {len(self.reglas)} reglas:\n    {detalles}",
            'resultados_individuales': resultados
        }

class MotorDiagnostico:
    def __init__(self, regla_principal):
        self.regla_principal = regla_principal
    
    def evaluar(self, paciente):
        resultado = self.regla_principal.evaluar(paciente)
        
        diagnostico = {
            'paciente': paciente.nombre_completo(),
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'tiene_sop': resultado['cumple'],
            'probabilidad': resultado['probabilidad'],
            'detalles': resultado['detalles'],
            'nivel_riesgo': self._clasificar_riesgo(resultado['probabilidad'])
        }
        
        return diagnostico
    
    def _clasificar_riesgo(self, probabilidad):
        if probabilidad >= 0.7:
            return "ALTO"
        elif probabilidad >= 0.4:
            return "MEDIO"
        else:
            return "BAJO"

# Menu del sistema
class MenuSistema:
    def __init__(self):
        reglas = [
            ReglaIMC(peso=1.0),
            ReglaHormonal(peso=1.5),
            ReglaCiclo(peso=1.2)
        ]
        estrategia = PromedioPonderado()
        regla_compuesta = ReglaCompuesta(reglas, estrategia, "Diagnostico SOP Completo")
        
        self.motor = MotorDiagnostico(regla_compuesta)
        self.medico = Medico("Dr. Juan", "Perez", 45, "MED001", "Ginecologia", "12345678")
        self.pacientes_registrados = []
    
    def mostrar_menu(self):
        print("SISTEMA DE PREDIAGNOSTICO DE SOP (Sindrome de Ovario Poliquistico)")
        print("\n1. Registrar paciente manualmente")
        print("2. Realizar diagnostico")
        print("3. Ver pacientes registrados")
        print("4. Cambiar estrategia de combinacion")
        print("5. Salir")
    
    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("\nSeleccione una opcion: ").strip()
            
            if opcion == "1":
                self.registrar_paciente_manual()
            elif opcion == "2":
                self.realizar_diagnostico()
            elif opcion == "3":
                self.ver_pacientes()
            elif opcion == "4":
                self.cambiar_estrategia()
            elif opcion == "5":
                print("\nGracias por usar el sistema. Hasta pronto.\n")
                break
            else:
                print("\nOpcion no valida. Intente de nuevo.")
    
    def registrar_paciente_manual(self):
        print("\n--- REGISTRO MANUAL DE PACIENTE ---")
        try:
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            edad = int(input("Edad: "))
            id = input("id: ").strip()
            peso = float(input("Peso (kg): "))
            altura = float(input("Altura (m): "))
            ciclo = input("Ciclo menstrual regular? (s/n): ").strip().lower() == 's'
            lh = float(input("Nivel LH (mIU/mL): "))
            fsh = float(input("Nivel FSH (mIU/mL): "))
            testosterona = float(input("Testosterona (ng/dL): "))
            insulina = float(input("Insulina (µU/mL): "))
            
            paciente = Paciente(nombre, apellido, edad, id,
                              peso, altura, ciclo, lh, fsh, testosterona, insulina)
            self.pacientes_registrados.append(paciente)
            
            print(f"\nPaciente {paciente.nombre_completo()} registrado exitosamente.")
        except ValueError:
            print("\nError: Datos invalidos. Intente de nuevo.")
    
    def realizar_diagnostico(self):
        if not self.pacientes_registrados:
            print("\nNo hay pacientes registrados. Registre uno primero.")
            return
        
        print("\n--- PACIENTES DISPONIBLES ---")
        for i, p in enumerate(self.pacientes_registrados, 1):
            print(f"{i}. {p.nombre_completo()} (ID: {p.id})")
        
        try:
            seleccion = int(input("\nSeleccione numero de paciente: ")) - 1
            paciente = self.pacientes_registrados[seleccion]
            
            print(f"\nRealizando diagnostico para {paciente.nombre_completo()}...")
            resultado = self.medico.diagnosticar(paciente, self.motor)
            
            print("\n" + "="*60)
            print("  RESULTADO DEL DIAGNOSTICO")
            print("="*60)
            print(f"Paciente: {resultado['paciente']}")
            print(f"Fecha: {resultado['fecha']}")
            print(f"Diagnostico: {'SOP DETECTADO' if resultado['tiene_sop'] else 'NO SE DETECTO SOP'}")
            print(f"Probabilidad: {resultado['probabilidad']*100:.1f}%")
            print(f"Nivel de riesgo: {resultado['nivel_riesgo']}")
            print(f"\nDetalles:\n{resultado['detalles']}")
            print("="*60)
            
        except (ValueError, IndexError):
            print("\nSeleccion invalida.")
    
    def ver_pacientes(self):
        if not self.pacientes_registrados:
            print("\nNo hay pacientes registrados.")
            return
        
        print("\n--- PACIENTES REGISTRADOS ---")
        for i, p in enumerate(self.pacientes_registrados, 1):
            print(f"\n{i}. {p}")
            if p.diagnostico:
                print(f"   Diagnostico: {'SOP' if p.diagnostico['tiene_sop'] else 'No SOP'} "
                      f"(Prob: {p.diagnostico['probabilidad']*100:.1f}%)")
    
    def cambiar_estrategia(self):
        print("\n--- ESTRATEGIAS DISPONIBLES ---")
        print("1. Promedio Ponderado")
        print("2. Bayes Simple")
        
        opcion = input("\nSeleccione estrategia: ").strip()
        
        reglas = [
            ReglaIMC(peso=1.0),
            ReglaHormonal(peso=1.5),
            ReglaCiclo(peso=1.2)
        ]
        
        if opcion == "1":
            estrategia = PromedioPonderado()
            nombre = "Promedio Ponderado"
        elif opcion == "2":
            estrategia = BayesSimple()
            nombre = "Bayes Simple"
        else:
            print("\nOpcion no valida.")
            return
        
        regla_compuesta = ReglaCompuesta(reglas, estrategia, f"Diagnostico SOP ({nombre})")
        self.motor = MotorDiagnostico(regla_compuesta)
        
        print(f"\nEstrategia cambiada a: {nombre}")


def main():
    menu = MenuSistema()
    menu.ejecutar()


if __name__ == "__main__":
    main()
