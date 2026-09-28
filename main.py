import flet as ft


def main(page: ft.Page):
    page.title = "Afraa"
    page.bgcolor = "#4A148C"
    page.add(
        ft.Text(
            "Afraa",
            size=60,
            color="#FFD700",
            weight=ft.FontWeight.BOLD,
        )
    )


ft.app(target=main, assets_dir="assets")
