import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDDYear(self):
        for y in self._model.getStagione():
            self._view._ddAnno.options.append(ft.dropdown.Option(y))
        self._view.update_page()

    def handleCreaGrafo(self,e):
        pilota,score = self._model.buildGraph(self._view._ddAnno.value)
        nodi, archi = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente:\nI nodi sono {nodi}\nGli archi sono {archi}"))
        self._view.txt_result.controls.append(ft.Text(f"Miglior pilota: {pilota.surname} con score {score}"))

        self._view.update_page()

    def handleCerca(self, e):
        self._view.txt_result.controls.clear()
        try:
            k = int(self._view._txtIntK.value)
        except ValueError:
            return self._view.create_alert("numero non valido")
        team , score = self._model.getDreamTeam(k)
        self._view.txt_result.controls.append(ft.Text(f"Il miglior team ha ottenuto uno score di: {score}\nIl team e formato da:"))
        for t in team:
            self._view.txt_result.controls.append(ft.Text(f"{t.surname}"))
        self._view.update_page()