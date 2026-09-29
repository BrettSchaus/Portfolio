import os
import hashlib
import flet as ft
from flet_permission_handler import PermissionHandler, Permission, PermissionStatus
from PIL import Image as PILImage

def main(page: ft.Page):
    page.title = "Android Gallery with Caching"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10

    # Cache directory for generated thumbnails
    cache_base = os.getenv("FLET_APP_STORAGE_CACHE", "/tmp")
    cache_dir = os.path.join(cache_base, "thumb_cache")
    os.makedirs(cache_dir, exist_ok=True)

    gallery_grid = ft.GridView(
        expand=True,
        max_extent=120,
        child_aspect_ratio=1.0,
        spacing=6,
        run_spacing=6,
    )

    ph = None

    if os.getenv("FLET_PLATFORM") == "android":
        ph = PermissionHandler()

    def get_or_create_thumbnail(image_path: str) -> str:
        """Generates a small thumbnail and saves it to cache, or returns existing cached path."""
        # Create a unique filename based on the file path string
        file_hash = hashlib.md5(image_path.encode("utf-8")).hexdigest()
        thumb_path = os.path.join(cache_dir, f"{file_hash}.jpg")

        # If thumbnail already exists, skip processing
        if os.path.exists(thumb_path):
            return thumb_path

        try:
            with PILImage.open(image_path) as img:
                # Resize image while preserving aspect ratio (max 250x250)
                img.thumbnail((250, 250))
                # Convert to RGB to ensure saving as JPEG succeeds
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(thumb_path, "JPEG", quality=80)
            return thumb_path
        except Exception:
            # Fallback to full image if Pillow fails
            return image_path

    def load_dcim_photos():
        if os.getenv("FLET_PLATFORM") == "android":
            possible_paths = [
                "/storage/emulated/0/DCIM/Camera",
                "/storage/emulated/0/DCIM",
                "/storage/emulated/0/Pictures",
                "/sdcard/DCIM/Camera",
                "/sdcard/DCIM",
                "/sdcard/Pictures",
            ]
        else:
            possible_paths = [
                os.path.expanduser("~/Pictures"),
            ]

        found_paths = []

        for path in possible_paths:
            if os.path.exists(path):
                found_paths.append(path)

        if not found_paths:
            page.show_dialog(
                ft.AlertDialog(
                    title=ft.Text("No photo directories found"),
                    content=ft.Text(
                        "I couldn't find any of these directories:\n\n"
                        + "\n".join(possible_paths)
                    ),
                )
            )
            return

        # Use the first directory that exists
        dcim_path = found_paths[0]

        gallery_grid.controls.clear()

        valid_exts = (".jpg", ".jpeg", ".png", ".webp")

        files_found = []

        try:
            for file in os.listdir(dcim_path):
                if file.lower().endswith(valid_exts):
                    files_found.append(file)

        except Exception as ex:
            page.show_dialog(
                ft.AlertDialog(
                    title=ft.Text("Directory access error"),
                    content=ft.Text(
                        f"Path:\n{dcim_path}\n\n"
                        f"Error:\n{ex}"
                    ),
                )
            )
            return

        if not files_found:
            page.show_dialog(
                ft.AlertDialog(
                    title=ft.Text("Directory is empty"),
                    content=ft.Text(
                        f"Directory found:\n{dcim_path}\n\n"
                        "But no supported image files were found."
                    ),
                )
            )
            return

        for file in files_found:
            full_path = os.path.join(dcim_path, file)

            thumb_path = get_or_create_thumbnail(full_path)

            gallery_grid.controls.append(
                ft.Container(
                    content=ft.Image(
                        src=thumb_path,
                        fit=ft.BoxFit.COVER,
                        border_radius=ft.BorderRadius(
                            top_left=6,
                            top_right=6,
                            bottom_left=6,
                            bottom_right=6,
                        ),
                    ),
                    on_click=lambda _, p=full_path: open_preview(p),
                )
            )

        page.update()

    async def request_and_load(e=None):
        if os.getenv("FLET_PLATFORM") == "android":
            status = await ph.request(Permission.PHOTOS)

            if status == PermissionStatus.GRANTED:
                load_dcim_photos()
            else:
                page.show_dialog(
                    ft.SnackBar(
                        content=ft.Text("Photo permission was not granted.")
                    )
                )
        else:
            # Linux desktop testing
            load_dcim_photos()

    def open_preview(original_image_path):
        def close_dlg(e):
            page.pop_dialog()

        dialog = ft.AlertDialog(
            content=ft.Container(
                content=ft.Image(
                    src=original_image_path,
                    fit=ft.BoxFit.CONTAIN,
                    expand=True,
                ),
                expand=True,
            ),
            content_padding=0,
            inset_padding=0,
        )

        page.show_dialog(dialog)

    load_btn = ft.Button(
        content="Load Device Photos",
        icon=ft.Icons.PHOTO_LIBRARY,
        on_click=request_and_load,
    )

    page.add(
        ft.Container(
            content=ft.Row(
                [load_btn],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.Padding.only(top=20),
        ),
        gallery_grid,
    )

    # Automatically request permission and load photos on Android
    if os.getenv("FLET_PLATFORM") == "android":
        page.run_task(request_and_load)

if __name__ == "__main__":
    ft.run(main)