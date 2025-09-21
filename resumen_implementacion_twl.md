# 🔧 Resumen Específico: Implementación del Plot t-W-L en tu Pipeline `@src/`

## 📂 Estructura de Archivos Modificados

### 1. `src/analysis/twl_map.py` - Módulo Principal

```python
# Funciones principales implementadas:
- generate_twl_map_for_window()     # Generación completa del mapa t-W-L
- _calculate_optimal_w_range()      # Cálculo automático de rangos W
- twl_occupancy_to_detection_tensor() # Conversión a tensor RGB para CenterNet
- create_twl_detection_plot()       # Visualización con bounding boxes
- _plot_save()                      # Guardado de plots PNG
- _resize_and_clip()                # Procesamiento de imagen
```

### 2. `src/core/high_freq_pipeline.py` - Pipeline de Alta Frecuencia

```python
# Modificaciones clave:
- hybrid_detect_and_classify_candidates_in_band()  # Detección híbrida TWL
- Integración de twl_occupancy_to_detection_tensor()
- Fallback automático SNR cuando TWL falla
- Generación obligatoria de plots TWL
- Cambio de np.logspace a np.geomspace para W_ms
```

### 3. `src/core/pipeline.py` - Orquestador Principal

```python
# Actualización:
- _process_file_chunked_high_freq() ahora recibe det_model
- Integración completa con detección híbrida
```

### 4. `src/config/user_config.py` - Configuración

```python
# Nuevo parámetro agregado:
TWL_HYBRID_DETECTION: bool = True  # Activa/desactiva detección híbrida
```

### 5. `src/config/config.py` - Configuración Global

```python
# Exposición del parámetro:
TWL_HYBRID_DETECTION = user_config.TWL_HYBRID_DETECTION
```

## 🔄 Flujo de Procesamiento Implementado

### Pipeline de Alta Frecuencia:

```
1. Verificación TWL_HYBRID_DETECTION
2. Generación de mapa t-W-L con generate_twl_map_for_window()
3. Conversión a tensor RGB 512×512 con twl_occupancy_to_detection_tensor()
4. Detección con CenterNet usando el tensor TWL
5. Si falla → Fallback a SNR tradicional
6. Clasificación binaria de candidatos
7. Generación de plots con create_twl_detection_plot()
```

### Pipeline Clásico (Frecuencias Bajas):

```
1. Verificación de disponibilidad de datos Stokes
2. Generación de mapa t-W-L (si hay Q,U disponibles)
3. Manejo de errores cuando POL_TYPE=INTEN, NPOL=1
4. Generación de plots en carpeta individual_plots/
```

## 📊 Productos Generados

### Archivos de Salida:

- **PNG**: `*_twl.png` - Visualizaciones del mapa t-W-L
- **NPZ**: `*_twl.npz` - Datos estructurados con métricas
- **Plots de detección**: Con bounding boxes para candidatos híbridos

### Estructura de Datos NPZ:

```python
{
    'OCCUP': occupancy_map,      # Mapa de ocupación de banda
    'COHERENCE': coherence_map,  # Mapa de coherencia espectral
    'SNR': snr_series,          # Serie temporal de SNR
    'W_ms': W_ms,              # Vector de anchos en ms
    't_ms': t_ms,              # Vector de tiempos en ms
    'metadata': {...}          # Metadatos del procesamiento
}
```

## 🎯 Características Técnicas Implementadas

### 1. Cálculo Automático de Rangos:

```python
def _calculate_optimal_w_range(slice_duration_ms):
    # Calcula W_min_ms y W_max_ms automáticamente
    # Basado en duración del slice y resolución temporal
    w_min_ms = max(0.1, slice_duration_ms * 0.001)
    w_max_ms = min(300.0, slice_duration_ms * 0.1)
    return w_min_ms, w_max_ms
```

### 2. Detección Híbrida:

