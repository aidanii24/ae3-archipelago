from textwrap import dedent
from typing import Any

from kivy.properties import ColorProperty, DictProperty, NumericProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list.list import MDGridLayout
from kivymd.uix.recycleview import MDRecycleView

from kvui import Builder

from .AE3_Interface import ConnectionStatus

BASE_WIDGETS: str = dedent(
    """\
    <StatusPanel@MDBoxLayout>:
        orientation: 'vertical'
        size_hint_x: 0.98
        size_hint_y: None
        height: dp(40)
        pos_hint: {'center_x': 0.5}
        padding: 20, 10
        md_bg_color: (*app.theme_cls.surfaceContainerHighColor[:3], 0.98)
    <StatusLabelComplete@StatusLabel>:
        label_text: ''
        value_text: ''
        status_text: ''
        value_color: app.theme_cls.onSurfaceColor
        orientation: 'horizontal'
        MDLabel:
            text: self.parent.label_text
            bold: True
            color: app.theme_cls.onSurfaceColor
            size_hint: 0.3, 1.0
        MDLabel:
            text: self.parent.value_text
            color: self.parent.value_color
            size_hint: 0.4, 1.0
            halign: 'center'
        MDLabel:
            text: self.parent.status_text
            color: app.theme_cls.onSurfaceColor
            size_hint: 0.3, 1.0
            halign: 'right'
    <PairedLabelComplete@PairedLabel>:
        label_text: ''
        value_text: ''
        value_color: app.theme_cls.onSurfaceColor
        size_hint_y: None
        height: 40
        orientation: 'horizontal'
        MDLabel:
            text: self.parent.label_text
            bold: True
            color: app.theme_cls.onSurfaceColor
        MDLabel:
            text: self.parent.value_text
            color: app.theme_cls.onSurfaceColor
            size_hint: 0.3, 1.0
            halign: 'center'
    <IndicatedStatusLabelComplete@IndicatedStatusLabel>
        label_text: ''
        value_text: ''
        status_text: ''
        value_color: app.theme_cls.onSurfaceColor
        indicator_value: 0
        indicator_color: app.theme_cls.primaryColor
        orientation: 'vertical'
        MDBoxLayout:
            padding: 20, 10, 20, 5
            orientation: 'horizontal'
            MDLabel:
                text: self.parent.parent.label_text
                color: app.theme_cls.onSurfaceColor
                bold: True
            MDLabel:
                text: self.parent.parent.value_text
                color: self.parent.parent.value_color
                halign: 'center'
            MDLabel:
                text: self.parent.parent.status_text
                color: app.theme_cls.onSurfaceColor
                halign: 'center'
        MDLinearProgressIndicator:
            indicator_color: self.parent.indicator_color
            size_hint_y: None
            height: 5
            value: self.parent.indicator_value
    <IndicatedPairedLabelComplete@IndicatedPairedLabel>
        label_text: ''
        value_text: ''
        value_color: app.theme_cls.onSurfaceColor
        indicator_value: 0
        indicator_color: app.theme_cls.primaryColor
        orientation: 'vertical'
        MDBoxLayout:
            padding: 20, 10, 20, 5
            orientation: 'horizontal'
            MDLabel:
                text: self.parent.parent.label_text
                color: app.theme_cls.onSurfaceColor
                bold: True
            MDLabel:
                text: self.parent.parent.value_text
                color: app.theme_cls.onSurfaceColor
                halign: 'center'
        MDLinearProgressIndicator:
            indicator_color: self.parent.indicator_color
            size_hint_y: None
            height: 5
            value: self.parent.indicator_value
    """
)

QUICK_STATUS_PANEL_KV: str = dedent(
    """\
    QuickStatusPanel:
        id: QuickStatusPanel
        size_hint_y: None
        height: self.minimum_height
        pos_hint: {'top': 1}
        spacing: 7
        orientation: 'vertical'
        StatusPanel:
            StatusLabelComplete:
                id: StatusDisplay
                label_text: 'Game Status'
                value_text: 'Waiting for PCSX2'
                status_text: 'Port: 28011'
                value_color: app.theme_cls.onSurfaceColor
        StatusPanel:
            padding: 0
            IndicatedStatusLabelComplete:
                id: GoalDisplay
                label_text: 'Goal Target'
                value_text: 'Goal Unknown'
                status_text: '0/0'
                value_color: app.theme_cls.onSurfaceColor
        StatusPanel:
            size_hint_y: None
            height: self.minimum_height
            padding: 20, 20, 20, 0
            spacing: 20
            MDLabel:
                text: "Post Game Conditions (Final Channel Set Unlock)"
                color: self.theme_cls.onSurfaceColor
                bold: True
            PGCView:
                id: PostGameConditionDisplay
                viewclass: 'IndicatedPairedLabelComplete'
                size_hint_y: None
                MDRecycleGridLayout:
                    cols: 3
                    spacing: 20
                    height: 20
                    default_size: None, dp(40)
                    default_size_hint: 1, None
    """
)


