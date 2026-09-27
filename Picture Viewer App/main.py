import os
import hashlib
import flet as ft
from flet_permission_handler import PermissionHandler, Permission
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
        dcim_path = os.path.expanduser("~/Pictures")  # When testing on laptop
        # dcim_path = "/storage/emulated/0/DCIM/Camera"
        if not os.path.exists(dcim_path):
            dcim_path = "/sdcard/DCIM/Camera"

        if not os.path.exists(dcim_path):
            page.snack_bar = ft.SnackBar(ft.Text("DCIM/Camera folder not found."))
            page.snack_bar.open = True
            page.update()
            return

        gallery_grid.controls.clear()
        valid_exts = (".jpg", ".jpeg", ".png", ".webp")

        for file in os.listdir(dcim_path):
            if file.lower().endswith(valid_exts):
                full_path = os.path.join(dcim_path, file)

                # Get small cached thumbnail for the grid tile
                thumb_path = get_or_create_thumbnail(full_path)

                gallery_grid.controls.append(
                    ft.Container(
                        content=ft.Image(
                            src=thumb_path, # Display low-res thumbnail in grid
                            fit=ft.ImageFit.COVER,
                            border_radius=ft.border_radius.all(6),
                        ),
                        # Pass full original path to preview dialog
                        on_click=lambda _, p=full_path: open_preview(p),
                    )
                )
        page.update()

    async def request_and_load(e):
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
        """Displays full-resolution photo on click."""
        def close_dlg(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            content=ft.Image(src=original_image_path, fit=ft.ImageFit.CONTAIN),
            actions=[ft.TextButton("Close", on_click=close_dlg)],
            content_padding=0,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    load_btn = ft.Button(
        content="Load Device Photos",
        icon=ft.Icons.PHOTO_LIBRARY,
        on_click=request_and_load,
    )

    page.add(
        ft.Row([load_btn], alignment=ft.MainAxisAlignment.CENTER),
        gallery_grid,
    )

if __name__ == "__main__":
    ft.run(main)