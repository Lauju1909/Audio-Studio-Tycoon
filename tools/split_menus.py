"""Zerlegt menus/<name>.py verbatim in ein Paket menus/<name>/<gruppe>.py.

Querverweise zwischen Menues (Klassen oeffnen einander ueber globale Namen) bleiben
erhalten: __init__ verlinkt alle Untermodule miteinander (link_namespaces).
Usage: python tools/split_menus.py business|gameplay
"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GROUPS = {
    "business": {
        "finance": ["SubscriptionServiceMenu", "BankMenu", "LoanMenu", "DonationMenu", "MonetizationMenu",
                    "SupportGiftCardTypeMenu", "GiftCardCodeInput", "StockMarketMenu",
                    "StockRivalDetailMenu", "SubscriptionVaultMenu", "CreatorSponsorshipMenu", "IPOMenu"],
        "live_services": ["ServiceMenu", "ContractWorkMenu", "GameServiceOptionsMenu", "AddMtxMenu",
                          "MovieDealMenu", "AntiCheatMenu", "MMOPaymentMenu", "MMOManagementMenu",
                          "MMOOptionsMenu", "StreamingPlatformMenu", "CloudGamingMenu", "MetaverseMenu",
                          "TransmediaMenu", "TransmediaDealMenu"],
        "products": ["LicenseShopMenu", "LicenseSelectMenu", "EngineLicensingMenu", "EngineLicenseFeeMenu",
                     "GamePortingMenu", "PortPlatformMenu", "AddonMenu", "AddonNameMenu", "BundleMenu",
                     "BundleNameMenu", "ProductionMenu", "ProductionAmountMenu", "PublisherDealsMenu",
                     "PublisherDealDetailsMenu", "MerchMenu", "MerchAmountMenu"],
        "corporate": ["EspionageMenu", "ESportsMenu", "ESportsCreateLeagueMenu", "ESportsManageLeagueMenu",
                      "ESportsChampionshipMenu", "ESportsSponsorMenu", "AcquisitionMenu",
                      "SubsidiaryManagementMenu"],
    },
    "gameplay": {
        "main": ["MainMenu", "CompanyNameMenu", "GameMenu", "CreditsMenu", "ShareholderMenu",
                 "DeveloperMenu", "ChartMenu", "ActiveGamesMenu", "GameDetailsMenu", "ReviewResultMenu",
                 "GOTYMenu"],
        "project_setup": ["CoDevPartnerMenu", "ProjectTypeMenu", "TopicMenu", "GenreMenu", "PlatformMenu",
                          "AudienceMenu", "GameSizeMenu", "EngineSelectMenu", "MarketingMenu",
                          "ProjectTeamSelectMenu", "GameNameMenu", "DevelopmentSliderMenu", "DRMChoiceMenu",
                          "CrowdfundingChoiceMenu", "DifficultyMenu", "SubGenreMenu", "SequelMenu",
                          "RemakeSelectMenu", "RemasterSelectMenu", "PublisherMenu"],
        "development": ["DevProgressMenu", "AAADevEventMenu", "InfluencerEventMenu", "UnionEventMenu",
                        "ExpoMenu"],
    },
}


def fix_rel(s):
    return re.sub(r"from \.(?!\.)", "from ..", s)


def main(name):
    src_path = ROOT / "menus" / f"{name}.py"
    text = src_path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
    lines = text.split("\n")
    tree = ast.parse(text)
    body = tree.body
    first_def = next(i for i, n in enumerate(body) if isinstance(n, (ast.ClassDef, ast.FunctionDef)))
    header_end = body[first_def].lineno - 1  # Zeilen davor = Header
    header_nodes = body[:first_def]
    assert all(isinstance(n, (ast.Import, ast.ImportFrom, ast.Assign, ast.Expr)) for n in header_nodes)
    header = fix_rel("\n".join(lines[:header_end]).rstrip())
    group_of = {c: g for g, cs in GROUPS[name].items() for c in cs}
    chunks = {g: [] for g in GROUPS[name]}
    prev_end = header_end
    for n in body[first_def:]:
        seg = lines[prev_end:n.end_lineno]
        prev_end = n.end_lineno
        if not isinstance(n, ast.ClassDef):
            raise SystemExit(f"unexpected top-level node {type(n).__name__} at {n.lineno}")
        if n.name not in group_of:
            raise SystemExit(f"unassigned class {n.name}")
        chunks[group_of[n.name]].append(fix_rel("\n".join(seg)).strip("\n"))
    pkg = ROOT / "menus" / name
    pkg.mkdir(exist_ok=True)
    for g, cs in chunks.items():
        (pkg / f"{g}.py").write_text(header + "\n\n\n" + "\n\n\n".join(cs) + "\n", encoding="utf-8", newline="\n")
    mods = list(GROUPS[name])
    init = f'"""Menues: {name} (aufgeteilt nach Themen)."""\nfrom .._linking import link_namespaces\n'
    init += "".join(f"from . import {m}\nfrom .{m} import *  # noqa: F401,F403\n" for m in mods)
    init += f"\nlink_namespaces([{', '.join(mods)}])\n"
    (pkg / "__init__.py").write_text(init, encoding="utf-8", newline="\n")
    src_path.unlink()
    print("ok", name)


if __name__ == "__main__":
    main(sys.argv[1])
