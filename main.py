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
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    state = {"records": load_data()}

    # العناصر
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
                    bgcolor="#FFFFFF",
                    border_radius=12,
                    padding=12,
                )
            )
        page.update()

    # نافذة الرسالة السرية
    def close_dialog(e):
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text("💕", size=30),
        content=ft.Column(
            [
                ft.Text("بحبك", size=30, color="#E91E63",
                        weight=ft.FontWeight.BOLD),
                ft.Text("ولك شبر ونص", size=18, color="#6A1B9A"),
                ft.Text("🌹 💕 🌹", size=24),
            ],
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        actions=[ft.TextButton("إغلاق", on_click=close_dialog)],
    )

    def add_day(e):
        val = (wage_input.value or "").strip()
        if not val:
            return
        if val == "018755":
            wage_input.value = ""
            page.dialog = dlg
            dlg.open = True
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

    # الواجهة
    page.add(
        name_text,
        ft.Container(height=10),
        ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [ft.Text("أيام", size=12, color="#4A148C"), days_text],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor="#FFFFFF",
                    border_radius=14,
                    padding=12,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        [ft.Text("مجموع", size=12, color="#4A148C"), total_text],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor="#FFFFFF",
                    border_radius=14,
                    padding=12,
                    expand=True,
                ),
            ],
            spacing=10,
        ),
        ft.Container(height=10),
        wage_input,
        ft.Container(height=6),
        ft.Row(
            [
                ft.ElevatedButton(
                    "➕ إضافة",
                    on_click=add_day,
                    bgcolor="#0288D1",
                    color="#FFFFFF",
                    height=48,
                    expand=True,
                ),
                ft.ElevatedButton(
                    "🗑 حذف",
                    on_click=reset_all,
                    bgcolor="#E53935",
                    color="#FFFFFF",
                    height=48,
                    expand=True,
                ),
            ],
            spacing=10,
        ),
        ft.Container(height=10),
        ft.Text("📋 السجلات", size=15, color="#FFD700",
                weight=ft.FontWeight.BOLD),
        records_list,
    )

    refresh()


ft.app(target=main, assets_dir="assets")
