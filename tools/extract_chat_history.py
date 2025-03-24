#!/usr/bin/env python3
"""Script to extract chat history from GitHub Actions logs."""

import re
import sys
from pathlib import Path


def extract_interactions(log_content: str) -> tuple[list[str], list[str]]:
    """Extract user actions and AI responses from the log content."""
    user_actions = []
    ai_responses = []
    
    # Patterns à rechercher
    user_pattern = r"USER_REQUEST>(.*?)</USER_REQUEST"
    ai_pattern = r"ASSISTANT:(.*?)(?=USER_REQUEST>|$)"
    
    # Extraction
    user_matches = re.findall(user_pattern, log_content, re.DOTALL)
    ai_matches = re.findall(ai_pattern, log_content, re.DOTALL)
    
    # Nettoyage
    user_actions = [action.strip() for action in user_matches]
    ai_responses = [response.strip() for response in ai_matches]
    
    return user_actions, ai_responses


def format_markdown(user_actions: list[str], ai_responses: list[str]) -> str:
    """Format the interactions as a markdown table."""
    markdown = "# Historique des Interactions avec l'IA\n\n"
    markdown += "| Action Utilisateur | Réponse Cascade |\n"
    markdown += "|-------------------|------------------|\n"
    
    for user, ai in zip(user_actions, ai_responses):
        # Nettoyer et formater les cellules
        user = user.replace("\n", "<br>").replace("|", "\\|")
        ai = ai.replace("\n", "<br>").replace("|", "\\|")
        markdown += f"| {user} | {ai} |\n"
    
    return markdown


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python extract_chat_history.py <log_file>")
        sys.exit(1)
        
    log_file = Path(sys.argv[1])
    if not log_file.exists():
        print(f"Error: File {log_file} not found")
        sys.exit(1)
        
    # Lecture du fichier
    log_content = log_file.read_text(encoding="utf-8")
    
    # Extraction et formatage
    user_actions, ai_responses = extract_interactions(log_content)
    markdown = format_markdown(user_actions, ai_responses)
    
    # Écriture du résultat
    output_file = Path("docs/ai_logs/user_interactions.md")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(markdown, encoding="utf-8")
    print(f"Generated: {output_file}")


if __name__ == "__main__":
    main()
