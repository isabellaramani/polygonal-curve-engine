import matplotlib.pyplot as plt
from matplotlib.widgets import Button


class PolygonVisualizer:
    def __init__(self, history):
        """Inizializza il motore grafico interattivvo."""
        self.history = history
        # Fotogramma iniziale
        self.current_step = 0

        # Creiamo la finestra
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        plt.subplots_adjust(bottom=0.2)

        # Disegniamo la circonferenza unitaria
        circle = plt.Circle(
            (0, 0), 1, color="gray", fill=False, linestyle="--", alpha=0.5
        )
        self.ax.add_patch(circle)

        (self.line,) = self.ax.plot([], [], "b-", linewidth=2)
        self.scatter = self.ax.scatter([], [], color="red", zorder=5)
        self.my_texts = []

        self.ax.set_xlim(-1.5, 1.5)
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.set_aspect("equal")

        # Botton indietro e avanti
        axprev = plt.axes([0.2, 0.05, 0.2, 0.075])
        axnext = plt.axes([0.6, 0.05, 0.2, 0.075])

        # Creiamo il bottone Indietro
        self.bprev = Button(axprev, "<- Indietro")
        self.bprev.on_clicked(self.prev_step)  # Cosa fa quando clicchi

        # Creiamo il bottone Avanti
        self.bnext = Button(axnext, "Avanti ->")
        self.bnext.on_clicked(self.next_step)  # Cosa fa quando clicchi

    def draw_step(self, idx):
        """Disegna il fotogramma i-esimo e si ferma."""
        vertices = self.history[idx]
        if not vertices:
            return

        # Aggiorniamo la linea e i punti
        x_coords = [v.x for v in vertices]
        y_coords = [v.y for v in vertices]
        x_coords.append(vertices[0].x)
        y_coords.append(vertices[0].y)
        self.line.set_data(x_coords, y_coords)

        # Aggiorniamo i punti
        points = [[v.x, v.y] for v in vertices]
        self.scatter.set_offsets(points)

        # Agggiorniamo i nomi dei vertici
        for txt in self.my_texts:
            txt.remove()
        self.my_texts = []

        # Aggiungiamo i nomi dei vertici vicino ai punti
        for v in vertices:
            t = self.ax.text(v.x * 1.1, v.y * 1.1, v.name, fontsize=10, ha="center")
            self.my_texts.append(t)

        # Aggiorniamo il titolo con il numero del passo
        self.ax.set_title(f"Passo {idx + 1} di {len(self.history)}")

        # Aggiorna lo schermo
        plt.draw()

    def next_step(self, event):
        """Fotogramma successivo."""
        if self.current_step < len(self.history) - 1:
            self.current_step += 1
            self.draw_step(self.current_step)

    def prev_step(self, event):
        """Fotogramma precedente."""
        if self.current_step > 0:
            self.current_step -= 1
            self.draw_step(self.current_step)

    def show(self, interval=None):
        """Avvia l'interfaccia."""
        if not self.history:
            print("Niente da mostrare.")
            return

        # Disegniamo il fotogramma iniziale
        self.draw_step(0)

        # Apre la finestra
        plt.show(block=True)
