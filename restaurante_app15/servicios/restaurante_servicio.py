import os
import webbrowser
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self):
        self.archivo_servicio = ArchivoServicio()

    def obtener_usuarios(self):
        return self.archivo_servicio.cargar_json("datos/usuarios.json")

    def obtener_productos(self):
        return self.archivo_servicio.cargar_json("datos/productos.json")

    def obtener_ventas(self):
        datos = self.archivo_servicio.cargar_json("datos/ventas.json")
        ventas = []
        for v in datos:
            ventas.append(
                Venta(
                    v.get("id_venta", ""),
                    v.get("nombre_usuario", "Desconocido"),
                    v.get("id_producto", 0),
                    v.get("nombre_producto", "Producto"),
                    v.get("precio", 0.0)
                )
            )
        return ventas

    def registrar_venta(self, id_usuario, id_producto):
        if not id_usuario or not id_producto:
            return False, "Debe seleccionar un usuario y un producto"

        usuarios = self.obtener_usuarios()
        productos = self.obtener_productos()

        usr = next((u for u in usuarios if u.get("id") == id_usuario), None)
        prod = next((p for p in productos if p.get("id") == id_producto), None)

        nombre_usr = usr.get("nombre") if usr else f"Usuario #{id_usuario}"
        nombre_prod = prod.get("nombre") if prod else "Producto"
        precio_prod = prod.get("precio", 0.0) if prod else 0.0

        ventas = self.archivo_servicio.cargar_json("datos/ventas.json")
        nuevo_id = f"V{len(ventas) + 1:03d}"
        
        nueva_venta = {
            "id_venta": nuevo_id,
            "id_usuario": id_usuario,
            "nombre_usuario": nombre_usr,
            "id_producto": id_producto,
            "nombre_producto": nombre_prod,
            "precio": precio_prod
        }
        ventas.append(nueva_venta)
        
        self.archivo_servicio.guardar_json("datos/ventas.json", ventas)
        return True, "Venta registrada con éxito"

    def generar_reporte_pdf(self):
        ventas = self.obtener_ventas()
        if not ventas:
            return False, "No hay ventas registradas para generar el reporte"

        os.makedirs("reportes", exist_ok=True)
        pdf_path = os.path.join("reportes", "reporte_ventas.pdf")

        doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
        elements = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor("#1e293b"))
        subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=colors.HexColor("#64748b"))

        # Validar y cargar la imagen del logo
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_folder = os.path.join(base_dir, "assets", "logo")
        logo_path = None

        if os.path.exists(logo_folder):
            for file in os.listdir(logo_folder):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    candidate = os.path.join(logo_folder, file)
                    try:
                        with PILImage.open(candidate) as img:
                            img.verify()
                        logo_path = candidate
                        break
                    except Exception:
                        continue

        texto_header = [
            Paragraph("<b>Reporte de Ventas</b>", title_style),
            Paragraph("Sistema de Gestión de Restaurante", subtitle_style)
        ]

        if logo_path:
            img_logo = RLImage(logo_path, width=60, height=60)
            header_data = [[img_logo, texto_header]]
            col_widths = [70, 430]
        else:
            header_data = [[texto_header]]
            col_widths = [500]

        t_header = Table(header_data, colWidths=col_widths)
        t_header.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ]))
        elements.append(t_header)
        elements.append(Spacer(1, 20))

        data = [["ID Venta", "Atendido por", "Producto", "Precio"]]
        total = 0.0
        for v in ventas:
            data.append([v.id_venta, v.nombre_usuario, getattr(v, 'nombre_producto', 'Producto'), f"${getattr(v, 'precio', 0.0):.2f}"])
            total += getattr(v, 'precio', 0.0)

        data.append(["", "", "Total:", f"${total:.2f}"])

        t = Table(data, colWidths=[80, 160, 180, 80])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2563eb")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('BACKGROUND', (0,1), (-1,-2), colors.HexColor("#f8fafc")),
            ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ]))
        elements.append(t)

        doc.build(elements)
        webbrowser.open(os.path.abspath(pdf_path))
        return True, f"Reporte PDF generado con éxito en:\n{os.path.abspath(pdf_path)}"