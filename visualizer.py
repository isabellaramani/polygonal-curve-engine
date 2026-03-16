import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
from poligonali_stellate import Polygonal, Vertex


class PolygonalVisualizer:
    def __init__(self, history=None):
        """Inizializza l'interfaccia. Se history è None, parte in modalità editing."""
        self.history = history if history is not None else []
        self.current_step = 0
        self.input_vertices = []

        # Stato dell'interfaccia
        self.editing_mode = len(self.history) == 0

        # Creiamo la finestra facendo spazio a sinistra (left=0.3)
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(left=0.3, bottom=0.15, top=0.9)

        # Circonferenza unitaria di riferimento
        circle = plt.Circle(
            (0, 0), 1, color="gray", fill=False, linestyle="--", alpha=0.3
        )
        self.ax.add_patch(circle)

        (self.line,) = self.ax.plot([], [], "b-", linewidth=2)
        self.scatter = self.ax.scatter([], [], color="red", zorder=5)
        self.my_texts = []
        self.ax.set_aspect("equal")

        # Testo sopra la casella
        self.fig.text(0.05, 0.85, "Coordinate (x y):", fontsize=10, weight="bold")

        # Casella di testo
        axbox = plt.axes([0.05, 0.8, 0.2, 0.04])
        self.text_box = TextBox(axbox, "", initial="")
        self.text_box.on_submit(self.add_vertex)

        # Bottone Aggiungi
        axadd = plt.axes([0.05, 0.74, 0.2, 0.05])
        self.badd = Button(axadd, "Aggiungi")
        self.badd.on_clicked(lambda e: self.add_vertex(self.text_box.text))

        # Bottone Elimina Ultimo
        axdel = plt.axes([0.05, 0.68, 0.2, 0.05])
        self.bdel = Button(axdel, "Elimina Ultimo", color="mistyrose")
        self.bdel.on_clicked(self.delete_last)

        # Bottone Riduci (Lancia l'algoritmo)
        axrun = plt.axes([0.05, 0.15, 0.2, 0.06])
        self.brun = Button(axrun, "RIDUCI", color="lightgreen")
        self.brun.on_clicked(self.run_reduction)

        # Testo per la lista vertici
        self.list_text = self.fig.text(
            0.05,
            0.65,
            "Stai creando la seguente\npoligonale:",
            va="top",
            fontsize=10,
            weight="bold",
        )
        self.vertices_display = self.fig.text(0.05, 0.60, "", va="top", fontsize=9)

        # Bottoni navigazione
        self.axprev = plt.axes([0.4, 0.05, 0.15, 0.05])
        self.axnext = plt.axes([0.7, 0.05, 0.15, 0.05])
        self.bprev = Button(self.axprev, "Indietro")
        self.bnext = Button(self.axnext, "Avanti")
        self.bprev.on_clicked(self.prev_step)
        self.bnext.on_clicked(self.next_step)

        # Nascondi navigazione se siamo in editing
        self.axprev.set_visible(False)
        self.axnext.set_visible(False)
        # Inizializziamo il riferimento per il testo del Winding Number
        self.winding_text = None
        if not self.editing_mode:
            self.setup_reduction_view()

    def add_vertex(self, text):
        if not text.strip():
            return
        try:
            x, y = map(float, text.split())
            name = f"v{len(self.input_vertices) + 1}"
            self.input_vertices.append(Vertex(name, x, y))
            self.text_box.set_val("")  # Svuota box
            self.update_editor_plot()
        except ValueError:
            self.ax.set_title("Errore! Inserisci due numeri (es: 1.5 2)", color="red")

    def delete_last(self, event):
        if self.input_vertices:
            self.input_vertices.pop()
            self.update_editor_plot()

    def update_editor_plot(self):
        """Aggiorna il grafico mentre l'utente inserisce i punti."""
        if not self.input_vertices:
            self.line.set_data([], [])
            self.scatter.set_offsets([[0, 0]])  # placeholder
            self.vertices_display.set_text("")
            return

        x = [v.x for v in self.input_vertices]
        y = [v.y for v in self.input_vertices]

        # Mostra l'elenco testuale a sinistra
        v_list = "\n".join(
            [f"{v.name}: ({v.x}, {v.y})" for v in self.input_vertices[-10:]]
        )
        self.vertices_display.set_text(v_list)

        # Adatta la scala
        limit = max(max(abs(i) for i in x + y), 1.5) * 1.2
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)

        # Chiudi la poligonale graficamente
        self.line.set_data(x + [x[0]], y + [y[0]])
        self.scatter.set_offsets([[v.x, v.y] for v in self.input_vertices])
        plt.draw()

    def run_reduction(self, event):
        if len(self.input_vertices) < 3:
            self.ax.set_title("Servono almeno 3 vertici!", color="red")
            return

        # Esegui l'algoritmo
        P = Polygonal(self.input_vertices)

        P.reduce_polygonal()

        self.history = P.history
        self.current_step = 0  # Reset dell'indice al primo passo
        self.editing_mode = False

        # Puliamo i testi dell'editor prima di cambiare vista
        self.vertices_display.set_text("")

        self.setup_reduction_view()
        self.draw_step(0)  # Forza il disegno del primo fotogramma della storia

    def setup_reduction_view(self):
        """Prepara l'interfaccia per mostrare i passi della riduzione."""
        self.axprev.set_visible(True)
        self.axnext.set_visible(True)
        # Nascondi controlli editing
        self.text_box.ax.set_visible(False)
        self.badd.ax.set_visible(False)
        self.bdel.ax.set_visible(False)
        self.brun.ax.set_visible(False)
        self.list_text.set_visible(False)
        self.vertices_display.set_visible(False)

        self.ax.set_title("Riduzione completata. Naviga tra i passi.", color="green")
        plt.draw()

    def draw_step(self, idx):
        vertices = self.history[idx + 1]
        max_coord = max(
            max(abs(v.x) for v in vertices), max(abs(v.y) for v in vertices), 1.2
        )
        limit = max_coord * 1.3
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)

        x_coords = [v.x for v in vertices] + [vertices[0].x]
        y_coords = [v.y for v in vertices] + [vertices[0].y]
        self.line.set_data(x_coords, y_coords)
        self.scatter.set_offsets([[v.x, v.y] for v in vertices])

        # Pulizia testi dei vertici
        for txt in self.my_texts:
            txt.remove()
        self.my_texts = []
        for v in vertices:
            t = self.ax.text(
                v.x + (limit * 0.03), v.y + (limit * 0.03), v.name, fontsize=9
            )
            self.my_texts.append(t)

        if self.winding_text is not None:
            self.winding_text.remove()

        current_p = Polygonal(self.history[idx])
        wn = current_p.get_winding_number()

        # Creiamo il nuovo testo centrato sopra il grafico
        self.winding_text = self.fig.text(
            0.6,  # Centro visivo spostato a destra
            0.95,
            f"Il numero di avvolgimento è: {wn}",
            ha="center",
            va="center",
            fontsize=11,
            weight="bold",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
        )

        self.ax.set_title(f"Passo {idx + 1} di {len(self.history)-1}")
        plt.draw()

    def next_step(self, event):
        if self.current_step < len(self.history) - 1:
            self.current_step += 1
            self.draw_step(self.current_step)

    def prev_step(self, event):
        if self.current_step > 0:
            self.current_step -= 1
            self.draw_step(self.current_step)

    def show(self, interval=1000):
        plt.show()
