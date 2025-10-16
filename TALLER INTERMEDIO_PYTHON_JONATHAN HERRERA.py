#!/usr/bin/env python
# coding: utf-8

# ==============================================================
# MAPA SST NICARAGUA - ATLAS (CON TODOS LOS RÍOS)
# ==============================================================

import numpy as np
import matplotlib.pyplot as plt
import cmocean
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os

# --------------------------------------------------------------
# CONFIGURACIÓN DE ZONA
# --------------------------------------------------------------
dominio = [-87.0, -82.0, 10.5, 15.0]
zona = 'Nicaragua'
nombre_png = "SST_Nicaragua_ATLAS_RIOS_COMPLETOS.png"
nombre_pdf = "INFORME_SST_Nicaragua.pdf"

print("Zona:", zona)
print("Dominio:", dominio)

# --------------------------------------------------------------
# GRID DE LAT/LON
# --------------------------------------------------------------
lon = np.linspace(dominio[0], dominio[1], 600)
lat = np.linspace(dominio[2], dominio[3], 600)
lon2d, lat2d = np.meshgrid(lon, lat)

# --------------------------------------------------------------
# DATOS SINTÉTICOS DE TEMPERATURA
# --------------------------------------------------------------
sst = 27 + (lat2d - dominio[2]) / (dominio[3]-dominio[2]) * 3
sst += 0.5 * np.sin(5 * (lon2d - dominio[0]) / (dominio[1]-dominio[0]) * np.pi) \
       * np.cos(5 * (lat2d - dominio[2]) / (dominio[3]-dominio[2]) * np.pi)

# --------------------------------------------------------------
# RELIEVE SINTÉTICO (sombras)
# --------------------------------------------------------------
relieve = 0.3 * np.sin(3*(lon2d-dominio[0])) * np.cos(3*(lat2d-dominio[2]))

# --------------------------------------------------------------
# MAPA CON CARTOPY
# --------------------------------------------------------------
fig = plt.figure(figsize=(14,10))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent(dominio, crs=ccrs.PlateCarree())

# Tierra y océano
ax.add_feature(cfeature.LAND, facecolor='whitesmoke')
ax.add_feature(cfeature.OCEAN, facecolor='lightcyan')
ax.add_feature(cfeature.COASTLINE, linewidth=1, edgecolor='black')
ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='gray')

# Cuadrícula y etiquetas
gl = ax.gridlines(draw_labels=True, linestyle='--', color='gray', alpha=0.5)
gl.top_labels = False
gl.right_labels = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

# --------------------------------------------------------------
# PLOTEO DE SST CON SOMBREADO
# --------------------------------------------------------------
img = ax.pcolormesh(lon2d, lat2d, sst+relieve, cmap=cmocean.cm.thermal, vmin=26, vmax=30)
cbar = plt.colorbar(img, ax=ax, orientation='vertical', label='Temperatura superficial (°C)', pad=0.02)

# --------------------------------------------------------------
# CIUDADES PRINCIPALES
# --------------------------------------------------------------
ciudades = {
    "Managua": (-86.2419, 12.1364),
    "León": (-86.3419, 12.4379),
    "Granada": (-85.9496, 11.9299),
    "Masaya": (-86.0967, 11.9686),
    "Bluefields": (-83.7746, 12.0072)
}

for nombre, (lon_c, lat_c) in ciudades.items():
    ax.plot(lon_c, lat_c, 'ko', markersize=6, transform=ccrs.PlateCarree())
    ax.text(lon_c + 0.03, lat_c + 0.03, nombre, fontsize=11, weight='bold',
            transform=ccrs.PlateCarree(), ha='left', va='bottom')

# --------------------------------------------------------------
# LAGOS
# --------------------------------------------------------------
lagos = {
    "Lago Xolotlán": [-86.4, -86.1, 12.9, 13.2],
    "Lago Cocibolca": [-85.9, -85.0, 10.9, 11.8]
}

for nombre, (lon_min, lon_max, lat_min, lat_max) in lagos.items():
    rect_lon = [lon_min, lon_max, lon_max, lon_min, lon_min]
    rect_lat = [lat_min, lat_min, lat_max, lat_max, lat_min]
    ax.plot(rect_lon, rect_lat, color='blue', linewidth=2, transform=ccrs.PlateCarree())
    ax.text((lon_min+lon_max)/2, (lat_min+lat_max)/2, nombre,
            color='blue', fontsize=10, weight='bold', ha='center', va='center',
            transform=ccrs.PlateCarree())

