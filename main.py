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
    page.bgcolor = "#0D47A1"
    page.padding = 0
    page.spacing = 0

    state = {"records": load_data()}

    # ═══ الاسم ═══
    name_text = ft.Text(
        "Afraa",
        size=44,
        color="#FFD700",
        weight=ft.FontWeight.BOLD,
    )

    # ═══ الإحصائيات (بطاقات زجاجية) ═══
    days_text = ft.Text("0", size=22, color="#FFFFFF",
                         weight=ft.FontWeight.BOLD)
    total_text = ft.Text("0", size=22, color="#FFFFFF",
                          weight=ft.FontWeight.BOLD)

    days_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("📅 أيام", size=12, color="#B3E5FC",
                        weight=ft.FontWeight.BOLD),
                days_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        bgcolor=ft.Colors.with_opacity(0.35, "#FFFFFF"),
        border_radius=20,
        border=ft.border.all(1.5, ft.Colors.with_opacity(0.7, "#00E5FF")),
        padding=16,
        expand=True,
    )

    total_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("💰 مجموع", size=12, color="#B3E5FC",
                        weight=ft.FontWeight.BOLD),
                total_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        bgcolor=ft.Colors.with_opacity(0.35, "#FFFFFF"),
        border_radius=20,
        border=ft.border.all(1.5, ft.Colors.with_opacity(0.7, "#FFD700")),
        padding=16,
        expand=True,
    )

    # ═══ حقل الإدخال الزجاجي 💎 ═══
    wage_input = ft.TextField(
        label="💧 الأجر اليومي",
        hint_text="أدخل المبلغ...",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.RIGHT,
        border_radius=24,
        border_width=1.5,
        border_color=ft.Colors.with_opacity(0.7, "#00E5FF"),
        focused_border_color="#FFD700",
        bgcolor=ft.Colors.with_opacity(0.30, "#FFFFFF"),
        color="#FFFFFF",
        text_style=ft.TextStyle(size=17, color="#FFFFFF"),
        label_style=ft.TextStyle(
            color="#B3E5FC",
            weight=ft.FontWeight.BOLD,
            size=14,
        ),
        cursor_color="#FFD700",
        height=64,
    )

    # ═══ قائمة السجلات ═══
    records_list = ft.Column(spacing=6)

    # ═══ الرسالة الرومانسية (Overlay) ═══
    def close_love(e):
        love_overlay.visible = False
        page.update()

    love_overlay = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.95, "#E91E63"),
        visible=False,
        expand=True,
        content=ft.Column(
            [
                ft.Text("💕", size=90),
                ft.Text("بحبك", size=64, color="#FFD700",
                        weight=ft.FontWeight.BOLD),
                ft.Text("ولك شبر ونص", size=30, color="#FFFFFF",
                        weight=ft.FontWeight.BOLD),
                ft.Text("🌹  💕  🌹", size=48),
                ft.Text("💖 💗 💝 💞", size=36),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "💕 إغلاق",
                    on_click=close_love,
                    bgcolor="#FFFFFF",
                    color="#E91E63",
                    height=52,
                    width=180,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=14,
        ),
    )

    # ═══ التحديث ═══
    def refresh():
        recs = state["records"]
        days_text.value = str(len(recs))
        try:
            total = sum(float(r["wage"]) for r in recs)
        except Exception:
            total = 0
        total_text.value = f"{total:,.0f}"

        records_list.controls.clear()
        for r in reversed(recs):
            records_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(r.get("date", ""), size=13,
                                    color="#B3E5FC"),
                            ft.Text(f"{float(r['wage']):,.0f}", size=16,
                                    color="#FFFFFF",
                                    weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.25, "#FFFFFF"),
                    border_radius=14,
                    border=ft.border.all(
                        1, ft.Colors.with_opacity(0.4, "#00E5FF")
                    ),
                    padding=12,
                )
            )
        page.update()

    # ═══ المعالجات ═══
    def add_day(e):
        val = (wage_input.value or "").strip()
        if not val:
            return
        if val == "018755":
            wage_input.value = ""
            love_overlay.visible = True
            page.update()
            return
        try:
            wage = float(val)
        except ValueError:
            return
        now = datetime.now()
        state["records"].append({
            "wage": wage,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M"),
            "timestamp": now.timestamp(),
        })
        save_data(state["records"])
        wage_input.value = ""
        refresh()

    def reset_all(e):
        state["records"] = []
        save_data([])
        refresh()

    # ═══ الأزرار الزجاجية 💎 ═══
    add_btn = ft.Container(
        content=ft.Text("➕ إضافة اليوم", size=15, color="#FFFFFF",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER),
        bgcolor=ft.Colors.with_opacity(0.50, "#00BCD4"),
        border_radius=22,
        border=ft.border.all(1.5, ft.Colors.with_opacity(0.7, "#00E5FF")),
        padding=ft.padding.symmetric(horizontal=16, vertical=16),
        alignment=ft.alignment.center,
        height=56,
        expand=True,
        ink=True,
        on_click=add_day,
    )

    reset_btn = ft.Container(
        content=ft.Text("🗑 إعادة تعيين", size=15, color="#FFFFFF",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER),
        bgcolor=ft.Colors.with_opacity(0.50, "#E53935"),
        border_radius=22,
        border=ft.border.all(1.5, ft.Colors.with_opacity(0.7, "#FF8A80")),
        padding=ft.padding.symmetric(horizontal=16, vertical=16),
        alignment=ft.alignment.center,
        height=56,
        expand=True,
        ink=True,
        on_click=reset_all,
    )

    # ═══ المحتوى ═══
    content = ft.Column(
        [
            ft.Container(height=25),
            name_text,
            ft.Container(height=20),
            ft.Row([days_card, total_card], spacing=12),
            ft.Container(height=18),
            wage_input,
            ft.Container(height=10),
            ft.Row([add_btn, reset_btn], spacing=12),
            ft.Container(height=18),
            ft.Text("📋 السجلات", size=15, color="#FFD700",
                    weight=ft.FontWeight.BOLD),
            records_list,
            ft.Container(height=25),
        ],
        spacing=8,
        scroll=ft.ScrollMode.AUTO,
    )

    # ═══ الجذر: خلفية متدرجة (بدون Stack معقد) ═══
    page.add(
        ft.Container(
            content=ft.Container(
                content=content,
                padding=20,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#4A148C", "#0D47A1", "#006064"],
            ),
            expand=True,
        ),
        love_overlay,
    )

    refresh()


ft.app(target=main, assets_dir="assets")
