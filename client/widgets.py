from textwrap import dedent
from typing import Any

from kivy.animation import Animation, AnimationTransition
from kivy.properties import ColorProperty, DictProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.scrollview import ScrollView

from kvui import Builder

from .game_interface import ConnectionStatus
from .state import QSPDisplayMode

BASE_WIDGETS: str = dedent(
    """\
    <StatusPanel@MDBoxLayout>:
        qsp_index_hint: 0
        qsp_modes: []
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
            id: StatusPanel
            StatusLabelComplete:
                id: StatusLabel
                label_text: 'Game Status'
                value_text: 'Waiting for PCSX2'
                status_text: 'Port: 28011'
                value_color: app.theme_cls.onSurfaceColor
        StatusPanel:
            id: GoalPanel
            qsp_modes: [10]
            padding: 0
            IndicatedStatusLabelComplete:
                id: GoalLabel
                label_text: 'Goal Target'
                value_text: 'Goal Unknown'
                status_text: '0/0'
                value_color: app.theme_cls.onSurfaceColor
        StatusPanel:
            id: PostGameConditionPanel
            qsp_modes: [10]
            size_hint_y: None
            height: self.minimum_height
            padding: 20, 20, 20, 0
            spacing: 20
            MDLabel:
                text: "Post Game Conditions (Final Channel Set Unlock)"
                color: self.theme_cls.onSurfaceColor
                bold: True
            AE3RecycleView:
                id: PostGameConditionView
                viewclass: 'IndicatedPairedLabelComplete'
                size_hint_y: None
                MDRecycleGridLayout:
                    cols: 3
                    spacing: 20
                    default_size: None, dp(40)
                    default_size_hint: 1, None
        StatusPanel:
            id: ChannelSelectPreviewPanel
            hint_size_y: None
            height: self.minimum_height
            qsp_modes: [20, 30]
            AE3ScrollView:
                id: ChannelSelectPreviewScroll
                size_hint_y: None
                do_scroll_x: True
                do_scroll_y: False
                height: dp(40)
                ChannelSelectPreviewLayout:
                    id: ChannelSelectPreviewLayout
                    viewport_size: self.parent.width
                    orientation: "horizontal"
                    spacing: 150
                    adaptive_size: True
            AE3RecycleView:
                id: OverviewView
                viewclass: 'IndicatedPairedLabelComplete'
                size_hint_y: None
                MDRecycleGridLayout:
                    cols: 3
                    spacing: 20
                    default_size: None, dp(40)
                    default_size_hint: 1, None
    """
)


