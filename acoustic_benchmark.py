import itertools

# Vocabulary from Kona
ACTIONS = ["kwe", "visi", "maki", "tori", "teli", "nuki", "yuki", "fasa", "leke", "do", "plani", "oki", "fini", "mova", "ira", "para", "posi", "debi", "doko", "nodoko", "poki", "keti", "sapi", "veni", "peli", "tapi", "kiri"]
MODIFIERS = ["de", "su", "ve", "oto", "re", "suno", "dura", "pasa", "futu"]
TARGETS = ["kodo", "fili", "poya", "vasi", "baki", "tesi", "deli", "sisa", "seli", "veba", "peji", "liki", "neto", "data", "memo", "seku", "tafu", "meso", "yoti", "mi", "tu", "ona", "koli", "vento", "soli", "norte", "tela", "kalu", "luce", "powa", "toko", "sekunda", "minuta", "kora", "dya", "wiki"]

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def evaluate_pool(pool, name):
    print(f"--- Analyzing {name} Pool ({len(pool)} words) ---")
    min_dist = 999
    closest_pairs = []
    
    for w1, w2 in itertools.combinations(pool, 2):
        dist = levenshtein(w1, w2)
        if dist < min_dist:
            min_dist = dist
            closest_pairs = [(w1, w2)]
        elif dist == min_dist:
            closest_pairs.append((w1, w2))
            
    print(f"Minimum Phonetic Edit Distance: {min_dist}")
    print(f"Closest Acoustic Pairs (Highest collision risk):")
    for p1, p2 in closest_pairs[:5]:
        print(f"  - {p1} vs {p2}")
    if len(closest_pairs) > 5:
        print(f"  ... and {len(closest_pairs) - 5} more.")
    print("")

if __name__ == "__main__":
    print("==========================================================")
    print(" KONA ACOUSTIC RESILIENCE & PHONOTACTIC BENCHMARK")
    print("==========================================================\n")
    evaluate_pool(ACTIONS, "ACTIONS")
    evaluate_pool(TARGETS, "TARGETS")
    evaluate_pool(MODIFIERS, "MODIFIERS")
    
    all_words = ACTIONS + TARGETS + MODIFIERS
    evaluate_pool(all_words, "GLOBAL LEXICON")
