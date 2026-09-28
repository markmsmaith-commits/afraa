import flet as ft
import json
import os
from datetime import datetime

DATA_FILE = "afraa_data.json"
SECRET_CODE = "018755"

PURPLE = "#6A1B9A"
DEEP_BLUE = "#0288D1"
GOLD = "#FFD700"
PINK = "#FF4081"
RED = "#E53935"


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
    page.bgcolor = "#1A0B2E"

    state = {"records": load_data()}

    # ─── الاسم الذهبي ───
    name = ft.Text(
        "𝔸𝕗𝕣𝕒𝕒",
        size=56,
        color=GOLD,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    # ─── الإحصائيات ───
    days_txt = ft.Text("0", size=24, color=DEEP_BLUE, weight=ft.FontWeight.BOLD)
    total_txt = ft.Text("0", size=24, color=DEEP_BLUE, weight=ft.FontWeight.BOLD)

    days_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("عدد الأيام", size=13, color=PURPLE,
                        weight=ft.FontWeight.BOLD),
                days_txt,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        bgcolor="#FFFFFF",
        border_radius=20,
        border=ft.border.all(2, DEEP_BLUE),
        padding=14,
        expand=True,
    )

    total_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("المجموع الكلي", size=13, color=PURPLE,
                        weight=ft.FontWeight.BOLD),
                total_txt,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        bgcolor="#FFFFFF",
        border_radius=20,
        border=ft.border.all(2, GOLD),
        padding=14,
        expand=True,
    )

    # ─── حقل الإدخال ───
    wage_input = ft.TextField(
        label="الأجر اليومي",
        hint_text="أدخل المبلغ...",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.RIGHT,
        border_radius=20,
        border_color=DEEP_BLUE,
        focused_border_color=GOLD,
        bgcolor="#FFFFFF",
        color="#1A0B2E",
        height=60,
    )

    # ─── قائمة السجلات ───
    records_list = ft.Column(spacing=8)

    def refresh():
        recs = state["records"]
        days_txt.value = str(len(recs))
        try:
            total = sum(float(r["wage"]) for r in recs)
        except Exception:
            total = 0
        total_txt.value = f"{total:,.0f}"

        records_list.controls.clear()
        for r in reversed(recs):
            records_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(r.get("date", ""), size=14,
                                            color=PURPLE,
                                            weight=ft.FontWeight.BOLD),
                                    ft.Text(r.get("time", ""), size=11,
                                            color="#666666"),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Text(
                                f"{float(r['wage']):,.0f}",
                                size=18,
                                color=DEEP_BLUE,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor="#FFFFFF",
                    border_radius=16,
                    border=ft.border.all(2, DEEP_BLUE),
                    padding=12,
                )
            )
        page.update()

    # ─── نافذة الرسالة الرومانسية ───
    def close_love(e):
        love_dialog.open = False
        page.update()

    love_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            "💖 بحبك 💖",
            size=30,
            color=PINK,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        ),
        content=ft.Column(
            [
                ft.Text("🌹 💕 🌹", size=32, text_align=ft.TextAlign.CENTER),
                ft.Text(
                    "ولك شبر ونص",
                    size=22,
                    color=PURPLE,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text("💖 💗 💝 💞 💕", size=26,
                        text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
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

        if val == SECRET_CODE:
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
        bgcolor=DEEP_BLUE,
        color="#FFFFFF",
        height=52,
        expand=True,
    )

    reset_btn = ft.ElevatedButton(
        "🗑 إعادة تعيين",
        on_click=reset_all,
        bgcolor=RED,
        color="#FFFFFF",
        height=52,
        expand=True,
    )

    # ─── المحتوى ───
    content = ft.Column(
        [
            ft.Container(height=20),
            name,
            ft.Container(height=10),
            ft.Row([days_card, total_card], spacing=10),
            ft.Container(height=10),
            wage_input,
            ft.Row([add_btn, reset_btn], spacing=10),
            ft.Container(height=10),
            ft.Text("📋 السجلات", size=16, color=GOLD,
                    weight=ft.FontWeight.BOLD),
            records_list,
            ft.Container(height=20),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    # ─── الخلفية مع الباندا ───
    page.add(
        ft.Container(
            content=ft.Container(
                content=content,
                padding=18,
            ),
            image_src="bg.jpg",
            image_fit=ft.ImageFit.COVER,
            expand=True,
        )
    )

    refresh()


ft.app(target=main, assets_dir="assets")
