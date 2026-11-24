"""
app/crop_machinery_service.py — Core agronomic decision engine for Phase B:
1. Dynamic microclimate alternative crop suggestion engine.
2. Plot-size calibrated machinery and tool allocation (smallholder, medium, commercial).
3. Chronological 5-stage cultivation lifecycle timeline.
"""

from typing import Any

ALTERNATIVE_CROP_RULES: dict[str, dict[str, Any]] = {
    "wheat": {
        "condition": lambda rain, et0: rain < 25 or et0 > 4.0,
        "suggested_crop": "mustard",
        "water_saving_pct": 58,
        "profit_diff_inr_ha": 18500.0,
        "reason_hi": "इस क्षेत्र में शुष्क मौसम और कम पानी के पूर्वानुमान के अनुसार, गेहूं की जगह सरसों (Mustard) लगाना 58% पानी बचाएगा और ₹18,500/हेक्टेयर तक अतिरिक्त मुनाफा देगा।",
        "reason_en": "Given dry seasonal forecasts and water conservation targets, planting Mustard instead of Wheat saves 58% irrigation water and delivers up to +₹18,500/Ha extra net margin.",
    },
    "rice": {
        "condition": lambda rain, et0: rain < 40 or et0 > 4.5,
        "suggested_crop": "maize",
        "water_saving_pct": 65,
        "profit_diff_inr_ha": 14200.0,
        "reason_hi": "कम वर्षा या गिरते भूजल स्तर में धान की तुलना में मक्का (Maize) 65% कम पानी लेता है और खरीफ/रबी में बेहतर मूल्य स्थिरता प्रदान करता है।",
        "reason_en": "Under water-stress and low rainfall indicators, Maize requires 65% less water than Paddy Rice while providing strong market price stability.",
    },
    "sugarcane": {
        "condition": lambda rain, et0: rain < 35,
        "suggested_crop": "mustard",
        "water_saving_pct": 72,
        "profit_diff_inr_ha": 22000.0,
        "reason_hi": "गन्ने की 12 महीने की लंबी जल खपत के मुकाबले दलहन/तिलहन चक्र मिट्टी की उर्वरता लौटाता है और भूजल रीचार्ज में मदद करता है।",
        "reason_en": "Compared to high water-intensity 12-month Sugarcane, an oilseed/pulse rotation restores soil fertility and cuts irrigation burden by 72%.",
    },
}


def evaluate_alternative_crop(
    crop: str, area_ha: float, rain_prob_48h_pct: int = 15, et0_fao_mm_day: float = 4.0, language: str = "hi"
) -> dict[str, Any]:
    """
    Evaluates whether an alternative crop yields superior water efficiency
    or margin under prevailing microclimate conditions.
    """
    crop_lower = crop.lower()
    rule = ALTERNATIVE_CROP_RULES.get(crop_lower)

    if rule and rule["condition"](rain_prob_48h_pct, et0_fao_mm_day):
        is_hi = language == "hi"
        return {
            "has_alternative": True,
            "original_crop": crop_lower,
            "suggested_crop": rule["suggested_crop"],
            "water_saving_pct": rule["water_saving_pct"],
            "profit_difference_inr_ha": rule["profit_diff_inr_ha"],
            "total_extra_profit_inr": round(rule["profit_diff_inr_ha"] * area_ha, 2),
            "reason": rule["reason_hi"] if is_hi else rule["reason_en"],
        }

    is_hi = language == "hi"
    return {
        "has_alternative": False,
        "original_crop": crop_lower,
        "suggested_crop": crop_lower,
        "water_saving_pct": 0,
        "profit_difference_inr_ha": 0.0,
        "total_extra_profit_inr": 0.0,
        "reason": "चयनित फसल वर्तमान स्थानीय मौसम और मिट्टी के पूर्ण अनुकूल है।"
        if is_hi
        else "Selected crop is well-adapted to current local microclimate and soil.",
    }


