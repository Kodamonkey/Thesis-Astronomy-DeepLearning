#!/usr/bin/env python3
"""
Script para generar histograma de detecciones de FRB121102
Autor: Seba
Fecha: 2025
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict
import os

def create_frb121102_histogram():
    """
    Genera un histograma de las detecciones de FRB121102 por archivo de observación
    """
    
    # Datos de bursts confirmados por literatura (24 eventos)
    confirmed_literature = {
        '3096': 2,  # 564.15, 564.64
        '3098': 3,  # 564.77, 565.35, 563.5
        '3099': 2,  # 557.55, 564.17
        '3100': 10, # 565.38, 557.11, 563.91, 564.75, 563.87, 565.97, 564.96, 557.7, 563.53
        '3101': 5,  # 558.49, 557.92, 558.01, 566.12, 565.31
        '3102': 3   # 563.14, 556.67, 563.94, 556.01
    }
    
    # Datos de nuevos candidatos sin confirmar (15 eventos)
    candidates_unconfirmed = {
        '3096': 3,  # 579.6, 565.46, 484.19
        '3098': 3,  # 581.24, 571.6, 563.5
        '3099': 3,  # 411.4, 420.31, 396.29
        '3100': 2,  # 404.21, 260.22
        '3101': 2,  # 380.95, 555.9
        '3102': 2   # 564.79, 565.27
    }
    
    # Datos de nuevos eventos confirmados (2 eventos)
    new_confirmed = {
        '3096': 1,  # 563.6
        '3098': 0,
        '3099': 0,
        '3100': 0,
        '3101': 0,
        '3102': 1   # 564.88
    }
    
    # Archivos de observación
    files = ['3096', '3098', '3099', '3100', '3101', '3102']
    
    # Configurar el gráfico
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Posiciones de las barras
    x = np.arange(len(files))
    width = 0.25
    
    # Crear las barras
    bars1 = ax.bar(x - width, [confirmed_literature[f] for f in files], width, 
                   label='Confirmados por literatura', color='purple', alpha=0.8)
    bars2 = ax.bar(x, [candidates_unconfirmed[f] for f in files], width,
                   label='Candidatos sin confirmar', color='cyan', alpha=0.8)
    bars3 = ax.bar(x + width, [new_confirmed[f] for f in files], width,
                   label='Nuevos eventos confirmados', color='green', alpha=0.8)
    
    # Configurar el gráfico
    ax.set_xlabel('Archivo de Observación', fontsize=12, fontweight='bold')
    ax.set_ylabel('Número de Detecciones', fontsize=12, fontweight='bold')
    ax.set_title('Distribución de Detecciones de FRB121102 por Archivo de Observación\nPipeline DRAFTS++ vs Literatura', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(files, fontsize=11)
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Agregar valores en las barras
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            if height > 0:  # Solo mostrar valores mayores a 0
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                       f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    add_value_labels(bars1)
    add_value_labels(bars2)
    add_value_labels(bars3)
    
    # Configurar límites del eje Y
    ax.set_ylim(0, max([max(confirmed_literature.values()), 
                       max(candidates_unconfirmed.values()), 
                       max(new_confirmed.values())]) + 1)
    
    # Agregar estadísticas en el gráfico
    total_confirmed = sum(confirmed_literature.values())
    total_candidates = sum(candidates_unconfirmed.values())
    total_new = sum(new_confirmed.values())
    total_detections = total_confirmed + total_candidates + total_new
    
    stats_text = f'Total de detecciones: {total_detections}\n'
    stats_text += f'Confirmados por literatura: {total_confirmed}\n'
    stats_text += f'Candidatos sin confirmar: {total_candidates}\n'
    stats_text += f'Nuevos eventos confirmados: {total_new}'
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Ajustar layout
    plt.tight_layout()
    
    # Crear directorio figures si no existe
    os.makedirs('figures', exist_ok=True)
    
    # Guardar el gráfico
    plt.savefig('figures/frb121102_detection_histogram.png', dpi=300, bbox_inches='tight')
    plt.savefig('figures/frb121102_detection_histogram.pdf', bbox_inches='tight')
    
    print("✅ Histograma generado exitosamente:")
    print("   - figures/frb121102_detection_histogram.png")
    print("   - figures/frb121102_detection_histogram.pdf")
    print(f"\n📊 Estadísticas:")
    print(f"   - Total de detecciones: {total_detections}")
    print(f"   - Confirmados por literatura: {total_confirmed}")
    print(f"   - Candidatos sin confirmar: {total_candidates}")
    print(f"   - Nuevos eventos confirmados: {total_new}")
    
    return fig

def create_summary_table():
    """
    Crea una tabla resumen de los datos para verificación
    """
    print("\n📋 Tabla resumen de detecciones por archivo:")
    print("=" * 60)
    print(f"{'Archivo':<8} {'Literatura':<12} {'Candidatos':<12} {'Confirmados':<12} {'Total':<8}")
    print("-" * 60)
    
    files = ['3096', '3098', '3099', '3100', '3101', '3102']
    confirmed_literature = {'3096': 2, '3098': 3, '3099': 2, '3100': 10, '3101': 5, '3102': 3}
    candidates_unconfirmed = {'3096': 3, '3098': 3, '3099': 3, '3100': 2, '3101': 2, '3102': 2}
    new_confirmed = {'3096': 1, '3098': 0, '3099': 0, '3100': 0, '3101': 0, '3102': 1}
    
    for file in files:
        lit = confirmed_literature[file]
        cand = candidates_unconfirmed[file]
        new = new_confirmed[file]
        total = lit + cand + new
        print(f"{file:<8} {lit:<12} {cand:<12} {new:<12} {total:<8}")
    
    print("-" * 60)
    print(f"{'TOTAL':<8} {sum(confirmed_literature.values()):<12} {sum(candidates_unconfirmed.values()):<12} {sum(new_confirmed.values()):<12} {sum(confirmed_literature.values()) + sum(candidates_unconfirmed.values()) + sum(new_confirmed.values()):<8}")

if __name__ == "__main__":
    print("🚀 Generando histograma de detecciones de FRB121102...")
    
    # Crear el histograma
    fig = create_frb121102_histogram()
    
    # Mostrar tabla resumen
    create_summary_table()
    
    print("\n✅ Proceso completado exitosamente!")
    print("📁 Los archivos se guardaron en el directorio 'figures/'")
