# main.py - Archivo principal del Asistente de Aprendizaje Gamificado
from assistant import AsistenteAprendizaje
import os
import platform

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    sistema = platform.system()
    if sistema == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def mostrar_banner():
    print("🎮" + "="*50 + "🎮")
    print("🎓 ASISTENTE DE APRENDIZAJE ADAPTATIVO 🎓")
    print("💫 ¡Ahora con Sistema de Gamificación! 💫")
    print("🎮" + "="*50 + "🎮")

def mostrar_menu():
    print("\n📋 ¿Qué quieres hacer hoy?")
    print("┌─────────────────────────────────────────┐")
    print("│ 1. 👤 Crear perfil de usuario          │")
    print("│ 2. 📚 Generar plan de estudio          │")
    print("│ 3. 📊 Ver progreso y estadísticas      │")
    print("│ 4. ⏰ Registrar sesión de estudio      │")
    print("│ 5. 🏆 Ver mis logros y puntos          │")
    print("│ 6. 🤖 Centro de IA (NUEVO)             │")
    print("│ 7. 🚪 Salir                            │")
    print("└─────────────────────────────────────────┘")

def mostrar_consejos():
    consejos = [
        "💡 Consejo: Estudia a la misma hora cada día para crear hábito",
        "🔥 Tip: Las rachas de estudio te dan más puntos",
        "⭐ Dato: Puedes ganar logros especiales estudiando temprano o tarde",
        "🎯 Truco: Sesiones más largas dan más puntos, pero la constancia es clave",
        "🏆 Meta: Intenta mantener una racha de al menos 7 días seguidos"
    ]
    
    import random
    print(f"\n{random.choice(consejos)}")

def main():
    limpiar_pantalla()  # Limpiar al iniciar
    mostrar_banner()
    print("🌟 ¡Bienvenido a tu asistente personal de aprendizaje!")
    print("🎮 Gana puntos, desbloquea logros y sube de nivel mientras aprendes")
    
    asistente = AsistenteAprendizaje()
    
    # Mostrar resumen rápido si hay usuarios
    if asistente.datos["usuarios"]:
        print(f"\n📊 Tienes {len(asistente.datos['usuarios'])} usuario(s) registrado(s)")
        print(f"📚 {len(asistente.datos['planes'])} plan(es) de estudio activo(s)")
        print(f"⏰ {len(asistente.datos['sesiones'])} sesión(es) completada(s)")
    
    while True:
        try:
            mostrar_menu()
            mostrar_consejos()
            
            opcion = input("\n🎯 Elige una opción (1-7): ").strip()
            
            # Limpiar pantalla antes de mostrar cada opción
            limpiar_pantalla()
            
            if opcion == "1":
                mostrar_banner()
                print("👤 CREAR NUEVO PERFIL DE USUARIO")
                print("="*40)
                asistente.crear_usuario()
                
            elif opcion == "2":
                mostrar_banner()
                print("📚 GENERAR PLAN DE ESTUDIO")
                print("="*40)
                asistente.crear_plan_estudio()
                
            elif opcion == "3":
                mostrar_banner()
                print("📊 PROGRESO Y ESTADÍSTICAS")
                print("="*40)
                asistente.mostrar_progreso()
                
            elif opcion == "4":
                mostrar_banner()
                print("⏰ REGISTRAR SESIÓN DE ESTUDIO")
                print("="*40)
                asistente.registrar_sesion()
                
            elif opcion == "5":
                mostrar_banner()
                print("🏆 CENTRO DE LOGROS Y PUNTOS")
                print("="*40)
                asistente.mostrar_logros()
                
            elif opcion == "6":
                mostrar_banner()
                print("🤖 CENTRO DE INTELIGENCIA ARTIFICIAL")
                print("="*40)
                asistente.menu_ia_avanzado()
                
            elif opcion == "7":
                limpiar_pantalla()
                mostrar_banner()
                print("🎉 ¡Excelente trabajo!")
                print("💪 ¡Sigue estudiando para desbloquear más logros!")
                print("🌟 Recuerda: La constancia es la clave del éxito")
                print("🤖 ¡La IA estará aquí para ayudarte siempre!")
                print("👋 ¡Hasta la próxima!")
                
                # Mensaje personalizado si hay datos
                if asistente.datos["sesiones"]:
                    total_tiempo = sum(s["duracion"] for s in asistente.datos["sesiones"])
                    print(f"📊 Has estudiado un total de {total_tiempo} minutos. ¡Increíble!")
                
                break
                
            else:
                mostrar_banner()
                print("❌ Opción inválida. Por favor elige un número del 1 al 7.")
                
            # Pausa para que el usuario pueda leer los resultados
            input("\n⏸️ Presiona ENTER para volver al menú principal...")
                
        except KeyboardInterrupt:
            limpiar_pantalla()
            mostrar_banner()
            print("🛑 Interrupción detectada")
            print("👋 ¡Hasta luego! ¡Sigue aprendiendo!")
            break
            
        except Exception as e:
            limpiar_pantalla()
            mostrar_banner()
            print(f"❌ Error inesperado: {e}")
            print("💡 Intenta de nuevo o verifica que todos los archivos estén correctos")
            
            # Opción para continuar o salir en caso de error
            continuar = input("\n¿Quieres continuar? (s/n): ").lower().strip()
            if continuar != 's':
                break

def mostrar_ayuda():
    """Función para mostrar ayuda sobre cómo usar el asistente"""
    print("\n📖 GUÍA RÁPIDA DE USO:")
    print("1. Primero crea tu perfil de usuario")
    print("2. Genera un plan de estudio para el tema que quieras")
    print("3. Registra sesiones de estudio para ganar puntos")
    print("4. Ve tu progreso y estadísticas para mantenerte motivado")
    print("5. Desbloquea logros estudiando consistentemente")
    print("6. ¡Usa el Centro de IA para recomendaciones personalizadas!")
    print("\n🎯 Consejos para maximizar puntos:")
    print("• Estudia todos los días para mantener rachas")
    print("• Sesiones más largas = más puntos")
    print("• Alta satisfacción (8-10) = puntos bonus")
    print("• Estudia temprano (antes 8am) o tarde (después 10pm) para logros especiales")

if __name__ == "__main__":
    main()