# Restaurante App - Manejo de Eventos (Semana 15)

NOMBRE:Tatiana Morocho
FECHA:27/0672026
## Descripción del Proyecto
Evolución del sistema `restaurante_app15` desarrollado para la asignatura de Programación Orientada a Objetos. En esta entrega (Semana 15), se implementan los **fundamentos de manejo de eventos** en Tkinter integrando una nueva sección de **Ventas**, la cual relaciona usuarios y productos mediante una arquitectura modular de tres capas y persistencia en archivos JSON.

---

## Evolución Realizada (Semana 15)
- **Módulo de Ventas:** Incorporación del modelo `Venta` para gestionar la relación entre `Usuario` y `Producto`.
- **Persistencia en JSON:** Integración de `ventas.json` coordinada por la capa de servicios (`RestauranteServicio`).
- **Manejo de Eventos mediante `command=`:** Implementación de un botón interactivo configurado con `command=self._callback_registrar_venta`.
- **Delegación de Responsabilidades:** El callback recopila las entradas de la interfaz gráfica y delega las validaciones y el guardado al servicio.
- **Recursos Visuales (`assets/`):** Integración de logotipo (`logo.png`) e íconos del sistema en la interfaz gráfica.

---

## Flujo de Eventos
1. **Acción del Usuario:** Selecciona un usuario y un producto en la vista `MainView` y presiona el botón **Registrar Venta**.
2. **Asociación Evento-Callback:** El parámetro `command=` activa el método callback sin ejecutarlo directamente (`command=self._callback_registrar_venta`).
3. **Delegación a Servicio:** El callback envía los identificadores a `RestauranteServicio.registrar_venta()`.
4. **Persistencia:** La lógica de negocio valida la existencia de las entidades y guarda la venta en `datos/ventas.json`.
5. **Respuesta Visual:** Se muestra un mensaje de confirmación (`messagebox`) y se refresca el componente `Treeview` de ventas.

---

## Estructura del Sistema
```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── venta.py
│   └── ...
├── servicios/
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   └── main_view.py
├── assets/
│   └── logo.png
└── main.py