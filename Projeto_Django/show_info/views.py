from django.http import JsonResponse
from django.shortcuts import render
from datetime import date, timedelta
from .sems_api import crosslogin, get_inverter_data


def index(request):
    inverter_sn = "5010KETU229W6177"
    account = "demo@goodwe.com"
    password = "GoodweSems123!@#"

    try:
        token = crosslogin(account, password, "us")

        # Data de ontem
        ontem = date.today() - timedelta(days=1)
        dt_str = ontem.strftime("%Y-%m-%d 00:00:00")

        dados = {}
        for col in ["Pac", "Eday", "Cbattery1"]:
            resp = get_inverter_data(token, inverter_sn, col, dt_str, "eu")
            lista = resp.get("data", {}).get("column1", [])
            if lista:
                dados[col] = lista[-1].get("column")
            else:
                dados[col] = "N/A"

    except Exception as e:
        dados = {"Pac": "Erro", "Eday": str(e), "Cbattery1": "Erro"}

    contexto = {
        "inverter_sn": inverter_sn,
        "pac": dados.get("Pac"),
        "eday": dados.get("Eday"),
        "cbattery1": dados.get("Cbattery1"),
        "data": ontem.strftime("%d/%m/%Y")
    }
    return render(request, "show_info/index.html", contexto)

def alexa_data(request):
    inverter_sn = "5010KETU229W6177"
    account = "demo@goodwe.com"
    password = "GoodweSems123!@#"
    
    # Data de ontem
    ontem = date.today() - timedelta(days=1)
    dt_str = ontem.strftime("%Y-%m-%d 00:00:00")
    
    dados = {}
    try:
        token = crosslogin(account, password, "us")
        for col in ["Pac", "Eday", "Cbattery1"]:
            resp = get_inverter_data(token, inverter_sn, col, dt_str, "eu")
            lista = resp.get("data", {}).get("column1", [])
            if lista:
                dados[col] = lista[-1].get("column")
            else:
                dados[col] = "N/A"
    except Exception as e:
        dados = {"Pac": "Erro", "Eday": str(e), "Cbattery1": "Erro"}

    # Monta o JSON que a Alexa vai ler
    alexa_json = {
        "inverter_sn": inverter_sn,
        "data": ontem.strftime("%d/%m/%Y"),
        "Pac": dados.get("Pac"),
        "Eday": dados.get("Eday"),
        "Cbattery1": dados.get("Cbattery1")
    }
    
    return JsonResponse(alexa_json)
