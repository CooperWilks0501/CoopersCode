import tkinter as tk
from tkinter import ttk
import random

cocktails = [
    {"name": "Margarita",
     "ingredients": ["2 oz Tequila", "1 oz Lime juice", "1 oz Triple sec", "Salt for rim (optional)"],
     "instructions": "Shake all ingredients with ice, strain into a salt-rimmed glass."},

    {"name": "Mojito",
     "ingredients": ["2 oz White rum", "1 oz Lime juice", "2 tsp Sugar", "6 Mint leaves", "Soda water"],
     "instructions": "Muddle mint leaves with sugar and lime juice. Add rum, fill with soda water, stir gently."},

    {"name": "Old Fashioned",
     "ingredients": ["2 oz Bourbon or rye whiskey", "1 sugar cube", "2 dashes Angostura bitters", "Orange twist"],
     "instructions": "Muddle sugar and bitters, add whiskey and ice, stir gently, garnish with orange twist."},

    {"name": "Cosmopolitan",
     "ingredients": ["1.5 oz Vodka", "1 oz Cranberry juice", "0.5 oz Triple sec", "0.5 oz Lime juice"],
     "instructions": "Shake all ingredients with ice, strain into a chilled cocktail glass."},

    {"name": "Daiquiri",
     "ingredients": ["2 oz White rum", "1 oz Lime juice", "0.75 oz Simple syrup"],
     "instructions": "Shake all ingredients with ice and strain into a chilled glass."},

    {"name": "Negroni",
     "ingredients": ["1 oz Gin", "1 oz Campari", "1 oz Sweet vermouth"],
     "instructions": "Stir all ingredients with ice and strain into a rocks glass with ice. Garnish with orange peel."},

    {"name": "Manhattan",
     "ingredients": ["2 oz Rye whiskey", "1 oz Sweet vermouth", "2 dashes Angostura bitters"],
     "instructions": "Stir all ingredients with ice, strain into a chilled glass, garnish with cherry."},

    {"name": "Whiskey Sour",
     "ingredients": ["2 oz Whiskey", "1 oz Lemon juice", "0.5 oz Simple syrup", "Optional: egg white"],
     "instructions": "Shake ingredients with ice, strain into glass, garnish with cherry or lemon."},

    {"name": "Gin & Tonic",
     "ingredients": ["2 oz Gin", "4 oz Tonic water", "Lime wedge"],
     "instructions": "Pour gin over ice, top with tonic water, garnish with lime wedge."},

    {"name": "Bloody Mary",
     "ingredients": ["1.5 oz Vodka", "3 oz Tomato juice", "0.5 oz Lemon juice",
                     "2 dashes Worcestershire sauce", "Tabasco sauce, salt, pepper", "Celery stick garnish"],
     "instructions": "Mix all ingredients with ice, stir gently, garnish with celery."},

    {"name": "Pina Colada",
     "ingredients": ["2 oz White rum", "1 oz Coconut cream", "1 oz Pineapple juice"],
     "instructions": "Blend all ingredients with ice until smooth, serve with pineapple slice."},

    {"name": "French 75",
     "ingredients": ["1 oz Gin", "0.5 oz Lemon juice", "0.5 oz Simple syrup", "3 oz Champagne"],
     "instructions": "Shake gin, lemon juice, and syrup with ice, strain into flute, top with champagne."},

    {"name": "Tom Collins",
     "ingredients": ["2 oz Gin", "1 oz Lemon juice", "0.5 oz Simple syrup", "Club soda"],
     "instructions": "Shake gin, lemon juice, and syrup with ice, strain into glass, top with club soda."},

    {"name": "Mint Julep",
     "ingredients": ["2 oz Bourbon", "4-5 Mint leaves", "0.5 oz Simple syrup"],
     "instructions": "Muddle mint with syrup, add bourbon and crushed ice, stir gently."},

    {"name": "Mai Tai",
     "ingredients": ["1 oz White rum", "1 oz Dark rum", "0.5 oz Lime juice",
                     "0.5 oz Orange curaçao", "0.5 oz Orgeat syrup"],
     "instructions": "Shake all but dark rum with ice, strain into glass, float dark rum on top."},

    {"name": "Caipirinha",
     "ingredients": ["2 oz Cachaça", "1 Lime (cut into wedges)", "2 tsp Sugar"],
     "instructions": "Muddle lime and sugar, add cachaça and ice, stir well."},

    {"name": "Sidecar",
     "ingredients": ["2 oz Cognac", "1 oz Triple sec", "0.75 oz Lemon juice"],
     "instructions": "Shake all with ice, strain into sugar-rimmed glass."},

    {"name": "Screwdriver",
     "ingredients": ["2 oz Vodka", "4 oz Orange juice"],
     "instructions": "Pour vodka into glass filled with ice, top with orange juice."},

    {"name": "Bellini",
     "ingredients": ["2 oz Prosecco", "1 oz Peach puree"],
     "instructions": "Pour peach puree into flute, slowly add prosecco."},

    {"name": "Irish Coffee",
     "ingredients": ["1.5 oz Irish whiskey", "1 tsp Brown sugar", "4 oz Hot coffee", "Whipped cream"],
     "instructions": "Stir whiskey and sugar in coffee, top with whipped cream."},

    {"name": "Espresso Martini",
     "ingredients": ["1.5 oz Vodka", "1 oz Coffee liqueur", "1 oz Fresh espresso"],
     "instructions": "Shake all ingredients with ice, strain into martini glass."},

    {"name": "Long Island Iced Tea",
     "ingredients": ["0.5 oz Vodka", "0.5 oz Gin", "0.5 oz White rum", "0.5 oz Tequila",
                     "0.5 oz Triple sec", "1 oz Sour mix", "Splash of cola"],
     "instructions": "Shake all but cola with ice, strain into glass, top with cola."},

    {"name": "Aperol Spritz",
     "ingredients": ["3 oz Prosecco", "2 oz Aperol", "1 oz Soda water"],
     "instructions": "Build over ice in glass, stir gently, garnish with orange slice."},

    {"name": "Paloma",
     "ingredients": ["2 oz Tequila", "0.5 oz Lime juice", "Grapefruit soda"],
     "instructions": "Build over ice in glass, top with grapefruit soda."},

    {"name": "French Martini",
     "ingredients": ["1.5 oz Vodka", "0.5 oz Chambord", "2 oz Pineapple juice"],
     "instructions": "Shake all with ice, strain into martini glass."},

    {"name": "Zombie",
     "ingredients": ["1 oz Light rum", "1 oz Dark rum", "1 oz Apricot brandy", "1 oz Pineapple juice",
                     "1 oz Lime juice", "0.5 oz Grenadine"],
     "instructions": "Shake all with ice, strain into glass, garnish with fruit."},

    {"name": "Black Russian",
     "ingredients": ["2 oz Vodka", "1 oz Coffee liqueur"],
     "instructions": "Build over ice in a rocks glass, stir gently."},

    {"name": "White Russian",
     "ingredients": ["2 oz Vodka", "1 oz Coffee liqueur", "1 oz Cream"],
     "instructions": "Build over ice in a rocks glass, stir gently."},

    {"name": "Gin Fizz",
     "ingredients": ["2 oz Gin", "1 oz Lemon juice", "0.75 oz Simple syrup", "Club soda"],
     "instructions": "Shake gin, lemon juice, and syrup with ice, strain into glass, top with soda."}
]

class CocktailApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🍹 Random Cocktail Generator 🍸")
        self.geometry("520x570")
        self.configure(bg="#f8f0e3")

        self.style = ttk.Style(self)
        self.style.configure('TButton', font=('Arial', 14), padding=8)
        self.style.configure('Header.TLabel', font=('Arial', 22, 'bold'), background="#f8f0e3")
        self.style.configure('SubHeader.TLabel', font=('Arial', 16, 'italic'), background="#f8f0e3")
        self.style.configure('Body.TLabel', font=('Arial', 13), background="#f8f0e3", wraplength=480, justify="left")

        self.header_label = ttk.Label(self, text="Your Cocktail Recipe", style='Header.TLabel')
        self.header_label.pack(pady=(20, 15))

        self.cocktail_name = ttk.Label(self, text="", style='SubHeader.TLabel')
        self.cocktail_name.pack(pady=(0, 10))

        self.ingredients_label = ttk.Label(self, text="", style='Body.TLabel')
        self.ingredients_label.pack(pady=(0, 10))

        self.instructions_label = ttk.Label(self, text="", style='Body.TLabel')
        self.instructions_label.pack(pady=(0, 20))

        self.generate_button = ttk.Button(self, text="Generate Cocktail", command=self.show_random_cocktail)
        self.generate_button.pack()

        # Show one cocktail on start
        self.show_random_cocktail()

    def show_random_cocktail(self):
        cocktail = random.choice(cocktails)
        self.cocktail_name.config(text=cocktail["name"])

        ingredients_text = "Ingredients:\n" + "\n".join(f"• {ing}" for ing in cocktail["ingredients"])
        self.ingredients_label.config(text=ingredients_text)

        instructions_text = f"Instructions:\n{cocktail['instructions']}"
        self.instructions_label.config(text=instructions_text)

if __name__ == "__main__":
    app = CocktailApp()
    app.mainloop()
