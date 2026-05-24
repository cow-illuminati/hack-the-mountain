
import cli as cli
import os
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageOps

BG = "#080808"
PANEL = "#111111"
PANEL_SOFT = "#151515"
YELLOW = "#ffcc1a"
YELLOW_SOFT = "#ffd84d"
TEXT = "#f4d35e"
MUTED = "#b89b2d"
TRACK = "#2a2a2a"


class AutoCatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoCat")
        self.geometry("980x760")
        self.minsize(900, 680)
        self.configure(bg=BG)

        self.input_path = tk.StringVar(value="/home")
        self.output_path = tk.StringVar(value="")
        self.status_text = tk.StringVar(value="Ready.")
        self.progress_value = tk.DoubleVar(value=0)
        self.logo_photo = None

        self.scene_items = {
            "Scene_001": ["clip_0001.mp4", "clip_0002.mp4", "clip_0003.mov"],
            "Scene_002": ["clip_0004.mp4", "clip_0005.mov"],
            "Scene_003": ["clip_0006.mp4"],
        }

        self._build_style()
        self._build_ui()
        self._populate_demo_tree()

    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Root.TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("SoftPanel.TFrame", background=PANEL_SOFT)

        style.configure(
            "Section.TLabel",
            background=PANEL,
            foreground=YELLOW,
            font=("Helvetica", 12, "bold"),
        )
        style.configure(
            "SoftSection.TLabel",
            background=PANEL_SOFT,
            foreground=YELLOW,
            font=("Helvetica", 12, "bold"),
        )
        style.configure(
            "Body.TLabel",
            background=PANEL,
            foreground=TEXT,
            font=("Helvetica", 10),
        )
        style.configure(
            "SoftBody.TLabel",
            background=PANEL_SOFT,
            foreground=TEXT,
            font=("Helvetica", 10),
        )
        style.configure(
            "Status.TLabel",
            background=PANEL_SOFT,
            foreground=MUTED,
            font=("Helvetica", 10),
        )

        style.configure(
            "AutoCat.TButton",
            background=YELLOW,
            foreground=BG,
            padding=(12, 8),
            borderwidth=0,
            font=("Helvetica", 10, "bold"),
        )
        style.map(
            "AutoCat.TButton",
            background=[("active", YELLOW_SOFT), ("pressed", "#e7b800")],
        )

        style.configure(
            "Ghost.TButton",
            background=PANEL,
            foreground=YELLOW,
            padding=(10, 8),
            borderwidth=1,
            relief="solid",
            font=("Helvetica", 10, "bold"),
        )
        style.map(
            "Ghost.TButton",
            background=[("active", "#1a1a1a"), ("pressed", TRACK)],
            foreground=[("active", YELLOW_SOFT)],
        )

        style.configure(
            "AutoCat.Horizontal.TProgressbar",
            troughcolor=TRACK,
            bordercolor=TRACK,
            background=YELLOW,
            lightcolor=YELLOW,
            darkcolor=YELLOW,
            thickness=14,
        )

        style.configure(
            "Treeview",
            background=PANEL,
            fieldbackground=PANEL,
            foreground=TEXT,
            rowheight=28,
            borderwidth=0,
            font=("Helvetica", 10),
        )
        style.map(
            "Treeview",
            background=[("selected", YELLOW)],
            foreground=[("selected", BG)],
        )
        style.configure(
            "Treeview.Heading",
            background=BG,
            foreground=YELLOW,
            borderwidth=0,
            font=("Helvetica", 10, "bold"),
            relief="flat",
        )

    def _build_ui(self):
        root = ttk.Frame(self, style="Root.TFrame", padding=24)
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(2, weight=1)

        self._build_header(root)
        self._build_controls(root)
        self._build_scene_panel(root)

    def _build_header(self, parent):
        header = ttk.Frame(parent, style="Root.TFrame")
        header.grid(row=0, column=0, sticky="w", pady=(0, 18))

        logo_path = os.path.join(os.path.dirname(__file__), "logo.jpeg")
        if os.path.exists(logo_path):
            image = Image.open(logo_path)
            image = ImageOps.exif_transpose(image)
            image.thumbnail((320, 90), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(image)

            logo_label = tk.Label(
                header,
                image=self.logo_photo,
                bg=BG,
                bd=0,
                highlightthickness=0,
            )
            logo_label.grid(row=0, column=0, sticky="w")
        else:
            fallback = tk.Canvas(header, width=220, height=70, bg=BG, highlightthickness=0)
            fallback.grid(row=0, column=0, sticky="w")
            self._draw_logo(fallback)

    def _draw_logo(self, canvas):
        lw = 4
        canvas.create_rectangle(20, 8, 44, 32, outline=YELLOW, width=lw)
        canvas.create_rectangle(8, 20, 32, 44, outline=YELLOW, width=lw)

    def _build_controls(self, parent):
        panel = ttk.Frame(parent, style="Panel.TFrame", padding=20)
        panel.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        panel.columnconfigure(0, weight=1)
        panel.columnconfigure(1, weight=1)

        ttk.Label(panel, text="Import", style="Section.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 14)
        )

        input_card = ttk.Frame(panel, style="SoftPanel.TFrame", padding=18)
        input_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        input_card.columnconfigure(0, weight=1)

        ttk.Label(input_card, text="Input folder", style="SoftSection.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )

        ttk.Label(
            input_card,
            textvariable=self.input_path,
            style="SoftBody.TLabel",
            wraplength=360
        ).grid(row=1, column=0, sticky="ew", pady=(0, 12))

        arrow_wrap = tk.Frame(input_card, bg=PANEL_SOFT, height=150)
        arrow_wrap.grid(row=2, column=0, sticky="ew", pady=(4, 12))
        arrow_wrap.grid_propagate(False)
        arrow_wrap.columnconfigure(0, weight=1)
        arrow_wrap.rowconfigure(0, weight=1)

        arrow_button = tk.Button(
            arrow_wrap,
            text="↓",
            command=self.pick_input_folder,
            bg=BG,
            fg=YELLOW,
            activebackground="#101010",
            activeforeground=YELLOW_SOFT,
            relief="flat",
            bd=0,
            font=("Helvetica", 42, "bold"),
            cursor="hand2",
            width=3,
            height=1,
        )
        arrow_button.grid(row=0, column=0)

        ttk.Button(
            input_card,
            text="Browse input",
            style="AutoCat.TButton",
            command=self.pick_input_folder
        ).grid(row=3, column=0, pady=(0, 4))

        output_card = ttk.Frame(panel, style="SoftPanel.TFrame", padding=18)
        output_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        output_card.columnconfigure(0, weight=1)

        ttk.Label(output_card, text="Output folder", style="SoftSection.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )

        output_entry = tk.Entry(
            output_card,
            textvariable=self.output_path,
            bg=BG,
            fg=TEXT,
            insertbackground=YELLOW,
            relief="flat",
            font=("Helvetica", 10),
        )
        output_entry.grid(row=1, column=0, sticky="ew", ipady=8, pady=(0, 12))

        ttk.Button(
            output_card,
            text="Browse output",
            style="Ghost.TButton",
            command=self.pick_output_folder
        ).grid(row=2, column=0, sticky="w", pady=(0, 18))

        ttk.Button(
            output_card,
            text="Organize",
            style="AutoCat.TButton",
            command=self.run_mock_job
        ).grid(row=3, column=0, sticky="w", pady=(0, 14))

        self.progress = ttk.Progressbar(
            output_card,
            style="AutoCat.Horizontal.TProgressbar",
            maximum=100,
            variable=self.progress_value,
            mode="determinate",
        )
        self.progress.grid(row=4, column=0, sticky="ew", pady=(0, 8))

        self.percent_label = ttk.Label(output_card, text="0%", style="SoftSection.TLabel")
        self.percent_label.grid(row=5, column=0, sticky="w")

        ttk.Label(
            output_card,
            textvariable=self.status_text,
            style="Status.TLabel"
        ).grid(row=6, column=0, sticky="w", pady=(4, 0))

    def _build_scene_panel(self, parent):
        panel = ttk.Frame(parent, style="Panel.TFrame", padding=20)
        panel.grid(row=2, column=0, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)

        ttk.Label(panel, text="Scenes", style="Section.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        tree_wrap = ttk.Frame(panel, style="Panel.TFrame")
        tree_wrap.grid(row=1, column=0, sticky="nsew")
        tree_wrap.columnconfigure(0, weight=1)
        tree_wrap.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_wrap, columns=("type", "count"), show="tree headings")
        self.tree.heading("#0", text="Name")
        self.tree.heading("type", text="Type")
        self.tree.heading("count", text="Count")
        self.tree.column("#0", width=420)
        self.tree.column("type", width=140, anchor="center")
        self.tree.column("count", width=120, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<Double-1>", self.on_tree_double_click)

        scroll = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.grid(row=0, column=1, sticky="ns")

    def pick_input_folder(self):
        folder = filedialog.askdirectory(title="Select input folder")
        if folder:
            self.input_path.set(folder)
            self.status_text.set("Input folder selected.")

    def pick_output_folder(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_path.set(folder)
            self.status_text.set("Output folder selected.")

    def run_mock_job(self):
        self.progress_value.set(0)
        self.percent_label.config(text="0%")
        self.status_text.set("Organize job running...")
        self._animate_progress(0)

    def _animate_progress(self, value):
        if value > 100:
            self.status_text.set("Check logs for status...")
            print ("working")
            cli.aucat(self.input_path.get())
            # HERE ?? ^
            return

        self.progress_value.set(value)
        self.percent_label.config(text=f"{int(value)}%")

        if value < 35:
            self.status_text.set("Scanning files...")
        elif value < 70:
            self.status_text.set("Classifying scenes...")
        else:
            self.status_text.set("Writing folders...")

        self.after(30, lambda: self._animate_progress(value + 1))

    def _populate_demo_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        root_id = self.tree.insert(
            "", "end", text="Organized Output",
            values=("folder", len(self.scene_items)), open=True
        )

        for scene, files in self.scene_items.items():
            scene_id = self.tree.insert(
                root_id, "end", text=scene, values=("scene", len(files)), open=False
            )
            for clip in files:
                self.tree.insert(scene_id, "end", text=clip, values=("video", 1))

    def on_tree_double_click(self, event=None):
        item = self.tree.selection()
        if not item:
            return
        name = self.tree.item(item[0], "text")
        self.status_text.set(f"Selected: {name}")


if __name__ == "__main__":
    app = AutoCatApp()
    app.mainloop()

