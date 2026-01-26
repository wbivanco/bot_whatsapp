# 📘 README — Alta de Cliente en WhatsApp Cloud API (Meta)
**Inapsis | Guía paso a paso para conectar un número real a tu backend (producción)**

## 🎯 Objetivo
Dejar operativo un cliente para que:
- 📩 **Reciba mensajes** en WhatsApp (entrantes → webhook → backend)
- 📤 **Envíe respuestas automáticas** desde tu backend usando Cloud API
- 🚀 Quede listo para producción (no modo prueba)

---

## ✅ Requisitos previos

### 1) Tener un Business Manager (Portfolio empresarial)
- Debe estar creado y accesible desde **Meta Business Settings**
- Recomendado: **negocio verificado** (no siempre obligatorio, pero ayuda)

### 2) Tener una App en Meta Developers
- Debe ser tu app (ej: `Bot Inapsis`)
- Debe tener agregado el producto: **WhatsApp**

### 3) Tener el backend disponible públicamente
Para webhooks necesitas una URL pública:
- Producción: dominio propio con HTTPS
- Dev: `ngrok` (solo para pruebas)

Ejemplo:
```
https://TU_DOMINIO/bot_whatsapp/whatsapp
```

---

## 🧩 Conceptos clave (importante)

En Cloud API vas a manejar 3 IDs:

### ✅ WABA_ID (WhatsApp Business Account ID)
Es la “cuenta de WhatsApp Business” dentro del Business Manager.

### ✅ PHONE_NUMBER_ID (Identificador del número)
Es el ID técnico del número real conectado.

### ✅ ACCESS TOKEN
Token para autenticar llamadas a Graph API.

📌 Regla de oro:
- Para **enviar mensajes** → usás `PHONE_NUMBER_ID`
- Para **suscribir webhooks** → usás `WABA_ID`

---

# 🏗️ Flujo completo para dar de alta un cliente

---

## PASO 1 — Crear App en Meta Developers (una sola vez para Inapsis)
📍 https://developers.facebook.com/apps/

1. **Crear App**
2. Tipo: Business / Consumer (Meta cambia nombres, elegí la que habilite WhatsApp)
3. Agregar producto: **WhatsApp**
4. Dentro de WhatsApp elegir: **Cloud API**

---

## PASO 2 — Poner la app en modo “Producción”
📍 En tu app → menú izquierdo → **Publicar**

- Completar campos obligatorios (si te los pide):
  - URL Política de privacidad
  - URL Términos del servicio
  - Email de contacto
  - Categoría

Luego:
✅ Cambiar estado a **Publicada / Producción**

📌 Esto no siempre “habilita WhatsApp”, pero evita restricciones de modo desarrollo.

---

## PASO 3 — Crear / Seleccionar WABA (Cuenta de WhatsApp Business)
📍 Business Settings → **Cuentas → Cuentas de WhatsApp**

Ahí vas a ver:
- “Inapsis”
- y quizás “Test WhatsApp Business Account”

📌 Para clientes reales usás la cuenta real, no la de test.

🔎 Copiar el:
✅ **WABA_ID**

Ejemplo:
```
WABA_ID=1442469167296760
```

---

## PASO 4 — Agregar método de pago
📍 Business Settings → **Facturación y pagos**

Agregar:
- Tarjeta / método válido

📌 Es obligatorio para iniciar conversaciones (y para operar en producción sin límites raros).

---

## PASO 5 — Registrar el número real del cliente
📍 WhatsApp Manager → **Números de teléfono** → “Añadir número de teléfono”

### Requisitos del número:
- No debe estar activo en WhatsApp normal ni WhatsApp Business App
- Debe poder recibir SMS o llamada para verificación

📌 Si el número estaba usado antes en WhatsApp:
1) En el celular → WhatsApp → Configuración → Cuenta  
2) **Eliminar cuenta / dar de baja número**
3) Esperar un rato y volver a intentar registrar

---

## PASO 6 — Aprobar nombre para mostrar (Display Name)
En WhatsApp Manager:
- Definir nombre
- Esperar aprobación

📌 A veces se aprueba rápido, a veces tarda.

---

## PASO 7 — Obtener el PHONE_NUMBER_ID real
📍 WhatsApp Manager → Números de teléfono → Seleccionar número

Copiar:
✅ **Identificador del número de teléfono (PHONE_NUMBER_ID)**

Ejemplo:
```
PHONE_NUMBER_ID=930757380118662
```

---

## PASO 8 — Generar Access Token permanente (recomendado)
📍 App → WhatsApp → Configuración

Lo correcto para producción es usar un:
✅ **System User Token** (token permanente)

Pasos típicos:
1. Business Settings → Usuarios → **Usuarios del sistema**
2. Crear uno (System User)
3. Asignarle activos:
   - WhatsApp account (WABA)
   - Permisos
