import requests
import time
from functools import lru_cache

BASE = "https://pokeapi.co/api/v2"

@lru_cache(maxsize=None)
def get_json(url: str):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[ERROR] Falló request a {url}")
        print(f"[ERROR] {type(e).__name__}: {e}")
        raise

@lru_cache(maxsize=None)
def default_pokemon_for_species(species_name: str) -> str:
    """
    Convierte una especie (pokemon-species) al 'pokemon' default (variety) que acepta /pokemon/{name}.
    Evita 404 como /pokemon/deoxys/ (debe ser deoxys-normal).
    """
    data = get_json(f"{BASE}/pokemon-species/{species_name}/")
    for v in data.get("varieties", []):
        if v.get("is_default"):
            return v["pokemon"]["name"]
    return data["varieties"][0]["pokemon"]["name"]

def species_for_generations(gen_ids):
    out = set()
    for gid in gen_ids:
        data = get_json(f"{BASE}/generation/{gid}/")
        out.update(s["name"] for s in data["pokemon_species"])
    return sorted(out)

def build_game_list(vg_name: str, gen_cut_ids, hm_moves_for_this_game, sleep_s=0.15, verbose=True):
    pool_species = species_for_generations(gen_cut_ids)
    hm_moves_for_this_game = list(hm_moves_for_this_game)

    if verbose:
        print(f"\n=== {vg_name.upper()} | pool gens {gen_cut_ids} ===")
        print(f"HM esperados: {hm_moves_for_this_game}")
        print(f"[INFO] Pool especies: {len(pool_species)}")

    machine_moves_in_game = set()
    per_species_machine_moves = {}  # species -> set(moves machine en ese vg)

    for i, species in enumerate(pool_species, start=1):
        try:
            time.sleep(sleep_s)

            pokemon_name = default_pokemon_for_species(species)

            # Log de mapeo (limitado para no spamear)
            if verbose and pokemon_name != species and i <= 30:
                print(f"[MAP] species '{species}' -> pokemon '{pokemon_name}'")

            p = get_json(f"{BASE}/pokemon/{pokemon_name}/")

            learned = set()
            for mv in p["moves"]:
                move_name = mv["move"]["name"]
                for d in mv["version_group_details"]:
                    if (
                        d["version_group"]["name"] == vg_name
                        and d["move_learn_method"]["name"] == "machine"
                    ):
                        learned.add(move_name)
                        break

            per_species_machine_moves[species] = learned
            machine_moves_in_game.update(learned)

            if verbose and (i % 50 == 0):
                print(f"[PROG] {i}/{len(pool_species)} especies procesadas...")

        except requests.exceptions.HTTPError as e:
            print(f"[ERROR] HTTPError en juego '{vg_name}', species '{species}': {e}")
            continue
        except Exception as e:
            print(f"[ERROR] Error en juego '{vg_name}', species '{species}': {type(e).__name__}: {e}")
            continue

    # Regla tuya: ignorar HM inexistentes en este juego/pool
    required_effective = [m for m in hm_moves_for_this_game if m in machine_moves_in_game]
    ignored = [m for m in hm_moves_for_this_game if m not in machine_moves_in_game]
    required_set = set(required_effective)

    winners = [sp for sp in pool_species if required_set.issubset(per_species_machine_moves.get(sp, set()))]
    with open(f"{vg}.csv", "w", encoding="utf-8") as f:
        f.write("pokemon\n")
        for p in winners:
            f.write(f"{p}\n")


    print(f"HM exigidos:  {required_effective}")
    if ignored:
        print(f"HM ignorados (no existen como machine en este juego/pool): {ignored}")
    print(f"Ganadores ({len(winners)}):")
    print(", ".join(winners) if winners else "(ninguno)")

    return winners, required_effective, ignored

# =========================
# HM por “familia” de juegos
# =========================
GEN1_HMS = ["cut", "surf", "strength"]
GEN2_HMS = ["cut", "surf", "strength", "waterfall", "whirlpool"]
GEN3_RSE_HMS = ["surf", "strength", "rock-smash", "waterfall", "dive"]           # Ruby/Sapphire/Emerald
GEN3_FRLG_HMS = ["cut", "surf", "strength", "rock-smash", "waterfall"]           # FireRed/LeafGreen

# =========================
# Juegos (version_groups), pools y HM específicos
# =========================
GAMES = [
    ("red-blue",          [1],       GEN1_HMS),
    ("yellow",            [1],       GEN1_HMS),

    ("gold-silver",       [1, 2],    GEN2_HMS),
    ("crystal",           [1, 2],    GEN2_HMS),

    ("ruby-sapphire",     [1, 2, 3], GEN3_RSE_HMS),
    ("emerald",           [1, 2, 3], GEN3_RSE_HMS),

    # Ajuste que pediste:
    ("firered-leafgreen", [1, 2, 3], GEN3_FRLG_HMS),
]

results = {}

print("\n===== INICIO DEL CHEQUEO DE HM =====")

for vg, gens_pool, hm_list in GAMES:
    winners, required_effective, ignored = build_game_list(
        vg_name=vg,
        gen_cut_ids=gens_pool,
        hm_moves_for_this_game=hm_list,
        sleep_s=0.15,   # subí si ves 429
        verbose=True
    )
    results[vg] = winners

print("\n===== FIN DEL PROCESO =====")