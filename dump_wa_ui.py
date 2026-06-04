"""
Dump WhatsApp Desktop UI tree to find the Voice Call button name.
Run this WHILE WhatsApp is open on a chat screen.
"""
import time
import subprocess
import sys

# Make sure WhatsApp is focused
try:
    import pygetwindow as gw
    windows = gw.getWindowsWithTitle("WhatsApp")
    if windows:
        windows[0].activate()
        time.sleep(1)
        print(f"WhatsApp window found: {windows[0].title}")
    else:
        print("WhatsApp not open!")
        sys.exit(1)
except Exception as e:
    print(f"pygetwindow error: {e}")

# Try uiautomation first
try:
    import uiautomation as auto
    print("\n=== Using uiautomation ===")
    wa = auto.WindowControl(searchDepth=1, Name="WhatsApp")
    print(f"Window found: {wa.Name}")
    
    # Find all buttons in top area
    print("\n--- All Buttons ---")
    for btn in wa.GetChildren():
        try:
            children = btn.GetChildren()
            for c in children:
                if hasattr(c, 'Name') and c.Name:
                    print(f"  [{c.ControlTypeName}] Name={c.Name!r}")
        except:
            pass
    
    # Deep search for call-related controls
    print("\n--- Deep search for 'call' ---")
    def find_controls(ctrl, depth=0, max_depth=5):
        if depth > max_depth:
            return
        try:
            name = ctrl.Name or ''
            ctype = ctrl.ControlTypeName or ''
            if name and ('call' in name.lower() or 'voice' in name.lower() or 'audio' in name.lower()):
                print(f"{'  '*depth}[{ctype}] {name!r}")
            for child in ctrl.GetChildren():
                find_controls(child, depth+1, max_depth)
        except:
            pass
    
    find_controls(wa)

except ImportError:
    print("uiautomation not installed, trying pywinauto...")
    try:
        from pywinauto import Application, Desktop
        app = Application(backend="uia").connect(title="WhatsApp")
        win = app.top_window()
        print("WhatsApp window connected")
        
        print("\n--- Controls with 'call' in name ---")
        def search_tree(wrapper, depth=0):
            if depth > 6:
                return
            try:
                name = wrapper.window_text() or ''
                atype = wrapper.element_info.control_type or ''
                if 'call' in name.lower() or 'voice' in name.lower():
                    print(f"{'  '*depth}[{atype}] {name!r}")
                for child in wrapper.children():
                    search_tree(child, depth+1)
            except:
                pass
        search_tree(win)
    except Exception as e2:
        print(f"pywinauto error: {e2}")
        print("\nTrying raw accessibility via comtypes...")