def get_plot_scaled_machinery_plan(area_ha: float, language: str = "hi") -> dict[str, Any]:
    """
    Allocates realistic farm machinery tailored to physical acreage:
    - Smallholder: < 0.5 Ha (< 2 Bigha)
    - Medium: 0.5 to 2.5 Ha (2 to 10 Bigha)
    - Commercial: > 2.5 Ha (> 10 Bigha)
    """
    is_hi = language == "hi"

    if area_ha < 0.5:
        tier = "smallholder"
        tier_title = "छोटे किसान (रकबा < 2 बीघा)" if is_hi else "Smallholder Plot (< 2 Bigha / < 0.5 Ha)"
        desc = (
            "किराए के भारी ट्रैक्टर के अनावश्यक खर्च से बचें; हस्तचालित व देशी औजारों से लागत न्यूनतम रखें।"
            if is_hi
            else "Avoid heavy tractor rental debt; maximize margins with manual and animal-drawn implements."
        )
        tools = [
            {
                "name": "देसी हल / बैल कल्टीवेटर" if is_hi else "Desi Plough / Bullock Cultivator",
                "role": "प्राथमिक जुताई व मिट्टी भुरभुरी करना" if is_hi else "Primary tillage and seedbed preparation",
                "hire_cost": "₹0 - ₹400/बीघा" if is_hi else "₹0 - ₹400/Bigha",
            },
            {
                "name": "हस्तचालित सिंगल-रो सीडर (Hand Seeder)" if is_hi else "Manual Single-Row Push Seeder",
                "role": "उचित दूरी व गहराई पर सटीक बीज बुवाई" if is_hi else "Uniform seed spacing and depth placement",
                "hire_cost": "₹150/दिन" if is_hi else "₹150/day",
            },
            {
                "name": "मैनुअल नैपसैक स्प्रेयर (16L)" if is_hi else "Manual Knapsack Sprayer (16 Litre)",
                "role": "कीट नियंत्रण व जीवामृत/नीमास्त्र छिड़काव" if is_hi else "Pest management and bio-input foliar spray",
                "hire_cost": "₹100/दिन" if is_hi else "₹100/day",
            },
            {
                "name": "हंसिया / दांती (Sickle Reaper)" if is_hi else "Serrated Hand Sickle / Hand Reaper",
                "role": "कटाई व बंडल बांधना" if is_hi else "Manual harvesting and field bundling",
                "hire_cost": "₹50/दिन" if is_hi else "₹50/day",
            },
        ]
    elif area_ha <= 2.5:
        tier = "medium"
        tier_title = "मध्यम किसान (रकबा 2 से 10 बीघा)" if is_hi else "Medium Farm Plot (2 to 10 Bigha / 0.5 to 2.5 Ha)"
        desc = (
            "पावर टिलर या 25 HP मिनी-ट्रैक्टर किराए पर लें; सीड-कम-फर्टिलाइजर ड्रिल से 25% खाद बचाएं।"
            if is_hi
            else "Rent 25 HP mini-tractor or power tiller; save 25% fertilizer using a Seed-cum-Fertilizer drill."
        )
        tools = [
            {
                "name": "पावर टिलर / 25 HP मिनी-ट्रैक्टर" if is_hi else "Power Tiller / 25 HP Mini-Tractor",
                "role": "तेज जुताई व पलेवा तैयारी" if is_hi else "Rapid secondary tillage and seedbed leveling",
                "hire_cost": "₹700 - ₹900/घंटा" if is_hi else "₹700 - ₹900/hr",
            },
            {
                "name": "सीड-कम-फर्टिलाइजर ड्रिल (9-टाइन)" if is_hi else "Seed-cum-Fertilizer Drill (9-Tyne)",
                "role": "बीज और डीएपी खाद को एक साथ सटीक गहराई पर डालना"
                if is_hi
                else "Simultaneous precision seed and basal fertilizer drilling",
                "hire_cost": "₹500/एकड़" if is_hi else "₹500/Acre",
            },
            {
                "name": "बैटरी-चालित बूम स्प्रेयर (Battery Sprayer)" if is_hi else "Battery-Operated Backpack Boom Sprayer",
                "role": "समान छिड़काव व कम शारीरिक श्रम" if is_hi else "Even foliar coverage with low physical fatigue",
                "hire_cost": "₹200/दिन" if is_hi else "₹200/day",
            },
            {
                "name": "ट्रैक्टर-चालित रीपर (Tractor Reaper Binder)" if is_hi else "Tractor-Drawn Reaper Binder",
                "role": "1 एकड़ की कटाई मात्र 1 घंटे में" if is_hi else "Cuts and bundles 1 Acre in under 1 hour",
                "hire_cost": "₹1,200/एकड़" if is_hi else "₹1,200/Acre",
            },
        ]
    else:
        tier = "commercial"
        tier_title = (
            "व्यावसायिक खेत (रकबा > 10 बीघा / > 2.5 हे.)" if is_hi else "Commercial Large Farm (> 10 Bigha / > 2.5 Ha)"
        )
        desc = (
            "45–55 HP ट्रैक्टर, लेजर लैंड लेवलर व कंबाइन हार्वेस्टर से समय व ईंधन की अधिकतम बचत।"
            if is_hi
            else "Deploy 45–55 HP Tractor with Laser Land Leveler and Combine Harvester with SMS for scale."
        )
        tools = [
            {
                "name": "लेजर लैंड लेवलर + 50 HP ट्रैक्टर" if is_hi else "Laser Land Leveler + 50 HP Tractor",
                "role": "खेत को शत-प्रतिशत समतल करना (30% सिंचाई पानी की बचत)"
                if is_hi
                else "Precision laser leveling (saves 30% irrigation water)",
                "hire_cost": "₹800/घंटा" if is_hi else "₹800/hr",
            },
            {
                "name": "रोटावेटर (Rotary Tiller / Rotavator)" if is_hi else "Tractor Rotavator (Rotary Tiller)",
                "role": "फसल अवशेषों को काटकर मिट्टी में मिलाना"
                if is_hi
                else "Single-pass residue pulverization into organic matter",
                "hire_cost": "₹1,000/घंटा" if is_hi else "₹1,000/hr",
            },
            {
                "name": "न्यूमेटिक प्रिसिजन प्लांटर / सुपर सीडर" if is_hi else "Pneumatic Precision Planter / Super Seeder",
                "role": "पराली जलाए बिना सीधी गेहूं/मक्का बुवाई"
                if is_hi
                else "Direct no-till drilling through standing crop residue",
                "hire_cost": "₹1,500/एकड़" if is_hi else "₹1,500/Acre",
            },
            {
                "name": "कंबाइन हार्वेस्टर संग एसएमएस (SMS Attach)"
                if is_hi
                else "Combine Harvester with Straw Management (SMS)",
                "role": "कटाई, गहाई व सफाई एक साथ"
                if is_hi
                else "Combined cutting, threshing, and uniform straw spreading",
                "hire_cost": "₹2,200/एकड़" if is_hi else "₹2,200/Acre",
            },
        ]

    return {"tier": tier, "title": tier_title, "description": desc, "tools": tools}


