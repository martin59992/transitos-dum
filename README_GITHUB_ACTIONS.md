# 🌟 Sistema de Efemérides Automáticas

## ¿Cómo funciona?

Este dashboard se actualiza **automáticamente cada día** con posiciones planetarias reales usando **GitHub Actions**.

---

## 📦 Archivos que tenés que subir

Subí **todos** estos archivos a tu repositorio GitHub:

```
transitos-dum/
├── .github/
│   └── workflows/
│       └── actualizar-efemerides.yml    ← GitHub Actions config
├── index.html                            ← Dashboard
├── interpretaciones.json                 ← 455 interpretaciones
├── efemerides_actuales.json             ← Efemérides del día (se actualiza solo)
└── actualizar_efemerides.py             ← Script de actualización
```

---

## 🚀 Configuración en GitHub (solo una vez)

### 1. Subir archivos

Subí todos los archivos listados arriba a tu repo.

### 2. Habilitar GitHub Actions

1. Andá a tu repo: `https://github.com/martin59992/transitos-dum`
2. Click en **Settings** → **Actions** → **General**
3. En "Workflow permissions", seleccioná:
   - ✅ **Read and write permissions**
4. Click en **Save**

### 3. Ejecutar por primera vez

1. Andá a la pestaña **Actions**
2. Click en **Actualizar Efemérides Diarias** (en el menú izquierdo)
3. Click en **Run workflow** → **Run workflow**
4. Esperá 1-2 minutos

¡Listo! Ahora se ejecutará **automáticamente cada día a las 00:00 UTC**.

---

## ✅ Verificar que funciona

1. Andá a **Actions** en tu repo
2. Deberías ver el workflow ejecutándose (punto amarillo 🟡)
3. Cuando termina: punto verde ✅
4. El archivo `efemerides_actuales.json` se actualiza automáticamente

---

## 🔧 ¿Cómo obtiene las efemérides?

El script intenta en orden:

1. **Astro-Seek API** (gratis, sin autenticación)
2. **Astronomy API** (opcional, requiere credenciales)
3. **Cálculo astronómico** (fallback si las APIs fallan)

### Para mejorar la precisión (opcional):

Si querés usar APIs más precisas, podés conseguir credenciales gratis en:
- https://astronomyapi.com (50 llamadas/día gratis)

Agregá las credenciales como **GitHub Secrets**:
1. Settings → Secrets → Actions
2. New repository secret:
   - `ASTRONOMY_API_ID`
   - `ASTRONOMY_API_SECRET`

---

## 📅 Frecuencia de actualización

- **Automática**: Todos los días a las 00:00 UTC
- **Manual**: Podés ejecutarlo cuando quieras desde Actions → Run workflow

---

## 🐛 Troubleshooting

### El workflow no se ejecuta
- Verificá que GitHub Actions esté habilitado
- Verificá que tenga permisos de escritura

### El archivo no se actualiza
- Revisá los logs en Actions
- Verificá que el script tenga permisos para hacer commit

### Las APIs fallan
- El fallback astronómico siempre funciona
- Precisión: ±1-2° (suficiente para tránsitos)

---

## 🎯 Resultado

Tu dashboard ahora:
✅ Se actualiza solo cada día
✅ Usa posiciones planetarias reales
✅ No requiere mantenimiento manual
✅ Funciona 24/7

