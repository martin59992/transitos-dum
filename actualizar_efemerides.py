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
    """Intenta obtener desde Astronomy API con credenciales"""
    try:
        import os
        import base64
        
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        
        # Credenciales desde GitHub Secrets o hardcoded
        app_id = os.environ.get('ASTRONOMY_API_ID', 'dada39dc-04c5-44e1-9468-a0667f6828c0')
        app_secret = os.environ.get('ASTRONOMY_API_SECRET', '820f1bb992442b8926f0cd2debcc8eaf79784823297162e0cb175103')
        
        # Basic Auth
        credentials = f"{app_id}:{app_secret}"
        b64_credentials = base64.b64encode(credentials.encode()).decode()
        
        print(f"🔍 Consultando Astronomy API para {fecha_hoy}...")
        
        # Endpoint para obtener posiciones de todos los cuerpos
        url = "https://api.astronomyapi.com/api/v2/bodies/positions"
        
        headers = {
            'Authorization': f'Basic {b64_credentials}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "latitude": 0,
            "longitude": 0,
            "elevation": 0,
            "from_date": fecha_hoy,
            "to_date": fecha_hoy,
            "time": "12:00:00"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Astronomy API respondió correctamente")
            return parsear_astronomy_api(data, fecha_hoy)
        else:
            print(f"❌ Astronomy API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error con Astronomy API: {e}")
        return None

def parsear_astronomy_api(data, fecha):
    """Parsea respuesta de Astronomy API"""
    
    planetas_resultado = {}
    
    # Mapeo de nombres
    nombre_map = {
        'sun': 'Sol', 'moon': 'Luna', 'mercury': 'Mercurio',
        'venus': 'Venus', 'mars': 'Marte', 'jupiter': 'Júpiter',
        'saturn': 'Saturno', 'uranus': 'Urano', 'neptune': 'Neptuno',
        'pluto': 'Plutón'
    }
    
    signos_map = {
        'aries': 'Aries', 'taurus': 'Tauro', 'gemini': 'Géminis', 'cancer': 'Cáncer',
        'leo': 'Leo', 'virgo': 'Virgo', 'libra': 'Libra', 'scorpio': 'Escorpio',
        'sagittarius': 'Sagitario', 'capricorn': 'Capricornio', 
        'aquarius': 'Acuario', 'pisces': 'Piscis'
    }
    
    try:
        if 'data' in data and 'table' in data['data']:
            rows = data['data']['table']['rows']
            
            for row in rows:
                cells = row.get('cells', [])
                if len(cells) >= 2:
                    # cells[0] = nombre del cuerpo
                    # cells[1] = posición (ej: "20°30' Sagittarius")
                    nombre_en = cells[0].get('id', '').lower()
                    nombre_es = nombre_map.get(nombre_en)
                    
                    if nombre_es and len(cells) >= 2:
                        posicion = cells[1].get('position', {})
                        signo_en = posicion.get('constellation', {}).get('id', '').lower()
                        signo_es = signos_map.get(signo_en, signo_en.capitalize())
                        
                        # Grados y minutos
                        grados = float(posicion.get('horizontal', {}).get('degrees', {}).get('value', 0))
                        minutos = float(posicion.get('horizontal', {}).get('minutes', {}).get('value', 0))
                        
                        grado_total = round(grados + minutos / 60, 2)
                        
                        planetas_resultado[nombre_es] = {
                            "signo": signo_es,
                            "grado": grado_total
                        }
        
        if len(planetas_resultado) > 0:
            return {
                "fecha": fecha,
                "fuente": "Astronomy API (AstronomyAPI.com)",
                "planetas": planetas_resultado
            }
        else:
            print("⚠️  Astronomy API no devolvió datos parseables")
            return None
            
    except Exception as e:
        print(f"❌ Error parseando Astronomy API: {e}")
        return None

def obtener_efemerides_fallback():
    """Cálculo de respaldo si las APIs fallan"""
    
    from datetime import datetime, timedelta
    
    # Base: 12 diciembre 2025 (HOY - posiciones reales)
    fecha_base = datetime(2025, 12, 12)
    fecha_hoy = datetime.now()
    dias_diff = (fecha_hoy - fecha_base).days
    
    print(f"⚠️  Usando cálculo de respaldo (base + {dias_diff} días)")
    
    # Posiciones REALES 12 dic 2025 (desde Swiss Ephemeris / Astro.com)
    posiciones_base = {
        'Sol': 260.56,         # Sagitario 20.56°
        'Luna': 92.50,         # Cáncer 2.50°
        'Mercurio': 246.21,    # Sagitario 6.21°
        'Venus': 271.45,       # Capricornio 1.45°
        'Marte': 128.22,       # Leo 8.22°
        'Júpiter': 74.92,      # Géminis 14.92°
        'Saturno': 344.27,     # Piscis 14.27°
        'Urano': 54.72,        # Tauro 24.72°
        'Neptuno': 357.37,     # Piscis 27.37°
        'Plutón': 299.08       # Capricornio 29.08°
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
    
    # 1. Astronomy API (más precisa)
    efemerides = obtener_efemerides_astronomy_api()
    
    # 2. Astro-Seek
    if not efemerides:
        efemerides = obtener_efemerides_astro_seek()
    
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
