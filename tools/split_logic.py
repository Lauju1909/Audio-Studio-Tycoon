"""Verschiebt GameState-Methoden verbatim in systems/<domain>.py (Mixins).

Usage: python tools/split_logic.py <domain>
Kopiert Methodenquelltext 1:1, entfernt ihn aus logic.py, schreibt LF/UTF-8 ohne BOM.
"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DOMAINS = {
    "soundcon": ("SoundconMixin", "SoundCon, Soundtrack-Label, Radio und Jingles.", [
        "can_attend_soundcon", "book_soundcon_booth", "conduct_soundcon_qa",
        "conduct_soundcon_qa_interactive", "finish_soundcon", "found_soundtrack_label",
        "sign_radio_contract", "create_radio_jingle"]),
    "rivals": ("RivalsMixin", "Rivalen, Aktienmarkt der Rivalen und Branchennews.", [
        "_init_rivals", "_process_rivals", "get_share_price", "buy_shares", "sell_shares",
        "_generate_industry_news"]),
    "dev": ("DevMixin", "Entwicklungsprojekte: Spiele, Engines, Ports, Updates, Addons.", [
        "reset_draft", "estimate_dev_time", "start_development", "can_start_development",
        "start_crowdfunding_campaign", "start_port_project", "start_merch_campaign",
        "start_update_project", "start_manufacturing_job", "add_mtx_to_game", "buy_anti_cheat",
        "use_ai_assets", "use_ai_soundtrack", "release_patch", "release_dlc",
        "release_mmo_update", "create_addon", "create_bundle", "finalize_game",
        "finalize_engine", "start_engine_project", "create_engine", "_finish_update_project",
        "_process_port_projects", "generate_contract_work_options", "start_contract_work",
        "finish_contract_work"]),
    "scoring": ("ScoringMixin", "Hype, Review-, Verkaufs- und Entwicklungskosten-Berechnung.", [
        "calculate_hype", "calculate_review", "calculate_sales", "calculate_dev_cost",
        "get_current_charts"]),
    "events": ("EventsMixin", "Zufallsereignisse, Trends, Mails, Sponsoring, Turniere, Erfolge.", [
        "check_random_event", "apply_event", "trigger_personality_event",
        "answer_personality_event", "receive_fan_mail", "answer_fan_mail", "process_emails",
        "add_welcome_emails", "_check_goty", "_check_achievements", "update_trends",
        "generate_trend", "_process_sponsorships", "add_sponsorship", "_process_tournaments",
        "_process_esports_leagues", "toggle_exclusive_esports"]),
    "persistence": ("PersistenceMixin", "Speichern/Laden und globale Einstellungen.", [
        "save_game", "delete_save_game", "get_save_slots_info", "load_game",
        "load_global_settings", "save_global_settings"]),
    "finance": ("FinanceMixin", "Finanzen, Berichte, Abos, Streaming, Cloud, Podcasts.", [
        "track_income", "track_expense", "finalize_weekly_balance", "get_financial_report",
        "get_yearly_report", "_send_monthly_bank_statement", "delete_bank_statement",
        "get_financial_summary", "donate", "is_bankrupt", "_process_engine_licensing",
        "_process_cloud_gaming", "_process_audio_pass", "_process_podcast_network",
        "update_subscription_service", "found_streaming_platform",
        "upgrade_streaming_server", "_process_streaming_platform_monthly", "watch_ad"]),
    "research": ("ResearchMixin", "Forschung und freischaltbare Inhalte.", [
        "get_research_block_reason", "start_research", "complete_research",
        "get_researchable_features", "get_researchable_topics", "get_researchable_genres",
        "get_researchable_audiences", "get_researchable_technologies",
        "_unlock_historical_topics", "_init_starter_engine"]),
    "hardware": ("HardwareMixin", "Soundkarten-Hardware und Accessibility-Lab.", [
        "start_sound_card_project", "unlock_hardware_technology",
        "update_hardware_development", "release_sound_card", "get_accessibility_lab_actions",
        "get_accessibility_weekly_fans", "update_accessibility_reputation",
        "run_accessibility_lab_action"]),
    "team": ("TeamMixin", "Team-Boni, Training und Teambuilding.", [
        "_active_employees", "get_team_bonus", "get_team_slider_bonus",
        "get_team_speed_modifier", "get_team_bug_modifier", "get_team_quality_modifier",
        "train_employee", "start_training", "perform_teambuilding"]),
    "business": ("BusinessMixin", "Lizenzen, Publishing, Produktion, Server, Buero.", [
        "get_available_licenses", "buy_license", "generate_publisher_deals",
        "get_unused_licenses", "get_active_licenses", "use_license", "produce_physical_copies",
        "build_server_room", "expand_server_capacity", "apply_mmo_update",
        "_generate_publishing_offer", "accept_publishing_offer", "reject_publishing_offer",
        "build_presswerk", "expand_storage", "produce_copies", "can_upgrade_office",
        "upgrade_office", "get_office_info", "has_office_bonus", "place_office_item",
        "remove_office_item", "get_office_item", "place_office_room", "buy_office_furniture",
        "expand_office_grid"]),
}


def main(domain):
    cls, doc, names = DOMAINS[domain]
    logic = ROOT / "logic.py"
    text = logic.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
    lines = text.split("\n")
    tree = ast.parse(text)
    gs = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "GameState")
    methods = {n.name: n for n in gs.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    missing = [n for n in names if n not in methods]
    if missing:
        raise SystemExit(f"missing in GameState: {missing}")
    # Import-Block (Zeilen vor der Klasse, ohne Docstring und Mixin-Imports)
    header = []
    for ln in lines[: gs.lineno - 1]:
        if ln.startswith("from systems.") or ln.startswith('"""'):
            continue
        header.append(ln)
    start_idx = next(i for i, l in enumerate(header) if l.startswith(("import ", "from ")))
    header = header[start_idx:]
    # Docstring-Rest des Modul-Docstrings entfernen: header beginnt ab erstem import
    ranges = []
    for n in names:
        m = methods[n]
        start = min([m.lineno] + [d.lineno for d in m.decorator_list]) - 1
        while start > 0 and lines[start - 1].startswith("    #"):
            start -= 1
        ranges.append((start, m.end_lineno))
    chunks = ["\n".join(lines[s:e]) for s, e in sorted(ranges)]
    out = f'"""{doc} Mixin fuer GameState."""\n' + "\n".join(header).rstrip() + f"\n\n\nclass {cls}:\n"
    out += "\n\n".join(chunks) + "\n"
    (ROOT / "systems" / f"{domain}.py").write_text(out, encoding="utf-8", newline="\n")
    drop = set()
    for s, e in ranges:
        drop.update(range(s, e))
    new_lines = [l for i, l in enumerate(lines) if i not in drop]
    new_text = "\n".join(new_lines)
    new_text = re.sub(r"\n{4,}", "\n\n\n", new_text)
    # Mixin in Basisklassen eintragen
    new_text = new_text.replace(
        "class GameState(", "class GameState(", 1)
    m = re.search(r"class GameState\(([^)]*)\):", new_text)
    bases = [b.strip() for b in m.group(1).split(",")]
    bases.append(cls)
    new_text = new_text.replace(m.group(0), f"class GameState({', '.join(bases)}):", 1)
    new_text = new_text.replace(
        "from systems.hr import HRMixin",
        f"from systems.hr import HRMixin\nfrom systems.{domain} import {cls}", 1)
    logic.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"moved {len(names)} methods -> systems/{domain}.py")


if __name__ == "__main__":
    main(sys.argv[1])
