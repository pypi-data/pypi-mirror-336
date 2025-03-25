import time
import json
import os

class BigBank:
    def __init__(self):
        # Get the directory where this package is installed
        self.save_dir = os.path.dirname(os.path.abspath(__file__))  
        self.save_file = os.path.join(self.save_dir, "bigbank_save.json")

        self.balance = 0
        self.last_generated = 0
        self.load()
    
    def save(self):
        with open(self.save_file, "w") as f:
            json.dump({"balance": self.balance, "last_generated": self.last_generated}, f)
    
    def load(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as f:
                data = json.load(f)
                self.balance = data.get("balance", 0)
                self.last_generated = data.get("last_generated", 0)
    
    def get_balance(self):
        """Returns the current balance."""
        return self.balance
    
    def generate_money(self):
        """Generates money, respecting the cooldown."""
        cooldown_time = 5
        time_since_last = time.time() - self.last_generated
        if time_since_last < cooldown_time:
            time_left = cooldown_time - time_since_last
            raise CooldownError(f"Cooldown active! Please wait {time_left:.2f} seconds.")
        
        earnings = 10
        self.balance += earnings
        self.last_generated = time.time()
        self.save()
        return f"Generated {earnings} coins! Balance: {self.balance}"

class CooldownError(Exception):
    pass
