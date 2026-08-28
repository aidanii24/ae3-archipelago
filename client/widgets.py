from textwrap import dedent
from typing import Any

from kivy.animation import Animation, AnimationTransition
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    DictProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.scrollview import ScrollView

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
                AE3ScrollView:
                    id: ChannelSelectPreviewScroll
                    size_hint_y: None
                    do_scroll_x: True
                    do_scroll_y: False
                    height: dp(30)
                    ChannelSelectPreviewLayout:
                        id: ChannelSelectPreviewLayout
                        viewport_size: self.parent.width
                        orientation: 'horizontal'
                        focused_color: app.theme_cls.primaryColor
                        unfocused_color: app.theme_cls.onSurfaceColor
                        spacing: dp(150)
                        adaptive_size: True
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
                    MDRecycleGridLayout:
                        cols: min(len(self.parent.data), 3)
                        spacing: 20
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
        cspl: ChannelSelectPreviewLayout | None = self.ids.get("ChannelSelectPreviewLayout", None)
        if not cspl:
            return

        cspl.set_labels(channel_names)
        cspl.on_viewport_size(cspl, cspl.size)

    def update_active_channel_index(self, index: int = 0, data: list[dict] | None = None):
        if not data:
            data = []

        csp: AE3ScrollView | None = self.ids.get("ChannelSelectPreviewScroll", None)
        if not csp:
            return

        cspl: ChannelSelectPreviewLayout | None = self.ids.get("ChannelSelectPreviewLayout", None)
        if not cspl:
            return

        if index < 0 or index > len(cspl.children):
            return

        scroll_ratio: float = cspl.get_center_ratio_to_child_index(index)

        csp.switch_focused_label(cspl.children[len(cspl.children) - index - 1])
        csp.scroll_to_x(scroll_ratio)

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


class BigFocusLabel(MDLabel):
    is_focused = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        theme_manager = MDApp.get_running_app().theme_cls
        theme_manager.bind(onSurfaceColor=lambda i, v: self.set_text_color())

        self.on_is_focused(self, self.is_focused)

    def on_is_focused(self, instance, is_focused):
        instance.bold = is_focused
        instance.opacity = 1.0 if is_focused else 0.6

        instance.set_text_color()

    def set_text_color(self):
        theme_manager = MDApp.get_running_app().theme_cls
        self.text_color = theme_manager.primaryColor if self.is_focused else theme_manager.onSurfaceColor


class AE3ScrollView(ScrollView):
    focused_label: BigFocusLabel = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.animation = Animation()
        self.is_animating: bool = False

    def _set_is_animating(self, value: bool):
        self.is_animating = value

    def scroll_to_x(self, x: float = 0.0, duration: float = 0.15):
        if self.is_animating:
            self.animation.stop(self)

        self.animation = Animation(scroll_x=x, duration=duration, transition=AnimationTransition.in_out_quad)
        self.animation.bind(on_complete=lambda anim, widget: self._set_is_animating(False))

        self.animation.start(self)

    def switch_focused_label(self, new_focus: BigFocusLabel):
        if self.focused_label:
            self.focused_label.is_focused = False

        new_focus.is_focused = True

        self.focused_label = new_focus


class ChannelSelectPreviewLayout(MDBoxLayout):
    viewport_size: float = NumericProperty()
    current_focus: int = NumericProperty()

    def set_labels(self, names: list[str]):
        theme_manager = MDApp.get_running_app().theme_cls
        self.clear_labels()

        for d in names:
            label = BigFocusLabel(
                text=d,
                adaptive_size=True,
                valign="middle",
                halign="center",
                theme_text_color="Custom",
                is_focused=False,
            )

            label.font_size = "20sp"

            self.add_widget(label)

    def clear_labels(self):
        labels: list[Widget] = list(self.children)
        for label in labels:
            self.remove_widget(label)

    def get_center_ratio_to_child_index(self, index: int) -> float:
        if not self.width:
            return 0

        reverse_index: int = len(self.children) - index - 1
        children_to_count: list[MDLabel] = self.children[reverse_index:]

        cum_length: float = 0.0
        for w in children_to_count[1:]:
            cum_length += w.width + self.spacing

        target = children_to_count[0]
        cum_length += target.width / 2
        cum_length += self.viewport_size * (index / len(self.children)) - self.viewport_size / 2

        return min(max(0, cum_length / self.width), 1.0)

    def on_viewport_size(self, instance, size):
        if not self.viewport_size or not self.children:
            return

        viewport_size = self.parent.width - self.parent.parent.padding[0] - self.parent.parent.padding[2]

        first: MDLabel = self.children[0]
        last: MDLabel = self.children[-1]

        first.padding = [0, 0, viewport_size / 2 - first.width, 0]
        last.padding = [self.viewport_size / 2 - last.width / 2, 0, 0, 0]


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
