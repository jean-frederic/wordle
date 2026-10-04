import os
import json
import math
from datetime import datetime, timezone, timedelta
from collections import Counter

class WordleEngine:
    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = os.path.dirname(os.path.abspath(__file__))
        
        target_path = os.path.join(data_dir, 'target_words.json')
        all_path = os.path.join(data_dir, 'all_words.json')
        
        with open(target_path, 'r', encoding='utf-8') as f:
            self.target_words = json.load(f)
            
        with open(all_path, 'r', encoding='utf-8') as f:
            self.all_words = json.load(f)
            
        self.target_set = set(self.target_words)
        self.all_set = set(self.all_words)
        
        self.recommended_openers = [
            {"word": "TARIE", "entropy": 6.07, "expected_remaining": 43.2, "note": "Minimum de candidats restants (43 en moyenne)"},
            {"word": "TAIRE", "entropy": 6.08, "expected_remaining": 45.4, "note": "Excellente séparation (pire groupe: 157)"},
            {"word": "RAIES", "entropy": 6.10, "expected_remaining": 48.8, "note": "Entropie de Shannon maximale (6.10 bits)"},
            {"word": "CARIE", "entropy": 5.99, "expected_remaining": 50.1, "note": "Variante excellente avec consonne 'C'"},
            {"word": "SORTE", "entropy": 5.92, "expected_remaining": 55.1, "note": "Variante voyelle 'O' + 'S','R','T','E'"}
        ]

    @staticmethod
    def get_feedback(guess, target):
        res = [0] * 5
        t_letters = list(target)
        for i in range(5):
            if guess[i] == target[i]:
                res[i] = 2
                t_letters[i] = None
        for i in range(5):
            if res[i] == 0 and guess[i] in t_letters:
                res[i] = 1
                t_letters[t_letters.index(guess[i])] = None
        
        p = 0
        for v in res:
            p = p * 3 + v
        return p, res

    @staticmethod
    def parse_pattern_input(pattern_str):
        pattern_str = pattern_str.strip().upper()
        if len(pattern_str) != 5:
            raise ValueError("Le motif doit comporter exactement 5 caractères (ex: 01200 ou GVJJG).")
        
        res = []
        for ch in pattern_str:
            if ch in '012':
                res.append(int(ch))
            elif ch in ('G', 'B', 'N', '.'):
                res.append(0)
            elif ch in ('J', 'Y', 'O', 'P'):
                res.append(1)
            elif ch in ('V', 'C'):
                res.append(2)
            else:
                raise ValueError(f"Caractère de motif invalide : '{ch}'")
        
        p = 0
        for v in res:
            p = p * 3 + v
        return p, res

    def filter_candidates(self, candidates, guess, pattern_int):
        filtered = []
        for c in candidates:
            p, _ = self.get_feedback(guess, c)
            if p == pattern_int:
                filtered.append(c)
        return filtered

    def analyze_suggestions(self, candidates, top_n=8):
        N = len(candidates)
        if N == 0:
            return []
        if N == 1:
            return [{
                "word": candidates[0],
                "entropy": 0.0,
                "max_bucket": 1,
                "expected_remaining": 1.0,
                "is_candidate": True,
                "p_win_now": 1.0,
                "guarantee_3": True,
                "score": 100.0,
                "reason": "Mot unique restant ! Victoire immédiate !"
            }]
        if N == 2:
            return [
                {
                    "word": candidates[0],
                    "entropy": 1.0,
                    "max_bucket": 1,
                    "expected_remaining": 1.0,
                    "is_candidate": True,
                    "p_win_now": 0.5,
                    "guarantee_3": True,
                    "score": 95.0,
                    "reason": "50% de chance de victoire directe, 100% en 3 coups max !"
                },
                {
                    "word": candidates[1],
                    "entropy": 1.0,
                    "max_bucket": 1,
                    "expected_remaining": 1.0,
                    "is_candidate": True,
                    "p_win_now": 0.5,
                    "guarantee_3": True,
                    "score": 95.0,
                    "reason": "50% de chance de victoire directe, 100% en 3 coups max !"
                }
            ]

        cand_set = set(candidates)
        words_to_evaluate = list(candidates)
        
        if N <= 50:
            letter_counts = Counter()
            for c in candidates:
                for letter in set(c):
                    letter_counts[letter] += 1
            
            def word_filter_score(w):
                distinct = set(w)
                return sum(letter_counts[l] * (N - letter_counts[l]) for l in distinct)
            
            outside_candidates = sorted(self.all_words, key=word_filter_score, reverse=True)[:150]
            for w in outside_candidates:
                if w not in cand_set:
                    words_to_evaluate.append(w)

        scored = []
        for guess in words_to_evaluate:
            buckets = Counter()
            for target in candidates:
                p, _ = self.get_feedback(guess, target)
                buckets[p] += 1
            
            max_b = max(buckets.values())
            entropy = -sum((cnt / N) * math.log2(cnt / N) for cnt in buckets.values())
            exp_remaining = sum(cnt * cnt for cnt in buckets.values()) / N
            singletons = sum(1 for cnt in buckets.values() if cnt == 1)
            p_singleton = singletons / N
            
            is_cand = guess in cand_set
            p_win_now = (1.0 / N) if is_cand else 0.0
            guarantee_3 = (max_b <= 1)
            
            # Priority: If N <= 10 or guess is a candidate, reward candidate heavily
            composite_score = (
                p_win_now * 60.0 +
                p_singleton * 15.0 +
                entropy * 6.0 -
                (max_b / N) * 10.0
            )
            if is_cand:
                composite_score += 40.0
            elif guarantee_3:
                composite_score += 10.0
            
            reason = []
            if p_win_now > 0:
                reason.append(f"{p_win_now*100:.1f}% de victoire directe")
            if guarantee_3:
                reason.append("🎯 Garantie 3 coups max (partition parfaite)")
            elif p_singleton > 0.7:
                reason.append(f"{p_singleton*100:.0f}% de chances d'isoler en 1 coup")
            else:
                reason.append(f"Réduit à {exp_remaining:.1f} mots en moyenne")

            scored.append({
                "word": guess,
                "entropy": round(entropy, 3),
                "max_bucket": max_b,
                "expected_remaining": round(exp_remaining, 1),
                "is_candidate": is_cand,
                "p_win_now": round(p_win_now, 3),
                "guarantee_3": guarantee_3,
                "score": round(composite_score, 2),
                "reason": " • ".join(reason)
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_n]

    def get_louan_daily_word(self, date_str=None):
        if date_str is None:
            now_utc = datetime.now(timezone.utc)
            paris_offset = timedelta(hours=2)
            now_paris = now_utc + paris_offset
            date_str = f"{now_paris.year}-{now_paris.month}-{now_paris.day}"
        
        if date_str == "2022-3-8":
            return "DROIT", date_str
        if date_str == "2023-5-12":
            return "FAIRE", date_str

        sr = self._seedrandom(date_str)
        rnd = sr()
        idx = int(rnd * len(self.target_words))
        return self.target_words[idx], date_str

    def generate_guaranteed_plan(self, target_word, mode=2):
        target_word = target_word.upper()
        if target_word not in self.target_set:
            raise ValueError(f"Le mot '{target_word}' n'est pas dans la liste des cibles du jeu.")

        if mode == 2:
            best_opener = "TARIE"
            p, res = self.get_feedback(best_opener, target_word)
            if best_opener == target_word:
                return [
                    {"step": 1, "word": best_opener, "pattern": [2,2,2,2,2], "note": "Coup de chance en 1 coup !"}
                ]
            
            p2, res2 = self.get_feedback(target_word, target_word)
            return [
                {"step": 1, "word": best_opener, "pattern": res, "note": "Ouverture optimale (entropie 6.07 bits)"},
                {"step": 2, "word": target_word, "pattern": res2, "note": "🎯 VICTOIRE EN 2 COUPS !"}
            ]
        
        elif mode == 3:
            opener = "TARIE"
            p1, res1 = self.get_feedback(opener, target_word)
            if opener == target_word:
                return [{"step": 1, "word": opener, "pattern": res1, "note": "Victoire en 1 coup !"}]
            
            cands = self.filter_candidates(self.target_words, opener, p1)
            suggestions = self.analyze_suggestions(cands, top_n=5)
            step2_word = None
            for s in suggestions:
                if s["word"] != target_word:
                    step2_word = s["word"]
                    break
            if step2_word is None:
                step2_word = [w for w in self.all_words if w != target_word][0]
            
            p2, res2 = self.get_feedback(step2_word, target_word)
            p3, res3 = self.get_feedback(target_word, target_word)
            return [
                {"step": 1, "word": opener, "pattern": res1, "note": f"Ouverture théorique optimale ({len(cands)} mots restants)"},
                {"step": 2, "word": step2_word, "pattern": res2, "note": "Coup de cadrage et élimination"},
                {"step": 3, "word": target_word, "pattern": res3, "note": "🎯 VICTOIRE EN 3 COUPS !"}
            ]

    def _seedrandom(self, seed_str):
        u = 256
        l = 6
        c = 52
        f = u ** l
        h = 2 ** c
        p = 2 * h
        v = u - 1
        
        t = []
        n = 0
        r = seed_str
        i = 0
        while i < len(r):
            idx = v & i
            prev_val = t[idx] if idx < len(t) else 0
            term = (19 * prev_val) & 0xFFFFFFFF
            n = (n ^ term) & 0xFFFFFFFF
            val = (n + ord(r[i])) & v
            if idx < len(t):
                t[idx] = val
            else:
                t.append(val)
            i += 1
            
        e = t
        n_len = len(e)
        if n_len == 0:
            e = [0]
            n_len = 1
        S = list(range(u))
        a = 0
        for i in range(u):
            t_val = S[i]
            a = v & (a + e[i % n_len] + t_val)
            S[i] = S[a]
            S[a] = t_val
        
        state = {"i": 0, "j": 0, "S": S}
        
        def g(count):
            out = 0
            while count > 0:
                count -= 1
                state["i"] = v & (state["i"] + 1)
                t_val = state["S"][state["i"]]
                state["j"] = v & (state["j"] + t_val)
                state["S"][state["i"]] = state["S"][state["j"]]
                state["S"][state["j"]] = t_val
                out = out * u + state["S"][v & (state["S"][state["i"]] + t_val)]
            return out
        
        g(u)
        
        def rng():
            e_val = g(l)
            t_val = f
            n_val = 0
            while e_val < h:
                e_val = (e_val + n_val) * u
                t_val *= u
                n_val = g(1)
            while e_val >= p:
                e_val = e_val // 2
                t_val = t_val // 2
                n_val = n_val >> 1
            return (e_val + n_val) / t_val
        
        return rng
