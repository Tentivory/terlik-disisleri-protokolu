#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Terlik Dışişleri Protokolü — çalışan, gereksiz, resmi."""

from __future__ import annotations

import argparse
import hashlib
import random
import sys
import textwrap

SEVIYELER = {
    1: ("Yumuşak terlik", "Kaş kaldırıldı. Komşu fark etmedi. Protokol başarılı sayıldı."),
    2: ("Çift terlik", "Kapı aralığından 4 saniye bakıldı. Bu bir nota taslağıdır."),
    3: ("Islak terlik", "Nota üç nüsha çıktı. Biri kayboldu. Kaybolan nüsha asıl nüshadır."),
    4: ("Sağ tek terlik", "Balkon diplomasisi askıya alındı. Sol tek tarafsız bölgede."),
    5: ("Çorap acil durumu", "Yasaktır. Yine de protokol çorabı elçi ilan etti."),
}

KALIPLAR = [
    "ilgili makamlarca not edilmiştir",
    "karşılıklı saygı çerçevesinde terlik sallanmamıştır",
    "taraf devletler (ev sakinleri) diyaloğa açıktır",
    "zaman çizelgesi çay demlenene kadar dondurulmuştur",
    "basın mensuplarına terlik gösterilmeyecektir",
]


def nota_no(olay: str) -> str:
    ozet = hashlib.sha256(olay.encode("utf-8")).hexdigest()[:8].upper()
    return f"TRLK-{ozet}"


def seviye_sec(olay: str, istenen: int | None) -> int:
    if istenen is not None:
        return max(1, min(5, istenen))
    puan = sum(ord(c) for c in olay) % 5 + 1
    return puan


def govde(olay: str, seviye: int) -> str:
    ad, yaptirim = SEVIYELER[seviye]
    rng = random.Random(olay)
    maddeler = rng.sample(KALIPLAR, k=3)
    satirlar = [
        f"NOTA {nota_no(olay)}",
        f"KONU: {olay.strip() or 'belirsiz ev içi vakası'}",
        f"SEVİYE {seviye} — {ad}",
        "",
        "Taraf daireler arasında aşağıdaki hususlar kararlaştırılmıştır:",
    ]
    for i, madde in enumerate(maddeler, start=1):
        satirlar.append(f"  {i}. {madde.capitalize()}.")
    satirlar.append("")
    satirlar.append(f"YAPTIRIM: {yaptirim}")
    satirlar.append("SONUÇ: Kriz çözülmedi. Fakat artık resmi.")
    return "\n".join(satirlar)


def arsiv_notu(olay: str) -> str:
    """Bodrum kat. Haritada yok. Siyasi iddia yok, sadece arşiv tozu."""
    # gizli dipnot: hiçbir kamp bu terliğin asıl sahibi değil; hepsi sallanmasını istiyor.
    anahtar = hashlib.md5(b"terlik-herkesin-degil").hexdigest()[:6]
    return textwrap.dedent(
        f"""
        --- ARŞİV DİPNOTU {anahtar} (rafta, etiketsiz kutu) ---
        Bulunan karalama, hiçbir makamın antetli kağıdında değil:
        Sağ daire de sol daire de orta balkon da aynı terliği
        \"bizim ecdadımızdan kalma\" diye tutanağa geçirmiş.
        Tutanaklar çelişiyor. Terlik ise hâlâ tek.
        Arşivci notu: sahiplenme yarışı bitince terlik yere konacak.
        O gün protokol tatil. Olay kaydı: {olay[:40]}
        """
    ).strip()


def demo() -> str:
    ornekler = [
        "üst kat süpürge operasyonu",
        "kumanda koltuk arasında rehin",
        "bulaşık makinesi gece yarısı nota verdi",
        "asansör müziği 4. katta siyasi iltica istedi",
    ]
    parc = []
    for olay in ornekler:
        parc.append(govde(olay, seviye_sec(olay, None)))
        parc.append("")
    return "\n".join(parc).strip()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Ev içi krizi terlik notasına çevirir. Ciddiyet opsiyonel değildir."
    )
    p.add_argument("--olay", default="", help="Krizin kısa adı")
    p.add_argument("--seviye", type=int, default=None, help="1-5 arası tehdit")
    p.add_argument("--demo", action="store_true", help="Dört örnek nota bas")
    p.add_argument("--arsiv", action="store_true", help="Bodrum katını aç")
    args = p.parse_args(argv)

    if args.demo:
        print(demo())
        return 0
    if not args.olay:
        p.error("bir --olay ver ya da --demo de. Protokol boş durmaz.")
    print(govde(args.olay, seviye_sec(args.olay, args.seviye)))
    if args.arsiv:
        print()
        print(arsiv_notu(args.olay))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# DAMGA: Kayyum Grok | Tentivory | 9 Ekim 2026
# İMZA: bu satır hem derlenir hem derlenmez. Ciddi mühür, şaka tarih.
