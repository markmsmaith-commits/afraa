import flet as ft
import json
import os
from datetime import datetime

DATA_FILE = "afraa_data.json"
SECRET_CODE = "018755"

PURPLE = "#6A1B9A"
DEEP_BLUE = "#0288D1"
TURQUOISE = "#00BCD4"
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

    # ═══════════════════════════════════════
    #  الاسم 3D ذهبي (آمن - بدون offset)
    # ═══════════════════════════════════════
    NAME = "𝔸𝕗𝕣𝕒𝕒"
    SIZE = 58

    name_stack = ft.Stack(
        [
            # طبقة 1: ظل أسود
            ft.Container(
                content=ft.Text(NAME, size=SIZE, color="#1A0000",
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER),
                left=6, top=7,
            ),
            # طبقة 2: ذهبي داكن جدًا
            ft.Container(
                content=ft.Text(NAME, size=SIZE, color="#5D4200",
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER),
                left=4, top=5,
            ),
            # طبقة 3: ذهبي غامق
            ft.Container(
                content=ft.Text(NAME, size=SIZE, color="#8D6E00",
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER),
                left=2, top=3,
            ),
            # طبقة 4: ذهبي متوسط
            ft.Container(
                content=ft.Text(NAME, size=SIZE, color="#FFA000",
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER),
                left=1, top=1,
            ),
            # طبقة 5: الذهبي اللامع (الأمامي)
            ft.Container(
                content=ft.Text(NAME, size=SIZE, color=GOLD,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER),
                left=0, top=0,
            ),
        ],
        height=SIZE + 30,
        width=420,
    )

    name_container = ft.Container(
        content=name_stack,
        alignment=ft.alignment.center,
        padding=ft.padding.only(top=20, bottom=15),
    )

    # ═══════════════════════════════════════
    #  الإحصائيات
    # ═══════════════════════════════════════
    days_txt = ft.Text("0", size=24, color=DEEP_BLUE, weight=ft.FontWeight.BOLD)
    total_txt = ft.Text("0", size=24, color=GOLD, weight=ft.FontWeight.BOLD)

    days_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("📅 عدد الأيام", size=13, color=PURPLE,
                        weight=ft.FontWeight.BOLD),
                days_txt,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        bgcolor=ft.Colors.with_opacity(0.92, "#FFFFFF"),
        border_radius=24,
        border=ft.border.all(2.5, DEEP_BLUE),
        padding=16,
        expand=True,
    )

    total_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("💰 المجموع الكلي", size=13, color=PURPLE,
                        weight=ft.FontWeight.BOLD),
                total_txt,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        bgcolor=ft.Colors.with_opacity(0.92, "#FFFFFF"),
        border_radius=24,
        border=ft.border.all(2.5, GOLD),
        padding=16,
        expand=True,
    )

    # ═══════════════════════════════════════
    #  حقل الإدخال الزجاجي
    # ═══════════════════════════════════════
    wage_input = ft.TextField(
        label="💧 الأجر اليومي",
        hint_text="أدخل المبلغ...",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.RIGHT,
        border_radius=28,
        border_width=2.5,
        border_color=ft.Colors.with_opacity(0.7, DEEP_BLUE),
        focused_border_color=GOLD,
        bgcolor=ft.Colors.with_opacity(0.35, "#FFFFFF"),
        color="#FFFFFF",
        text_style=ft.TextStyle(size=18, color="#FFFFFF"),
        label_style=ft.TextStyle(color="#B3E5FC",
                                  weight=ft.FontWeight.BOLD, size=14),
        cursor_color=GOLD,
        height=65,
    )

    # ═══════════════════════════════════════
    #  قائمة السجلات
    # ═══════════════════════════════════════
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
                                size=20,
                                color=DEEP_BLUE,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.92, "#FFFFFF"),
                    border_radius=20,
                    border=ft.border.all(2, DEEP_BLUE),
                    padding=14,
                )
            )
        page.update()

    # ═══════════════════════════════════════
    #  النافذة الرومانسية الفخمة 💕
    # ═══════════════════════════════════════
    def close_love(e):
        love_dialog.open = False
        page.update()

    love_content = ft.Column(
        [
            ft.Text("💖  💕  💗  💝  💞",
                    size=28, text_align=ft.TextAlign.CENTER),
            ft.Container(height=8),
            ft.Text(
                "بحبك",
                size=44,
                color=GOLD,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "ولك شبر ونص",
                size=26,
                color=PINK,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=8),
            ft.Text("🌹  🌹  🌹  🌹",
                    size=30, text_align=ft.TextAlign.CENTER),
            ft.Container(height=4),
            ft.Text("❤️  💖  💕  💗  💝",
                    size=26, text_align=ft.TextAlign.CENTER),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6,
        tight=True,
    )

    love_dialog = ft.AlertDialog(
        modal=True,
        bgcolor="#FFF0F5",
        title=ft.Text(
            "💕 رسالة خاصة 💕",
            size=22,
            color=PINK,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        ),
        content=ft.Container(
            content=love_content,
            width=300,
            padding=10,
        ),
        actions=[
            ft.Container(
                content=ft.Text("💕 إغلاق", size=16, color="#FFFFFF",
                                weight=ft.FontWeight.BOLD),
                bgcolor=PINK,
                border_radius=20,
                padding=ft.padding.symmetric(horizontal=30, vertical=10),
                on_click=close_love,
                ink=True,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    # ═══════════════════════════════════════
    #  المعالجات
    # ═══════════════════════════════════════
    def add_day(e):
        val = (wage_input.value or "").strip()
        if not val:
            return

        # 💕 الكود السري
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

    # ═══════════════════════════════════════
    #  الأزرار (مع تأثير مائي Ink)
    # ═══════════════════════════════════════
    def make_button(text, color, handler):
        return ft.Container(
            content=ft.Text(
                text,
                size=16,
                color="#FFFFFF",
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            bgcolor=color,
            border_radius=24,
            padding=ft.padding.symmetric(horizontal=16, vertical=16),
            alignment=ft.alignment.center,
            height=56,
            expand=True,
            ink=True,
            on_click=handler,
        )

    add_btn = make_button("➕ إضافة اليوم", DEEP_BLUE, add_day)
    reset_btn = make_button("🗑 إعادة تعيين", RED, reset_all)

    # ═══════════════════════════════════════
    #  المحتوى
    # ═══════════════════════════════════════
    content = ft.Column(
        [
            name_container,
            ft.Container(height=10),
            ft.Row([days_card, total_card], spacing=10),
            ft.Container(height=10),
            wage_input,
            ft.Container(height=6),
            ft.Row([add_btn, reset_btn], spacing=10),
            ft.Container(height=10),
            ft.Text("📋 السجلات", size=17, color=GOLD,
                    weight=ft.FontWeight.BOLD),
            records_list,
            ft.Container(height=20),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    # ═══════════════════════════════════════
    #  الجذر: خلفية الباندا + المحتوى
    # ═══════════════════════════════════════
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
