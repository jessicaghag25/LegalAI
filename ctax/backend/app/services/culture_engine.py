from app.schemas.tax import CelebrationPacket, FamilyHubCreate, SupportedLanguage

THEMES = {
    "south_asian": {"animation": "diwali_sparkles", "icons": ["diyas", "stars", "books"]},
    "east_asian": {"animation": "lantern_glow", "icons": ["lanterns", "coins", "scrolls"]},
    "muslim": {"animation": "crescent_stars", "icons": ["crescent", "stars", "moon"]},
    "global": {"animation": "confetti_stars", "icons": ["stars", "badges", "coins"]},
}

MESSAGES: dict[SupportedLanguage, str] = {
    "en": "Great teamwork! Your family unlocked a new inclusive achievement.",
    "fr": "Excellent travail d'équipe! Votre famille a débloqué une nouvelle réussite inclusive.",
    "pa": "ਸ਼ਾਨਦਾਰ ਟੀਮਵਰਕ! ਤੁਹਾਡੇ ਪਰਿਵਾਰ ਨੇ ਇਕ ਨਵੀਂ ਸਮੇਤਕ ਉਪਲਬਧੀ ਹਾਸਲ ਕੀਤੀ ਹੈ।",
    "hi": "बहुत बढ़िया टीमवर्क! आपके परिवार ने एक नया समावेशी अचीवमेंट अनलॉक किया है।",
    "es": "¡Excelente trabajo en equipo! Su familia desbloqueó un nuevo logro inclusivo.",
    "tl": "Mahusay na teamwork! Na-unlock ng pamilya ninyo ang bagong inclusive na achievement.",
    "sw": "Hongereni kwa ushirikiano! Familia yako imefungua mafanikio mapya jumuishi.",
    "ti": "ብሉጽ ስራሕ ጉጅለ! ስድራኹም ሓድሽ ኣካታቲ ሽልማት ከፊቱ።",
}


def _theme_for(hub: FamilyHubCreate) -> dict[str, list[str] | str]:
    tags = {tag for member in hub.members for tag in member.culture.culture_tags}
    religions = {tag for member in hub.members for tag in member.culture.religion_tags}

    if "south_asian" in tags:
        return THEMES["south_asian"]
    if "east_asian" in tags:
        return THEMES["east_asian"]
    if "islam" in religions or "muslim" in religions:
        return THEMES["muslim"]
    return THEMES["global"]


def build_celebration_packet(hub: FamilyHubCreate, member_id: str) -> CelebrationPacket:
    member = next((m for m in hub.members if m.member_id == member_id), None)
    if not member:
        lang: SupportedLanguage = hub.preferred_language
    else:
        lang = member.preferred_language

    theme = _theme_for(hub)
    return CelebrationPacket(
        member_id=member_id,
        language=lang,
        animation_theme=str(theme["animation"]),
        icon_set=list(theme["icons"]),
        localized_message=MESSAGES.get(lang, MESSAGES["en"]),
    )


def culturally_respectful_tip(region: str, language: SupportedLanguage) -> str:
    base = {
        "en": "Review prior-year deductions respectfully with each family member before confirming claims.",
        "fr": "Passez en revue les déductions de l'année précédente avec respect avant de confirmer les demandes.",
        "pa": "ਦਾਅਵੇ ਫਾਈਨਲ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ ਪਿਛਲੇ ਸਾਲ ਦੀਆਂ ਕਟੌਤੀਆਂ ਹਰ ਪਰਿਵਾਰਕ ਮੈਂਬਰ ਨਾਲ ਆਦਰ ਨਾਲ ਵੇਖੋ।",
        "hi": "दावे अंतिम करने से पहले पिछले साल की कटौतियों को हर परिवार सदस्य के साथ सम्मानपूर्वक देखें।",
        "es": "Revise las deducciones del año anterior con respeto junto a cada integrante de la familia.",
        "tl": "Suriin nang may paggalang ang mga deduction noong nakaraang taon kasama ang bawat miyembro ng pamilya.",
        "sw": "Pitia kwa heshima makato ya mwaka uliopita pamoja na kila mwanafamilia kabla ya kuthibitisha madai.",
        "ti": "ቅድሚ ምርግጋጽ ጥራይ ዓመት ዝሓለፈ ቅናሽ ምስ ኩሎም ኣባላት ስድራ ብኽብሪ መርምሩ።",
    }
    locale_addon = " CRA/IRS specific documents may vary by region."
    return base.get(language, base["en"]) + locale_addon + f" [{region}]"
