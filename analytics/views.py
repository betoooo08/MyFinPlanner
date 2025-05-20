from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv
import tempfile
from finances.models import Goal, GoalContribution, Transaction, Budget, Report
from .models import Insight
from dotenv import load_dotenv
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from io import BytesIO
from django.conf import settings
from datetime import datetime



# Cargar el archivo .env desde la ruta específica
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../api_keys.env'))

# Inicializa el cliente de OpenAI con la API Key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Depuración: Imprime la clave para verificar que se cargó correctamente
print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")

@login_required
def Export_to_CSV(request):
    temp_dir = tempfile.gettempdir()

    # Metas
    goals_file_path = os.path.join(temp_dir, 'Goals.csv')
    with open(goals_file_path, 'w', newline='', encoding='utf-8') as goals_file:
        writer = csv.writer(goals_file)
        writer.writerow(['Name', 'Target Amount', 'Current Amount', 'Deadline', 'Description'])
        for goal in Goal.objects.filter(user=request.user):
            writer.writerow([goal.name, goal.target_amount, goal.current_amount, goal.deadline, goal.description])

    # Contribuciones
    contributions_file_path = os.path.join(temp_dir, 'ContributionsGoals.csv')
    with open(contributions_file_path, 'w', newline='', encoding='utf-8') as contributions_file:
        writer = csv.writer(contributions_file)
        writer.writerow(['Goal Name', 'Amount', 'Date'])
        for contribution in GoalContribution.objects.filter(goal__user=request.user):
            writer.writerow([contribution.goal.name, contribution.amount, contribution.date])

    return HttpResponse(f"Archivos generados en: {goals_file_path} y {contributions_file_path}")

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content.strip()

