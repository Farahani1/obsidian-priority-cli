import argparse
from decision.priority import process_vault


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update task priorities in Obsidian vault")
    parser.add_argument("vault_path", help="Path to your Obsidian vault")
    parser.add_argument("--reset", action="store_true", help="Recompute priorities for ALL tasks (overwrite existing)")
    args = parser.parse_args()
    
    process_vault(args.vault_path, reset=args.reset)