4. Generar token con permisos:
   - `whatsapp_business_messaging`
   - `whatsapp_business_management`

📌 Guardar el token como secreto (ENV, Vault, etc.)

---

## PASO 9 — Configurar Webhook en la app (Meta)
📍 App → WhatsApp → Configuración → Webhooks

Completar:

### URL de devolución de llamada (Callback URL)
Ejemplo:
```
https://TU_DOMINIO/bot_whatsapp/whatsapp
```

### Verify Token
Es una clave que inventás vos (string), ej:
```
VERIFY_TOKEN=INAPSIS_2026_WEBHOOK
```

Luego:
✅ **Verificar y guardar**

---

## PASO 10 — Suscribir la app al WABA (PASO CLAVE)
⚠️ Importante:
❌ NO se hace con `PHONE_NUMBER_ID`  
✅ Se hace con `WABA_ID`

### Curl correcto
```bash
curl -X POST "https://graph.facebook.com/v22.0/WABA_ID/subscribed_apps" \
  -H "Authorization: Bearer TU_TOKEN"
```

Ejemplo real:
```bash
curl -X POST "https://graph.facebook.com/v22.0/1442469167296760/subscribed_apps" \
  -H "Authorization: Bearer TU_TOKEN"
```

Respuesta esperada:
```json
{"success": true}
```

---

# ✅ Prueba final (enviar mensaje desde backend)

## Endpoint correcto para enviar mensajes
📌 Usar siempre:

```
https://graph.facebook.com/v22.0/PHONE_NUMBER_ID/messages
```

Ejemplo:
```bash
https://graph.facebook.com/v22.0/930757380118662/messages
```

## Curl de prueba
```bash
curl -X POST "https://graph.facebook.com/v22.0/930757380118662/messages" \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "5493834241994",
    "type": "text",
    "text": { "body": "Hola prueba desde Inapsis" }
  }'
```

---

# ✅ Prueba final (recibir mensajes reales)
1. Desde un celular cualquiera → mandar WhatsApp al número del cliente
2. Tu webhook debe recibir evento `messages`
3. Tu backend debe responder automáticamente

📌 Si no llega el webhook:
- revisar HTTPS
- revisar que el endpoint GET de verificación funcione
- revisar que esté suscrito a messages
- revisar que la app esté suscrita al WABA

---

# 🧾 Variables de entorno recomendadas (.env)

```env
META_GRAPH_VERSION=v22.0

WHATSAPP_WABA_ID=1442469167296760
WHATSAPP_PHONE_NUMBER_ID=930757380118662

WHATSAPP_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WHATSAPP_VERIFY_TOKEN=INAPSIS_2026_WEBHOOK

WHATSAPP_API_URL=https://graph.facebook.com/v22.0/930757380118662/messages
```

---

# 🧨 Errores comunes y solución rápida

## ❌ (#131030) Recipient phone number not in allowed list
📌 Causa:
Estás usando **número de prueba** o modo test.

✅ Solución:
- Usar `PHONE_NUMBER_ID` real
- Asegurar que la app está en producción
- Asegurar WABA suscrito:
  ```bash
  POST /WABA_ID/subscribed_apps
  ```

---

## ❌ Unsupported post request /subscribed_apps con PHONE_NUMBER_ID
📌 Causa:
Estás intentando:

❌ `/PHONE_NUMBER_ID/subscribed_apps`

✅ Solución:
Usar:

✅ `/WABA_ID/subscribed_apps`

---

## ❌ "Unknown path components: /register"
📌 Causa:
Endpoint incorrecto (o versión incorrecta).

✅ Solución:
Para registrar número se usa el flujo de registro correcto (y normalmente hoy se hace desde el panel).

---

## ❌ No llegan mensajes entrantes al webhook
Checklist:
- [ ] webhook verificado y guardado
- [ ] callback url pública HTTPS
- [ ] app suscrita al WABA (`subscribed_apps`)
- [ ] evento `messages` activado
- [ ] tu backend responde `200 OK`

---

# 📌 Checklist final para alta de cliente (resumen rápido)

- [ ] App creada y publicada  
- [ ] Método de pago cargado  
- [ ] WABA creada / seleccionada  
- [ ] Número real agregado y conectado  
- [ ] PHONE_NUMBER_ID copiado  
- [ ] Token permanente generado  
- [ ] Webhook configurado y verificado  
- [ ] `POST /WABA_ID/subscribed_apps` hecho  
- [ ] Mensaje saliente funciona  
- [ ] Mensaje entrante llega al webhook  

---

# 🧩 Notas Inapsis (recomendación)
Para escalar con múltiples clientes:

### Opción 1 (más simple)
📌 Un WABA para Inapsis y varios números adentro  
- cada cliente = un número

### Opción 2 (más profesional / multi-empresa)
📌 Cada cliente con su propio Business Manager + WABA  
- vos como partner/tech provider
- más complejo pero más “enterprise”
