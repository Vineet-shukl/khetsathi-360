"""
app/organic_engine.py — Organic Farming Transition, Economics & Direct Supplier Route Engine.

Calculates:
  1. Complete Bio-Input Package replacing chemical DAP, Urea, and MOP
     (Vermicompost, Liquid Bio-NPK consortia, Jeevamrut, and Neem Cake).
  2. Economic Comparison: Conventional vs. Certified Organic:
     - 15% to 22% reduction in synthetic input costs
     - 20% to 30% certified organic price premium
     - Paramparagat Krishi Vikas Yojana (PKVY) ₹50,000/ha subsidy support
     - Net farmer profit and Return on Investment (ROI) delta.
  3. Verified Direct-to-Buyer, FPO & Certification Supplier Routes:
     - Jaivik Kheti Government Portal (jaivikkheti.in)
     - PGS-India (Participatory Guarantee System) Free Cluster Certification
     - APEDA Organic Mandi & Exporter Network
     - Local FPO Aggregation Clusters.
"""

from app.contracts import (
    CropId,
    OrganicAdvisoryResponse,
    OrganicEconomics,
    OrganicInputPlan,
    OrganicSupplierRoute,
)
from app.yield_model import INPUT_COST_PER_HA, MSP_TABLE, TYPICAL_YIELDS

# Bio-Input Requirements per Hectare by Crop
ORGANIC_INPUT_SPECS: dict[str, dict] = {
    "wheat": {
        "vermicompost_t_ha": 2.5,
        "bio_npk_l_ha": 2.0,
        "jeevamrut_l_ha": 500.0,
        "neem_cake_kg_ha": 250.0,
        "bio_control": "Trichoderma viride (seed treatment) + Pseudomonas fluorescens",
    },
    "rice": {
        "vermicompost_t_ha": 3.0,
        "bio_npk_l_ha": 2.5,
        "jeevamrut_l_ha": 600.0,
        "neem_cake_kg_ha": 300.0,
        "bio_control": "Azolla microphylla bio-cover + Neem oil spray (1500 ppm)",
    },
    "maize": {
        "vermicompost_t_ha": 2.5,
        "bio_npk_l_ha": 2.0,
        "jeevamrut_l_ha": 500.0,
        "neem_cake_kg_ha": 200.0,
        "bio_control": "Beauveria bassiana for Fall Armyworm defense",
    },
    "mustard": {
        "vermicompost_t_ha": 2.0,
        "bio_npk_l_ha": 1.5,
        "jeevamrut_l_ha": 400.0,
        "neem_cake_kg_ha": 200.0,
        "bio_control": "Yellow sticky traps + 5% Neem seed kernel extract (NSKE)",
    },
    "gram": {
        "vermicompost_t_ha": 1.5,
        "bio_npk_l_ha": 1.5,
        "jeevamrut_l_ha": 350.0,
        "neem_cake_kg_ha": 150.0,
        "bio_control": "Rhizobium leguminosarum + Trichoderma seed inoculation",
    },
    "sugarcane": {
        "vermicompost_t_ha": 5.0,
        "bio_npk_l_ha": 4.0,
        "jeevamrut_l_ha": 1000.0,
        "neem_cake_kg_ha": 500.0,
        "bio_control": "Trichogramma chilonis egg parasitoid + Trash mulching",
    },
}