def get_cultivation_lifecycle_stages(crop: str, area_ha: float, language: str = "hi") -> list[dict[str, Any]]:
    """
    Provides a 5-stage chronological cultivation plan with exact days,
    actions, and tools.
    """
    is_hi = language == "hi"
    crop.lower()

    stages = [
        {
            "stage_num": 1,
            "title": "खेत तैयारी व बेसल खाद बुवाई" if is_hi else "Field Preparation & Basal Fertilization",
            "timeline": "दिन 0 (Day 0)" if is_hi else "Day 0",
            "activity": "2-3 गहरी जुताई करें। अनुशंसित डीएपी व पोटाश की 100% मात्रा बीज बुवाई से ठीक पहले डालें।"
            if is_hi
            else "Execute 2-3 deep tilling passes. Apply 100% recommended DAP & MOP right before sowing.",
            "tools": "देसी हल / रोटावेटर / सीड ड्रिल" if is_hi else "Plough / Rotavator / Seed Drill",
        },
        {
            "stage_num": 2,
            "title": "बीज उपचार व बुवाई" if is_hi else "Seed Treatment & Precision Sowing",
            "timeline": "दिन 1 से 3" if is_hi else "Days 1 to 3",
            "activity": "बीजामृत या ट्राइकोडर्मा (5g/kg) से बीज उपचार करें। 4-5 सेमी गहराई पर लाइन में बुवाई करें।"
            if is_hi
            else "Treat certified seed with Beejamrit/Trichoderma (5g/kg). Sow at 4-5 cm depth in rows.",
            "tools": "हस्तचालित सीडर / सीड-कम-फर्टिलाइजर ड्रिल" if is_hi else "Hand Seeder / Seed Drill",
        },
        {
            "stage_num": 3,
            "title": "प्रथम सिंचाई व यूरिया टॉप-ड्रेसिंग" if is_hi else "First Irrigation & Urea Top-Dress (CRI)",
            "timeline": "दिन 21 से 25" if is_hi else "Days 21 to 25",
            "activity": "क्राउन रूट (CRI) अवस्था पर पहली हल्की सिंचाई दें। मौसम साफ होने पर यूरिया की पहली 50% किस्त डालें।"
            if is_hi
            else "Deliver first light irrigation at CRI stage. Apply 50% Urea top-dress only under clear rain forecast.",
            "tools": "ट्यूबवेल / स्प्रिंकलर / यूरिया ब्रॉडकास्टर" if is_hi else "Tubewell / Sprinkler / Broadcaster",
        },
        {
            "stage_num": 4,
            "title": "फूल व दाना भराव अवस्था" if is_hi else "Flowering & Grain Filling Stage",
            "timeline": "दिन 65 से 75" if is_hi else "Days 65 to 75",
            "activity": "खेत में नमी बनाए रखें। 0.5% जिंक सल्फेट या 19:19:19 घुलनशील पर्णीय छिड़काव करें।"
            if is_hi
            else "Maintain critical root moisture. Spray 0.5% Zinc Sulphate or 19:19:19 foliar spray.",
            "tools": "नैपसैक स्प्रेयर / बूम स्प्रेयर" if is_hi else "Knapsack / Boom Sprayer",
        },
        {
            "stage_num": 5,
            "title": "परिपक्वता व कटाई-गहाई" if is_hi else "Crop Maturity & Mechanical Harvest",
            "timeline": "दिन 110 से 130" if is_hi else "Days 110 to 130",
            "activity": "जब दाने में नमी 14-16% रह जाए तब कटाई करें। गहाई के बाद अनाज को धूप में सुखाकर <12% नमी पर सुरक्षित भंडार करें।"
            if is_hi
            else "Harvest when grain moisture drops to 14-16%. Sun-dry to <12% moisture before hermetic storage.",
            "tools": "हंसिया / रीपर बाइंडर / कंबाइन हार्वेस्टर" if is_hi else "Sickle / Reaper Binder / Combine Harvester",
        },
    ]

    return stages
