"""Petit organiseur de fichiers Windows, sans dépendance externe."""

from __future__ import annotations

import shutil
import tkinter as tk
from collections import Counter
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


CATEGORIES: dict[str, set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tif", ".tiff", ".heic", ".svg", ".ico"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".webm", ".m4v", ".mpeg", ".mpg", ".3gp"},
    "Musique": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma", ".opus", ".aiff"},
    "PDF": {".pdf"},
    "Documents": {".doc", ".docx", ".odt", ".rtf", ".txt", ".md", ".pages", ".epub"},
    "Tableurs": {".xls", ".xlsx", ".ods", ".csv", ".tsv"},
    "Presentations": {".ppt", ".pptx", ".odp", ".key"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".tgz"},
    "Programmes": {".exe", ".msi", ".msix", ".appx", ".deb", ".rpm", ".dmg", ".pkg"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".yml", ".yaml", ".java", ".c", ".cpp", ".h", ".cs", ".php", ".sh", ".sql"},
    "Autres": set(),
}

# Les navigateurs utilisent ces extensions pendant le téléchargement. On les ignore
# pour ne pas déplacer un fichier avant que son téléchargement soit terminé.
INCOMPLETE_SUFFIXES = {".crdownload", ".part", ".partial", ".download", ".tmp"}


def category_for(path: Path) -> str:
    suffix = path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Autres"


def non_overwriting_path(path: Path) -> Path:
    """Return an available name without replacing an existing file."""
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    index = 2
    while True:
        candidate = path.with_name(f"{stem} ({index}){suffix}")
        if not candidate.exists():
            return candidate
        index += 1


def organize(source: Path, destination: Path) -> tuple[Counter[str], list[str]]:
    """Move top-level files from source into categorized destination folders."""
    source = source.expanduser().resolve()
    destination = destination.expanduser().resolve()
    if not source.is_dir():
        raise ValueError("Le dossier source n’existe pas ou n’est pas accessible.")
    if source == destination or source in destination.parents:
        raise ValueError("Le dossier de destination ne peut pas être dans le dossier source.")

    moved: Counter[str] = Counter()
    errors: list[str] = []
    for item in source.iterdir():
        if not item.is_file() or item.suffix.lower() in INCOMPLETE_SUFFIXES:
            continue
        category = category_for(item)
        target_dir = destination / category
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            target = non_overwriting_path(target_dir / item.name)
            shutil.move(str(item), str(target))
            moved[category] += 1
        except OSError as error:
            errors.append(f"{item.name} : {error}")
    return moved, errors


class OrganizerApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Organiseur de fichiers")
        self.geometry("760x540")
        self.minsize(680, 500)
        self.configure(bg="#F2F6FA")
        icon_path = Path(__file__).with_name("organiseur_icone.ico")
        if icon_path.exists():
            self.iconbitmap(default=str(icon_path))

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#F2F6FA")
        style.configure("Card.TFrame", background="#FFFFFF")
        style.configure("TLabel", background="#F2F6FA", foreground="#25364A", font=("Segoe UI", 10))
        style.configure("Card.TLabel", background="#FFFFFF", foreground="#25364A", font=("Segoe UI", 10))
        style.configure("Section.TLabel", background="#FFFFFF", foreground="#17324D", font=("Segoe UI", 11, "bold"))
        style.configure("TEntry", padding=(9, 8), fieldbackground="#FFFFFF", foreground="#25364A")
        style.configure("Browse.TButton", padding=(12, 8), background="#E8F0F6", foreground="#17324D", font=("Segoe UI", 9, "bold"))
        style.map("Browse.TButton", background=[("active", "#D9E7F1")])
        style.configure("Accent.TButton", padding=(18, 11), background="#168C83", foreground="#FFFFFF", font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("Accent.TButton", background=[("active", "#11746C"), ("disabled", "#A9C5C0")])

        home = Path.home()
        self.source_var = tk.StringVar(value=str(home / "Downloads"))
        self.destination_var = tk.StringVar(value=str(home / "Fichiers organises"))
        self.status_var = tk.StringVar(value="Choisis les dossiers, puis lance le rangement.")
        self._build_ui()
        # Le premier tri se fait à l'ouverture, comme demandé. La fenêtre permet
        # ensuite de modifier les dossiers et de relancer le tri.
        self.after(400, self._run)

    def _build_ui(self) -> None:
        page = ttk.Frame(self, padding=22)
        page.pack(fill="both", expand=True)

        header = tk.Frame(page, bg="#17324D", padx=22, pady=18)
        header.pack(fill="x", pady=(0, 18))
        tk.Label(header, text="✦  TON ESPACE, BIEN RANGÉ", bg="#17324D", fg="#83D6C7", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(header, text="Organiseur de fichiers", bg="#17324D", fg="#FFFFFF", font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(5, 2))
        tk.Label(header, text="Un peu d’ordre dans tes téléchargements, en un clic.", bg="#17324D", fg="#D5E2EC", font=("Segoe UI", 10)).pack(anchor="w")

        card = ttk.Frame(page, style="Card.TFrame", padding=(20, 18))
        card.pack(fill="both", expand=True)
        ttk.Label(card, text="Où ranger tes fichiers ?", style="Section.TLabel").pack(anchor="w", pady=(0, 12))
        self._folder_row(card, "Dossier à trier", self.source_var, self._choose_source)
        self._folder_row(card, "Dossier principal", self.destination_var, self._choose_destination)

        ttk.Label(card, text="Le rangement se fera par catégorie", style="Section.TLabel").pack(anchor="w", pady=(18, 9))
        chip_row = tk.Frame(card, bg="#FFFFFF")
        chip_row.pack(fill="x", anchor="w")
        chips = [
            ("Images", "#EAF2FF", "#315E9E"), ("Vidéos", "#F0EAFE", "#6E4FA1"),
            ("Musique", "#FCEAF0", "#A34D69"), ("PDF & documents", "#FFF1DF", "#96612B"),
            ("Archives", "#E8F5EF", "#347553"), ("Code & autres", "#EAF0F3", "#4B6474"),
        ]
        for name, background, foreground in chips:
            tk.Label(chip_row, text=name, bg=background, fg=foreground, font=("Segoe UI", 9, "bold"), padx=10, pady=6).pack(side="left", padx=(0, 7), pady=(0, 7))

        tk.Label(
            card,
            text="Les dossiers et les téléchargements en cours sont ignorés. Les fichiers existants ne sont jamais remplacés.",
            bg="#FFFFFF", fg="#6A7B8A", font=("Segoe UI", 9), wraplength=650, justify="left",
        ).pack(anchor="w", pady=(8, 0))

        footer = ttk.Frame(page)
        footer.pack(fill="x", pady=(14, 0))
        ttk.Button(footer, text="Lancer le rangement", command=self._run, style="Accent.TButton").pack(side="left")
        ttk.Label(footer, textvariable=self.status_var, wraplength=400, foreground="#347553").pack(side="left", padx=(14, 0))

    def _folder_row(self, parent: ttk.Frame, label: str, variable: tk.StringVar, callback: object) -> None:
        row = ttk.Frame(parent, style="Card.TFrame")
        row.pack(fill="x", pady=5)
        ttk.Label(row, text=label, width=19, style="Card.TLabel").pack(side="left")
        ttk.Entry(row, textvariable=variable).pack(side="left", fill="x", expand=True, padx=(0, 8))
        ttk.Button(row, text="Parcourir…", command=callback, style="Browse.TButton").pack(side="left")

    def _choose_source(self) -> None:
        selected = filedialog.askdirectory(title="Choisir le dossier à trier", initialdir=self.source_var.get())
        if selected:
            self.source_var.set(selected)

    def _choose_destination(self) -> None:
        selected = filedialog.askdirectory(title="Choisir le dossier principal", initialdir=self.destination_var.get())
        if selected:
            self.destination_var.set(selected)

    def _run(self) -> None:
        source, destination = Path(self.source_var.get()), Path(self.destination_var.get())
        try:
            moved, errors = organize(source, destination)
        except (OSError, ValueError) as error:
            messagebox.showerror("Impossible de ranger les fichiers", str(error), parent=self)
            return

        count = sum(moved.values())
        if count == 0 and not errors:
            summary = "Aucun fichier à ranger."
        else:
            summary = f"{count} fichier(s) rangé(s).\n" + "\n".join(
                f"• {category} : {number}" for category, number in sorted(moved.items())
            )
            if errors:
                summary += f"\n\n{len(errors)} fichier(s) n’ont pas pu être déplacés :\n" + "\n".join(errors[:8])
                if len(errors) > 8:
                    summary += f"\n… et {len(errors) - 8} autre(s)."
        self.status_var.set(f"✓ {count} fichier(s) rangé(s) • {len(errors)} erreur(s)")
        messagebox.showinfo("Rangement terminé", summary, parent=self)


if __name__ == "__main__":
    OrganizerApp().mainloop()
