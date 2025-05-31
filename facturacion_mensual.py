import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages

# Datos de facturas obtenidos del MCP
invoices = [
    {"client_id": 42, "amount": 350.00, "issued_at": "2024-01-20"},
    {"client_id": 43, "amount": 75.99, "issued_at": "2024-02-01"},
    {"client_id": 44, "amount": 210.75, "issued_at": "2024-02-10"},
    {"client_id": 45, "amount": 499.50, "issued_at": "2024-02-15"},
    {"client_id": 46, "amount": 88.00, "issued_at": "2024-03-01"},
    {"client_id": 47, "amount": 155.25, "issued_at": "2024-03-05"},
    {"client_id": 48, "amount": 620.00, "issued_at": "2024-03-12"},
    {"client_id": 49, "amount": 99.99, "issued_at": "2024-03-20"},
    {"client_id": 50, "amount": 305.60, "issued_at": "2024-04-02"},
    {"client_id": 51, "amount": 175.00, "issued_at": "2024-04-10"},
    {"client_id": 52, "amount": 430.20, "issued_at": "2024-04-18"},
    {"client_id": 53, "amount": 95.00, "issued_at": "2024-05-01"},
    {"client_id": 54, "amount": 280.80, "issued_at": "2024-05-07"},
    {"client_id": 55, "amount": 510.40, "issued_at": "2024-05-15"},
    {"client_id": 56, "amount": 125.00, "issued_at": "2024-06-03"},
    {"client_id": 57, "amount": 390.25, "issued_at": "2024-06-11"},
    {"client_id": 58, "amount": 65.50, "issued_at": "2024-06-19"},
    {"client_id": 59, "amount": 233.00, "issued_at": "2024-07-01"},
    {"client_id": 60, "amount": 480.90, "issued_at": "2024-07-08"},
    {"client_id": 61, "amount": 110.00, "issued_at": "2024-07-15"},
    {"client_id": 62, "amount": 189.70, "issued_at": "2024-08-02"},
    {"client_id": 63, "amount": 330.00, "issued_at": "2024-08-09"},
    {"client_id": 64, "amount": 72.80, "issued_at": "2024-08-16"},
    {"client_id": 65, "amount": 278.45, "issued_at": "2024-09-03"},
    {"client_id": 66, "amount": 550.00, "issued_at": "2024-09-10"},
    {"client_id": 67, "amount": 130.20, "issued_at": "2024-09-17"},
    {"client_id": 68, "amount": 199.00, "issued_at": "2024-10-02"},
    {"client_id": 69, "amount": 415.50, "issued_at": "2024-10-09"},
    {"client_id": 70, "amount": 82.30, "issued_at": "2024-10-16"},
    {"client_id": 71, "amount": 303.75, "issued_at": "2024-11-04"},
    {"client_id": 72, "amount": 160.00, "issued_at": "2024-11-11"},
    {"client_id": 73, "amount": 250.90, "issued_at": "2024-11-18"},
    {"client_id": 74, "amount": 140.20, "issued_at": "2024-12-03"},
    {"client_id": 75, "amount": 375.00, "issued_at": "2024-12-10"},
    {"client_id": 76, "amount": 92.75, "issued_at": "2024-12-17"},
    {"client_id": 77, "amount": 288.10, "issued_at": "2025-01-05"},
    {"client_id": 78, "amount": 133.40, "issued_at": "2025-01-12"},
    {"client_id": 79, "amount": 205.00, "issued_at": "2025-01-19"},
    {"client_id": 80, "amount": 350.00, "issued_at": "2025-05-30"},
    {"client_id": 81, "amount": 1250.75, "issued_at": "2025-05-30"},
    {"client_id": 81, "amount": 890.50, "issued_at": "2025-06-15"}
]

# Crear DataFrame
for inv in invoices:
    inv['issued_at'] = datetime.strptime(inv['issued_at'], '%Y-%m-%d')
df = pd.DataFrame(invoices)
df['year'] = df['issued_at'].dt.year
df['month'] = df['issued_at'].dt.month

# Agrupar por año y mes
monthly = df.groupby(['year', 'month'])['amount'].sum().reset_index()

# Crear gráfica
plt.figure(figsize=(10,6))
for year in monthly['year'].unique():
    data = monthly[monthly['year'] == year]
    plt.plot(data['month'], data['amount'], marker='o', label=f'Año {year}')
plt.title('Variación de facturación por mes y año')
plt.xlabel('Mes')
plt.ylabel('Facturación (€)')
plt.legend()
plt.grid(True)

# Guardar como PDF
with PdfPages('variacion_facturacion.pdf') as pdf:
    pdf.savefig()
    plt.close()
print('PDF generado: variacion_facturacion.pdf')
