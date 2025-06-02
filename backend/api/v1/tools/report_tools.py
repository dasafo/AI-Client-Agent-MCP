from backend.mcp_instance import mcp
from backend.services.manager_service import get_manager_by_name, get_manager_by_email
from backend.services.client_service import get_all_clients, get_client_by_id
from backend.services.invoice_service import get_invoices_by_client_id, get_all_invoices
import openai
from typing import Optional
import smtplib
from email.message import EmailMessage
from backend.services.report_service import save_report, get_client_by_name, filter_invoices_by_period
import asyncpg
import matplotlib.pyplot as plt
import io
import base64
import re
from backend.core.config import SMTP_USER, SMTP_HOST, SMTP_PORT, SMTP_PASS, OPENAI_API_KEY, DATABASE_URL
from backend.core.logging import get_logger
from backend.models.report import ReportOut

logger = get_logger(__name__)

def build_report_prompt(invoices, client_name, period, report_type, manager_name=None, manager_email=None):
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

El informe debe estar en formato HTML profesional, con tablas y secciones claras. No incluyas sugerencias para desarrolladores ni comentarios meta; el informe debe estar listo para ser enviado directamente al manager.

Estructura el informe en las siguientes secciones:
1. Resumen ejecutivo (máximo 5 líneas)
2. Análisis de facturación (totales, pendientes, cobros, impagos)
3. Patrones o tendencias detectadas
4. Recomendaciones para el manager

Datos de facturación:
{chr(10).join([f"ID: {i['id']}, Monto: {i['amount']}, Estado: {i['status']}, Fecha: {i['issued_at']}" for i in invoices])}