# Verified Direct-to-Buyer & Government Supplier Routes
VERIFIED_SUPPLIER_ROUTES: list[OrganicSupplierRoute] = [
    OrganicSupplierRoute(
        channel_name="Jaivik Kheti Portal (जैविक खेती पोर्टल)",
        channel_type="Government Portal",
        url="https://www.jaivikkheti.in",
        contact_info="Toll Free: 1800-180-1551 / Ministry of Agriculture, GoI",
        benefit_description_hi="भारत सरकार का राष्ट्रीय जैविक ई-कॉमर्स मंच। बिना किसी बिचौलिए के सीधे पूरे देश के थोक खरीदारों, कंपनियों और उपभोक्ताओं को अपना जैविक अनाज बेचें।",
        benefit_description_en="Official Government of India organic direct selling portal. Connect directly with pan-India retail and wholesale buyers with zero middlemen commission.",
    ),
    OrganicSupplierRoute(
        channel_name="PGS-India (सहभागी प्रत्याभूति प्रणाली)",
        channel_type="Certification System",
        url="https://pgsindia-ncof.gov.in",
        contact_info="National Centre of Organic & Natural Farming (NCONF), Ghaziabad",
        benefit_description_hi="छोटे किसानों के लिए समूह आधारित निःशुल्क जैविक प्रमाणीकरण। 5 या अधिक किसानों का समूह बनाकर बिना किसी भारी फीस के 'Green' एवं 'Organic' प्रमाण पत्र पाएं।",
        benefit_description_en="Group-based free organic certification for smallholders. Form a local 5+ farmer cluster to receive authentic Green and Certified Organic seals without private agency fees.",
    ),
    OrganicSupplierRoute(
        channel_name="FPO Organic Aggregation Hubs (कृषक उत्पादक संगठन)",
        channel_type="FPO Cluster",
        url="https://sfacindia.com",
        contact_info="Small Farmers' Agri-Business Consortium (SFAC) / NABARD",
        benefit_description_hi="स्थानीय एफपीओ के माध्यम से जैविक उपज का एकमुश्त उठाव। पैकेजिंग, ग्रेडिंग और प्रीमियम जैविक ब्रांडों (Organic Mandya, 24 Mantra, BigBasket) को सीधी आपूर्ति।",
        benefit_description_en="Collective aggregation through local FPOs. Access grading, storage, and direct contract supply to major organic retail brands.",
    ),
    OrganicSupplierRoute(
        channel_name="APEDA National Programme for Organic Production (NPOP)",
        channel_type="Buyer Network",
        url="https://apeda.gov.in",
        contact_info="Agricultural and Processed Food Products Export Development Authority",
        benefit_description_hi="अंतरराष्ट्रीय निर्यात बाजार लिंक। बासमती चावल, सरसों व दालों के लिए 40% से 60% तक अधिक निर्यात मूल्य समर्थन।",
        benefit_description_en="International export linkage. High-value overseas trade channels for organic basmati, pulses, and spices yielding up to 40-60% export premiums.",
    ),
]


