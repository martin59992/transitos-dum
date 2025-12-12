#!/usr/bin/env python3
"""
Script para obtener efemérides reales desde APIs públicas
Ejecutado automáticamente por GitHub Actions cada día
"""

import requests
import json
from datetime import datetime
import sys

def obtener_efemerides_astro_seek():
    """Intenta obtener desde Astro-Seek API"""
    try:
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        url = f"https://widget.astro-seek.com/api/ephemeris?date={fecha_hoy}&latitude=0&longitude=0"
        
        print(f"🔍 Consultando Astro-Seek para {fecha_hoy}...")
        
        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; EfemeridesBot/1.0)',
            'Accept': 'application/json'
        })
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Astro-Seek respondió correctamente")
            return parsear_astro_seek(data, fecha_hoy)
        else:
            print(f"❌ Astro-Seek error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error con Astro-Seek: {e}")
        return None

def parsear_astro_seek(data, fecha):
    """Parsea respuesta de Astro-Seek"""
    
    planetas_resultado = {}
    
    # Mapeo de nombres
    nombre_map = {
        'Sun': 'Sol', 'Moon': 'Luna', 'Mercury': 'Mercurio',
        'Venus': 'Venus', 'Mars': 'Marte', 'Jupiter': 'Júpiter',
        'Saturn': 'Saturno', 'Uranus': 'Urano', 'Neptune': 'Neptuno',
        'Pluto': 'Plutón'
    }
    
    signo_map = {
        'Ari': 'Aries', 'Tau': 'Tauro', 'Gem': 'Géminis', 'Can': 'Cáncer',
        'Leo': 'Leo', 'Vir': 'Virgo', 'Lib': 'Libra', 'Sco': 'Escorpio',
        'Sag': 'Sagitario', 'Cap': 'Capricornio', 'Aqu': 'Acuario', 'Pis': 'Piscis'
    }
    
    if 'planets' in data:
        for planet in data['planets']:
            nombre_en = planet.get('name', '')
            nombre_es = nombre_map.get(nombre_en)
            
            if nombre_es:
                signo_corto = planet.get('sign', '')
                signo_es = signo_map.get(signo_corto, signo_corto)
                grado = float(planet.get('degree', 0))
                
                planetas_resultado[nombre_es] = {
                    "signo": signo_es,
                    "grado": round(grado, 2)
                }
    
    return {
        "fecha": fecha,
        "fuente": "Astro-Seek API",
        "planetas": planetas_resultado
    }

def obtener_efemerides_astronomy_api():
    """Intenta obtener desde Astronomy API (requiere credenciales)"""
    try:
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        
        # Esta API requiere autenticación (opcional si consigues credenciales)
        print("⚠️  Astronomy API requiere credenciales - saltando")
        return None
        
    except Exception as e:
        print(f"❌ Error con Astronomy API: {e}")
        return None

def obtener_efemerides_fallback():
    """Cálculo de respaldo si las APIs fallan"""
    
    from datetime import datetime, timedelta
    
    # Base: 11 diciembre 2025
    fecha_base = datetime(2025, 12, 11)
    fecha_hoy = datetime.now()
    dias_diff = (fecha_hoy - fecha_base).days
    
    print(f"⚠️  Usando cálculo de respaldo (base + {dias_diff} días)")
    
    # Posiciones base 11 dic 2025
    posiciones_base = {
        'Sol': 259.59,
        'Luna': 35.0,
        'Mercurio': 245.0,
        'Venus': 300.0,
        'Marte': 319.0,
        'Júpiter': 104.92,
        'Saturno': 356.27,
        'Urano': 58.72,
        'Neptuno': 359.37,
        'Plutón': 300.58
    }
    
    # Velocidades diarias
    velocidades = {
        'Sol': 0.9856,
        'Luna': 13.176,
        'Mercurio': 1.383,
        'Venus': 1.2,
        'Marte': 0.524,
        'Júpiter': 0.083,
        'Saturno': 0.033,
        'Urano': 0.012,
        'Neptuno': 0.006,
        'Plutón': 0.004
    }
    
    def grado_a_signo(grado_absoluto):
        signos = [
            'Aries', 'Tauro', 'Géminis', 'Cáncer', 'Leo', 'Virgo',
            'Libra', 'Escorpio', 'Sagitario', 'Capricornio', 'Acuario', 'Piscis'
        ]
        grado_normalizado = grado_absoluto % 360
        indice_signo = int(grado_normalizado // 30)
        grado_en_signo = grado_normalizado % 30
        return signos[indice_signo], round(grado_en_signo, 2)
    
    planetas_resultado = {}
    
    for planeta, grado_base in posiciones_base.items():
        grado_absoluto = (grado_base + velocidades[planeta] * dias_diff) % 360
        signo, grado = grado_a_signo(grado_absoluto)
        
        planetas_resultado[planeta] = {
            "signo": signo,
            "grado": grado
        }
    
    return {
        "fecha": fecha_hoy.strftime("%Y-%m-%d"),
        "fuente": "Cálculo astronómico (fallback)",
        "planetas": planetas_resultado
    }

def main():
    print("="*70)
    print("🌟 ACTUALIZACIÓN DE EFEMÉRIDES")
    print("="*70)
    print()
    
    # Intentar obtener efemérides (orden de prioridad)
    efemerides = None
    
    # 1. Astro-Seek
    efemerides = obtener_efemerides_astro_seek()
    
    # 2. Astronomy API
    if not efemerides:
        efemerides = obtener_efemerides_astronomy_api()
    
    # 3. Cálculo de respaldo
    if not efemerides:
        efemerides = obtener_efemerides_fallback()
    
    if not efemerides:
        print("❌ No se pudieron obtener efemérides")
        sys.exit(1)
    
    # Guardar
    output_file = 'efemerides_actuales.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(efemerides, f, ensure_ascii=False, indent=2)
    
    print()
    print("="*70)
    print("✅ EFEMÉRIDES ACTUALIZADAS")
    print("="*70)
    print(f"Fecha: {efemerides['fecha']}")
    print(f"Fuente: {efemerides['fuente']}")
    print(f"Archivo: {output_file}")
    print()
    print("Planetas:")
    for planeta, data in efemerides['planetas'].items():
        print(f"  {planeta:12s}: {data['signo']:12s} {data['grado']:6.2f}°")
    print()

if __name__ == "__main__":
    main()
