import flet as ft
import json
import os
from datetime import datetime

DATA_FILE = "afraa_data.json"


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_data(records):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def main(page: ft.Page):
    page.title = "Afraa"
    page.rtl = True
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#4A148C"

    state = {"records": load_data()}

    # ─── الاسم الجديد ───
    name_text = ft.Text(
        "𝔸𝕗𝕣𝕒𝕒",
        size=42,
        color="#FFD700",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    # ─── الإحصائيات ───
    days_value = ft.Text("0", size=26, color="#6A1B9A", weight=ft.FontWeight.BOLD)
    total_value = ft.Text("0", size=26, color="#6A1B9A", weight=ft.FontWeight.BOLD)

    days_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("عدد الأيام", size=14, color="#4A148C",
                        weight=ft.FontWeight.BOLD),
                days_value,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        bgcolor=ft.Colors.with_opacity(0.88, "#FFFFFF"),
        border_radius=16,
        border=ft.border.all(2, "#00BCD4"),
        padding=14,
        expand=True,
    )

    total_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("المجموع الكلي", size=14, color="#4A148C",
                        weight=ft.FontWeight.BOLD),
                total_value,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        bgcolor=ft.Colors.with_opacity(0.88, "#FFFFFF"),
        border_radius=16,
        border=ft.border.all(2, "#FFD700"),
        padding=14,
        expand=True,
    )

    # ─── حقل الإدخال ───
    wage_input = ft.TextField(
        label="الأجر اليومي",
        hint_text="أدخل المبلغ...",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.RIGHT,
        border_radius=16,
        border_color="#00BCD4",
        focused_border_color="#FFD700",
        bgcolor=ft.Colors.with_opacity(0.92, "#FFFFFF"),
        color="#4A148C",
        height=60,
    )

    # ─── قائمة السجلات ───
    records_list = ft.Column(spacing=8)

    def refresh():
        recs = state["records"]
        days_value.value = str(len(recs))
        try:
            total = sum(float(r["wage"]) for r in recs)
        except Exception:
            total = 0
        total_value.value = f"{total:,.0f}"

        records_list.controls.clear()
        for r in reversed(recs):
            records_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(r.get("date", ""), size=14,
                                            color="#4A148C",
                                            weight=ft.FontWeight.BOLD),
                                    ft.Text(r.get("time", ""), size=11,
                                            color="#666666"),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Text(
                                f"{float(r['wage']):,.0f}",
                                size=20,
                                color="#6A1B9A",
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.9, "#FFFFFF"),
                    border_radius=14,
                    border=ft.border.all(1.5, "#00BCD4"),
                    padding=12,
                )
            )
        page.update()

    # ─── الرسالة الرومانسية 💕 ───
    def close_love(e):
        love_dialog.open = False
        page.update()

    love_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("💖", size=40, text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                ft.Text("بحبك", size=36, color="#E91E63",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER),
                ft.Text("ولك شبر ونص", size=22, color="#6A1B9A",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER),
                ft.Text("🌹 💕 🌹", size=28, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            tight=True,
        ),
        actions=[
            ft.TextButton("💕 إغلاق", on_click=close_love),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    # ─── المعالجات ───
    def add_day(e):
        val = (wage_input.value or "").strip()
        if not val:
            return

        # الكود السري
        if val == "018755":
            wage_input.value = ""
            page.dialog = love_dialog
            love_dialog.open = True
            page.update()
            return

        try:
            wage = float(val)
        except ValueError:
            return

        now = datetime.now()
        state["records"].append(
            {
                "wage": wage,
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M"),
                "timestamp": now.timestamp(),
            }
        )
        save_data(state["records"])
        wage_input.value = ""
        refresh()

    def reset_all(e):
        state["records"] = []
        save_data([])
        refresh()

    # ─── الأزرار ───
    add_btn = ft.ElevatedButton(
        "➕ إضافة اليوم",
        on_click=add_day,
        bgcolor="#6A1B9A",
        color="#FFFFFF",
        height=54,
        expand=True,
    )

    reset_btn = ft.ElevatedButton(
        "🗑 إعادة تعيين",
        on_click=reset_all,
        bgcolor="#E53935",
        color="#FFFFFF",
        height=54,
        expand=True,
    )

    # ─── المحتوى ───
    content = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=20),
                name_text,
                ft.Container(height=10),
                ft.Row([days_card, total_card], spacing=12),
                ft.Container(height=10),
                wage_input,
                ft.Container(height=4),
                ft.Row([add_btn, reset_btn], spacing=12),
                ft.Container(height=6),
                ft.Text("📋 السجلات", size=17, color="#FFD700",
                        weight=ft.FontWeight.BOLD),
                records_list,
                ft.Container(height=20),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=20,
        expand=True,
    )

    # ─── الجذر مع خلفية الباندا ───
    page.add(
        ft.Stack(
            [
                ft.Image(src="bg.jpg", fit=ft.ImageFit.COVER, expand=True),
                ft.Container(bgcolor="#6A1B9A", opacity=0.55, expand=True),
                content,
            ],
            expand=True,
        )
    )
    refresh()


ft.app(target=main, assets_dir="assets")
