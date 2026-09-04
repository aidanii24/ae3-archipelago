import typing
from textwrap import dedent
from typing import Any

from kivy.properties import (
    ColorProperty,
    DictProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.carousel import Carousel
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.tooltip.tooltip import MDLabel

from kvui import Builder

from .game_interface import ConnectionStatus
from .state import QSPDisplayMode

BASE_WIDGETS: str = dedent(
    """\
    <StatusPanel@StatusPanelBase>:
        qsp_index_hint: 0
        qsp_modes: []
        orientation: 'vertical'
        adaptive_height: True
        pos_hint: {'center_x': 0.5}
        padding: 20, 10
        md_bg_color: (*app.theme_cls.surfaceContainerHighColor[:3], 0.98)
    <StatusLabelComplete@StatusLabel>:
        label_text: ''
        value_text: ''
        status_text: ''
        value_color: app.theme_cls.onSurfaceColor
        orientation: 'horizontal'
        adaptive_height:True
        MDLabel:
            text: self.parent.label_text
            bold: True
            color: app.theme_cls.onSurfaceColor
            size_hint: 0.3, None
            adaptive_height: True
        MDLabel:
            text: self.parent.value_text
            color: self.parent.value_color
            size_hint: 0.4, None
            adaptive_height: True
            halign: 'center'
        MDLabel:
            text: self.parent.status_text
            color: app.theme_cls.onSurfaceColor
            size_hint: 0.3, None
            adaptive_height: True
            halign: 'right'
    <PairedLabelComplete@PairedLabel>:
        label_text: ''
        value_text: ''
        value_color: app.theme_cls.onSurfaceColor
        size_hint_y: None
        adaptive_height:True
        orientation: 'horizontal'
        MDLabel:
            text: self.parent.label_text
            bold: True
            color: app.theme_cls.onSurfaceColor
            adaptive_height: True
        MDLabel:
            text: self.parent.value_text
            color: app.theme_cls.onSurfaceColor
            size_hint: 0.3, 1.0
            halign: 'center'
            adaptive_height: True
    <IndicatedStatusLabelComplete@IndicatedStatusLabel>
        label_text: ''
        value_text: ''
        status_text: ''
        value_color: app.theme_cls.onSurfaceColor
        indicator_value: 0
        indicator_color: app.theme_cls.primaryColor
        orientation: 'vertical'
        adaptive_height: True
        MDBoxLayout:
            orientation: 'horizontal'
            adaptive_height: True
            MDLabel:
                text: self.parent.parent.label_text
                color: app.theme_cls.onSurfaceColor
                bold: True
                adaptive_height: True
            MDLabel:
                text: self.parent.parent.value_text
                color: self.parent.parent.value_color
                adaptive_height: True
                halign: 'center'
            MDLabel:
                text: self.parent.parent.status_text
                color: app.theme_cls.onSurfaceColor
                adaptive_height: True
                halign: 'right'
        MDLinearProgressIndicator:
            indicator_color: self.parent.indicator_color
            track_color: (*app.theme_cls.primaryContainerColor[:3], 0.50)
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
        padding: 10, 10, 10, 5
        spacing: 10
        adaptive_height: True
        MDBoxLayout:
            orientation: 'horizontal'
            MDLabel:
                text: self.parent.parent.label_text
                color: app.theme_cls.onSurfaceColor
                bold: True
                shorten: True
                shorten_from: 'right'
            MDLabel:
                adaptive_width: True
                text: self.parent.parent.value_text
                color: app.theme_cls.onSurfaceColor
                halign: 'right'
        MDLinearProgressIndicator:
            indicator_color: self.parent.indicator_color
            track_color: (*app.theme_cls.primaryContainerColor[:3], 0.50)
            size_hint_y: None
            height: 5
            value: self.parent.indicator_value
    """
)

QUICK_STATUS_PANEL_KV: str = dedent(
    """\
    #:import math math
    QuickStatusPanel:
        id: QuickStatusPanel
        size_hint_y: None
        height: self.minimum_height
        pos_hint: {'top': 1}
        spacing: dp(5)
        padding: dp(12), dp(5)
        orientation: 'vertical'
        md_bg_color: (*self.theme_cls.surfaceContainerLowColor[:3], 0.9)
        StatusPanel:
            id: StatusPanel
            style: "elevated"
            MDBoxLayout:
                adaptive_height: True
                StatusLabelComplete:
                    id: StatusLabel
                    label_text: 'Game Status'
                    value_text: 'Waiting for PCSX2'
                    status_text: 'Port: 28011'
                    value_color: app.theme_cls.onSurfaceColor
        StatusPanel:
            qsp_modes: [10]
            style: "elevated"
            MDBoxLayout:
                id: GoalPanel
                adaptive_height: True
                IndicatedStatusLabelComplete:
                    id: GoalLabel
                    label_text: 'Goal Target'
                    value_text: 'Goal Unknown'
                    status_text: '0/0'
                    value_color: app.theme_cls.onSurfaceColor
        StatusPanel:
            qsp_modes: [10]
            style: "elevated"
            padding: dp(20), dp(20), dp(20), 0
            MDBoxLayout:
                orientation: "vertical"
                id: PostGameConditionPanel
                adaptive_height: True
                spacing: dp(20)
                MDLabel:
                    text: "Post Game Conditions (Final Channel Set Unlock)"
                    color: self.theme_cls.onSurfaceColor
                    bold: True
                AE3RecycleView:
                    id: PostGameConditionView
                    viewclass: 'IndicatedPairedLabelComplete'
                    size_hint_y: None
                    height: math.ceil(len(self.data) / 3) * dp(60)
                    MDRecycleGridLayout:
                        cols: min(len(self.parent.data), 3)
                        spacing: 20
                        default_size: None, dp(40)
                        default_size_hint: 1, None
        StatusPanel:
            qsp_modes: [20, 30]
            style: "elevated"
            padding: dp(20), dp(10), dp(20), 0
            MDBoxLayout:
                id: ChannelSelectPreviewPanel
                orientation: "vertical"
                adaptive_height: True
                spacing: dp(10)
                ChannelSelectPreviewCarousel:
                    id: ChannelSelectPreviewCarousel
                    anim_move_duration: 0.15
                    pos_hint: {'x': 0.0}
                    size_hint_y: None
                    height: dp(30)
                    do_scroll_x: True
                    do_scroll_y: False
                MDBoxLayout:
                    adaptive_height: True
                    IndicatedPairedLabelComplete:
                        id: ChannelSelectPreviewProgress
                        label_text: 'Total'
                        value_text: ''
                        indicator_value: 0
                AE3RecycleView:
                    id: OverviewView
                    viewclass: 'IndicatedPairedLabelComplete'
                    size_hint_y: None
                    height: math.ceil(len(self.data) / 3) * dp(50)
                    do_scroll_y: False
                    MDRecycleGridLayout:
                        cols: min(len(self.parent.data), 3)
                        spacing: dp(10)
                        adaptive_height: True
                        default_size: None, dp(40)
                        default_size_hint: 1, None
        MDBoxLayout:
            id: WidgetStash
            size_hint: None, None
            size: 0, 0
            opacity: 0.0
            disabled: True
    """
)


class QuickStatusPanel(MDBoxLayout):
    ids: DictProperty

    widget_stash: MDBoxLayout

    display_mode: QSPDisplayMode = ObjectProperty()

    def on_kv_post(self, widget: Widget):
        self.widget_stash = self.ids.get("WidgetStash")

    def set_display_mode(self, mode: QSPDisplayMode | int = QSPDisplayMode.MINIMAL):
        new_mode: QSPDisplayMode = QSPDisplayMode.MINIMAL
        if type(mode) is QSPDisplayMode:
            new_mode = mode
        else:
            new_mode = QSPDisplayMode(mode)

        if new_mode == self.display_mode:
            return

        self.display_mode = new_mode

    def on_display_mode(self, instance, mode):
        to_show: list[StatusPanelBase] = []
        to_hide: list[StatusPanelBase] = []

        for widget in self.children:
            if not isinstance(widget, StatusPanelBase):
                continue

            if widget.qsp_modes and mode not in widget.qsp_modes:
                to_hide.append(widget)

        for widget in self.widget_stash.children:
            if not isinstance(widget, StatusPanelBase):
                continue

            if not widget.qsp_modes or mode in widget.qsp_modes:
                to_show.append(widget)

        for panel in to_hide:
            self.remove_widget(panel)
            self.widget_stash.add_widget(panel)

        for panel in to_show:
            self.widget_stash.remove_widget(panel)
            self.add_widget(panel, 1)

    def update_game_port(self, port: int):
        status_display: StatusLabel | None = self.ids.get("StatusLabel", None)
        if not status_display:
            return

        status_display.set_status_text(f"Slot: {port}")

    def update_game_status(self, status: ConnectionStatus):
        status_display: StatusLabel | None = self.ids.get("StatusLabel", None)
        if not status_display:
            return

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
        goal_display: StatusLabel | None = self.ids.get("GoalLabel", None)
        if not goal_display:
            return

        goal_display.set_status_text(f"{current_amount}/{target_amount}")
        goal_display.set_value_text(goal_target)

    def update_goal_target_status(self, current_amount: int, target_amount: int):
        goal_display: StatusLabel | None = self.ids.get("GoalLabel", None)
        if not goal_display:
            return

        goal_display.set_status_text(f"{current_amount}/{target_amount}")

    def update_pgc_status(self, data: list[dict]):
        pgc_view: AE3RecycleView | None = self.ids.get("PostGameConditionView", None)
        if not pgc_view:
            return

        pgc_view.set_data(data)

    def set_channel_select_preview_labels(self, channel_names: list[str]):
        csp: ChannelSelectPreviewCarousel | None = self.ids.get("ChannelSelectPreviewCarousel", None)
        if not csp:
            return

        csp.set_labels(channel_names)

    def update_active_channel_label(self, channel_name: str, data: list[dict] | None = None):
        if not data:
            data = []

        csp: ChannelSelectPreviewCarousel | None = self.ids.get("ChannelSelectPreviewCarousel", None)
        if not csp:
            return

        csp.scroll_to_label(channel_name)

    def lock_channel_preview(self):
        csp: ChannelSelectPreviewCarousel | None = self.ids.get("ChannelSelectPreviewCarousel", None)
        if not csp:
            return

        csp.lock()

    def unlock_channel_preview(self):
        csp: ChannelSelectPreviewCarousel | None = self.ids.get("ChannelSelectPreviewCarousel", None)
        if not csp:
            return

        csp.unlock()

    def update_overview_status(self, data: list[dict], total: dict | None = None):
        overview_view: AE3RecycleView | None = self.ids.get("OverviewView", None)
        if not overview_view:
            return

        overview_view.set_data(data)
        if not total:
            return

        cspp: IndicatedPairedLabel = self.ids.get("ChannelSelectPreviewProgress", None)
        if not cspp:
            return

        cspp.set_label_text(total.get("label_text", ""))
        cspp.set_value_text(total.get("value_text", ""))
        cspp.set_indicator_value(total.get("indicator_value", 50))


class StatusPanelBase(MDCard):
    qsp_modes: ListProperty


class AE3RecycleView(MDRecycleView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = [{"label_text": "Unknown PGC", "value_text": "0/0", "indicator_value": 0}]

    def set_data(self, data: list[dict[str, Any]]):
        self.data = data


class ChannelSelectPreviewLayout(MDBoxLayout):
    viewport_size: float = NumericProperty()
    current_focus: int = NumericProperty()

    def clear_labels(self):
        labels: list[Widget] = list(self.children)
        for label in labels:
            self.remove_widget(label)


class ChannelSelectPreviewCarousel(Carousel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.labels: dict[str, MDLabel] = {}
        self.is_locked: bool = False

        theme_manager = MDApp.get_running_app().theme_cls
        theme_manager.bind(primaryColor=lambda i, v: self.set_label_color())

    def set_labels(self, labels: typing.Iterable[str]):
        for label in labels:
            w = MDLabel(theme_text_color="Custom", text=label, bold=True, valign="middle", halign="center")
            w.font_size = "20sp"
            self.labels[label] = w
            self.add_widget(w)

    def scroll_to_label(self, label_name: str):
        if self.is_locked:
            return

        if label_name not in self.labels:
            return

        if self.current_slide == self.labels[label_name]:
            return

        self.load_slide(self.labels[label_name])

    def lock_to_label(self, label_name: str):
        if self.is_locked:
            return

        self.scroll_to_label(label_name)
        self.lock()

    def lock(self):
        self.is_locked = True
        self.scroll_timeout = 0

    def unlock(self):
        self.is_locked = False
        self.scroll_timeout = 200

    def set_label_color(self):
        theme_manager = MDApp().get_running_instance().theme_cls

        for label in self.labels.values():
            label.color = theme_manager.primaryColor


class OverviewLayout(MDBoxLayout):
    title_text: str = StringProperty()

    def set_title_text(self, text):
        self.title_text = text


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
        self.indicator_value = max(min(progress, 100.0), 0.0)

    def on_indicator_value(self, instance, value):
        if value < 20:
            self.indicator_color = self.theme_cls.errorColor
        elif value < 70:
            self.indicator_color = self.theme_cls.tertiaryColor
        elif value < 100:
            self.indicator_color = self.theme_cls.secondaryColor
        else:
            self.indicator_color = self.theme_cls.primaryColor


class IndicatedPairedLabel(PairedLabel, IndicatedLabel):
    pass


class IndicatedStatusLabel(StatusLabel, IndicatedLabel):
    pass


def create_quick_status_panel() -> QuickStatusPanel:
    kv_string: str = BASE_WIDGETS + "\n" + QUICK_STATUS_PANEL_KV
    return Builder.load_string(kv_string)
