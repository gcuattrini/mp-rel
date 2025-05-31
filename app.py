from flask import Flask, request
import requests
import os

app = Flask(__name__)

# URL SECRETA DEL RELÉ (reemplazá esto por tu URL real)
RELE_URL_SECRETA = "http://tu-rele/activar?token=CLAVE123"

# ACCESS TOKEN de Mercado Pago (modo test o real)
ACCESS_TOKEN = "TU_ACCESS_TOKEN"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and data.get('type') == 'payment':
        payment_id = data['data']['id']

        # Verificar el estado del pago desde la API de Mercado Pago
        r = requests.get(
            f"https://api.mercadopago.com/v1/payments/{payment_id}",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        pago = r.json()

        if pago.get("status") == "approved" and "producto" in pago.get("description", "").lower():
            print("✅ Pago aprobado, activando relé")
            try:
                requests.get(RELE_URL_SECRETA)
            except Exception as e:
                print("⚠️ Error al activar el relé:", e)
    
    return '', 200

# Hacemos que Flask escuche en el puerto asignado por Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
