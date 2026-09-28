import tkinter as tk
from ui.login_view import LoginView

def main():
    root = tk.Tk()
    root.title("Sistema de Restaurante - Login")
    root.geometry("400x450")
    
    app = LoginView(root)
    root.mainloop()

if __name__ == "__main__":
    main()