Sé claro, profesional y conciso. El informe debe estar listo para ser enviado a un manager verificado que esté en la tabla managers.
"""
    if manager_name and manager_email:
        resumen += f"\n\nNota: Este informe será enviado a {manager_name} <{manager_email}>."
    return resumen

def generate_invoice_status_chart(invoices):
    # Contar facturas por estado
    estados = ['completed', 'pending', 'canceled']
    counts = [len([i for i in invoices if i['status'] == estado]) for estado in estados]
    # Crear gráfico
    fig, ax = plt.subplots()
    ax.bar(estados, counts, color=['#4CAF50', '#FFC107', '#F44336'])
    ax.set_ylabel('Número de facturas')
    ax.set_title('Facturas por estado')
    # Guardar en buffer
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf.read()

def clean_llm_html(html_text):
    """
    Sanitiza HTML generado por LLM eliminando etiquetas y atributos peligrosos.
    - Elimina bloques de código markdown
    - Elimina etiquetas peligrosas y su contenido
    - Elimina atributos peligrosos (on*, style, formaction, srcdoc, etc)
    - Elimina comentarios HTML
    """
    # Elimina bloques de código markdown tipo ```html ... ```
    cleaned = re.sub(r'```html\s*([\s\S]*?)```', r'\1', html_text, flags=re.IGNORECASE)
    # Elimina cualquier bloque ``` ... ```
    cleaned = re.sub(r'```[\s\S]*?```', '', cleaned)
    # Elimina comentarios HTML
    cleaned = re.sub(r'<!--.*?-->', '', cleaned, flags=re.DOTALL)
    # Elimina etiquetas peligrosas y su contenido (script, iframe, object, embed, style, link, meta, base)
    cleaned = re.sub(r'<\s*(script|iframe|object|embed|style|link|meta|base)[^>]*>[\s\S]*?<\s*/\s*\1\s*>', '', cleaned, flags=re.IGNORECASE)
    # Elimina etiquetas peligrosas auto-cerradas
    cleaned = re.sub(r'<\s*(script|iframe|object|embed|style|link|meta|base)[^>]*/>', '', cleaned, flags=re.IGNORECASE)
    # Elimina atributos on* (onerror, onclick, etc), style, formaction, srcdoc
    cleaned = re.sub(r'\s(on\w+|style|formaction|srcdoc)\s*=\s*"[^"]*"', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s(on\w+|style|formaction|srcdoc)\s*=\s*'[^']*'", '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s(on\w+|style|formaction|srcdoc)\s*=\s*[^ >]+', '', cleaned, flags=re.IGNORECASE)
    # Elimina javascript: en href/src
    cleaned = re.sub(r'(href|src)\s*=\s*(["\'])\s*javascript:[^\2]*\2', r'\1="#"', cleaned, flags=re.IGNORECASE)
    # Opcional: elimina cualquier etiqueta <meta> o <base> auto-cerrada
    cleaned = re.sub(r'<\s*(meta|base)[^>]*/?>', '', cleaned, flags=re.IGNORECASE)
    return cleaned.strip()

async def send_email_with_report(to_email, report_text, subject="Informe", invoices=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg.set_content("Este correo contiene un informe en HTML. Si no lo ves correctamente, usa un cliente compatible.")

    # Adjuntar gráfico como base64 si hay facturas
    html_report = clean_llm_html(report_text)
    if invoices:
        img_bytes = generate_invoice_status_chart(invoices)
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')
        img_tag = f'<img src="data:image/png;base64,{img_b64}" alt="Gráfico de facturas por estado" style="max-width:400px;"><br>'
        if '<img' not in html_report:
            html_report = img_tag + html_report
    msg.add_alternative(html_report, subtype='html')

    smtp_host = SMTP_HOST
    smtp_port = SMTP_PORT
    smtp_user = SMTP_USER
    smtp_pass = SMTP_PASS

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
            smtp.login(smtp_user, smtp_pass)
            smtp.send_message(msg)
        return True
    except Exception as e:
        logger.error(f"Error enviando email: {e}")
        raise

async def obtener_manager_autorizado(manager_name, manager_email):
    if manager_name:
        return await get_manager_by_name(manager_name)
    elif manager_email:
        return await get_manager_by_email(manager_email)
    return None

async def obtener_invoices_cliente_periodo(client_name, period):
    if client_name:
        client_obj = await get_client_by_name(client_name)
        if not client_obj:
            return None, None
        invoices = await get_invoices_by_client_id(client_obj['id'])
    else:
        client_obj = None
        invoices = await get_all_invoices()
    if period:
        invoices = filter_invoices_by_period(invoices, period)
    return client_obj, invoices

def generar_texto_informe_llm(invoices, client_name, period, report_type, manager):
    prompt = build_report_prompt(invoices, client_name, period, report_type, manager['name'], manager['email'])
    from openai import OpenAI
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": (
                "Eres un asistente experto en análisis de facturación empresarial con experiencia en contabilidad, finanzas y redacción de informes comerciales. "
                "Tu tarea principal es generar reportes claros, concisos y visualmente profesionales para managers de empresas, usando datos de facturación obtenidos de una base de datos conectada a un sistema MCP. "
                "Siempre valida que el destinatario esté autorizado y adapta el informe al tipo solicitado (general, ejecutivo, morosidad, etc.)."
            )},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

async def guardar_informe_db(client_obj, client_name, period, manager, report_type, report_text):
    client_id = client_obj['id'] if client_obj else None
    db_url = DATABASE_URL
    conn = await asyncpg.connect(dsn=db_url)
    save_result = await save_report(
        conn,
        client_id,
        client_name if client_name else None,
        period if period else None,
        manager['email'],
        manager['name'],
        report_type,
        report_text
    )
    await conn.close()
    return save_result

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
    try:
        manager = await obtener_manager_autorizado(manager_name, manager_email)
        if not manager:
            return {"success": False, "error": "Destinatario no autorizado para recibir informes."}
        client_obj, invoices = await obtener_invoices_cliente_periodo(client_name, period)
        if client_name and not client_obj:
            return {"success": False, "error": "Cliente no encontrado."}
        if not invoices:
            return {"success": False, "message": f"No hay facturas para el cliente '{client_name}' en el periodo '{period}'."}
        report_text = generar_texto_informe_llm(invoices, client_name, period, report_type, manager)
        await send_email_with_report(manager['email'], report_text, subject=f"Informe {report_type}", invoices=invoices)
        save_result = await guardar_informe_db(client_obj, client_name, period, manager, report_type, report_text)
        if not save_result.get("success", True):
            return {"success": False, "error": save_result.get("error", "Error al guardar el informe en la base de datos.")}
        return {"success": True, "message": f"Informe enviado a {manager['name']} <{manager['email']}>"}
    except Exception as e:
        logger.error(f"Error en generate_report: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool(
    name="list_reports",
    description="Listar todos los reportes generados en la base de datos."
)
async def list_reports() -> dict:
    try:
        db_url = DATABASE_URL
        conn = await asyncpg.connect(dsn=db_url)
        rows = await conn.fetch("SELECT * FROM reports ORDER BY created_at DESC")
        await conn.close()
        reports = [ReportOut(**dict(row)) for row in rows]
        return {"success": True, "reports": [r.model_dump() for r in reports]}
    except Exception as e:
        logger.error(f"Error al listar reportes: {e}")
        return {"success": False, "error": str(e)}
