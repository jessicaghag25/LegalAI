SUPPORTED_LANGUAGES = {
    "en": "English",
    "fr": "Français",
    "pa": "Punjabi",
    "hi": "Hindi",
    "es": "Español",
    "tl": "Tagalog",
    "sw": "Swahili",
    "ti": "Tigrinya",
}

LANGUAGE_DIALECT_HINTS = {
    "en": ["en-CA", "en-US"],
    "fr": ["fr-CA", "fr-FR"],
    "pa": ["pa-Guru", "pa-Arab"],
    "hi": ["hi-IN"],
    "es": ["es-MX", "es-ES"],
    "tl": ["tl-PH"],
    "sw": ["sw-KE", "sw-TZ"],
    "ti": ["ti-ER", "ti-ET"],
}

DISCLAIMERS = {
    "en": "CTax provides educational guidance and is not a substitute for professional tax advice.",
    "fr": "CTax offre des conseils éducatifs et ne remplace pas un avis fiscal professionnel.",
    "pa": "CTax ਸਿੱਖਿਆਤਮਕ ਮਦਦ ਦਿੰਦਾ ਹੈ ਅਤੇ ਪੇਸ਼ੇਵਰ ਟੈਕਸ ਸਲਾਹ ਦਾ ਬਦਲ ਨਹੀਂ ਹੈ।",
    "hi": "CTax शैक्षिक मार्गदर्शन प्रदान करता है और पेशेवर कर सलाह का विकल्प नहीं है।",
    "es": "CTax ofrece orientación educativa y no sustituye el asesoramiento fiscal profesional.",
    "tl": "Nagbibigay ang CTax ng gabay pang-edukasyon at hindi kapalit ng propesyonal na payo sa buwis.",
    "sw": "CTax hutoa mwongozo wa kielimu na si mbadala wa ushauri wa kitaalamu wa kodi.",
    "ti": "CTax ትምህርታዊ መምሪሒ ይህብ እንጂ ናይ ባለሙያ ግብሪ ምኽሪ መተካእታ ኣይኮነን።",
}

GLOSSARY = {
    "deduction": {
        "en": "An eligible expense that reduces taxable income.",
        "fr": "Une dépense admissible qui réduit le revenu imposable.",
    },
    "credit": {
        "en": "An amount that reduces tax owing directly.",
        "fr": "Un montant qui réduit directement l'impôt à payer.",
    },
    "carry_forward": {
        "en": "Unused credits or losses that may be claimed in future years.",
        "fr": "Crédits ou pertes inutilisés pouvant être reportés aux années futures.",
    },
}


def resolve_language(preferred: str | None) -> str:
    if preferred in SUPPORTED_LANGUAGES:
        return preferred
    return "en"


def tone_prefix(tone: str) -> str:
    mapping = {
        "formal": "Respectful",
        "informal": "Friendly",
        "kid_friendly": "Playful",
    }
    return mapping.get(tone, "Respectful")