@login_required
def AI_Goal_Insight(request):
    # Si no hay metas, no llamamos a OpenAI
    if not Goal.objects.filter(user=request.user).exists():
        return render(request, 'goals.html', {
            'goals': [],
            'active_page': 'goal_list'
        })

    # Exportar CSV
    Export_to_CSV(request)
    temp_dir = tempfile.gettempdir()

    # Leer metas
    goals_path = os.path.join(temp_dir, 'Goals.csv')
    goals_data = []
    with open(goals_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            goals_data.append(row)

    # Texto para prompt
    goals_text = "Financial Goals:\n" + ", ".join(headers) + "\n"
    for row in goals_data:
        goals_text += ", ".join(row) + "\n"

    # Leer contribuciones
    contributions_path = os.path.join(temp_dir, 'ContributionsGoals.csv')
    contributions_data = []
    with open(contributions_path, 'r', encoding='utf-8') as c:
        reader = csv.reader(c)
        c_headers = next(reader)
        for row in reader:
            contributions_data.append(row)

    contributions_text = "Historical Contributions to Goals:\n" + ", ".join(c_headers) + "\n"
    for row in contributions_data:
        contributions_text += ", ".join(row) + "\n"

    prompt = f"""
You are a friendly yet insightful personal finance advisor. Your task is to analyze a user's financial goals and the historical contributions made toward those goals. Based on the data provided below, generate a detailed yet simple-to-understand insight for the user.

Use the following approach:
1. Carefully review the financial goals: include the target amount, current amount, deadline, and description.
2. Analyze the history of contributions for each goal (amount and date).
3. For each goal, evaluate if the user is on track to reach it by the deadline based on their current progress and contribution patterns.
4. If the user is behind, gently explain why and give motivational yet realistic suggestions to improve (e.g. increasing monthly savings, extending the deadline, or adjusting the goal).
5. If the user is doing well, offer praise and encouragement.
6. Use financial-related emojis (💰📈⏳✅❗) to make your response more engaging.
7. Avoid overly technical language; your tone should be clear, supportive, and beginner-friendly.
8. If appropriate, calculate how much the user would need to contribute monthly (or weekly) to reach their goal in time.
9. If the provided data is empty or no goals/contributions exist, kindly inform the user that no financial goals or contributions have been set yet, and encourage them to create one to start planning for their future.

Now analyze the following user data and generate personalized insights:

{goals_text}

{contributions_text}
"""
    insight = get_completion(prompt)

    if goals_data:
        Insight.objects.create(
            user=request.user,
            prompt=prompt,
            response=insight,
            insight_type=Insight.GOALS
        )

    return render(request, 'goals.html', {
        'insight': insight,
        'goals_data': goals_data,
        'contributions_data': contributions_data,
        'headers': headers,
        'contributions_headers': c_headers,
        'active_page': 'goal_list',
    })

@login_required
def Export_Transactions_and_Budgets_to_CSV(request):
    temp_dir = tempfile.gettempdir()

    transactions_file_path = os.path.join(temp_dir, 'Transactions.csv')
    with open(transactions_file_path, 'w', newline='', encoding='utf-8') as transactions_file:
        writer = csv.writer(transactions_file)
        writer.writerow([
            'Date', 'Amount', 'Category', 'Description',
            'Type', 'Merchant', 'Created At'
        ])
        for transaction in Transaction.objects.filter(user=request.user):
            writer.writerow([
                transaction.date,
                transaction.amount,
                transaction.category.name,
                transaction.description,
                transaction.transaction_type,
                transaction.merchant,
                transaction.created_at,
            ])

    budgets_file_path = os.path.join(temp_dir, 'Budgets.csv')
    with open(budgets_file_path, 'w', newline='', encoding='utf-8') as budgets_file:
        writer = csv.writer(budgets_file)
        writer.writerow([
            'Category', 'Amount', 'Spent',
            'Remaining', 'Period', 'Alert Threshold'
        ])
        for budget in Budget.objects.filter(user=request.user):
            writer.writerow([
                budget.category.name,
                budget.amount,
                budget.spent,
                budget.remaining,
                budget.period,
                budget.alert_threshold,
            ])
    return HttpResponse(
        f"Archivos generados en: {transactions_file_path} y {budgets_file_path}"
    )

@login_required
def AI_Transactions_and_Budgets_Insight(request):
    if not Transaction.objects.filter(user=request.user).exists() and not Budget.objects.filter(user=request.user).exists():
        reports = Report.objects.filter(user=request.user)
        return render(request, 'reports.html', {
            'reports': reports,
            'active_page': 'report_list'
        })

    Export_Transactions_and_Budgets_to_CSV(request)
    temp_dir = tempfile.gettempdir()

    transactions_path = os.path.join(temp_dir, 'Transactions.csv')
    transactions_data = []
    with open(transactions_path, 'r', encoding='utf-8') as t_file:
        reader = csv.reader(t_file)
        transactions_headers = next(reader)
        for row in reader:
            transactions_data.append(row)

    transactions_text = "Transactions:\n" + ", ".join(transactions_headers) + "\n"
    for row in transactions_data:
        transactions_text += ", ".join(row) + "\n"

    budgets_path = os.path.join(temp_dir, 'Budgets.csv')
    budgets_data = []
    with open(budgets_path, 'r', encoding='utf-8') as b_file:
        reader = csv.reader(b_file)
        budgets_headers = next(reader)
        for row in reader:
            budgets_data.append(row)

    budgets_text = "Budgets:\n" + ", ".join(budgets_headers) + "\n"
    for row in budgets_data:
        budgets_text += ", ".join(row) + "\n"

    prompt = f"""
You are a helpful and insightful personal finance advisor. Your task is to analyze a user's financial transactions and their current budget distribution. Based on the data provided below, generate personalized and easy-to-understand recommendations for the user.

Use the following approach:
1. Review the transactions, including income and expenses, grouped by category.
2. Cross-reference the transactions with the user's budgets: check if they are staying within the limits, overspending, or underutilizing certain categories.
3. Point out any anomalies or unusual spending behavior (e.g., unusually high spending in a category compared to previous trends).
4. If the user receives income, suggest how to best distribute it among their budgets (e.g., savings, food, transportation) based on their recent spending patterns and needs.
5. Highlight areas where the user may need to increase or decrease their budgets.
6. Provide motivating tips on how to improve spending habits or stick to budgets more effectively.
7. Use financial-related emojis (💸📈💡🚨💰) to make your advice more engaging.
8. Avoid technical jargon; use a clear, friendly tone that anyone can understand.

Now analyze the following user data and generate insightful recommendations:

{transactions_text}

{budgets_text}
"""
    insight = get_completion(prompt)

    if transactions_data or budgets_data:
        Insight.objects.create(
            user=request.user,
            prompt=prompt,
            response=insight,
            insight_type=Insight.TRANSACTIONS_BUDGETS
        )

    return render(request, 'reports.html', {
        'insight': insight,
        'transactions_data': transactions_data,
        'budgets_data': budgets_data,
        'transactions_headers': transactions_headers,
        'budgets_headers': budgets_headers,
        'active_page': 'reports',
    })





@login_required
def export_financial_report_csv(request):
    response = HttpResponse(content_type='text/csv')
    filename = f"financial_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    
    # Encabezado del reporte
    writer.writerow(['MyFinPlanner - Financial Report'])
    writer.writerow([f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}'])
    writer.writerow([f'User: {request.user.username}'])
    writer.writerow([])

    # Transactions
    writer.writerow(['TRANSACTIONS'])
    writer.writerow(['Date', 'Amount', 'Category', 'Description', 'Type', 'Merchant', 'Created At'])
    transactions = Transaction.objects.filter(user=request.user)
    if transactions:
        for t in transactions:
            writer.writerow([
                t.date.strftime('%Y-%m-%d'), 
                f"${t.amount:.2f}", 
                t.category.name, 
                t.description,
                t.transaction_type, 
                t.merchant, 
                t.created_at.strftime('%Y-%m-%d %H:%M')
            ])
    else:
        writer.writerow(['No transactions found.'])

    # Budgets
    writer.writerow([])
    writer.writerow(['BUDGETS'])
    writer.writerow(['Category', 'Amount', 'Spent', 'Remaining', 'Period', 'Alert Threshold'])
    budgets = Budget.objects.filter(user=request.user)
    if budgets:
        for b in budgets:
            remaining = b.amount - b.spent
            writer.writerow([
                b.category.name, 
                f"${b.amount:.2f}", 
                f"${b.spent:.2f}", 
                f"${remaining:.2f}", 
                b.period, 
                f"{b.alert_threshold}%"
            ])
    else:
        writer.writerow(['No budgets found.'])

    # Goals
    writer.writerow([])
    writer.writerow(['GOALS'])
    writer.writerow(['Name', 'Target Amount', 'Current Amount', 'Progress', 'Deadline', 'Description'])
    goals = Goal.objects.filter(user=request.user)
    if goals:
        for g in goals:
            progress = (g.current_amount / g.target_amount * 100) if g.target_amount > 0 else 0
            writer.writerow([
                g.name, 
                f"${g.target_amount:.2f}", 
                f"${g.current_amount:.2f}", 
                f"{progress:.1f}%",
                g.deadline.strftime('%Y-%m-%d') if g.deadline else 'N/A', 
                g.description
            ])
    else:
        writer.writerow(['No goals found.'])

    return response
@login_required
def export_financial_report_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="financial_report.pdf"'
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.alignment = 1  # Centrado
    title_style.textColor = colors.blue
    
    section_style = styles['Heading2']
    section_style.textColor = colors.blue
    
    # Añadir logo
    logo_path = 'static/images/Logo.png'
    if os.path.exists(logo_path):
        img = Image(logo_path, width=120, height=120)
        img.hAlign = 'CENTER'
        elements.append(img)
        elements.append(Spacer(1, 10))  # Espacio entre logo y título

    elements.append(Paragraph("Financial Report", title_style))
    elements.append(Spacer(1, 20))
    # Fecha del reporte
    from datetime import datetime
    date_style = styles['Normal']
    date_style.alignment = 1
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", date_style))
    elements.append(Spacer(1, 30))
    
    # Transacciones
    elements.append(Paragraph("Transactions", section_style))
    elements.append(Spacer(1, 10))
    
    # Datos de transacciones
    transactions = Transaction.objects.filter(user=request.user)
    if transactions:
        data = [['Date', 'Amount', 'Category', 'Description', 'Type', 'Merchant']]
        for t in transactions:
            data.append([
                t.date.strftime('%Y-%m-%d'),
                f"${t.amount:.2f}",
                t.category.name,
                t.description[:30] + '...' if len(t.description) > 30 else t.description,
                t.transaction_type,
                t.merchant
            ])
        
        # Crear tabla
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("No transactions found.", styles['Normal']))
    
    elements.append(Spacer(1, 20))
    
    # Presupuestos
    elements.append(Paragraph("Budgets", section_style))
    elements.append(Spacer(1, 10))
    
    # Datos de presupuestos
    budgets = Budget.objects.filter(user=request.user)
    if budgets:
        data = [['Category', 'Amount', 'Spent', 'Remaining', 'Period', 'Alert']]
        for b in budgets:
            remaining = b.amount - b.spent
            data.append([
                b.category.name,
                f"${b.amount:.2f}",
                f"${b.spent:.2f}",
                f"${remaining:.2f}",
                b.period,
                f"{b.alert_threshold}%"
            ])
        
        # Crear tabla
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("No budgets found.", styles['Normal']))
    
    elements.append(Spacer(1, 20))
    
    # Metas
    elements.append(Paragraph("Goals", section_style))
    elements.append(Spacer(1, 10))
    
    # Datos de metas
    goals = Goal.objects.filter(user=request.user)
    if goals:
        data = [['Name', 'Target', 'Current', 'Progress', 'Deadline']]
        for g in goals:
            progress = (g.current_amount / g.target_amount * 100) if g.target_amount > 0 else 0
            data.append([
                g.name,
                f"${g.target_amount:.2f}",
                f"${g.current_amount:.2f}",
                f"{progress:.1f}%",
                g.deadline.strftime('%Y-%m-%d') if g.deadline else 'N/A'
            ])
        
        # Crear tabla
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("No goals found.", styles['Normal']))
    
    # Pie de página
    footer_text = "MyFinPlanner - Your Financial Companion"
    elements.append(Spacer(1, 30))
    footer_style = styles['Normal']
    footer_style.alignment = 1
    footer_style.textColor = colors.grey
    elements.append(Paragraph(footer_text, footer_style))
    
    # Construir el PDF
    doc.build(elements)
    return response