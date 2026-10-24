from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QComboBox,
    QCompleter,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import draft_advisor


class BackgroundWorker(QThread):
    result_ready = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, operation):
        super().__init__()
        self.operation = operation

    def run(self):
        try:
            self.result_ready.emit(self.operation())
        except Exception as exc:
            self.error.emit(str(exc))


class DraftWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dota Coach — Помощник драфта")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
        self.resize(940, 680)
        self.setStyleSheet("""
            QWidget {
                background: #181818;
                color: #EEEEEE;
                font-family: Consolas;
                font-size: 11px;
            }
            QGroupBox {
                border: 1px solid #444;
                border-radius: 6px;
                margin-top: 12px;
                padding: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #FFD700;
                left: 10px;
                padding: 0 4px;
            }
            QPushButton, QComboBox {
                background: #303030;
                color: #EEEEEE;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover { background: #454545; }
            QListWidget {
                background: #202020;
                border: 1px solid #444;
                border-radius: 4px;
            }
        """)

        self.heroes = []
        self.hero_by_name = {}
        self.catalog_info = ""
        self.catalog_requested = False
        self.workers = []
        self.recommendation_generation = 0

        root = QVBoxLayout(self)
        title = QLabel("Помощник драфта")
        title.setStyleSheet("color: #FFD700; font-size: 17px; font-weight: bold;")
        root.addWidget(title)
        root.addWidget(QLabel(
            "Добавьте выбранных героев обеих команд — подбор учитывает "
            "матчапы OpenDota и встроенные контрпики."
        ))

        picks_row = QHBoxLayout()
        self.ally_list = self._make_pick_group("Союзники", "allies", picks_row)
        self.enemy_list = self._make_pick_group("Соперники", "enemies", picks_row)
        root.addLayout(picks_row, 2)

        recommendations_group = QGroupBox("Кого выбрать дальше")
        recommendations_layout = QVBoxLayout(recommendations_group)
        self.recommendations = QListWidget()
        recommendations_layout.addWidget(self.recommendations)
        root.addWidget(recommendations_group, 3)

        self.status = QLabel("Загружаю список героев OpenDota...")
        self.status.setWordWrap(True)
        self.status.setStyleSheet("color: #BBBBBB;")
        root.addWidget(self.status)

    def showEvent(self, event):
        super().showEvent(event)
        if not self.catalog_requested:
            self.catalog_requested = True
            self._load_catalog()

    def _make_pick_group(self, title, team, parent_layout):
        group = QGroupBox(title)
        layout = QVBoxLayout(group)
        selector = QComboBox()
        selector.setEditable(True)
        selector.setInsertPolicy(QComboBox.NoInsert)
        selector.lineEdit().setPlaceholderText("Поиск героя...")
        selector.completer().setCompletionMode(QCompleter.PopupCompletion)
        selector.completer().setFilterMode(Qt.MatchContains)
        layout.addWidget(selector)

        buttons = QHBoxLayout()
        add_button = QPushButton("Добавить")
        add_button.clicked.connect(lambda: self._add_pick(team))
        buttons.addWidget(add_button)
        remove_button = QPushButton("Убрать выбранного")
        remove_button.clicked.connect(lambda: self._remove_pick(team))
        buttons.addWidget(remove_button)
        layout.addLayout(buttons)

        pick_list = QListWidget()
        layout.addWidget(pick_list)
        parent_layout.addWidget(group)

        if team == "allies":
            self.ally_selector = selector
        else:
            self.enemy_selector = selector
        return pick_list

    def _load_catalog(self):
        worker = BackgroundWorker(draft_advisor.load_hero_catalog)
        worker.result_ready.connect(
            lambda result, active_worker=worker: self._catalog_loaded(result)
        )
        worker.error.connect(self._catalog_failed)
        self._start_worker(worker)

    def _start_worker(self, worker):
        self.workers.append(worker)
        worker.finished.connect(lambda active=worker: self._worker_finished(active))
        worker.start()

    def _worker_finished(self, worker):
        if worker in self.workers:
            self.workers.remove(worker)
        worker.deleteLater()

    def _catalog_loaded(self, result):
        self.heroes, source = result
        self.catalog_info = source
        self.hero_by_name = {hero["name"]: hero for hero in self.heroes}
        for selector in (self.ally_selector, self.enemy_selector):
            selector.clear()
            for hero in self.heroes:
                label = hero["localized_name"]
                selector.addItem(label, hero["name"])
            selector.setCurrentIndex(-1)
            selector.lineEdit().clear()

        self.status.setText(
            f"Герои: {len(self.heroes)} · Источник: {self.catalog_info}. "
            "Оценки матчапов — статистика, а не гарантия победы."
        )
        self._refresh_recommendations()

    def _catalog_failed(self, error):
        self.status.setText(f"Не удалось загрузить список героев: {error}")

    def _add_pick(self, team):
        selector = self.ally_selector if team == "allies" else self.enemy_selector
        hero_id = selector.currentData()
        if not hero_id or selector.currentText() != selector.itemText(
            selector.currentIndex()
        ):
            self.status.setText("Выберите героя из списка, а не только введите его имя.")
            return

        if self._find_pick(hero_id):
            self.status.setText("Этот герой уже добавлен в драфт.")
            return

        hero = self.hero_by_name[hero_id]
        label = hero["localized_name"]
        roles = hero.get("roles", [])
        if roles:
            label += " — " + ", ".join(roles)
        item = QListWidgetItem(label)
        item.setData(Qt.UserRole, hero_id)
        target_list = self.ally_list if team == "allies" else self.enemy_list
        target_list.addItem(item)
        selector.setCurrentIndex(-1)
        selector.lineEdit().clear()
        self._refresh_recommendations()

    def _find_pick(self, hero_id):
        for pick_list in (self.ally_list, self.enemy_list):
            for index in range(pick_list.count()):
                if pick_list.item(index).data(Qt.UserRole) == hero_id:
                    return True
        return False

    def _remove_pick(self, team):
        pick_list = self.ally_list if team == "allies" else self.enemy_list
        row = pick_list.currentRow()
        if row >= 0:
            pick_list.takeItem(row)
            self._refresh_recommendations()

    def _selected_ids(self, pick_list):
        return [
            pick_list.item(index).data(Qt.UserRole)
            for index in range(pick_list.count())
        ]

    def _refresh_recommendations(self, *_):
        if not self.heroes:
            return

        allies = self._selected_ids(self.ally_list)
        enemies = self._selected_ids(self.enemy_list)
        ally_ids, enemy_ids = allies, enemies

        self.recommendation_generation += 1
        generation = self.recommendation_generation
        self.recommendations.clear()
        if not enemy_ids:
            self.status.setText(
                "Добавьте хотя бы одного героя соперника, чтобы получить "
                f"контрпики. Источник списка: {self.catalog_info}."
            )
            return

        local = draft_advisor.recommend_picks(
            self.heroes, ally_ids, enemy_ids, {}
        )
        self._render_recommendations(local)
        self.status.setText("Загружаю статистику матчапов OpenDota...")

        def fetch_recommendations():
            matchups, warnings = draft_advisor.load_matchups(enemy_ids)
            recommendations = draft_advisor.recommend_picks(
                self.heroes, ally_ids, enemy_ids, matchups
            )
            return recommendations, warnings

        worker = BackgroundWorker(fetch_recommendations)
        worker.result_ready.connect(
            lambda result, token=generation: self._matchups_loaded(token, result)
        )
        worker.error.connect(
            lambda error, token=generation: self._matchups_failed(token, error)
        )
        self._start_worker(worker)

    def _matchups_loaded(self, generation, result):
        if generation != self.recommendation_generation:
            return
        recommendations, warnings = result
        self._render_recommendations(recommendations)
        if warnings:
            self.status.setText(
                "Часть статистики недоступна; показаны доступные матчапы "
                "и встроенные контрпики. " + " ".join(warnings)
            )
        else:
            self.status.setText(
                "Рейтинг — ориентир по матчапам и контрпикам, не вероятность "
                f"победы. Герои: {self.catalog_info}."
            )

    def _matchups_failed(self, generation, error):
        if generation == self.recommendation_generation:
            self.status.setText(
                "Не удалось загрузить матчапы; показаны встроенные контрпики. "
                + error
            )

    def _render_recommendations(self, recommendations):
        self.recommendations.clear()
        if not recommendations:
            self.recommendations.addItem(
                "Пока нет рекомендаций — добавьте соперника из базы OpenDota."
            )
            return

        for recommendation in recommendations:
            hero = recommendation["hero"]
            roles = ", ".join(hero.get("roles", []))
            line = (
                f"{hero['localized_name']} · оценка пика "
                f"{recommendation['score']:.1f}"
            )
            if roles:
                line += f" · {roles}"
            item = QListWidgetItem(line)
            details = recommendation["reasons"] or [
                "Есть статистика матчапа против выбранного состава."
            ]
            item.setToolTip("\n".join(details))
            self.recommendations.addItem(item)