# --------------------------------------------------------------
# RÍOS PRINCIPALES COMPLETOS
# --------------------------------------------------------------
rios = {
    "Río Coco": [(-85.8, 15), (-84.5, 14.8), (-83, 15)],
    "Río Grande de Matagalpa": [(-86, 13.5), (-85.5, 13), (-85, 12.5)],
    "Río San Juan": [(-85.9, 11.2), (-84.7, 11.2), (-83.5, 11.2)],
    "Río Escondido": [(-85.0, 12.5), (-84.3, 12.1), (-83.8, 12.2)],
    "Río Tipitapa": [(-86.3, 12.2), (-86.1, 12.1), (-86.0, 12.1)],
    "Río Viejo": [(-86.5, 11.5), (-86.0, 11.3), (-85.6, 11.2)],
    "Río Yalagüina": [(-86.7, 13.0), (-86.3, 12.7), (-86.0, 12.6)]
}

for nombre, coords in rios.items():
    lon_r, lat_r = zip(*coords)
    ax.plot(lon_r, lat_r, color='blue', linewidth=2, linestyle='-', transform=ccrs.PlateCarree())
    ax.text(np.mean(lon_r), np.mean(lat_r), nombre, color='blue', fontsize=9,
            transform=ccrs.PlateCarree(), ha='center', va='bottom')

# --------------------------------------------------------------
# BARRA DE ESCALA MANUAL
# --------------------------------------------------------------
lon0, lat0 = dominio[0] + 0.25, dominio[2] + 0.25
ax.plot([lon0, lon0+0.5], [lat0, lat0], 'k-', linewidth=4, transform=ccrs.PlateCarree())
ax.text(lon0 + 0.25, lat0 - 0.05, '50 km', fontsize=11, ha='center', transform=ccrs.PlateCarree())

# --------------------------------------------------------------
# TÍTULO Y GUARDADO
# --------------------------------------------------------------
ax.set_title(f"Temperatura Superficial - {zona} (Atlas )", fontsize=18, weight='bold')
plt.tight_layout()
plt.savefig(nombre_png, dpi=600)
plt.close()

print(f"\n✅ Mapa Atlas generado y guardado como: {nombre_png}")

# --------------------------------------------------------------
# GENERAR INFORME EN PDF
# --------------------------------------------------------------
styles = getSampleStyleSheet()
doc = SimpleDocTemplate(nombre_pdf, pagesize=letter)
story = []

fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

titulo = f"Informe de Temperatura Superficial del Mar (SST)  - {zona} -Taller intermedio OCEAN HACK WEEK- 2025"
story.append(Paragraph(titulo, styles['Title']))
story.append(Spacer(1, 12))

story.append(Paragraph(f"<b>Fecha de generación:</b> {fecha_actual}", styles['Normal']))
story.append(Paragraph(f"<b>Dominio:</b> {dominio}", styles['Normal']))
story.append(Paragraph("<b>Resolución:</b> 600x600 puntos", styles['Normal']))
story.append(Paragraph("<b>Fuente:</b> Datos sintéticos para demostración (Atlas)", styles['Normal']))
story.append(Spacer(1, 12))

story.append(Paragraph("El siguiente mapa muestra la distribución espacial simulada de la "
                       "Temperatura Superficial del Mar (SST) en la región de Nicaragua, "
                       "incluyendo principales ríos, lagos y ciudades relevantes.", styles['Normal']))
story.append(Spacer(1, 12))

# Inserta la imagen del mapa
if os.path.exists(nombre_png):
    story.append(Image(nombre_png, width=6.5*inch, height=4.5*inch))
else:
    story.append(Paragraph("⚠️ Imagen no encontrada. No se pudo incluir el mapa.", styles['Normal']))

story.append(Spacer(1, 20))
story.append(Paragraph("<b>Elaborado por:</b> Jonathan Herrera Merlo", styles['Normal']))
story.append(Spacer(1, 12))
story.append(Paragraph("<b>Créditos:</b> Generado con Python (Cartopy, Matplotlib, CMOcean, ReportLab).", styles['Italic']))

doc.build(story)
print(f"📄 Informe PDF generado correctamente: {nombre_pdf}")
