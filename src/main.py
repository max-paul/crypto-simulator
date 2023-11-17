import tkinter as tk
from CryptoApp import CryptoInvestmentApp

def main():
    root = tk.Tk()
    app = CryptoInvestmentApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
