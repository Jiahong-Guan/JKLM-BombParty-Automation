from pynput import mouse

if __name__ == '__main__':
    def on_click(x, y, button, pressed):
        if pressed and button == mouse.Button.left:
            print(f"Mouse clicked at ({x}, {y})")


    # Create a listener for mouse events
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
