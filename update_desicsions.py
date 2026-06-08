from decision import process_vault

if __name__ == "__main__":
    your_vault_path = r"C:\path\to\your\obsidian\vault"   # Windows example
    # your_vault_path = "/Users/yourname/vault"           # macOS / Linux example
    
    if "your/obsidian/vault" in your_vault_path or not your_vault_path:
        print("⚠️  Please edit the script and set your actual Obsidian vault path!")
    else:
        process_vault(your_vault_path)