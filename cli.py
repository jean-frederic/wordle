import os
import sys
import time
from collections import Counter
from wordle_engine import WordleEngine

if sys.platform == 'win32':
    os.system('')
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GREY = "\033[90m"
CYAN = "\033[96m"

BG_GREEN = "\033[48;2;62;170;66m\033[37m\033[1m"
BG_ORANGE = "\033[48;2;205;135;41m\033[37m\033[1m"
BG_GREY = "\033[48;2;58;58;60m\033[37m\033[1m"

def render_colored_word(word, pattern):
    chars = []
    for letter, p in zip(word, pattern):
        if p == 2:
            chars.append(f"{BG_GREEN} {letter} {RESET}")
        elif p == 1:
            chars.append(f"{BG_ORANGE} {letter} {RESET}")
        else:
            chars.append(f"{BG_GREY} {letter} {RESET}")
    return " ".join(chars)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print(f"""
{CYAN}{BOLD}╔═══════════════════════════════════════════════════════════════════════╗
║                   LE MOT SOLVER - wordle.louan.me                     ║
║              Intelligence Artificielle • Objectif 2-3 Coups           ║
╚═══════════════════════════════════════════════════════════════════════╝{RESET}
""")

def run_interactive_assistant(engine):
    clear_screen()
    print_banner()
    print(f"{BOLD}Mode Assistant Interactif en Direct{RESET}")
    print(f"Jouez en parallèle sur {CYAN}https://wordle.louan.me{RESET}\n")

    candidates = engine.target_words[:]
    turn = 1

    print(f"{BOLD}💡 Meilleur mot d'ouverture recommandé pour le 1er coup :{RESET}")
    for op in engine.recommended_openers[:3]:
        print(f"  • {BOLD}{op['word']}{RESET} : {op['note']} (Entropie: {op['entropy']} bits)")
    print()

    while True:
        print(f"\n{CYAN}━━━ Coup #{turn} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
        print(f"Mots candidats encore possibles : {BOLD}{len(candidates)}{RESET}")

        if len(candidates) == 0:
            print(f"{YELLOW}⚠️ Aucun mot correspondant trouvé. Une erreur s'est peut-être glissée dans les couleurs.{RESET}")
            break
        elif len(candidates) == 1:
            sol = candidates[0]
            print(f"\n{GREEN}{BOLD}🎉 LE MOT EST TROUVÉ ! Entrez : {sol}{RESET}")
            break
        elif len(candidates) <= 15:
            cands_str = ", ".join(candidates)
            print(f"Candidats restants : {cands_str}")

        suggestions = engine.analyze_suggestions(candidates, top_n=5)
        print(f"\n{BOLD}🎯 Suggestions de l'IA (optimisées pour 2 ou 3 coups) :{RESET}")
        for idx, s in enumerate(suggestions, 1):
            tag = ""
            if s["guarantee_3"]:
                tag = f" {GREEN}[GARANTIE <= 3 COUPS]{RESET}"
            elif s["p_win_now"] > 0:
                tag = f" {YELLOW}[CHANCE 2 COUPS : {int(s['p_win_now']*100)}%]{RESET}"
            
            print(f"  {idx}. {BOLD}{s['word']}{RESET}{tag} -> {s['reason']}")

        print(f"\nEntrez le mot que vous avez joué (ou 'Q' pour quitter) :")
        played = input(f"{BOLD}> {RESET}").strip().upper()
        if played in ('Q', 'QUIT'):
            break
        if len(played) != 5:
            print(f"{YELLOW}Le mot doit faire exactement 5 lettres.{RESET}")
            continue

        print(f"\nEntrez le résultat des couleurs renvoyé par wordle.louan.me :")
        print(f"  • Format chiffres : {BOLD}0{RESET}=Gris, {BOLD}1{RESET}=Orange, {BOLD}2{RESET}=Vert (ex: {BOLD}01200{RESET})")
        print(f"  • Ou format lettres : {BOLD}G{RESET}=Gris, {BOLD}O/J{RESET}=Orange/Jaune, {BOLD}V{RESET}=Vert (ex: {BOLD}GOVGG{RESET})")
        pat_str = input(f"{BOLD}> {RESET}").strip().upper()
        
        try:
            pat_int, pat_list = engine.parse_pattern_input(pat_str)
        except Exception as e:
            print(f"{YELLOW}Erreur : {e}{RESET}")
            continue

        print(f"Résultat visualisé : {render_colored_word(played, pat_list)}")

        if pat_list == [2, 2, 2, 2, 2]:
            print(f"\n{GREEN}{BOLD}🏆 VICTOIRE EN {turn} COUP(S) ! Félicitations !{RESET}")
            break

        candidates = engine.filter_candidates(candidates, played, pat_int)
        turn += 1
        if turn > 6:
            print(f"\n{YELLOW}Nombre maximum de tentatives atteint.{RESET}")
            break

    input(f"\nAppuyez sur Entrée pour revenir au menu...")

def run_oracle(engine):
    clear_screen()
    print_banner()
    print(f"{BOLD}Mode Oracle Louan (Reverse-Engineering){RESET}\n")

    today_word, today_date = engine.get_louan_daily_word()
    print(f"📅 Date aujourd'hui (Europe/Paris) : {BOLD}{today_date}{RESET}")
    print(f"🔑 Mot secret du jour : {GREEN}{BOLD}{today_word}{RESET}\n")

    print("Options :")
    print("  [1] Voir la stratégie en 2 COUPS MAXIMUM pour aujourd'hui")
    print("  [2] Voir la stratégie en 3 COUPS MAXIMUM pour aujourd'hui")
    print("  [3] Calculer le mot pour une autre date (Archives)")
    print("  [0] Retour au menu principal")

    choice = input(f"\n{BOLD}> {RESET}").strip()
    if choice == '1':
        plan = engine.generate_guaranteed_plan(today_word, mode=2)
        print(f"\n{BOLD}⚡ PLAN EN 2 COUPS GARANTI POUR AUJOURD'HUI ({today_word}) :{RESET}\n")
        for step in plan:
            print(f"  Coup #{step['step']} : {render_colored_word(step['word'], step['pattern'])}  ({step['note']})")
        input(f"\nAppuyez sur Entrée pour continuer...")
    elif choice == '2':
        plan = engine.generate_guaranteed_plan(today_word, mode=3)
        print(f"\n{BOLD}🎯 PLAN EN 3 COUPS NATUREL & INDÉTECTABLE POUR AUJOURD'HUI ({today_word}) :{RESET}\n")
        for step in plan:
            print(f"  Coup #{step['step']} : {render_colored_word(step['word'], step['pattern'])}  ({step['note']})")
        input(f"\nAppuyez sur Entrée pour continuer...")
    elif choice == '3':
        custom_date = input("Entrez la date (format AAAA-M-J, ex: 2024-5-18) : ").strip()
        try:
            word, dt = engine.get_louan_daily_word(custom_date)
            print(f"\nMot secret pour le {BOLD}{dt}{RESET} : {GREEN}{BOLD}{word}{RESET}")
            plan2 = engine.generate_guaranteed_plan(word, mode=2)
            print(f"Stratégie 2 coups : {plan2[0]['word']} -> {plan2[1]['word']}")
        except Exception as e:
            print(f"{YELLOW}Erreur : {e}{RESET}")
        input(f"\nAppuyez sur Entrée pour continuer...")

def run_simulation(engine):
    clear_screen()
    print_banner()
    print(f"{BOLD}Benchmark & Simulation sur le Dictionnaire Français{RESET}\n")
    print("Test de l'algorithme Shannon sur 100 mots cibles aléatoires...")
    
    import random
    targets_sample = random.sample(engine.target_words, 100)
    results = Counter()
    t0 = time.time()
    
    first_guess = "TARIE"

    for i, target in enumerate(targets_sample, 1):
        cands = engine.target_words[:]
        turn = 0
        guess = first_guess
        while True:
            turn += 1
            if guess == target:
                results[turn] += 1
                break
            p_int, _ = engine.get_feedback(guess, target)
            cands = engine.filter_candidates(cands, guess, p_int)
            suggs = engine.analyze_suggestions(cands, top_n=1)
            guess = suggs[0]["word"] if suggs else cands[0]

    t1 = time.time()
    print(f"\nTerminé en {t1 - t0:.2f} secondes !")
    print(f"\n{BOLD}📊 Distribution des victoires :{RESET}")
    for k in sorted(results.keys()):
        bar = "█" * (results[k] // 2)
        print(f"  En {k} coup(s) : {results[k]:2d}%  {CYAN}{bar}{RESET}")

    total = len(targets_sample)
    avg = sum(k * v for k, v in results.items()) / total
    le_3 = (results[1] + results[2] + results[3]) / total * 100
    print(f"\n  • Moyenne des tentatives : {BOLD}{avg:.2f}{RESET}")
    print(f"  • Victoires en 2 ou 3 coups : {GREEN}{BOLD}{le_3:.1f}%{RESET}")
    input(f"\nAppuyez sur Entrée pour revenir au menu...")

def main():
    engine = WordleEngine()
    while True:
        clear_screen()
        print_banner()
        print(f"{BOLD}Menu Principal :{RESET}\n")
        print(f"  {CYAN}[1]{RESET} {BOLD}Assistant IA en direct{RESET} (calculateur d'entropie pendant votre partie)")
        print(f"  {CYAN}[2]{RESET} {BOLD}Oracle Louan{RESET} (mot du jour et trajectoire 2-3 coups garantie)")
        print(f"  {CYAN}[3]{RESET} {BOLD}Simulateur & Benchmark{RESET} (tester les performances)")
        print(f"  {CYAN}[4]{RESET} {BOLD}Lancer l'Interface Web{RESET} (recommandé !)")
        print(f"  {CYAN}[0]{RESET} Quitter\n")

        choice = input(f"{BOLD}Votre choix > {RESET}").strip()
        if choice == '1':
            run_interactive_assistant(engine)
        elif choice == '2':
            run_oracle(engine)
        elif choice == '3':
            run_simulation(engine)
        elif choice == '4':
            print(f"\nLancement du serveur Web local...")
            from web_server import start_server
            start_server(open_browser=True)
            break
        elif choice in ('0', 'q', 'exit'):
            print(f"\nAu revoir et bonnes parties !")
            break

if __name__ == "__main__":
    main()