class QuickStatusPanel(MDBoxLayout):
    ids: DictProperty

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_game_port(self, port: int):
        if "StatusDisplay" not in self.ids:
            return

        status_display: StatusLabel = self.ids.get("StatusDisplay")

        status_display.set_status_text(f"Port: {port}")

    def update_game_status(self, status: ConnectionStatus):
        if "StatusDisplay" not in self.ids:
            return

        status_display: StatusLabel = self.ids.get("StatusDisplay")

        match status:
            case ConnectionStatus.DISCONNECTED:
                status_display.set_value_text("Emulator Disconnected", self.theme_cls.errorColor)
            case ConnectionStatus.WRONG_GAME:
                status_display.set_value_text("Wrong Game", self.theme_cls.tertiaryColor)
            case ConnectionStatus.CONNECTED:
                status_display.set_value_text("In Emulator Menu", self.theme_cls.secondaryColor)
            case _:
                status_display.set_value_text("In Game", self.theme_cls.primaryColor)

    def set_goal_target_status(self, goal_target: str, current_amount: int = 0, target_amount: int = 0):
        if "GoalDisplay" not in self.ids:
            return
        goal_display: StatusLabel = self.ids.get("GoalDisplay")

        goal_display.set_status_text(f"{current_amount}/{target_amount}")
        goal_display.set_value_text(goal_target)

    def update_goal_target_status(self, current_amount: int, target_amount: int):
        if "GoalDisplay" not in self.ids:
            return
        goal_display: StatusLabel = self.ids.get("GoalDisplay")

        goal_display.set_status_text(f"{current_amount}/{target_amount}")

    def update_pgc_status(self, data: list[dict]):
        if "PostGameConditionDisplay" not in self.ids:
            return
        goal_display: PGCView = self.ids.get("PostGameConditionDisplay")

        goal_display.set_data(data)


class PGCView(MDRecycleView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = [{"label_text": "Unknown PGC", "value_text": "0/0", "indicator_value": 0}]

    def set_data(self, data: list[dict[str, Any]]):
        self.data = data


class ChannelOverview(MDBoxLayout):
    pass


class ShoppingAreaOverview(MDGridLayout):
    pass


class PairedLabel(MDBoxLayout):
    label_text: str = StringProperty()
    value_text: str = StringProperty()

    value_color: str = ColorProperty()

    def set_label_text(self, text: str):
        self.label_text = text

    def set_value_text(self, text: str, color: str = ""):
        self.value_text = text

        if color:
            self.value_color = color


class StatusLabel(PairedLabel):
    status_text: str = StringProperty()

    def set_status_text(self, text: str):
        self.status_text = text


class IndicatedLabel(MDBoxLayout):
    indicator_value: float = NumericProperty(0.0)
    indicator_color: str = ColorProperty(0.0)

    def set_indicator_value(self, progress: float):
        self.indicator_progress = max(min(progress, 100.0), 0.0)

    def on_indicator_value(self, instance, value):
        if value < 20:
            self.indicator_color = self.theme_cls.errorColor
        elif value < 70:
            self.indicator_color = self.theme_cls.tertiaryColor
        elif value < 100:
            self.indicator_color = self.theme_cls.secondaryColor
        else:
            self.indicator_color = self.theme_cls.inversePrimaryColor


class IndicatedPairedLabel(PairedLabel, IndicatedLabel):
    pass


class IndicatedStatusLabel(StatusLabel, IndicatedLabel):
    pass


def create_quick_status_panel() -> QuickStatusPanel:
    kv_string: str = BASE_WIDGETS + "\n" + QUICK_STATUS_PANEL_KV
    return Builder.load_string(kv_string)
