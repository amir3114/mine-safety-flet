
import flet as ft
import random
from datetime import datetime
from fpdf import FPDF

def main(page: ft.Page):
    page.title = "سامانه پایش ایمنی معادن"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    reports_file = "daily_reports.txt"
    alerts_file = "alerts.txt"

    def save_status(e):
        date = txt_date.value
        status = txt_status.value
        if not date or not status:
            page.show_snack_bar(ft.SnackBar(ft.Text("لطفاً تمامی فیلدها را پر کنید")))
            return
        with open(reports_file, "a") as f:
            f.write(f"{date} - {status}\n")
        page.clean()
        page.add(ft.Text("✅ وضعیت ثبت شد!", size=20))
        page.add(ft.ElevatedButton("بازگشت", on_click=lambda e: show_menu()))

    def save_alert(e):
        alert_type = txt_alert_type.value
        desc = txt_alert_desc.value
        if not alert_type or not desc:
            page.show_snack_bar(ft.SnackBar(ft.Text("لطفاً تمامی فیلدها را پر کنید")))
            return
        with open(alerts_file, "a") as f:
            f.write(f"⚠️ هشدار: {alert_type} - {desc}\n")
        page.clean()
        page.add(ft.Text("⚠️ هشدار ثبت شد!", size=20))
        page.add(ft.ElevatedButton("بازگشت", on_click=lambda e: show_menu()))

    def simulate_sensor(e):
        methane_level = random.uniform(0, 5)
        msg = f"سطح گاز متان: {methane_level:.2f} ppm\n"
        if methane_level > 2.5:
            msg += "🚨 هشدار: سطح گاز متان خطرناک است!"
            with open(alerts_file, "a") as f:
                f.write(f"⚠️ هشدار: سطح متان بالاست! ({methane_level:.2f})\n")
        else:
            msg += "✅ وضعیت سالم."
        page.clean()
        page.add(ft.Text(msg, size=16))
        page.add(ft.ElevatedButton("بازگشت", on_click=lambda e: show_menu()))

    def generate_pdf(e):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        try:
            with open(reports_file) as f:
                lines = f.readlines()
                pdf.cell(0, 10, txt="📊 گزارش ایمنی معدن", ln=True, align='C')
                pdf.ln(10)
                for line in lines:
                    pdf.cell(0, 8, txt=line.strip(), ln=True)
        except FileNotFoundError:
            pass

        try:
            with open(alerts_file) as f:
                lines = f.readlines()
                pdf.ln(10)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, txt="⚠️ هشدارها:", ln=True)
                pdf.set_font("Arial", size=10)
                for line in lines:
                    pdf.cell(0, 8, txt=line.strip(), ln=True)
        except FileNotFoundError:
            pass

        pdf.output("report.pdf")
        page.show_snack_bar(ft.SnackBar(ft.Text("📄 PDF ساخته شد!")))
        page.launch_url("report.pdf")

    def show_reports(e):
        page.clean()
        daily = ""
        alerts = ""

        try:
            with open(reports_file, "r") as f:
                daily = f.read()
        except FileNotFoundError:
            daily = "هنوز وضعیتی ثبت نشده."

        try:
            with open(alerts_file, "r") as f:
                alerts = f.read()
        except FileNotFoundError:
            alerts = "هیچ هشداری ثبت نشده."

        page.add(ft.Text("📜 گزارش وضعیت‌ها:\n" + daily, size=14))
        page.add(ft.Text("\n⚠️ گزارش هشدارها:\n" + alerts, size=14))
        page.add(ft.ElevatedButton("بازگشت", on_click=lambda e: show_menu()))

    def show_menu():
        page.clean()
        page.add(ft.Text("سامانه پایش ایمنی معادن", size=20, weight=ft.FontWeight.BOLD))

        # ثبت وضعیت ایمنی
        page.add(
            ft.ElevatedButton("ثبت وضعیت ایمنی", on_click=lambda e: (
                page.clean(),
                page.add(ft.Text("ثبت وضعیت", size=18)),
                page.add(ft.TextField(label="تاریخ", hint_text="1403/01/01", ref=txt_date_ref)),
                page.add(ft.TextField(label="وضعیت ایمنی", hint_text="مثلاً خوب / نیمه خوب / خطرناک", ref=txt_status_ref)),
                page.add(ft.ElevatedButton("ثبت", on_click=save_status))
            ))
        )

        # ثبت هشدار
        page.add(
            ft.ElevatedButton("ثبت هشدار", on_click=lambda e: (
                page.clean(),
                page.add(ft.Text("ثبت هشدار", size=18)),
                page.add(ft.TextField(label="نوع هشدار", hint_text="گاز متان، ریزش، تجهیزات", ref=txt_alert_type_ref)),
                page.add(ft.TextField(label="توضیحات", hint_text="توضیحات خود را بنویسید...", ref=txt_alert_desc_ref)),
                page.add(ft.ElevatedButton("ثبت", on_click=save_alert))
            ))
        )

        # گزارش‌ها
        page.add(ft.ElevatedButton("نمایش گزارش‌ها", on_click=show_reports))

        # ساخت PDF
        page.add(ft.ElevatedButton("ساخت PDF", on_click=generate_pdf))

        # سنسور
        page.add(ft.ElevatedButton("شبیه‌سازی سنسور متان", on_click=simulate_sensor))

        # خروج
        page.add(ft.ElevatedButton("خروج", on_click=lambda e: page.window_close()))

    txt_date_ref = ft.Ref[ft.TextField]()
    txt_status_ref = ft.Ref[ft.TextField]()
    txt_alert_type_ref = ft.Ref[ft.TextField]()
    txt_alert_desc_ref = ft.Ref[ft.TextField]()

    show_menu()

ft.app(target=main, view=ft.WEB_BROWSER)
