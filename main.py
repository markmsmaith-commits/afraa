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
    page.bgcolor = "#4A148C"
    page.padding = 0
    page.spacing = 0

    state = {"records": load_data()}

    # ═══ العناصر ═══
    name_text = ft.Text(
        "Afraa",
        size=42,
        color="#FFD700",
        weight=ft.FontWeight.BOLD,
    )

    days_text = ft.Text("0", size=22, color="#6A1B9A",
                         weight=ft.FontWeight.BOLD)
    total_text = ft.Text("0", size=22, color="#6A1B9A",
                          weight=ft.FontWeight.BOLD)

    wage_input = ft.TextField(
        label="الأجر اليومي",
        keyboard_type=ft.KeyboardType.NUMBER,
        bgcolor="#FFFFFF",
        color="#4A148C",
        border_radius=14,
        height=58,
    )

    records_list = ft.Column(spacing=6)

    # ═══ نافذة الرسالة الرومانسية (Overlay) ═══
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
                    "إغلاق 💕",
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
                                    color="#4A148C"),
                            ft.Text(f"{float(r['wage']):,.0f}", size=16,
                                    color="#6A1B9A",
                                    weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.92, "#FFFFFF"),
                    border_radius=12,
                    padding=12,
                )
            )
        page.update()

    # ═══ المعالجات ═══
    def add_day(e):
        val = (wage_input.value or "").strip()
        if not val:
            return

        # 💕 الكود السري
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

    # ═══ المحتوى الرئيسي ═══
    content = ft.Column(
        [
            ft.Container(height=20),
            name_text,
            ft.Container(height=15),
            ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("أيام", size=12, color="#4A148C"),
                                days_text,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        bgcolor=ft.Colors.with_opacity(0.9, "#FFFFFF"),
                        border_radius=14,
                        padding=14,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("مجموع", size=12, color="#4A148C"),
                                total_text,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        bgcolor=ft.Colors.with_opacity(0.9, "#FFFFFF"),
                        border_radius=14,
                        padding=14,
                        expand=True,
                    ),
                ],
                spacing=10,
            ),
            ft.Container(height=15),
            wage_input,
            ft.Container(height=8),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "➕ إضافة",
                        on_click=add_day,
                        bgcolor="#0288D1",
                        color="#FFFFFF",
                        height=50,
                        expand=True,
                    ),
                    ft.ElevatedButton(
                        "🗑 حذف",
                        on_click=reset_all,
                        bgcolor="#E53935",
                        color="#FFFFFF",
                        height=50,
                        expand=True,
                    ),
                ],
                spacing=10,
            ),
            ft.Container(height=15),
            ft.Text("📋 السجلات", size=15, color="#FFD700",
                    weight=ft.FontWeight.BOLD),
            records_list,
            ft.Container(height=20),
        ],
        spacing=8,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # ═══ الجذر: خلفية الباندا + المحتوى + نافذة الرسالة ═══
    page.add(
        ft.Stack(
            [
                # 1) صورة الباندا
                ft.Image(src="bg.jpg", fit=ft.ImageFit.COVER, expand=True),
                # 2) طبقة بنفسجية شفافة
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.55, "#4A148C"),
                    expand=True,
                ),
                # 3) المحتوى
                ft.Container(
                    content=content,
                    padding=20,
                    expand=True,
                ),
                # 4) نافذة الرسالة (مخفية حتى تُستدعى)
                love_overlay,
            ],
            expand=True,
        )
    )

    refresh()


ft.app(target=main, assets_dir="assets")
