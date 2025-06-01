from backend.mcp_instance import mcp
from backend.services.manager_service import get_manager_by_name, get_manager_by_email
from backend.services.client_service import get_all_clients, get_client_by_id
from backend.services.invoice_service import get_invoices_by_client_id, get_all_invoices
import openai
import os
from typing import Optional
import smtplib
from email.message import EmailMessage

def build_report_prompt(invoices, client_name, period, report_type):
    if period:
        periodo_texto = f"para el periodo {period}"
    else:
        periodo_texto = "considerando todas las facturas registradas"
    
    if client_name:
        cliente_texto = f"del cliente {client_name}"
    else:
        cliente_texto = "global"

    resumen = f"""
Eres un analista financiero profesional. Elabora un informe {report_type} de facturación {cliente_texto} {periodo_texto}.

Estructura el informe en las siguientes secciones:
1. Resumen ejecutivo (máximo 5 líneas)
2. Análisis de facturación (totales, pendientes, cobros, impagos)
3. Patrones o tendencias detectadas
4. Recomendaciones para el manager

Datos de facturación:
{chr(10).join([f"ID: {i['id']}, Monto: {i['amount']}, Estado: {i['status']}, Fecha: {i['issued_at']}" for i in invoices])}

Sé claro, profesional y conciso. El informe debe estar listo para ser enviado a un manager verificado que esté en la tabla managers.
"""
    return resumen

async def send_email_with_report(to_email, report_text, subject="Informe"):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("SMTP_USER")
    msg['To'] = to_email
    msg.set_content(report_text)

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 465))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
            smtp.login(smtp_user, smtp_pass)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Error enviando email: {e}")
        raise

@mcp.tool(
    name="generate_report",
    description="Genera un informe comercial y profesional y lo envía al manager autorizado por email."
)
async def generate_report(
    client_name: str,
    period: str,
    manager_name: str,
    manager_email: str,
    report_type: str
):
    # 1. Validar destinatario
    manager = None
    if manager_name:
        manager = await get_manager_by_name(manager_name)
    elif manager_email:
        manager = await get_manager_by_email(manager_email)
    if not manager:
        raise ValueError("Destinatario no autorizado para recibir informes.")
    
    # 2. Recopilar datos
    if client_name:
        clients = await get_all_clients()
        client = next((c for c in clients if c['name'].lower() == client_name.lower()), None)
        if not client:
            raise ValueError("Cliente no encontrado.")
        invoices = await get_invoices_by_client_id(client['id'])
    else:
        invoices = await get_all_invoices()

    # Filtrar por periodo si se proporciona
    if period:
        invoices = [i for i in invoices if period in str(i.get('issued_at', ''))]

    # Validación: si no hay facturas, no llamar a OpenAI
    if not invoices:
        return {"success": False, "message": f"No hay facturas para el cliente '{client_name}' en el periodo '{period}'."}
    
    # 3. Generar prompt y llamar al LLM (nueva API OpenAI)
    prompt = build_report_prompt(invoices, client_name, period, report_type)
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente experto en análisis de facturación empresarial con experiencia en contabilidad, finanzas y redacción de informes comerciales. "
                    "Tu tarea principal es generar reportes claros, concisos y visualmente profesionales para managers de empresas, usando datos de facturación obtenidos de una base de datos conectada a un sistema MCP. "
                    "Siempre valida que el destinatario esté autorizado y adapta el informe al tipo solicitado (general, ejecutivo, morosidad, etc.)."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    report_text = response.choices[0].message.content

    # 4. Enviar el informe por email
    await send_email_with_report(manager['email'], report_text, subject=f"Informe {report_type}")

    # 5. Confirmación
    return {"success": True, "message": f"Informe enviado a {manager['email']}"}
