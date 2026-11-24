"""
scripts/verify_bilingual_completeness.py
Authoritative verification test asserting 100% bilingual parity across:
1. frontend/index.html (Primary Root UI)
2. frontend/index_v1_legacy.html (Legacy UI)
3. frontend/future.html (Standalone Future Organic Hub)
"""

import re
import sys
from pathlib import Path


def test_file(filepath: Path):
    print("=" * 70)
    print(f"VERIFYING BILINGUAL COMPLETENESS: {filepath.name}")
    print("=" * 70)

    content = filepath.read_text(encoding="utf-8")
    errors = []

    # 1. Parse I18N blocks
    hi_match = re.search(r"hi:\s*\{(.*?)\n\s*\},", content, re.DOTALL)
    en_match = re.search(r"en:\s*\{(.*?)\n\s*\}", content, re.DOTALL)

    if not hi_match or not en_match:
        errors.append("Failed to locate I18N.hi or I18N.en dictionary.")
    else:
        # Extract keys defined as 'keyName: "..."'
        hi_keys = set(re.findall(r"^\s*([a-zA-Z0-9_]+)\s*:", hi_match.group(1), re.MULTILINE))
        en_keys = set(re.findall(r"^\s*([a-zA-Z0-9_]+)\s*:", en_match.group(1), re.MULTILINE))

        print(f"✓ Parsed I18N keys: hi={len(hi_keys)}, en={len(en_keys)}")
        diff_en = hi_keys - en_keys
        diff_hi = en_keys - hi_keys

        if diff_en:
            errors.append(f"Keys present in HI but missing in EN: {diff_en}")
        if diff_hi:
            errors.append(f"Keys present in EN but missing in HI: {diff_hi}")

    # 2. Check idMap / textMap target existence in DOM
    idmap_match = re.search(r"const (idMap|textMap) = \{(.*?)\};", content, re.DOTALL)
    if not idmap_match:
        errors.append("Could not find idMap or textMap object.")
    else:
        map_block = idmap_match.group(2)
        mapped_ids = re.findall(r'["\']([^"\']+)["\']:\s*dict\.([a-zA-Z0-9_]+)', map_block)
        print(f"✓ Mapped DOM elements: {len(mapped_ids)}")
        missing_ids = []
        for dom_id, prop in mapped_ids:
            if f'id="{dom_id}"' not in content and f"id='{dom_id}'" not in content:
                missing_ids.append((dom_id, prop))
        if missing_ids:
            errors.append(f"Mapped elements not found in HTML DOM: {missing_ids}")
        else:
            print("✓ All mapped elements exist in HTML DOM.")

    # 3. Check for any unmapped static Hindi nodes
    script_idx = content.find("<script")
    body_html = content[:script_idx] if script_idx != -1 else content
    tags = re.findall(r"<([a-z0-9]+)([^>]*)>([^<]+)</\1>", body_html, re.IGNORECASE)

    idmap_text = idmap_match.group(2) if idmap_match else ""
    dynamic_whitelist = {
        "geo-location-text",
        "converted-ha-pill",
        "ocr-status-text",
        "ocr-percent-text",
        "weather-loc-label",
        "weather-stat-line",
        "weather-guardrail-pill",
        "sat-vigor-title",
        "sat-ndvi-badge",
        "sat-ndvi-val-text",
        "sat-clay-text",
        "sat-density-text",
        "sat-cec-text",
        "sat-action-text",
        "conf-title",
        "out-dap-bags",
        "out-dap-sub",
        "out-urea-bags",
        "out-urea-sub",
        "out-mop-bags",
        "out-mop-sub",
        "irrigation-stage-pill",
        "org-net-gain-badge",
        "org-savings-val",
        "org-premium-val",
        "org-subsidy-val",
        "org-profit-val",
        "org-vc-bags",
        "org-bio-npk",
        "org-jeevamrut",
        "org-neem-cake",
        "shc-amendment-note",
        "assim-result",
        "slider-years-text",
        "chem-soc-val",
        "chem-cost-val",
        "chem-water-val",
        "chem-verdict",
        "org-soc-val",
        "org-worm-val",
        "org-water-val",
        "org-verdict",
        "jeev-dung",
        "jeev-urine",
        "jeev-jaggery",
        "jeev-flour",
        "jeev-water",
        "beej-dung",
        "beej-urine",
        "beej-milk",
        "beej-water",
        "neem-leaves",
        "neem-urine",
        "neem-dung",
        "neem-water",
        "eco-chem-total-cost",
        "eco-org-total-cost",
        "eco-org-mandi",
        "eco-org-net",
        "eco-extra-gain",
    }

    unmapped = []
    for tag_name, attrs, text in tags:
        text_clean = text.strip()
        if tag_name in ["title", "style"]:
            continue
        if re.search(r"[\u0900-\u097F]", text_clean) and len(text_clean) > 2:
            id_m = re.search(r'id=["\']([^"\']+)["\']', attrs)
            if not id_m:
                unmapped.append((tag_name, "NO_ID", text_clean))
            else:
                el_id = id_m.group(1)
                if el_id not in idmap_text and el_id not in dynamic_whitelist:
                    unmapped.append((tag_name, el_id, text_clean))

    if unmapped:
        errors.append(f"Unmapped static Hindi nodes remaining ({len(unmapped)}): {unmapped[:5]}")
    else:
        print("✓ Zero unmapped static Devanagari text nodes found in HTML body!")

    if errors:
        print(f"\n❌ FAILED with {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("\n✅ PASSED: 100% Bilingual Parity Confirmed!")
        return True


def main():
    root = Path(__file__).resolve().parent.parent
    files = [
        root / "frontend" / "index.html",
        root / "frontend" / "index_v1_legacy.html",
        root / "frontend" / "future.html",
    ]

    all_passed = True
    for f in files:
        if not f.exists():
            print(f"File not found: {f}")
            all_passed = False
            continue
        if not test_file(f):
            all_passed = False

    if not all_passed:
        print("\n💥 Bilingual parity test FAILED.")
        sys.exit(1)
    else:
        print("\n🎉 ALL 3 SURFACES PASSED 100% BILINGUAL VERIFICATION!")
        sys.exit(0)


if __name__ == "__main__":
    main()
