#!/usr/bin/env python3
"""
Script para obtener efemérides reales desde Astronomy API
Según documentación oficial: https://docs.astronomyapi.com/
"""

import requests
import json
from datetime import datetime
import sys
import base64

def obtener_efemerides_astronomy_api():
    """
    Astronomy API - Formato correcto según documentación oficial
    https://docs.astronomyapi.com/
    """
    try:
        import os
        
        fecha_hoy = datetime.now()
        
        # Credenciales
        app_id = os.environ.get('ASTRONOMY_API_ID', 'dada39dc-04c5-44e1-9468-a0667f6828c0')
        app_secret = os.environ.get('ASTRONOMY_API_SECRET', '820f1bb992442b8926f0cd2debcc8eaf79784823297162e0cb175103')
        
        print(f"🔍 Consultando Astronomy API para {fecha_hoy.strftime('%Y-%m-%d')}...")
        print(f"   App ID: {app_id[:20]}...")
        
        # Formato correcto: Basic Auth con base64(app_id:app_secret)
        credentials = f"{app_id}:{app_secret}"
        b64_credentials = base64.b64encode(credentials.encode()).decode()
        
        # Endpoint correcto según documentación
        url = "https://api.astronomyapi.com/api/v2/bodies/positions"
        
        headers = {
            'Authorization': f'Basic {b64_credentials}'
        }
        
        # Body en formato JSON (POST request)
        payload = {
            "style": "default",
            "observer": {
                "latitude": 0,
                "longitude": 0,
                "date": fecha_hoy.strftime("%Y-%m-%d")
            },
            "view": {
                "type": "constellation",
                "parameters": {
                    "constellation": "*"
                }
            }
        }
        
        print(f"   Enviando request POST...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"   Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Astronomy API respondió correctamente")
            return parsear_astronomy_api(data, fecha_hoy.strftime('%Y-%m-%d'))
        else:
            print(f"   ❌ Error: {response.text[:300]}")
            return None
            
    except Exception as e:
        print(f"❌ Error con Astronomy API: {e}")
        import traceback
        traceback.print_exc()
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
        print(f"   Parseando respuesta...")
        
        # La estructura puede variar según el endpoint
        if 'data' in data:
            if 'table' in data['data']:
                # Formato tabla
                rows = data['data']['table']['rows']
                
                for row in rows:
                    entry = row.get('entry', {})
                    cells = row.get('cells', [])
                    
                    if len(cells) >= 2:
                        nombre_en = cells[0].get('id', '').lower()
                        nombre_es = nombre_map.get(nombre_en)
                        
                        if nombre_es:
                            # Obtener posición
                            position_cell = cells[1] if len(cells) > 1 else {}
                            position = position_cell.get('position', {})
                            
                            # Constelación/Signo
                            constellation = position.get('constellation', {})
                            signo_en = constellation.get('id', '').lower()
                            signo_es = signos_map.get(signo_en, signo_en.capitalize())
                            
                            # Grados
                            horizontal = position.get('horizontal', {})
                            degrees_obj = horizontal.get('degrees', {})
                            minutes_obj = horizontal.get('minutes', {})
                            
                            grados = float(degrees_obj.get('value', 0))
                            minutos = float(minutes_obj.get('value', 0))
                            
                            grado_total = round(grados + minutos / 60, 2)
                            
                            planetas_resultado[nombre_es] = {
                                "signo": signo_es,
                                "grado": grado_total
                            }
                            
                            print(f"   Parseado: {nombre_es} en {signo_es} {grado_total}°")
        
        if len(planetas_resultado) >= 5:  # Al menos 5 planetas
            return {
                "fecha": fecha,
                "fuente": "Astronomy API (AstronomyAPI.com)",
                "planetas": planetas_resultado
            }
        else:
            print(f"   ⚠️  Solo se parsearon {len(planetas_resultado)} planetas")
            return None
            
    except Exception as e:
        print(f"   ❌ Error parseando: {e}")
        import traceback
        traceback.print_exc()
        return None

def obtener_efemerides_fallback():
    """Cálculo de respaldo"""
    
    from datetime import datetime
    
    fecha_base = datetime(2025, 12, 12)
    fecha_hoy = datetime.now()
    dias_diff = (fecha_hoy - fecha_base).days
    
    print(f"⚠️  Usando cálculo astronómico (base + {dias_diff} días)")
    
    posiciones_base = {
        'Sol': 260.56,
        'Luna': 92.50,
        'Mercurio': 246.21,
        'Venus': 271.45,
        'Marte': 128.22,
        'Júpiter': 74.92,
        'Saturno': 344.27,
        'Urano': 54.72,
        'Neptuno': 357.37,
        'Plutón': 299.08
    }
    
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
    
    # Intentar API
    efemerides = obtener_efemerides_astronomy_api()
    
    # Fallback si falla
    if not efemerides:
        print()
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