```python
def twl_occupancy_to_detection_tensor(occupancy_map):
    # Convierte mapa 2D t-W a tensor RGB 512×512
    # Compatible con CenterNet para detección
    # Normalización y redimensionamiento automático
```

### 3. Manejo Robusto de Errores:

```python
# Manejo de StokesUnavailableError
# Manejo de All-NaN slices
# Fallback automático a SNR tradicional
# Validación de tipos de datos FITS
```

## ⚙️ Configuraciones Específicas

### Parámetros TWL en user_config.py:

```python
TWL_WINDOW_MS = 1000.0        # Ventana temporal
TWL_STRIDE_MS = 500.0         # Solapamiento
TWL_N_SUBBANDS = 4            # Sub-bandas
TWL_W_MIN_MS = 0.1            # Ancho mínimo
TWL_W_MAX_MS = 300.0          # Ancho máximo
TWL_K_UMBRAL = 5.0            # Umbral SNR
TWL_CLIP_P_LO = 1.0           # Percentil inferior
TWL_CLIP_P_HI = 99.0          # Percentil superior
TWL_RESIZE_PX = 512           # Resolución de salida
TWL_SAVE_OCCUPANCY = True     # Guardar ocupación
TWL_SAVE_COHERENCE = True     # Guardar coherencia
```

## 📈 Resultados en tu Pipeline

### Integración Exitosa:

- ✅ **Pipeline de alta frecuencia**: Funcionamiento completo con detección híbrida
- ✅ **Pipeline clásico**: Extensión para frecuencias bajas
- ✅ **Detección híbrida**: Prueba de concepto exitosa con CenterNet
- ✅ **Sistema robusto**: Manejo de errores y fallbacks automáticos
- ✅ **Visualizaciones**: Plots PNG generados correctamente
- ✅ **Datos estructurados**: Archivos NPZ con métricas completas

### Archivos Generados en @src/output/:

```
individual_plots/
├── *_twl.png              # Mapas t-W-L visualizados
├── *_twl_detection.png    # Plots con bounding boxes
└── *_twl.npz              # Datos estructurados
```

## 🐛 Problemas Resueltos Durante la Implementación

### 1. Errores de Tipos:

- **TypeError**: `'>' not supported between instances of 'str' and 'int'`
- **Solución**: Casting estricto de tipos para valores del header FITS

### 2. Problemas de Renderizado:

- **KeyboardInterrupt**: En `scipy.ndimage.median_filter`
- **Solución**: Reemplazo con cálculo custom de mediana y MAD por bloques

### 3. Generación de Plots:

- **Problema**: Solo se generaban archivos .npz, no imágenes PNG
- **Solución**: Movimiento de generación de plots fuera de bloques condicionales

### 4. Rango de Anchos Limitado:

- **Problema**: Eje W limitado hasta ~100ms
- **Solución**: Implementación de `_calculate_optimal_w_range()` para cálculo automático

## 🎨 Características Visuales Implementadas

- **Morfología "bow-tie"**: Contraste mejorado alrededor del ancho óptimo
- **Franjas de ocupación**: Bandas brillantes que indican actividad de pulso
- **Contornos y curvas**: Wmax(t) support curve para análisis visual
- **Colormap científico**: Viridis con normalización adaptativa

## 🚀 Impacto Final

El sistema t-W-L ahora proporciona una **nueva dimensión de detección** basada en propiedades de polarización, especialmente valiosa en regímenes de alta frecuencia donde las firmas dispersivas tradicionales se atenúan. La implementación híbrida con CenterNet establece las bases para futuras mejoras en detección automática de FRBs.

## 📌 Notas Adicionales

### Documentación:

- Se han añadido comentarios detallados en el código para facilitar el mantenimiento
- La implementación está completamente integrada en el pipeline existente
- Los parámetros son configurables a través de `user_config.py`

### Próximos Pasos Sugeridos:

- Evaluar la posibilidad de integrar opciones interactivas en el plot
- Considerar la implementación de pruebas unitarias específicas
- Explorar optimizaciones adicionales para el procesamiento de datos grandes
