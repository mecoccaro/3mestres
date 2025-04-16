import os

from flask import Flask, render_template, request
import qrcode
from io import BytesIO
import base64
import pyshorteners
from dotenv import load_dotenv

load_dotenv()  # take environment variables


app = Flask(__name__)


@app.route('/validador')
def validador():
    # Obtener los parámetros de la URL (si existen)
    name = request.args.get('name', 'Miguel Eduardo Coccaro Montserrat')
    placa = request.args.get('placa', 'GDG11G')
    cedula = request.args.get('cedula', '26252261')
    marca = request.args.get('marca', 'JEEP')
    modelo = request.args.get('modelo', 'CHEROKEE SPORT')
    color = request.args.get('color', 'VERDE')
    ano = request.args.get('ano', '2007')

    main_url = os.getenv('url')

    url = f'{main_url}?name={name}&placa={placa}&cedula={cedula}&marca={marca}&modelo={modelo}&color={color}&ano={ano}'

    # Acortar la URL utilizando pyshorteners
    s = pyshorteners.Shortener()
    short_url = s.tinyurl.short(url)

    # Generar el código QR con la URL acortada
    qr_image = qrcode.make(short_url)

    # Guardar el código QR en memoria y convertirlo a base64
    img_byte_array = BytesIO()
    qr_image.save(img_byte_array)
    img_byte_array.seek(0)
    img_data = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')

    # Renderizar el HTML con el QR generado
    return render_template(
        './barutasemat.html',
        qr_data=img_data,
        name=name,
        placa=placa,
        cedula=cedula,
        marca=marca,
        modelo=modelo,
        color=color,
        ano=ano
    )


if __name__ == '__main__':
    app.run(debug=True)