def calculate_organic_advisory(
    crop: CropId,
    area_ha: float = 1.0,
    current_conventional_profit: float = 0.0,
) -> OrganicAdvisoryResponse:
    """
    Computes bio-input schedule, comparative economics, and direct buyer routes.
    """
    spec = ORGANIC_INPUT_SPECS.get(crop, ORGANIC_INPUT_SPECS["wheat"])
    msp = MSP_TABLE.get(crop, 2275.0)
    base_yield = TYPICAL_YIELDS.get(crop, 3.5)
    conv_cost_ha = INPUT_COST_PER_HA.get(crop, 32500.0)

    # 1. Bio-Input Requirements
    vc_t = round(spec["vermicompost_t_ha"] * area_ha, 2)
    vc_bags = round((vc_t * 1000.0) / 50.0, 1)
    bio_npk_l = round(spec["bio_npk_l_ha"] * area_ha, 1)
    jeevamrut_l = round(spec["jeevamrut_l_ha"] * area_ha, 0)
    neem_cake_kg = round(spec["neem_cake_kg_ha"] * area_ha, 1)
    neem_cake_bags = round(neem_cake_kg / 50.0, 1)

    app_hi = [
        f"1. बुवाई पूर्व: खेत की अंतिम जुताई पर {vc_t} टन ({vc_bags} बोरी) वर्मीकम्पोस्ट और {neem_cake_kg} किलो नीम की खली समान रूप से फैलाकर मिट्टी में मिलाएं।",
        "2. बीज उपचार: बुवाई से पहले तरल बायो-एनपीके (Azotobacter/Rhizobium + PSB) के 500 मिलीलीटर से बीजों का उपचार कर छाया में सुखाएं।",
        f"3. खड़ी फसल में जीवामृत: पहली व दूसरी सिंचाई के पानी के साथ {jeevamrut_l} लीटर जीवामृत को बहाकर खेत में पहुंचाएं।",
        f"4. कीट नियंत्रण: रासायनिक कीटनाशकों के स्थान पर {spec['bio_control']} का प्रयोग करें।",
    ]

    app_en = [
        f"1. Basal Prep: Broadcast {vc_t} tonnes ({vc_bags} bags) of vermicompost and {neem_cake_kg} kg neem cake during final field prep.",
        "2. Seed Treatment: Inoculate seeds with liquid Bio-NPK consortia (500 ml) and shade dry before sowing.",
        f"3. Jeevamrut Irrigation: Apply {jeevamrut_l} litres of fermented Jeevamrut mixed through irrigation channels.",
        f"4. Plant Defense: Deploy {spec['bio_control']} for non-chemical pest suppression.",
    ]

    input_plan = OrganicInputPlan(
        vermicompost_tonnes=vc_t,
        vermicompost_bags_50kg=vc_bags,
        bio_npk_consortia_litres=bio_npk_l,
        jeevamrut_litres=jeevamrut_l,
        neem_cake_kg=neem_cake_kg,
        neem_cake_bags_50kg=neem_cake_bags,
        bio_control_agent=spec["bio_control"],
        application_guidelines_hi=app_hi,
        application_guidelines_en=app_en,
    )

    # 2. Comparative Economics (PKVY & Certified Organic Premium)
    conv_input_cost = round(conv_cost_ha * area_ha, 0)
    # Organic input cost is ~18% lower (on-farm composting and bio-culture vs expensive synthetic DAP/Urea/Pesticides)
    org_input_cost = round(conv_input_cost * 0.82, 0)
    input_savings = round(conv_input_cost - org_input_cost, 0)

    # Organic market premium: 25% average premium over standard MSP in direct/FPO markets
    org_premium_pct = 25.0
    org_price_per_q = round(msp * (1.0 + org_premium_pct / 100.0), 0)

    # Stabilized organic yield accounts for 6% lower volume but 25% higher price
    org_yield = round(base_yield * 0.94 * area_ha, 2)
    org_prod_q = org_yield * 10.0
    org_gross_revenue = round(org_prod_q * org_price_per_q, 0)

    # PKVY annual government incentive: ₹50,000 / 3 years = ₹16,666 / ha / year
    pkvy_annual = round(16666.0 * area_ha, 0)

    org_net_profit = round(org_gross_revenue - org_input_cost + pkvy_annual, 0)

    # Calculate conventional benchmark profit if not passed
    if current_conventional_profit <= 0:
        conv_prod_q = (base_yield * area_ha) * 10.0
        conv_rev = conv_prod_q * msp
        conv_profit = conv_rev - conv_input_cost
    else:
        conv_profit = current_conventional_profit

    net_increase = round(org_net_profit - conv_profit, 0)
    total_benefit = round(input_savings + net_increase, 0)

    economics = OrganicEconomics(
        crop=crop,
        area_ha=area_ha,
        conventional_input_cost_inr=conv_input_cost,
        organic_input_cost_inr=org_input_cost,
        input_cost_savings_inr=input_savings,
        organic_market_premium_pct=org_premium_pct,
        expected_organic_price_per_q_inr=org_price_per_q,
        conventional_net_profit_inr=round(conv_profit, 0),
        organic_net_profit_inr=org_net_profit,
        net_profit_increase_inr=net_increase,
        pkvy_annual_assistance_inr=pkvy_annual,
        total_farmer_benefit_inr=total_benefit,
    )

    conversion_timeline = [
        "वर्ष 1 (रूपांतरण काल): रासायनिक खाद में 50% कटौती, वर्मीकम्पोस्ट व हरी खाद की शुरुआत। PGS-India पर निःशुल्क क्लस्टर पंजीकरण।",
        "वर्ष 2 (स्थिरीकरण): रासायनिक खाद पूरी तरह बंद। मिट्टी में केंचुआ व सूक्ष्मजीव संख्या में 3 गुना वृद्धि। 'PGS-Green' प्रमाण पत्र प्राप्त।",
        "वर्ष 3 (प्रमाणित जैविक लाभ): पूर्ण जैविक उत्पादन। 'PGS-Organic' मुहर के साथ 25–35% प्रीमियम मूल्य पर बिक्री एवं PKVY अनुदान का पूरा लाभ।",
    ]

    return OrganicAdvisoryResponse(
        input_plan=input_plan,
        economics=economics,
        supplier_routes=VERIFIED_SUPPLIER_ROUTES,
        conversion_timeline=conversion_timeline,
    )
