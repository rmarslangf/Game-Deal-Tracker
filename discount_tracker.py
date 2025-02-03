import tkinter as tk
from tkinter import Toplevel, ttk
import requests
from bs4 import BeautifulSoup
#=======================================RSS======================================================================
def get_discount_games():
    url = "https://isthereanydeal.com/feeds/TR/TRY/deals.rss"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "xml") 
        games = []

        for deal in soup.find_all("item"):
            title_element = deal.find("title")
            description_element = deal.find("description")

            if title_element and description_element:
                title = title_element.text.strip()
                description = description_element.text.strip()
                clean_description = BeautifulSoup(description, "html.parser")
                stores = []
                for line in clean_description.find_all("b"):
                    price = line.text.strip()
                    discount = line.find_next("i").text.strip() if line.find_next("i") else "N/A"
                    store_element = line.find_next("a")
                    store = store_element.text.strip() if store_element else "Unknown Store"
                    try:
                        price_value = float(price.replace("₺", "").replace(",", "."))
                    except ValueError:
                        price_value = float("inf")
                    stores.append((title, store, price_value, discount))
                
                games.extend(stores)
        return games
    else:
        print("Web sitesine erişimde hata oluştu. HTTP Durum Kodu:", response.status_code)
        return []
#=============================Price Filter on click/Tıklanıldığında Fiyat Filtresi==========================================
def toggle_sort():
    global ascending
    ascending = not ascending
    sorted_games = sorted(discounted_games, key=lambda x: x[2], reverse=not ascending)
    update_treeview(sorted_games)
#========================================View/Görünüm=====================================================
def update_treeview(games):
    tree.delete(*tree.get_children())
    for game in games:
        tree.insert("", "end", values=(game[0], game[1], f"₺{game[2]:.2f}", game[3]))
#========================================PopUp=====================================================
def show_discount_popup():
    global tree, discounted_games, ascending
    discounted_games = get_discount_games()
    if not discounted_games:
        return

    ascending = True
    popup = tk.Tk()
    popup.title("İndirimdeki Oyunlar")
    popup.geometry("700x400")
    popup.config(bg="#2C3E50")

    tree = ttk.Treeview(popup, columns=("Oyun", "Mağaza", "Fiyat", "İndirim"), show="headings")
    tree.heading("Oyun", text="Oyun")
    tree.heading("Mağaza", text="Mağaza")
    tree.heading("Fiyat", text="Fiyat", command=toggle_sort)
    tree.heading("İndirim", text="İndirim")

    tree.column("Oyun", width=250, anchor="center")
    tree.column("Mağaza", width=150, anchor="center")
    tree.column("Fiyat", width=100, anchor="center")
    tree.column("İndirim", width=100, anchor="center")

    tree.pack(pady=20, fill=tk.BOTH, expand=True)
    
    update_treeview(discounted_games)
    popup.mainloop()

show_discount_popup()
