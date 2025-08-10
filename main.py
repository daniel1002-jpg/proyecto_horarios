#!/usr/bin/env python3

import horarios

def main():
    try:
        data = horarios.read_horarios("data/horarios.json")
        horarios.validate_format(data)
        organized_data = horarios.organize_horarios(data)
        horarios.generate_html(organized_data, "output/horario.html")
    
        print("✅ Horario HTML generado exitosamente en output/horario.html")
        
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo data/horarios.json")
    except (KeyError, ValueError) as e:
        print(f"❌ Error en formato de datos: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
