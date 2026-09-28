import os

# Crear carpetas requeridas por la tarea
os.makedirs("assets/icons", exist_ok=True)
os.makedirs("assets/logo", exist_ok=True)

png_transparente = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc\`\x00\x00\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82'

iconos = ["add.png", "home.png", "users.png", "products.png", "sales.png", "logout.png", "pdf.png", "clean.png", "delete.png", "edit.png", "search.png", "books.png"]
logos = ["logo.png", "icono.png"]

for icon in iconos:
    with open(os.path.join("assets/icons", icon), "wb") as f:
        f.write(png_transparente)

for logo in logos:
    with open(os.path.join("assets/logo", logo), "wb") as f:
        f.write(png_transparente)

print("¡Listo! Carpetas e imágenes creadas en assets/icons y assets/logo sin errores.")