class QuickStatusPanel(MDBoxLayout):
    ids: DictProperty
    displays: dict[str, Widget]
    hidden: set[str]

    display_mode: QSPDisplayMode = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hidden = set()
        self.displays = {}

    def _get_widget_and_cache(self, wid: str) -> Widget | None:
        if wid not in self.displays:
            widget: Widget = self.ids.get(wid, None)
            if not widget:
                return None

            self.displays[wid] = widget
            return widget

        return self.displays.get(wid)

    def _hide_children(self, *wids):
        """
        Removes immediate children by id.
        Children removed using this function are not deleted, only orphaned.
        :param: *wids: Widget Ids of children to show
        """
        for wid in wids:
            if wid in self.hidden:
                continue

            widget: Widget | None = self._get_widget_and_cache(wid)
            if not widget:
                continue

            if widget not in self.children:
                continue

            self.remove_widget(widget)
            self.hidden.add(wid)

    def _show_children(self, *wids, indexes: list[int] | None = None):
        """
        Adds widgets as immediate children by id.
        :param: *wids: Widget Ids of children to show
        :param: index: Indexes that correspond to the index the child will be added back as if possible.
        """
        if not indexes:
            indexes = []

        for i, wid in enumerate(wids):
            widget: Widget | None = self._get_widget_and_cache(wid)
            if not widget:
                continue

            index: int = indexes[i] if i < len(indexes) else 0

            self.add_widget(widget, index=index)
            self.hidden.remove(wid)

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
        to_show: list[Widget] = []
        to_show_indexes: list[int] = []
        to_hide: list[Widget] = []

        for i, (wid, widget) in enumerate(self.ids.items()):
            if widget.__class__.__name__ != "StatusPanel":
                continue

            if not widget.qsp_modes:
                continue

            if mode in widget.qsp_modes:
                if wid not in self.hidden:
                    continue

                to_show.append(wid)
                index: int = getattr(widget, "qsp_index_hint", len(self.children) + i)
                to_show_indexes.append(index)
            elif wid not in self.hidden:
                to_hide.append(wid)

        self._hide_children(*to_hide)
        self._show_children(*to_show, indexes=to_show_indexes)

    def update_game_port(self, port: int):
        status_display: StatusLabel | None = self._get_widget_and_cache("StatusLabel")
        if not status_display:
            return

        status_display.set_status_text(f"Port: {port}")

    def update_game_status(self, status: ConnectionStatus):
        status_display: StatusLabel | None = self._get_widget_and_cache("StatusLabel")
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
        goal_display: StatusLabel | None = self._get_widget_and_cache("GoalLabel")
        if not goal_display:
            return

        goal_display.set_status_text(f"{current_amount}/{target_amount}")
        goal_display.set_value_text(goal_target)

    def update_goal_target_status(self, current_amount: int, target_amount: int):
        goal_display: StatusLabel | None = self._get_widget_and_cache("GoalLabel")
        if not goal_display:
            return

        goal_display.set_status_text(f"{current_amount}/{target_amount}")

    def update_pgc_status(self, data: list[dict]):
        pgc_view: AE3RecycleView | None = self._get_widget_and_cache("PostGameConditionView")
        if not pgc_view:
            return

        pgc_view.set_data(data)

    def set_channel_select_preview_labels(self, channel_names: list[str]):
        cspl: ChannelSelectPreviewLayout | None = self._get_widget_and_cache("ChannelSelectPreviewLayout")
        if not cspl:
            return

        cspl.set_labels(channel_names)
        cspl.on_viewport_size(cspl, cspl.size)

    def update_active_channel_index(self, index: int = 0, data: list[dict] | None = None):
        if not data:
            data = []

        csp: AE3ScrollView | None = self._get_widget_and_cache("ChannelSelectPreviewScroll")
        if not csp or csp in self.hidden:
            return

        cspl: ChannelSelectPreviewLayout | None = self._get_widget_and_cache("ChannelSelectPreviewLayout")
        if not cspl:
            return

        if index < 0 or index > len(cspl.children):
            return

        scroll_ratio: float = cspl.get_center_ratio_to_child_index(index)

        csp.switch_focused_label(cspl.children[len(cspl.children) - index - 1])
        csp.scroll_to_x(scroll_ratio)

    def update_overview_status(self, data: list[dict]):
        overview_view: AE3RecycleView | None = self._get_widget_and_cache("OverviewView")
        if not overview_view:
            return

        overview_view.set_data(data)


class AE3RecycleView(MDRecycleView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = [{"label_text": "Unknown PGC", "value_text": "0/0", "indicator_value": 0}]

    def set_data(self, data: list[dict[str, Any]]):
        self.data = data


class AE3ScrollView(ScrollView):
    focused_label: MDLabel = ObjectProperty()

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

    def switch_focused_label(self, new_focus: MDLabel):
        theme_manager = MDApp.get_running_app().root.theme_cls

        if self.focused_label:
            self.focused_label.bold = False
            self.focused_label.text_color = theme_manager.onSurfaceColor
            self.focused_label.opacity = 0.6

        new_focus.bold = True
        new_focus.text_color = theme_manager.primaryColor
        new_focus.opacity = 1.0

        self.focused_label = new_focus


class ChannelSelectPreviewLayout(MDBoxLayout):
    viewport_size: float = NumericProperty()
    current_focus: int = NumericProperty()

    def set_labels(self, names: list[str]):
        theme_manager = MDApp.get_running_app().root.theme_cls
        self.clear_labels()

        for d in names:
            label = MDLabel(
                text=d,
                adaptive_size=True,
                valign="middle",
                halign="center",
                opacity=0.6,
                text_color=theme_manager.onSurfaceColor,
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

        first: MDLabel = self.children[0]
        last: MDLabel = self.children[-1]

        first.padding = [0, 0, self.viewport_size / 2 - first.width / 2, 0]
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
        self.indicator_progress = max(min(progress, 100.0), 0.0)

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
