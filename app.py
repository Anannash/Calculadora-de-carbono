from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = '123'

transportesHuella = {
    'auto': 0.192,
    'bus': 0.089,
    'tren': 0.045,
    'avion': 0.285,
    'bici': 0.0,
    'moto':0.103,
    'barco':0.016
}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    textito = ""

    if request.method == 'POST':
        try:
            km = float(request.form['km'])
            tipoTransporte = request.form.get('tipoTransporte')

            if km < 0:
                result = "Ingrese un número positivo >=("
            else:
                transportin = transportesHuella.get(tipoTransporte)

                if transportin is None:
                    result = "Tipo de transporte incorrecto <=o."
                else:
                    calculo = km * transportin
                    result = f"Tu huella de carbono es {calculo:.2f} kg CO2 (Transporte: {tipoTransporte})"

                    # Recomendaciones
                    if tipoTransporte == 'auto' :
                        textito = "Comparte, conduce suave, camina o usa una bici para cortos " \
                        "trayectos, considera híbrido/eléctrico."
                    elif tipoTransporte == 'bus' :
                        textito = "Para viajes largos, es una opción mas eficiente que viajar solo." \
                        " Si puedes, averigua si hay autobuses con tecnologías menos contaminantes, como el tren bala."
                    elif tipoTransporte == 'tren' :
                        textito = "Si vas a otra ciudad o region accesible por tren, priorizalo " \
                        "suele ser una alternativa con menor impacto ambiental que otros medios para la misma distancia."
                    elif tipoTransporte == 'avion':
                        textito = "Vuela menos, elige vuelos directos, usa aerolineas modernas y " \
                        "considera apoyar proyectos que capturen carbono para mitigar el impacto de tu viaje."
                    elif tipoTransporte == 'bici':
                        textito = "La bici es una opción ecologica y saludable." \
                        " Si puedes, usa la bici para ir al trabajo o a la universidad, puedes obtar por una bici electrica."
                    elif tipoTransporte == 'moto':
                        textito = "Elige motos mas pequeñas que consuman menos conbustible, maneja suave y comparte viajes."
                    elif tipoTransporte == 'barco':
                        textito = "Si puedes usa vela y asi aprovechar el viento, elige rutas directas y manten el motor eficiente."
                    
                    result += f"<br><strong>Recomendación:</strong><br>{textito}"

                    historial = session.get('historial', [])
                    historial.append(result)
                    session['historial'] = historial

        except ValueError:
            result = "Por favor, ingresa un numero valido. щ(ಠ益ಠщ)"

    historial = session.get('historial', [])

    return render_template('index.html', result=result, historial=historial)


if __name__ == '__main__':
    app.run(debug=True)
