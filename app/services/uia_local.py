"""
uia_local.py — thread-safe UI Automation access (helper, not a tool)
===================================================================
pywinauto keeps ONE UIAutomation COM object (uia_defines.IUIA singleton) that belongs to
the thread that created it first. In the backend, tools run on worker threads (and the
screen watcher uses UIA too), so calls from another thread got empty/stale trees:
Spotify commands failed right after a song started ("already paused", "couldn't reach
the player controls") while the same code worked in a single-threaded script.

This module gives every thread its own CUIAutomation object and a tiny wrapper with the
few pywinauto-like methods spotify_service / youtube_player need.
"""

import ctypes
import threading

_tls = threading.local()
_user32 = ctypes.windll.user32

UIA_ButtonControlTypeId = 50000
UIA_HyperlinkControlTypeId = 50005
UIA_EditControlTypeId = 50004
UIA_ControlTypePropertyId = 30003
UIA_InvokePatternId = 10000
UIA_ValuePatternId = 10002
TreeScope_Descendants = 4

_CONTROL_TYPES = {"Button": UIA_ButtonControlTypeId, "Hyperlink": UIA_HyperlinkControlTypeId,
                  "Edit": UIA_EditControlTypeId}


def uia():
    """This thread's IUIAutomation (COM initialised for the thread on first use)."""
    u = getattr(_tls, "uia", None)
    if u is None:
        import comtypes
        import comtypes.client
        try:
            comtypes.CoInitialize()
        except Exception:
            pass
        comtypes.client.GetModule("UIAutomationCore.dll")
        from comtypes.gen.UIAutomationClient import CUIAutomation, IUIAutomation
        u = comtypes.client.CreateObject(CUIAutomation, interface=IUIAutomation)
        _tls.uia = u
    return u


class Rect:
    def __init__(self, r):
        self.left, self.top, self.right, self.bottom = r.left, r.top, r.right, r.bottom

    def width(self):
        return self.right - self.left

    def height(self):
        return self.bottom - self.top

    def __repr__(self):
        return f"(L{self.left}, T{self.top}, R{self.right}, B{self.bottom})"


class Element:
    """Minimal pywinauto-style wrapper around an IUIAutomationElement."""

    def __init__(self, el):
        self.el = el

    def window_text(self) -> str:
        try:
            return self.el.CurrentName or ""
        except Exception:
            return ""

    def rectangle(self) -> Rect:
        return Rect(self.el.CurrentBoundingRectangle)

    @property
    def handle(self) -> int:
        return self.el.CurrentNativeWindowHandle

    def control_type(self) -> int:
        return self.el.CurrentControlType

    def descendants(self, control_type: str = "Button") -> list["Element"]:
        u = uia()
        cond = u.CreatePropertyCondition(UIA_ControlTypePropertyId, _CONTROL_TYPES[control_type])
        arr = self.el.FindAll(TreeScope_Descendants, cond)
        return [Element(arr.GetElement(i)) for i in range(arr.Length)]

    def invoke(self):
        from comtypes.gen.UIAutomationClient import IUIAutomationInvokePattern
        pat = self.el.GetCurrentPattern(UIA_InvokePatternId)
        pat.QueryInterface(IUIAutomationInvokePattern).Invoke()

    def click_input(self):
        import pyautogui
        r = self.rectangle()
        pyautogui.click((r.left + r.right) // 2, (r.top + r.bottom) // 2)

    def value(self) -> str | None:
        try:
            from comtypes.gen.UIAutomationClient import IUIAutomationValuePattern
            pat = self.el.GetCurrentPattern(UIA_ValuePatternId)
            return pat.QueryInterface(IUIAutomationValuePattern).CurrentValue or ""
        except Exception:
            return None

    def set_focus(self):
        h = self.handle
        if h:
            if _user32.IsIconic(h):
                _user32.ShowWindow(h, 9)
            _user32.SetForegroundWindow(h)


def element_from_handle(hwnd: int) -> Element:
    return Element(uia().ElementFromHandle(hwnd))


def focused_element() -> Element:
    return Element(uia().GetFocusedElement())
