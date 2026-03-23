from web3 import Web3
import tkinter as tk
from tkinter import messagebox

# -------------------------------
# 🔗 Connect to Blockchain
# -------------------------------
# Use Sepolia (Infura/Alchemy) OR Ganache
RPC_URL = "https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID"
# For Ganache use:
# RPC_URL = "http://127.0.0.1:7545"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# -------------------------------
# 🧠 Functions
# -------------------------------
def load_wallet():
    global account
    private_key = entry_key.get()

    try:
        account = w3.eth.account.from_key(private_key)
        label_address.config(text=f"Address: {account.address}")
        messagebox.showinfo("Success", "Wallet Loaded Successfully")
    except:
        messagebox.showerror("Error", "Invalid Private Key")

def check_balance():
    try:
        balance = w3.eth.get_balance(account.address)
        eth_balance = w3.from_wei(balance, 'ether')
        label_balance.config(text=f"Balance: {eth_balance} ETH")
    except:
        messagebox.showerror("Error", "Load wallet first")

def simulate_transaction():
    try:
        receiver = entry_to.get()
        amount = float(entry_amount.get())

        nonce = w3.eth.get_transaction_count(account.address)

        tx = {
            'nonce': nonce,
            'to': receiver,
            'value': w3.to_wei(amount, 'ether'),
            'gas': 21000,
            'gasPrice': w3.to_wei('10', 'gwei')
        }

        label_tx.config(text=f"TX Prepared:\nTo: {receiver}\nAmount: {amount} ETH")
        messagebox.showinfo("Success", "Transaction Prepared (Not Sent)")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# -------------------------------
# 🎨 Tkinter UI
# -------------------------------
root = tk.Tk()
root.title("Blockchain Wallet Interaction")
root.geometry("500x400")

# Private Key Input
tk.Label(root, text="Enter Private Key").pack()
entry_key = tk.Entry(root, width=60)
entry_key.pack()

tk.Button(root, text="Load Wallet", command=load_wallet).pack(pady=5)

# Wallet Address
label_address = tk.Label(root, text="Address: ")
label_address.pack()

# Balance
tk.Button(root, text="Check Balance", command=check_balance).pack(pady=5)
label_balance = tk.Label(root, text="Balance: ")
label_balance.pack()

# Transaction Section
tk.Label(root, text="Receiver Address").pack()
entry_to = tk.Entry(root, width=60)
entry_to.pack()

tk.Label(root, text="Amount (ETH)").pack()
entry_amount = tk.Entry(root)
entry_amount.pack()

tk.Button(root, text="Simulate Transaction", command=simulate_transaction).pack(pady=10)

label_tx = tk.Label(root, text="")
label_tx.pack()

# Run App
root.mainloop()