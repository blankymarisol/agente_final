import json
import os
import platform
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from ia_assistant import RecomendadorIA

class AsistenteAprendizaje:
    def __init__(self):
        self.archivo_datos = "data/usuarios.json"
        self.crear_carpeta_datos()
        self.datos = self.cargar_datos()
        self.logros_disponibles = self.init_logros()
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        sistema = platform.system()
        if sistema == "Windows":
            os.system('cls')
        else:
            os.system('clear')
    
    def crear_carpeta_datos(self):
        if not os.path.exists("data"):
            os.makedirs("data")
            print("📁 Carpeta 'data' creada")
    
    def cargar_datos(self):
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    # Asegurar que existan todas las claves necesarias
                    if "puntos" not in datos:
                        datos["puntos"] = {}
                    if "logros" not in datos:
                        datos["logros"] = {}
                    if "rachas" not in datos:
                        datos["rachas"] = {}
                    return datos
            except:
                print("⚠️ Error al cargar datos, creando archivo nuevo")
                return self.datos_vacios()
        return self.datos_vacios()
    
    def datos_vacios(self):
        return {
            "usuarios": {},
            "planes": {},
            "sesiones": [],
            "puntos": {},
            "logros": {},
            "rachas": {}
        }
    
    def init_logros(self):
        return {
            "primer_dia": {"nombre": "🌱 Primer Paso", "descripcion": "Completar primera sesión", "puntos": 10},
            "racha_3": {"nombre": "🔥 En Racha", "descripcion": "3 días consecutivos", "puntos": 25},
            "racha_7": {"nombre": "⚡ Imparable", "descripcion": "7 días consecutivos", "puntos": 50},
            "racha_30": {"nombre": "👑 Leyenda", "descripcion": "30 días consecutivos", "puntos": 200},
            "madrugador": {"nombre": "🌅 Madrugador", "descripcion": "Estudiar antes de las 8am", "puntos": 15},
            "nocturno": {"nombre": "🌙 Búho Nocturno", "descripcion": "Estudiar después de las 10pm", "puntos": 15},
            "maraton": {"nombre": "🏃 Maratón", "descripcion": "Sesión de más de 2 horas", "puntos": 30},
            "consistente": {"nombre": "🎯 Consistente", "descripcion": "10 sesiones completadas", "puntos": 40},
            "explorador": {"nombre": "🗺️ Explorador", "descripcion": "Estudiar 3 temas diferentes", "puntos": 35},
            "perfeccionista": {"nombre": "💎 Perfeccionista", "descripcion": "5 sesiones con puntuación 9+", "puntos": 45}
        }
    
    def guardar_datos(self):
        try:
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(self.datos, f, indent=2, ensure_ascii=False)
            print("💾 Datos guardados correctamente")
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
    
    def crear_usuario(self):
        print("\n📝 Crear nuevo perfil")
        nombre = input("Tu nombre: ").strip()
        
        if not nombre:
            print("❌ El nombre no puede estar vacío")
            input("⏸️ Presiona ENTER para continuar...")
            return
        
        self.limpiar_pantalla()
        print("👤 CREAR NUEVO PERFIL DE USUARIO")
        print("="*40)
        print(f"✅ Nombre: {nombre}")
        
        print("\n¿Cuál es tu nivel?")
        print("1. Principiante 🌱")
        print("2. Intermedio 🌿") 
        print("3. Avanzado 🌳")
        nivel_num = input("Elige (1-3): ").strip()
        
        niveles = {"1": "principiante", "2": "intermedio", "3": "avanzado"}
        nivel = niveles.get(nivel_num, "principiante")
        
        self.limpiar_pantalla()
        print("👤 CREAR NUEVO PERFIL DE USUARIO")
        print("="*40)
        print(f"✅ Nombre: {nombre}")
        print(f"✅ Nivel: {nivel.title()}")
        
        print(f"\n¿Qué te interesa aprender?")
        print("Ejemplo: python, matemáticas, inglés, diseño")
        intereses_input = input("Escribe tus intereses (separados por comas): ").strip()
        
        if not intereses_input:
            intereses = ["programación"]
        else:
            intereses = [i.strip().lower() for i in intereses_input.split(",") if i.strip()]
        
        usuario_id = f"user_{len(self.datos['usuarios']) + 1}"
        
        self.datos["usuarios"][usuario_id] = {
            "nombre": nombre,
            "nivel": nivel,
            "intereses": intereses,
            "fecha_registro": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Inicializar datos de gamificación
        self.datos["puntos"][usuario_id] = 0
        self.datos["logros"][usuario_id] = []
        self.datos["rachas"][usuario_id] = {"actual": 0, "maxima": 0, "ultima_fecha": None}
        
        self.guardar_datos()
        
        self.limpiar_pantalla()
        print("🎉 ¡USUARIO CREADO EXITOSAMENTE!")
        print("="*40)
        print(f"👤 Nombre: {nombre}")
        print(f"📊 Nivel: {nivel.title()}")
        print(f"🎯 Intereses: {', '.join(intereses)}")
        print(f"🆔 Tu ID es: {usuario_id}")
        print(f"🎮 ¡Empiezas con 0 puntos! ¡A ganar logros!")
    
    def crear_plan_estudio(self):
        if not self.datos["usuarios"]:
            print("❌ Primero debes crear un usuario")
            input("⏸️ Presiona ENTER para continuar...")
            return
        
        print("\nUsuarios disponibles:")
        for user_id, user_data in self.datos["usuarios"].items():
            puntos = self.datos["puntos"].get(user_id, 0)
            print(f"🧑‍🎓 {user_id}: {user_data['nombre']} ({puntos} puntos)")
        
        usuario_id = input("\nID del usuario: ").strip()
        if usuario_id not in self.datos["usuarios"]:
            print("❌ Usuario no encontrado")
            input("⏸️ Presiona ENTER para continuar...")
            return
        
        usuario = self.datos["usuarios"][usuario_id]
        
        self.limpiar_pantalla()
        print("📚 GENERAR PLAN DE ESTUDIO")
        print("="*40)
        print(f"👤 Usuario: {usuario['nombre']} ({usuario['nivel']})")
        print(f"🎯 Intereses actuales: {', '.join(usuario['intereses'])}")
        
        tema = input("\n¿Qué tema específico quieres aprender?: ").strip()
        
        if not tema:
            print("❌ Debes especificar un tema")
            input("⏸️ Presiona ENTER para continuar...")
            return
        
        self.limpiar_pantalla()
        print("📚 GENERAR PLAN DE ESTUDIO")
        print("="*40)
        print(f"👤 Usuario: {usuario['nombre']}")
        print(f"📖 Tema: {tema}")
        
        try:
            dias = int(input("\n¿En cuántos días quieres completarlo? (ej: 30): "))
            if dias <= 0:
                dias = 30
        except:
            dias = 30
            print("⚠️ Usando 30 días por defecto")
        
        # Generar objetivos y recursos automáticamente
        objetivos = self.generar_objetivos(tema, usuario["nivel"])
        recursos = self.generar_recursos(tema)
        
        plan_id = f"plan_{len(self.datos['planes']) + 1}"
        fecha_limite = (datetime.now() + timedelta(days=dias)).strftime("%Y-%m-%d")
        
        self.datos["planes"][plan_id] = {
            "usuario_id": usuario_id,
            "tema": tema,
            "objetivos": objetivos,
            "recursos": recursos,
            "progreso": 0,
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d"),
            "fecha_limite": fecha_limite
        }
        
        # Bonus por crear plan
        self.agregar_puntos(usuario_id, 5, "Crear nuevo plan de estudio")
        
        self.guardar_datos()
        
        self.limpiar_pantalla()
        print("🎉 ¡PLAN CREADO EXITOSAMENTE!")
        print("="*40)
        print(f"🆔 ID del plan: {plan_id}")
        print(f"📖 Tema: {tema}")
        print(f"📅 Fecha límite: {fecha_limite}")
        print(f"🎯 +5 puntos por crear un plan!")
        
        print(f"\n🎯 Objetivos para nivel {usuario['nivel']}:")
        for i, obj in enumerate(objetivos, 1):
            print(f"   {i}. {obj}")
        
        print(f"\n📚 Recursos recomendados:")
        for i, rec in enumerate(recursos, 1):
            print(f"   {i}. {rec}")
    
    def generar_objetivos(self, tema, nivel):
        objetivos_base = {
            "python": {
                "principiante": [
                    "Aprender sintaxis básica de Python",
                    "Crear tu primer programa 'Hola Mundo'", 
                    "Entender variables, listas y loops",
                    "Hacer ejercicios básicos de programación"
                ],
                "intermedio": [
                    "Dominar funciones y módulos",
                    "Trabajar con archivos y datos",
                    "Usar librerías populares como requests",
                    "Crear un proyecto pequeño completo"
                ],
                "avanzado": [
                    "Programación orientada a objetos",
                    "APIs y web scraping",
                    "Optimización y testing de código",
                    "Desplegar aplicaciones"
                ]
            },
            "matemáticas": {
                "principiante": [
                    "Dominar operaciones básicas",
                    "Entender fracciones y decimales", 
                    "Geometría básica y áreas",
                    "Resolver problemas cotidianos"
                ],
                "intermedio": [
                    "Álgebra y ecuaciones",
                    "Trigonometría básica",
                    "Estadística y probabilidad",
                    "Funciones y gráficas"
                ],
                "avanzado": [
                    "Cálculo diferencial e integral",
                    "Álgebra lineal",
                    "Estadística avanzada",
                    "Matemáticas aplicadas"
                ]
            },
            "inglés": {
                "principiante": [
                    "Vocabulario básico (500 palabras)",
                    "Presente simple y continuo",
                    "Conversación básica diaria",
                    "Comprensión de textos simples"
                ],
                "intermedio": [
                    "Todos los tiempos verbales",
                    "Escritura de párrafos",
                    "Comprensión auditiva",
                    "Conversación fluida"
                ],
                "avanzado": [
                    "Inglés de negocios",
                    "Literatura y textos complejos",
                    "Preparación para exámenes oficiales",
                    "Presentaciones y debates"
                ]
            }
        }
        
        tema_lower = tema.lower()
        for key in objetivos_base:
            if key in tema_lower:
                return objetivos_base[key][nivel]
        
        # Objetivos genéricos si no encuentra el tema específico
        return [
            f"Entender los fundamentos de {tema}",
            f"Practicar {tema} regularmente", 
            f"Aplicar {tema} en situaciones reales",
            f"Alcanzar nivel {nivel} en {tema}"
        ]
    
    def generar_recursos(self, tema):
        recursos_base = {
            "python": [
                "🌐 Curso gratuito en freeCodeCamp",
                "📚 Libro: Python Crash Course",
                "💻 Práctica en HackerRank/LeetCode",
                "🎥 Videos de programación en YouTube"
            ],
            "matemáticas": [
                "🎓 Khan Academy (gratis)",
                "📖 Libro de texto recomendado",  
                "🎥 Canal de YouTube: Profesor10demates",
                "📱 App: Photomath para verificar"
            ],
            "inglés": [
                "🦜 Duolingo para vocabulario",
                "🎧 Podcasts: BBC Learning English",
                "💬 Intercambio de idiomas online",
                "📺 Series/películas con subtítulos"
            ],
            "diseño": [
                "🎨 Canva para practicar",
                "🎥 Tutoriales de Adobe en YouTube",
                "📚 Libro: The Design of Everyday Things",
                "🖼️ Inspiración en Dribbble/Behance"
            ]
        }
        
        tema_lower = tema.lower()
        for key in recursos_base:
            if key in tema_lower:
                return recursos_base[key]
        
        # Recursos genéricos
        return [
            f"🔍 Buscar cursos online de {tema}",
            f"📚 Libros especializados en {tema}",
            f"🎥 Videos educativos en YouTube",
            f"💪 Práctica diaria de {tema}"
        ]
    
    def mostrar_progreso(self):
        if not self.datos["planes"]:
            print("❌ No hay planes de estudio creados aún")
            print("💡 Usa la opción 2 para crear tu primer plan")
            return
        
        print("\n📊 Dashboard de Progreso")
        print("=" * 50)
        
        for plan_id, plan in self.datos["planes"].items():
            usuario = self.datos["usuarios"][plan["usuario_id"]]
            
            print(f"\n📚 {plan['tema'].title()}")
            print(f"👤 Estudiante: {usuario['nombre']} ({plan.get('nivel', usuario['nivel'])})")
            
            # Barra de progreso visual mejorada
            progreso = plan['progreso']
            barra_completa = int(progreso / 5)
            barra_vacia = 20 - barra_completa
            barra_visual = "█" * barra_completa + "░" * barra_vacia
            print(f"📈 Progreso: [{barra_visual}] {progreso}%")
            
            # Calcular días restantes
            fecha_limite = datetime.strptime(plan['fecha_limite'], "%Y-%m-%d")
            dias_restantes = (fecha_limite - datetime.now()).days
            
            if dias_restantes > 7:
                print(f"📅 Días restantes: {dias_restantes} ✅")
            elif dias_restantes > 0:
                print(f"⚠️ ¡Quedan solo {dias_restantes} días!")
            else:
                print(f"🚨 ¡Plazo vencido hace {abs(dias_restantes)} días!")
            
            print(f"🎯 Objetivos: {len(plan['objetivos'])} metas definidas")
            print("-" * 30)
        
        # Mostrar estadísticas del usuario
        self.mostrar_estadisticas_usuario()
    
    def mostrar_estadisticas_usuario(self):
        if not self.datos["sesiones"]:
            return
        
        print("\n📊 ESTADÍSTICAS GENERALES")
        print("=" * 30)
        
        # Estadísticas por usuario
        estadisticas_usuario = defaultdict(lambda: {
            "total_tiempo": 0,
            "total_sesiones": 0,
            "puntuacion_promedio": 0,
            "temas_estudiados": set()
        })
        
        for sesion in self.datos["sesiones"]:
            plan = self.datos["planes"][sesion["plan_id"]]
            usuario_id = plan["usuario_id"]
            
            estadisticas_usuario[usuario_id]["total_tiempo"] += sesion["duracion"]
            estadisticas_usuario[usuario_id]["total_sesiones"] += 1
            estadisticas_usuario[usuario_id]["puntuacion_promedio"] += sesion["puntuacion"]
            estadisticas_usuario[usuario_id]["temas_estudiados"].add(plan["tema"])
        
        for usuario_id, stats in estadisticas_usuario.items():
            usuario = self.datos["usuarios"][usuario_id]
            puntos = self.datos["puntos"].get(usuario_id, 0)
            racha_actual = self.datos["rachas"].get(usuario_id, {}).get("actual", 0)
            
            print(f"\n👤 {usuario['nombre']}")
            print(f"🎮 Puntos: {puntos}")
            print(f"🔥 Racha actual: {racha_actual} días")
            print(f"⏱️ Tiempo total: {stats['total_tiempo']} minutos")
            print(f"📚 Sesiones: {stats['total_sesiones']}")
            
            if stats['total_sesiones'] > 0:
                promedio = stats['puntuacion_promedio'] / stats['total_sesiones']
                print(f"😊 Satisfacción promedio: {promedio:.1f}/10")
            
            print(f"🗺️ Temas explorados: {len(stats['temas_estudiados'])}")
            
            # Mostrar progreso visual del nivel
            nivel_actual = self.calcular_nivel(puntos)
            puntos_siguiente = self.puntos_para_siguiente_nivel(puntos)
            print(f"⭐ Nivel: {nivel_actual}")
            if puntos_siguiente > 0:
                print(f"📈 Faltan {puntos_siguiente} puntos para subir de nivel")
    
    def calcular_nivel(self, puntos):
        if puntos < 50:
            return 1
        elif puntos < 150:
            return 2
        elif puntos < 300:
            return 3
        elif puntos < 500:
            return 4
        else:
            return 5 + (puntos - 500) // 200
    
    def puntos_para_siguiente_nivel(self, puntos):
        if puntos < 50:
            return 50 - puntos
        elif puntos < 150:
            return 150 - puntos
        elif puntos < 300:
            return 300 - puntos
        elif puntos < 500:
            return 500 - puntos
        else:
            siguiente_nivel = ((puntos - 500) // 200 + 1) * 200 + 500
            return siguiente_nivel - puntos
    
    def registrar_sesion(self):
        if not self.datos["planes"]:
            print("❌ No hay planes de estudio disponibles")
            print("💡 Crea un plan primero usando la opción 2")
            input("⏸️ Presiona ENTER para continuar...")
            return
        
        print("Planes disponibles:")
        for plan_id, plan in self.datos["planes"].items():
            usuario = self.datos["usuarios"][plan["usuario_id"]]
            print(f"📖 {plan_id}: {plan['tema']} - {usuario['nombre']} ({plan['progreso']}%)")
        
        plan_id = input("\nID del plan: ").strip()
        if plan_id not in self.datos["planes"]:
            print("❌ Plan no encontrado")
            input("⏸️ Presiona ENTER para continuar...")
            return
        
        plan = self.datos["planes"][plan_id]
        usuario = self.datos["usuarios"][plan["usuario_id"]]
        
        self.limpiar_pantalla()
        print("⏰ REGISTRAR SESIÓN DE ESTUDIO")
        print("="*40)
        print(f"📖 Plan: {plan['tema']}")
        print(f"👤 Usuario: {usuario['nombre']}")
        print(f"📊 Progreso actual: {plan['progreso']}%")
        
        try:
            duracion = int(input("\n¿Cuántos minutos estudiaste?: "))
            if duracion <= 0:
                print("❌ La duración debe ser mayor a 0")
                input("⏸️ Presiona ENTER para continuar...")
                return
        except:
            print("❌ Ingresa un número válido")
            input("⏸️ Presiona ENTER para continuar...")
            return
        
        self.limpiar_pantalla()
        print("⏰ REGISTRAR SESIÓN DE ESTUDIO")
        print("="*40)
        print(f"📖 Plan: {plan['tema']}")
        print(f"⏱️ Duración: {duracion} minutos")
        
        try:
            puntuacion = float(input("\n¿Cómo te sientes del 1 al 10?: "))
            puntuacion = max(1, min(10, puntuacion))
        except:
            puntuacion = 5.0
            print("⚠️ Usando puntuación 5.0 por defecto")
        
        notas = input("\nNotas sobre esta sesión (opcional): ").strip()
        
        # Calcular progreso basado en duración y puntuación
        incremento = min(10, max(3, duracion // 15))
        
        # Actualizar progreso
        progreso_anterior = self.datos["planes"][plan_id]["progreso"]
        nuevo_progreso = min(100, progreso_anterior + incremento)
        self.datos["planes"][plan_id]["progreso"] = round(nuevo_progreso, 1)
        
        # Registrar sesión
        sesion = {
            "plan_id": plan_id,
            "duracion": duracion,
            "puntuacion": puntuacion,
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "hora": datetime.now().strftime("%H:%M"),
            "notas": notas
        }
        
        self.datos["sesiones"].append(sesion)
        
        # Sistema de puntos y logros
        usuario_id = plan["usuario_id"]
        
        puntos_ganados = self.calcular_puntos_sesion(duracion, puntuacion)
        self.agregar_puntos(usuario_id, puntos_ganados, f"Sesión de {plan['tema']}")
        
        # Actualizar racha
        self.actualizar_racha(usuario_id)
        
        # Verificar logros
        nuevos_logros = self.verificar_logros(usuario_id, duracion, puntuacion, sesion["hora"])
        
        self.guardar_datos()
        
        # Mostrar resumen final
        self.limpiar_pantalla()
        print("🎉 ¡SESIÓN REGISTRADA EXITOSAMENTE!")
        print("="*40)
        print(f"📖 Tema: {plan['tema']}")
        print(f"⏱️ Duración: {duracion} minutos")
        print(f"😊 Satisfacción: {puntuacion}/10")
        print(f"📈 Progreso: {progreso_anterior}% → {nuevo_progreso}% (+{incremento}%)")
        print(f"🎮 Puntos ganados: +{puntos_ganados}")
        
        # Mostrar racha actual
        racha_actual = self.datos["rachas"][usuario_id]["actual"]
        if racha_actual > 1:
            print(f"🔥 Racha actual: {racha_actual} días")
        
        # Mostrar nuevos logros
        if nuevos_logros:
            print(f"\n🏆 ¡NUEVOS LOGROS DESBLOQUEADOS!")
            for logro in nuevos_logros:
                info = self.logros_disponibles[logro]
                print(f"   {info['nombre']}: {info['descripcion']} (+{info['puntos']} puntos)")
        
        # Motivación basada en progreso
        if nuevo_progreso >= 100:
            print("\n🎉 ¡FELICITACIONES! ¡Completaste tu plan de estudio!")
            self.agregar_puntos(usuario_id, 50, "¡Plan completado!")
        elif nuevo_progreso >= 75:
            print("\n🔥 ¡Excelente! Ya casi terminas")
        elif nuevo_progreso >= 50:
            print("\n💪 ¡Vas muy bien! Ya pasaste la mitad")
        elif nuevo_progreso >= 25:
            print("\n🌟 ¡Buen progreso! Sigue así")
        else:
            print("\n🌱 ¡Cada paso cuenta! Sigue adelante")
        
        # Mostrar nivel actual
        puntos_totales = self.datos["puntos"][usuario_id]
        nivel = self.calcular_nivel(puntos_totales)
        print(f"\n⭐ Nivel actual: {nivel} ({puntos_totales} puntos)")
        
        if notas:
            print(f"📝 Notas: {notas}")
    
    def calcular_puntos_sesion(self, duracion, puntuacion):
        # Puntos base por duración
        puntos_base = min(duracion // 10, 20)  # Máximo 20 puntos por duración
        
        # Bonus por satisfacción alta
        if puntuacion >= 8:
            puntos_base += 5
        elif puntuacion >= 6:
            puntos_base += 2
        
        return max(puntos_base, 1)  # Mínimo 1 punto
    
    def agregar_puntos(self, usuario_id, puntos, razon):
        if usuario_id not in self.datos["puntos"]:
            self.datos["puntos"][usuario_id] = 0
        
        self.datos["puntos"][usuario_id] += puntos
        print(f"🎮 +{puntos} puntos por: {razon}")
    
    def actualizar_racha(self, usuario_id):
        if usuario_id not in self.datos["rachas"]:
            self.datos["rachas"][usuario_id] = {"actual": 0, "maxima": 0, "ultima_fecha": None}
        
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        racha_data = self.datos["rachas"][usuario_id]
        
        # Si es el primer día o ayer no estudió
        if racha_data["ultima_fecha"] is None:
            racha_data["actual"] = 1
        else:
            fecha_anterior = datetime.strptime(racha_data["ultima_fecha"], "%Y-%m-%d")
            fecha_actual = datetime.strptime(fecha_hoy, "%Y-%m-%d")
            diferencia = (fecha_actual - fecha_anterior).days
            
            if diferencia == 1:  # Día consecutivo
                racha_data["actual"] += 1
            elif diferencia == 0:  # Mismo día, no cambia racha
                pass
            else:  # Se rompió la racha
                racha_data["actual"] = 1
        
        # Actualizar racha máxima
        if racha_data["actual"] > racha_data["maxima"]:
            racha_data["maxima"] = racha_data["actual"]
        
        racha_data["ultima_fecha"] = fecha_hoy
        
        # Mostrar racha
        if racha_data["actual"] > 1:
            print(f"🔥 ¡Racha de {racha_data['actual']} días!")
    
    def verificar_logros(self, usuario_id, duracion, puntuacion, hora):
        if usuario_id not in self.datos["logros"]:
            self.datos["logros"][usuario_id] = []
        
        logros_usuario = self.datos["logros"][usuario_id]
        nuevos_logros = []
        
        # Primer día
        if "primer_dia" not in logros_usuario and len(self.datos["sesiones"]) == 1:
            logros_usuario.append("primer_dia")
            nuevos_logros.append("primer_dia")
            self.agregar_puntos(usuario_id, self.logros_disponibles["primer_dia"]["puntos"], "Logro: Primer Paso")
        
        # Rachas
        racha_actual = self.datos["rachas"][usuario_id]["actual"]
        if racha_actual >= 30 and "racha_30" not in logros_usuario:
            logros_usuario.append("racha_30")
            nuevos_logros.append("racha_30")
            self.agregar_puntos(usuario_id, self.logros_disponibles["racha_30"]["puntos"], "Logro: Leyenda")
        elif racha_actual >= 7 and "racha_7" not in logros_usuario:
            logros_usuario.append("racha_7")
            nuevos_logros.append("racha_7")
            self.agregar_puntos(usuario_id, self.logros_disponibles["racha_7"]["puntos"], "Logro: Imparable")
        elif racha_actual >= 3 and "racha_3" not in logros_usuario:
            logros_usuario.append("racha_3")
            nuevos_logros.append("racha_3")
            self.agregar_puntos(usuario_id, self.logros_disponibles["racha_3"]["puntos"], "Logro: En Racha")
        
        # Madrugador / Nocturno
        hora_num = int(hora.split(":")[0])
        if hora_num < 8 and "madrugador" not in logros_usuario:
            logros_usuario.append("madrugador")
            nuevos_logros.append("madrugador")
            self.agregar_puntos(usuario_id, self.logros_disponibles["madrugador"]["puntos"], "Logro: Madrugador")
        elif hora_num >= 22 and "nocturno" not in logros_usuario:
            logros_usuario.append("nocturno")
            nuevos_logros.append("nocturno")
            self.agregar_puntos(usuario_id, self.logros_disponibles["nocturno"]["puntos"], "Logro: Búho Nocturno")
        
        # Maratón
        if duracion >= 120 and "maraton" not in logros_usuario:
            logros_usuario.append("maraton")
            nuevos_logros.append("maraton")
            self.agregar_puntos(usuario_id, self.logros_disponibles["maraton"]["puntos"], "Logro: Maratón")
        
        # Consistente
        sesiones_usuario = [s for s in self.datos["sesiones"] if self.datos["planes"][s["plan_id"]]["usuario_id"] == usuario_id]
        if len(sesiones_usuario) >= 10 and "consistente" not in logros_usuario:
            logros_usuario.append("consistente")
            nuevos_logros.append("consistente")
            self.agregar_puntos(usuario_id, self.logros_disponibles["consistente"]["puntos"], "Logro: Consistente")
        
        return nuevos_logros
    
    def mostrar_logros(self):
        """Función para mostrar logros del usuario"""
        if not self.datos["usuarios"]:
            print("❌ No hay usuarios creados")
            return
        
        print("\n🏆 CENTRO DE LOGROS")
        print("=" * 40)
        
        for usuario_id, usuario_data in self.datos["usuarios"].items():
            print(f"\n👤 {usuario_data['nombre']}")
            logros_usuario = self.datos["logros"].get(usuario_id, [])
            puntos_totales = self.datos["puntos"].get(usuario_id, 0)
            
            print(f"🎮 Puntos totales: {puntos_totales}")
            print(f"🏆 Logros desbloqueados: {len(logros_usuario)}/{len(self.logros_disponibles)}")
            
            print("\n✅ Logros conseguidos:")
            if logros_usuario:
                for logro in logros_usuario:
                    info = self.logros_disponibles[logro]
                    print(f"   {info['nombre']}: {info['descripcion']}")
            else:
                print("   Ninguno aún")
            
            print("\n🔒 Logros por desbloquear:")
            logros_pendientes = [l for l in self.logros_disponibles if l not in logros_usuario]
            for logro in logros_pendientes[:3]:  # Mostrar solo los primeros 3
                info = self.logros_disponibles[logro]
                print(f"   {info['nombre']}: {info['descripcion']} (+{info['puntos']} puntos)")
            
            if len(logros_pendientes) > 3:
                print(f"   ... y {len(logros_pendientes) - 3} más")
            
            print("-" * 30)

    # ===== FUNCIONES DE IA =====
    
    def mostrar_recomendaciones_ia(self):
        """Nueva función para mostrar recomendaciones personalizadas de IA"""
        if not self.datos["usuarios"]:
            print("❌ No hay usuarios creados")
            print("💡 Crea un usuario primero para recibir recomendaciones personalizadas")
            input("⏸️ Presiona ENTER para continuar...")
            return
        
        print("Usuarios disponibles:")
        for user_id, user_data in self.datos["usuarios"].items():
            puntos = self.datos["puntos"].get(user_id, 0)
            print(f"🧑‍🎓 {user_id}: {user_data['nombre']} ({puntos} puntos)")
        
        usuario_id = input("\nID del usuario para recomendaciones: ").strip()
        if usuario_id not in self.datos["usuarios"]:
            print("❌ Usuario no encontrado")
            input("⏸️ Presiona ENTER para continuar...")
            return
        
        # Crear instancia del recomendador IA
        recomendador = RecomendadorIA(self.datos)
        usuario = self.datos["usuarios"][usuario_id]
        
        self.limpiar_pantalla()
        print("🤖 RECOMENDACIONES PERSONALIZADAS DE IA")
        print("="*50)
        print(f"👤 Usuario: {usuario['nombre']}")
        print(f"📊 Nivel: {usuario['nivel'].title()}")
        print(f"🎮 Puntos: {self.datos['puntos'].get(usuario_id, 0)}")
        
        # Mostrar análisis de patrones
        patrones = recomendador.patrones_estudio
        if patrones["duracion_promedio"] > 0:
            print(f"\n📈 ANÁLISIS DE TUS PATRONES:")
            print(f"⏰ Duración promedio: {patrones['duracion_promedio']} minutos")
            print(f"😊 Satisfacción promedio: {patrones['satisfaccion_promedio']:.1f}/10")
            if patrones["racha_maxima"] > 0:
                print(f"🔥 Racha máxima: {patrones['racha_maxima']} días")
        
        # Horario óptimo
        print(f"\n{recomendador.recomendar_horario_optimo(usuario_id)}")
        print(f"{recomendador.recomendar_duracion_ideal(usuario_id)}")
        
        # Recomendaciones personalizadas
        recomendaciones = recomendador.generar_recomendaciones_personalizadas(usuario_id)
        
        print(f"\n🎯 RECOMENDACIONES PERSONALIZADAS:")
        print("-" * 40)
        for i, rec in enumerate(recomendaciones, 1):
            print(f"{i}. {rec}")
        
        print(f"\n💡 PRÓXIMOS PASOS SUGERIDOS:")
        self._mostrar_proximos_pasos(usuario_id, recomendador)
    
    def _mostrar_proximos_pasos(self, usuario_id, recomendador):
        """Muestra próximos pasos personalizados"""
        usuario = self.datos["usuarios"][usuario_id]
        planes_usuario = {k: v for k, v in self.datos["planes"].items() 
                         if v["usuario_id"] == usuario_id}
        
        if not planes_usuario:
            print("1. 📚 Crear tu primer plan de estudio")
            print("2. 🎯 Definir objetivos específicos y alcanzables")
            print("3. ⏰ Establecer un horario de estudio regular")
        else:
            # Analizar planes actuales
            plan_mas_atrasado = None
            menor_progreso = 100
            
            for plan_id, plan in planes_usuario.items():
                if plan["progreso"] < menor_progreso:
                    menor_progreso = plan["progreso"]
                    plan_mas_atrasado = plan
            
            if plan_mas_atrasado:
                print(f"1. 🚀 Enfócate en '{plan_mas_atrasado['tema']}' (progreso: {plan_mas_atrasado['progreso']}%)")
                print(f"2. ⏰ Dedica al menos {recomendador.patrones_estudio.get('duracion_promedio', 25)} minutos hoy")
                print("3. 🎯 Revisa tus objetivos y ajústalos si es necesario")
        
        # Sugerencia de nuevo tema basado en intereses
        if len(usuario["intereses"]) > len(planes_usuario):
            intereses_sin_plan = [i for i in usuario["intereses"] 
                                if not any(i.lower() in plan["tema"].lower() 
                                         for plan in planes_usuario.values())]
            if intereses_sin_plan:
                print(f"4. 🌟 Considera crear un plan para: {intereses_sin_plan[0]}")
    
    def generar_plan_con_ia(self):
        """Genera un plan de estudio usando recomendaciones de IA"""
        if not self.datos["usuarios"]:
            print("❌ Primero debes crear un usuario")
            input("⏸️ Presiona ENTER para continuar...")
            return
        
        print("Usuarios disponibles:")
        for user_id, user_data in self.datos["usuarios"].items():
            puntos = self.datos["puntos"].get(user_id, 0)
            racha = self.datos["rachas"].get(user_id, {}).get("actual", 0)
            print(f"🧑‍🎓 {user_id}: {user_data['nombre']} ({puntos} pts, racha: {racha})")
        
        usuario_id = input("\nID del usuario: ").strip()
        if usuario_id not in self.datos["usuarios"]:
            print("❌ Usuario no encontrado")
            input("⏸️ Presiona ENTER para continuar...")
            return
        
        usuario = self.datos["usuarios"][usuario_id]
        recomendador = RecomendadorIA(self.datos)
        
        self.limpiar_pantalla()
        print("🤖 GENERADOR DE PLANES CON IA")
        print("="*40)
        print(f"👤 Usuario: {usuario['nombre']}")
        
        # Mostrar temas sugeridos basados en intereses
        print(f"\n🎯 Tus intereses registrados: {', '.join(usuario['intereses'])}")
        
        # Sugerir temas no explorados
        planes_existentes = [plan["tema"].lower() for plan in self.datos["planes"].values() 
                           if plan["usuario_id"] == usuario_id]
        temas_sugeridos = [interes for interes in usuario["intereses"] 
                          if not any(interes.lower() in plan_tema for plan_tema in planes_existentes)]
        
        if temas_sugeridos:
            print(f"💡 Temas sugeridos para explorar: {', '.join(temas_sugeridos)}")
        
        tema = input("\n¿Qué tema quieres estudiar?: ").strip()
        if not tema:
            print("❌ Debes especificar un tema")
            input("⏸️ Presiona ENTER para continuar...")
            return
        
        # Generar plan personalizado con IA
        plan_ia = recomendador.generar_plan_personalizado(usuario_id, tema)
        
        self.limpiar_pantalla()
        print("🤖 PLAN GENERADO CON IA")
        print("="*40)
        print(f"📖 Tema: {plan_ia['tema']}")
        print(f"📊 Nivel: {plan_ia['nivel'].title()}")
        print(f"⏰ Duración recomendada por sesión: {plan_ia['duracion_recomendada']} minutos")
        
        print(f"\n{plan_ia['horario_sugerido']}")
        
        print(f"\n🎯 OBJETIVOS PERSONALIZADOS:")
        for i, objetivo in enumerate(plan_ia['objetivos'], 1):
            print(f"   {i}. {objetivo}")
        
        print(f"\n📚 RECURSOS PERSONALIZADOS:")
        for i, recurso in enumerate(plan_ia['recursos'], 1):
            print(f"   {i}. {recurso}")
        
        print(f"\n💡 TIPS PERSONALIZADOS PARA TI:")
        for i, tip in enumerate(plan_ia['tips_personalizados'], 1):
            print(f"   {i}. {tip}")
        
        crear_plan = input(f"\n¿Crear este plan personalizado? (s/n): ").lower().strip()
        if crear_plan == 's':
            # Preguntar duración del plan
            try:
                dias = int(input("¿En cuántos días quieres completarlo? (sugerido: 30): "))
                if dias <= 0:
                    dias = 30
            except:
                dias = 30
                print("⚠️ Usando 30 días por defecto")
            
            # Crear el plan en el sistema
            plan_id = f"plan_{len(self.datos['planes']) + 1}"
            fecha_limite = (datetime.now() + timedelta(days=dias)).strftime("%Y-%m-%d")
            
            self.datos["planes"][plan_id] = {
                "usuario_id": usuario_id,
                "tema": plan_ia['tema'],
                "objetivos": plan_ia['objetivos'],
                "recursos": plan_ia['recursos'],
                "progreso": 0,
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d"),
                "fecha_limite": fecha_limite,
                "generado_con_ia": True,
                "duracion_recomendada": plan_ia['duracion_recomendada']
            }
            
            # Bonus por crear plan con IA
            self.agregar_puntos(usuario_id, 10, "Crear plan personalizado con IA")
            
            self.guardar_datos()
            
            self.limpiar_pantalla()
            print("🎉 ¡PLAN CON IA CREADO EXITOSAMENTE!")
            print("="*40)
            print(f"🤖 Plan inteligente generado: {plan_id}")
            print(f"📖 Tema: {tema}")
            print(f"📅 Fecha límite: {fecha_limite}")
            print(f"🎮 +10 puntos por usar IA!")
            print(f"💡 Sigue las recomendaciones personalizadas para mejores resultados")
        else:
            print("📝 Plan no creado. Puedes generar otro cuando quieras")
    
    def dashboard_inteligente(self):
        """Dashboard con análisis inteligente y recomendaciones"""
        if not self.datos["usuarios"]:
            print("❌ No hay usuarios para analizar")
            input("⏸️ Presiona ENTER para continuar...")
            return
        
        print("👥 Selecciona usuario para análisis inteligente:")
        for user_id, user_data in self.datos["usuarios"].items():
            puntos = self.datos["puntos"].get(user_id, 0)
            racha = self.datos["rachas"].get(user_id, {}).get("actual", 0)
            sesiones = sum(1 for s in self.datos["sesiones"] 
                          if self.datos["planes"].get(s["plan_id"], {}).get("usuario_id") == user_id)
            print(f"🧑‍🎓 {user_id}: {user_data['nombre']} ({puntos} pts, {racha}d racha, {sesiones} sesiones)")
        
        usuario_id = input("\nID del usuario: ").strip()
        if usuario_id not in self.datos["usuarios"]:
            print("❌ Usuario no encontrado")
            input("⏸️ Presiona ENTER para continuar...")
            return
        
        usuario = self.datos["usuarios"][usuario_id]
        recomendador = RecomendadorIA(self.datos)
        
        self.limpiar_pantalla()
        print("🤖 DASHBOARD INTELIGENTE")
        print("="*50)
        print(f"👤 {usuario['nombre']} | Nivel: {usuario['nivel'].title()}")
        
        # Análisis inteligente del rendimiento
        puntos_totales = self.datos["puntos"].get(usuario_id, 0)
        nivel_actual = self.calcular_nivel(puntos_totales)
        racha_actual = self.datos["rachas"].get(usuario_id, {}).get("actual", 0)
        racha_maxima = self.datos["rachas"].get(usuario_id, {}).get("maxima", 0)
        
        print(f"\n📊 MÉTRICAS CLAVE:")
        print(f"🎮 Puntos: {puntos_totales} (Nivel {nivel_actual})")
        print(f"🔥 Racha actual: {racha_actual} días (récord: {racha_maxima})")
        
        # Calcular estadísticas de sesiones del usuario
        sesiones_usuario = [s for s in self.datos["sesiones"] 
                           if self.datos["planes"].get(s["plan_id"], {}).get("usuario_id") == usuario_id]
        
        if sesiones_usuario:
            tiempo_total = sum(s["duracion"] for s in sesiones_usuario)
            satisfaccion_promedio = sum(s["puntuacion"] for s in sesiones_usuario) / len(sesiones_usuario)
            
            print(f"📚 Sesiones totales: {len(sesiones_usuario)}")
            print(f"⏰ Tiempo invertido: {tiempo_total} minutos ({tiempo_total//60}h {tiempo_total%60}m)")
            print(f"😊 Satisfacción promedio: {satisfaccion_promedio:.1f}/10")
            
            # Análisis de tendencias
            print(f"\n📈 ANÁLISIS INTELIGENTE:")
            
            # Tendencia de satisfacción
            if len(sesiones_usuario) >= 3:
                ultimas_3 = sesiones_usuario[-3:]
                satisfaccion_reciente = sum(s["puntuacion"] for s in ultimas_3) / 3
                
                if satisfaccion_reciente > satisfaccion_promedio + 1:
                    print("📈 Tendencia positiva: Tu satisfacción está mejorando")
                elif satisfaccion_reciente < satisfaccion_promedio - 1:
                    print("📉 Alerta: Tu satisfacción ha bajado recientemente")
                else:
                    print("➡️ Satisfacción estable")
        
        # Recomendaciones principales
        recomendaciones = recomendador.generar_recomendaciones_personalizadas(usuario_id)
        print(f"\n🎯 TOP 3 RECOMENDACIONES:")
        for i, rec in enumerate(recomendaciones[:3], 1):
            print(f"{i}. {rec}")
        
        print(f"\n{recomendador.recomendar_horario_optimo(usuario_id)}")
        print(f"{recomendador.recomendar_duracion_ideal(usuario_id)}")
    
    def mostrar_estadisticas_avanzadas(self):
        """Estadísticas avanzadas con análisis inteligente"""
        if not self.datos["sesiones"]:
            print("❌ No hay datos suficientes para análisis avanzado")
            input("⏸️ Presiona ENTER para continuar...")
            return
        
        recomendador = RecomendadorIA(self.datos)
        
        self.limpiar_pantalla()
        print("📊 ESTADÍSTICAS AVANZADAS CON IA")
        print("="*50)
        
        # Análisis global de la plataforma
        total_usuarios = len(self.datos["usuarios"])
        total_sesiones = len(self.datos["sesiones"])
        total_planes = len(self.datos["planes"])
        tiempo_total_plataforma = sum(s["duracion"] for s in self.datos["sesiones"])
        
        print(f"🌍 ESTADÍSTICAS GLOBALES:")
        print(f"👥 Usuarios activos: {total_usuarios}")
        print(f"📚 Planes creados: {total_planes}")
        print(f"⏰ Sesiones completadas: {total_sesiones}")
        print(f"🕒 Tiempo total estudiado: {tiempo_total_plataforma//60}h {tiempo_total_plataforma%60}m")
        
        if total_sesiones > 0:
            satisfaccion_global = sum(s["puntuacion"] for s in self.datos["sesiones"]) / total_sesiones
            duracion_promedio_global = tiempo_total_plataforma / total_sesiones
            print(f"😊 Satisfacción promedio: {satisfaccion_global:.1f}/10")
            print(f"⏱️ Duración promedio por sesión: {duracion_promedio_global:.1f} minutos")
        
        print(f"\n💡 La IA ha analizado {total_sesiones} sesiones para generar estos insights")

    def menu_ia_avanzado(self):
        """Menú especializado para funciones de IA"""
        while True:
            self.limpiar_pantalla()
            print("🤖 CENTRO DE INTELIGENCIA ARTIFICIAL")
            print("="*50)
            print("¿Qué análisis inteligente quieres ver?")
            print("┌─────────────────────────────────────────┐")
            print("│ 1. 🎯 Recomendaciones personalizadas   │")
            print("│ 2. 📚 Generar plan con IA              │")
            print("│ 3. 📊 Dashboard inteligente             │")
            print("│ 4. 📈 Estadísticas avanzadas           │")
            print("│ 5. 🔙 Volver al menú principal         │")
            print("└─────────────────────────────────────────┘")
            
            opcion = input("\n🤖 Elige una opción (1-5): ").strip()
            
            if opcion == "1":
                self.limpiar_pantalla()
                print("🤖 RECOMENDACIONES PERSONALIZADAS")
                print("="*40)
                self.mostrar_recomendaciones_ia()
                
            elif opcion == "2":
                self.limpiar_pantalla()
                print("🤖 GENERADOR DE PLANES CON IA")
                print("="*40)
                self.generar_plan_con_ia()
                
            elif opcion == "3":
                self.limpiar_pantalla()
                print("🤖 DASHBOARD INTELIGENTE")
                print("="*40)
                self.dashboard_inteligente()
                
            elif opcion == "4":
                self.limpiar_pantalla()
                print("🤖 ESTADÍSTICAS AVANZADAS")
                print("="*40)
                self.mostrar_estadisticas_avanzadas()
                
            elif opcion == "5":
                break
                
            else:
                print("❌ Opción inválida. Por favor elige un número del 1 al 5.")
            
            if opcion in ["1", "2", "3", "4"]:
                input("\n⏸️ Presiona ENTER para continuar...")