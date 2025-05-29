import json
import random
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class RecomendadorIA:
    def __init__(self, datos_usuario):
        self.datos = datos_usuario
        self.patrones_estudio = self.analizar_patrones()
    
    def analizar_patrones(self):
        """Analiza los patrones de estudio del usuario"""
        if not self.datos["sesiones"]:
            return {}
        
        patrones = {
            "horas_preferidas": [],
            "duracion_promedio": 0,
            "satisfaccion_promedio": 0,
            "dias_mas_activos": {},
            "temas_favoritos": {},
            "racha_maxima": 0
        }
        
        # Analizar sesiones
        for sesion in self.datos["sesiones"]:
            # Extraer hora si existe
            if "hora" in sesion:
                hora = int(sesion["hora"].split(":")[0])
                patrones["horas_preferidas"].append(hora)
            
            patrones["duracion_promedio"] += sesion["duracion"]
            patrones["satisfaccion_promedio"] += sesion["puntuacion"]
            
            # Analizar día de la semana
            try:
                fecha = datetime.strptime(sesion["fecha"], "%Y-%m-%d")
                dia_semana = fecha.strftime("%A")
                if dia_semana not in patrones["dias_mas_activos"]:
                    patrones["dias_mas_activos"][dia_semana] = 0
                patrones["dias_mas_activos"][dia_semana] += 1
            except:
                pass
            
            # Analizar temas
            plan = self.datos["planes"].get(sesion["plan_id"], {})
            if "tema" in plan:
                tema = plan["tema"]
                if tema not in patrones["temas_favoritos"]:
                    patrones["temas_favoritos"][tema] = 0
                patrones["temas_favoritos"][tema] += 1
        
        # Calcular promedios
        total_sesiones = len(self.datos["sesiones"])
        if total_sesiones > 0:
            patrones["duracion_promedio"] = patrones["duracion_promedio"] // total_sesiones
            patrones["satisfaccion_promedio"] = patrones["satisfaccion_promedio"] / total_sesiones
        
        # Analizar rachas máximas
        for usuario_id, racha_data in self.datos["rachas"].items():
            if racha_data["maxima"] > patrones["racha_maxima"]:
                patrones["racha_maxima"] = racha_data["maxima"]
        
        return patrones
    
    def generar_recomendaciones_personalizadas(self, usuario_id):
        """Genera recomendaciones basadas en el análisis del usuario"""
        if usuario_id not in self.datos["usuarios"]:
            return ["❌ Usuario no encontrado"]
        
        usuario = self.datos["usuarios"][usuario_id]
        recomendaciones = []
        
        # Recomendaciones basadas en progreso
        recomendaciones.extend(self._recomendaciones_progreso(usuario_id))
        
        # Recomendaciones basadas en patrones de estudio
        recomendaciones.extend(self._recomendaciones_patrones())
        
        # Recomendaciones basadas en nivel
        recomendaciones.extend(self._recomendaciones_nivel(usuario["nivel"]))
        
        # Recomendaciones basadas en rachas
        recomendaciones.extend(self._recomendaciones_rachas(usuario_id))
        
        # Recomendaciones motivacionales
        recomendaciones.extend(self._recomendaciones_motivacionales(usuario_id))
        
        return recomendaciones[:8]  # Máximo 8 recomendaciones
    
    def _recomendaciones_progreso(self, usuario_id):
        """Recomendaciones basadas en el progreso actual"""
        recomendaciones = []
        
        planes_usuario = {k: v for k, v in self.datos["planes"].items() 
                         if v["usuario_id"] == usuario_id}
        
        if not planes_usuario:
            recomendaciones.append("🎯 Crea tu primer plan de estudio para comenzar tu aventura de aprendizaje")
            return recomendaciones
        
        for plan_id, plan in planes_usuario.items():
            progreso = plan["progreso"]
            tema = plan["tema"]
            
            if progreso < 25:
                recomendaciones.append(f"🌱 En {tema}: Dedica 15-20 minutos diarios para establecer el hábito")
            elif progreso < 50:
                recomendaciones.append(f"🚀 En {tema}: ¡Vas bien! Aumenta a 25-30 minutos para acelerar")
            elif progreso < 75:
                recomendaciones.append(f"💪 En {tema}: Estás en la recta final, mantén la constancia")
            elif progreso < 100:
                recomendaciones.append(f"🔥 En {tema}: ¡Casi terminas! Un último empujón")
            
            # Verificar fecha límite
            try:
                fecha_limite = datetime.strptime(plan["fecha_limite"], "%Y-%m-%d")
                dias_restantes = (fecha_limite - datetime.now()).days
                
                if dias_restantes <= 3 and progreso < 90:
                    recomendaciones.append(f"⚠️ {tema}: Quedan {dias_restantes} días. Considera sesiones más largas")
                elif dias_restantes <= 0:
                    recomendaciones.append(f"🚨 {tema}: Plazo vencido. Evalúa extender el plan o ajustar objetivos")
            except:
                pass
        
        return recomendaciones
    
    def _recomendaciones_patrones(self):
        """Recomendaciones basadas en patrones de estudio"""
        recomendaciones = []
        
        if not self.patrones_estudio["horas_preferidas"]:
            return recomendaciones
        
        # Analizar horas preferidas
        horas_comunes = Counter(self.patrones_estudio["horas_preferidas"])
        if horas_comunes:
            hora_favorita = horas_comunes.most_common(1)[0][0]
            if 6 <= hora_favorita <= 10:
                recomendaciones.append(f"🌅 Tu mejor momento es a las {hora_favorita}:00. ¡Aprovecha las mañanas!")
            elif 14 <= hora_favorita <= 18:
                recomendaciones.append(f"☀️ Rindes bien en las tardes ({hora_favorita}:00). Mantén esa rutina")
            elif hora_favorita >= 20:
                recomendaciones.append(f"🌙 Eres más productivo en las noches ({hora_favorita}:00)")
        
        # Recomendaciones sobre duración
        duracion_prom = self.patrones_estudio["duracion_promedio"]
        if duracion_prom > 0:
            if duracion_prom < 20:
                recomendaciones.append("⏰ Tus sesiones son cortas. Intenta llegar a 25-30 minutos para mayor efectividad")
            elif duracion_prom > 90:
                recomendaciones.append("🧠 Sesiones muy largas pueden causar fatiga. Considera descansos cada 45-60 min")
            else:
                recomendaciones.append(f"✅ Duración ideal de {duracion_prom} min. ¡Sigue así!")
        
        # Recomendaciones sobre satisfacción
        satisfaccion_prom = self.patrones_estudio["satisfaccion_promedio"]
        if satisfaccion_prom > 0:
            if satisfaccion_prom < 6:
                recomendaciones.append("😔 Satisfacción baja. Prueba cambiar de ambiente o método de estudio")
            elif satisfaccion_prom >= 8:
                recomendaciones.append("😊 ¡Excelente satisfacción! Estás en la zona óptima de aprendizaje")
        
        return recomendaciones
    
    def _recomendaciones_nivel(self, nivel):
        """Recomendaciones específicas por nivel"""
        recomendaciones_por_nivel = {
            "principiante": [
                "📚 Enfócate en conceptos fundamentales antes de avanzar",
                "🎯 Establece metas pequeñas y alcanzables (15-20 min diarios)",
                "🔄 La repetición es clave en esta etapa. Repasa constantemente"
            ],
            "intermedio": [
                "🚀 Es momento de aplicar lo aprendido en proyectos prácticos",
                "🔗 Conecta diferentes conceptos para entendimiento profundo",
                "📈 Aumenta gradualmente la complejidad de los ejercicios"
            ],
            "avanzado": [
                "🎓 Busca casos de estudio complejos y desafiantes",
                "👥 Enseña a otros para reforzar tu conocimiento",
                "🔬 Experimenta con aplicaciones innovadoras del tema"
            ]
        }
        
        return random.sample(recomendaciones_por_nivel.get(nivel, []), 
                           min(2, len(recomendaciones_por_nivel.get(nivel, []))))
    
    def _recomendaciones_rachas(self, usuario_id):
        """Recomendaciones basadas en rachas de estudio"""
        recomendaciones = []
        
        if usuario_id not in self.datos["rachas"]:
            recomendaciones.append("🔥 Construye una racha de estudio: ¡Estudia hoy y mañana!")
            return recomendaciones
        
        racha_data = self.datos["rachas"][usuario_id]
        racha_actual = racha_data["actual"]
        racha_maxima = racha_data["maxima"]
        
        if racha_actual == 0:
            recomendaciones.append("🔄 Reinicia tu racha de estudio. ¡Un pequeño paso hoy marca la diferencia!")
        elif racha_actual < 3:
            recomendaciones.append(f"🌱 Racha de {racha_actual} día(s). ¡Llega a 3 para desbloquear el logro!")
        elif racha_actual < 7:
            recomendaciones.append(f"🔥 {racha_actual} días seguidos. ¡Objetivo: llegar a una semana completa!")
        elif racha_actual >= 7:
            recomendaciones.append(f"👑 ¡Increíble racha de {racha_actual} días! Eres una máquina de aprendizaje")
        
        if racha_maxima > racha_actual and racha_actual > 0:
            recomendaciones.append(f"🎯 Tu récord es {racha_maxima} días. ¡Puedes superarlo!")
        
        return recomendaciones
    
    def _recomendaciones_motivacionales(self, usuario_id):
        """Recomendaciones motivacionales personalizadas"""
        puntos_totales = self.datos["puntos"].get(usuario_id, 0)
        total_sesiones = sum(1 for s in self.datos["sesiones"] 
                           if self.datos["planes"].get(s["plan_id"], {}).get("usuario_id") == usuario_id)
        
        motivacionales = []
        
        if puntos_totales < 50:
            motivacionales.append("⭐ Cada sesión te acerca a tu primer nivel. ¡Sigue adelante!")
        elif puntos_totales < 200:
            motivacionales.append("🚀 Estás construyendo un hábito sólido. ¡La constancia es tu superpoder!")
        else:
            motivacionales.append("🏆 Eres un verdadero estudiante dedicado. ¡Inspiras a otros!")
        
        if total_sesiones >= 10:
            motivacionales.append("💪 Tu disciplina es admirable. ¡Los grandes logros vienen de pequeños pasos!")
        
        # Motivación basada en tiempo de estudio
        tiempo_total = sum(s["duracion"] for s in self.datos["sesiones"]
                          if self.datos["planes"].get(s["plan_id"], {}).get("usuario_id") == usuario_id)
        
        if tiempo_total >= 300:  # 5 horas
            horas = tiempo_total // 60
            motivacionales.append(f"⏰ Has invertido {horas} horas en tu crecimiento. ¡Eso es dedicación real!")
        
        return motivacionales[:2]  # Máximo 2 motivacionales
    
    def recomendar_horario_optimo(self, usuario_id):
        """Sugiere el mejor horario basado en patrones"""
        if not self.patrones_estudio["horas_preferidas"]:
            return "🕐 Aún no tengo suficientes datos. Estudia a diferentes horas para encontrar tu momento óptimo"
        
        horas_exitosas = Counter(self.patrones_estudio["horas_preferidas"])
        mejor_hora = horas_exitosas.most_common(1)[0][0]
        
        franjas_horarias = {
            range(6, 10): "🌅 Mañana temprano",
            range(10, 14): "☀️ Mañana tardía", 
            range(14, 18): "🌤️ Tarde",
            range(18, 22): "🌆 Noche temprana",
            range(22, 24): "🌙 Noche tardía"
        }
        
        franja = "🕐 Horario personalizado"
        for rango, nombre in franjas_horarias.items():
            if mejor_hora in rango:
                franja = nombre
                break
        
        return f"🎯 Tu horario óptimo: {franja} (alrededor de las {mejor_hora}:00)"
    
    def recomendar_duracion_ideal(self, usuario_id):
        """Sugiere duración ideal basada en satisfacción vs duración"""
        if not self.datos["sesiones"]:
            return "⏰ Comienza con sesiones de 20-25 minutos para crear el hábito"
        
        # Encontrar sesiones del usuario
        sesiones_usuario = []
        for sesion in self.datos["sesiones"]:
            plan = self.datos["planes"].get(sesion["plan_id"], {})
            if plan.get("usuario_id") == usuario_id:
                sesiones_usuario.append(sesion)
        
        if not sesiones_usuario:
            return "⏰ Comienza con sesiones de 20-25 minutos"
        
        # Analizar relación duración-satisfacción
        duracion_satisfaccion = []
        for sesion in sesiones_usuario:
            duracion_satisfaccion.append((sesion["duracion"], sesion["puntuacion"]))
        
        # Encontrar el punto dulce
        satisfaccion_por_rango = defaultdict(list)
        for duracion, satisfaccion in duracion_satisfaccion:
            if duracion <= 20:
                satisfaccion_por_rango["corta"].append(satisfaccion)
            elif duracion <= 45:
                satisfaccion_por_rango["media"].append(satisfaccion)
            elif duracion <= 90:
                satisfaccion_por_rango["larga"].append(satisfaccion)
            else:
                satisfaccion_por_rango["muy_larga"].append(satisfaccion)
        
        mejor_rango = "media"
        mejor_satisfaccion = 0
        
        for rango, satisfacciones in satisfaccion_por_rango.items():
            if satisfacciones:
                promedio = sum(satisfacciones) / len(satisfacciones)
                if promedio > mejor_satisfaccion:
                    mejor_satisfaccion = promedio
                    mejor_rango = rango
        
        recomendaciones_duracion = {
            "corta": "⚡ Tu punto dulce: 15-20 minutos. Sesiones cortas pero efectivas",
            "media": "🎯 Tu zona óptima: 25-45 minutos. Equilibrio perfecto",
            "larga": "🏃 Rindes bien en sesiones largas: 60-90 minutos",
            "muy_larga": "🧠 Eres de resistencia: +90 minutos. Recuerda tomar descansos"
        }
        
        return recomendaciones_duracion.get(mejor_rango, "🎯 Experimenta con diferentes duraciones")
    
    def generar_plan_personalizado(self, usuario_id, tema):
        """Genera un plan de estudio personalizado usando IA"""
        if usuario_id not in self.datos["usuarios"]:
            return None
        
        usuario = self.datos["usuarios"][usuario_id]
        nivel = usuario["nivel"]
        
        # Base de conocimiento para diferentes temas y niveles
        planes_ia = {
            "python": {
                "principiante": {
                    "objetivos": [
                        "Dominar la sintaxis básica de Python",
                        "Crear programas simples con variables y loops",
                        "Entender listas, diccionarios y funciones",
                        "Hacer tu primer proyecto: calculadora o juego simple"
                    ],
                    "recursos_personalizados": [
                        "🎯 Para tu nivel: Curso interactivo Python.org",
                        "📚 Libro recomendado: 'Automate the Boring Stuff'",
                        "💻 Práctica: Ejercicios en Codecademy",
                        "🎥 Videos: Canal 'Python para Principiantes' YouTube"
                    ],
                    "hitos_semanales": [
                        "Semana 1: Variables, tipos de datos, input/output",
                        "Semana 2: Condicionales y loops básicos",
                        "Semana 3: Listas y funciones simples",
                        "Semana 4: Proyecto final: programa interactivo"
                    ]
                },
                "intermedio": {
                    "objetivos": [
                        "Programación orientada a objetos",
                        "Manejo de archivos y excepciones", 
                        "Usar librerías como requests y pandas",
                        "Crear una aplicación web simple"
                    ],
                    "recursos_personalizados": [
                        "🚀 Nivel intermedio: Real Python tutorials",
                        "📊 Proyecto: Análisis de datos con pandas",
                        "🌐 Flask para web development",
                        "🔧 GitHub para versionar tu código"
                    ]
                }
            },
            "matemáticas": {
                "principiante": {
                    "objetivos": [
                        "Operaciones básicas con confianza",
                        "Fracciones, decimales y porcentajes",
                        "Geometría básica y medidas",
                        "Resolver problemas del mundo real"
                    ],
                    "recursos_personalizados": [
                        "🎓 Khan Academy: módulos interactivos",
                        "📱 App: Photomath (para verificar resultados)",
                        "📚 Cuaderno de ejercicios diarios",
                        "🎯 Problemas cotidianos: cocina, compras, etc."
                    ]
                }
            }
        }
        
        # Personalizar según patrones del usuario
        duracion_recomendada = 30
        if self.patrones_estudio["duracion_promedio"] > 0:
            duracion_recomendada = min(60, max(20, self.patrones_estudio["duracion_promedio"]))
        
        plan_base = planes_ia.get(tema.lower(), {}).get(nivel, {
            "objetivos": [f"Dominar los fundamentos de {tema}", f"Aplicar {tema} en proyectos reales"],
            "recursos_personalizados": [f"Buscar cursos especializados en {tema}"]
        })
        
        # Agregar recomendaciones personalizadas
        plan_personalizado = {
            "tema": tema,
            "nivel": nivel,
            "duracion_recomendada": duracion_recomendada,
            "objetivos": plan_base.get("objetivos", []),
            "recursos": plan_base.get("recursos_personalizados", []),
            "horario_sugerido": self.recomendar_horario_optimo(usuario_id),
            "tips_personalizados": self.generar_recomendaciones_personalizadas(usuario_id)[:3]
        }
        
        return plan_personalizado