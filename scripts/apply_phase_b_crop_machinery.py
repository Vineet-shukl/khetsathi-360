"""
scripts/apply_phase_b_crop_machinery.py
Applies Phase B into frontend/index.html:
1. Floating Top-Right Alternate Crop Pop-up with minimize/expand/close actions.
2. Plot-Scaled Farm Machinery & 5-Stage Cultivation Lifecycle Card in Step 3.
3. 100% Bilingual parity in I18N.hi and I18N.en.
4. Reactive JS integration calling /api/v1/crop/alternative-and-machinery.
"""

from pathlib import Path
import re

def apply_phase_b():
    html_path = Path("frontend/index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Floating Top-Right Alternate Crop Pop-up HTML
    floating_popup_html = """
  <!-- Phase B: Floating Top-Right Smart Alternative Crop Pop-up -->
  <aside id="floating-crop-advisor" aria-label="वैकल्पिक फसल सुझाव" class="hidden fixed top-20 right-3 sm:right-6 z-40 w-[92vw] sm:w-[380px] rounded-2xl bg-white/95 backdrop-blur-md border-2 border-amber-400 shadow-2xl transition-all duration-300 transform">
    <div class="p-3.5 bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 rounded-t-2xl flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span class="text-xl" aria-hidden="true">💡</span>
        <div>
          <h4 id="lbl-alt-popup-title" class="text-xs font-black tracking-wide uppercase">वैकल्पिक फसल सुझाव</h4>
          <span id="alt-popup-badge" class="text-[10px] font-extrabold bg-white/90 text-amber-950 px-2 py-0.5 rounded-full inline-block">+₹18,500/हे. लाभ</span>
        </div>
      </div>
      <div class="flex items-center gap-1">
        <button id="btn-minimize-alt-popup" type="button" class="min-h-[36px] min-w-[36px] p-1.5 rounded-lg hover:bg-amber-400 font-black text-xs transition flex items-center justify-center" aria-label="छोटा करें">
          <span id="alt-min-icon">➖</span>
        </button>
        <button id="btn-close-alt-popup" type="button" class="min-h-[36px] min-w-[36px] p-1.5 rounded-lg hover:bg-amber-400 font-black text-xs transition flex items-center justify-center" aria-label="बंद करें">
          <span>✖️</span>
        </button>
      </div>
    </div>

    <div id="alt-popup-body" class="p-4 space-y-3 text-xs">
      <p id="alt-popup-reason" class="text-slate-800 leading-relaxed font-semibold">
        इस क्षेत्र में शुष्क मौसम और कम पानी के पूर्वानुमान के अनुसार, गेहूं की जगह सरसों (Mustard) लगाना 58% पानी बचाएगा और ₹18,500/हेक्टेयर तक अतिरिक्त मुनाफा देगा।
      </p>

      <div class="flex flex-col gap-2 pt-1">
        <button id="btn-apply-alt-crop" type="button" class="min-h-[44px] w-full px-3.5 py-2 bg-emerald-800 hover:bg-emerald-700 text-white font-extrabold rounded-xl shadow transition flex items-center justify-center gap-2">
          <span>🌾</span> <span id="lbl-apply-alt-crop">सरसों (Mustard) अपनाएं</span>
        </button>
        <button id="btn-view-machinery-plan" type="button" class="min-h-[44px] w-full px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold rounded-xl border border-slate-300 transition flex items-center justify-center gap-1.5">
          <span>🚜</span> <span id="lbl-view-machinery">औजार व खेती चक्र देखें</span>
        </button>
      </div>
    </div>
  </aside>
"""

    if "id=\"floating-crop-advisor\"" not in html:
        target_body = '<div id="toast-banner"'
        html = html.replace(target_body, floating_popup_html + "\n  " + target_body)
        print("1. Added Floating Crop Advisor Popup before toast banner")

    # 2. Machinery & Cultivation Lifecycle Card HTML in Step 3
    machinery_card_html = """
        <!-- Phase B: Plot-Scaled Machinery & 5-Stage Cultivation Lifecycle -->
        <div id="machinery-lifecycle-card" class="card p-5 border-2 border-emerald-600 bg-gradient-to-br from-slate-50 via-white to-emerald-50/30 space-y-5 shadow-md">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 pb-3">
            <div class="flex items-center gap-2.5">
              <span class="text-2xl" aria-hidden="true">🚜</span>
              <div>
                <span id="lbl-machinery-badge" class="text-[10px] sm:text-xs font-black uppercase tracking-wider text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-full inline-block">
                  खेत रकबा आधारित औजार योजना
                </span>
                <h4 id="lbl-machinery-title" class="text-sm sm:text-base font-black text-emerald-950">
                  खेत आकार अनुसार औजार व बुवाई-से-कटाई संपूर्ण चक्र
                </h4>
              </div>
            </div>
            <div class="text-left sm:text-right">
              <span id="machinery-tier-tag" class="text-xs font-black text-amber-950 bg-amber-100 px-3 py-1 rounded-xl border border-amber-300 shadow-2xs">
                मध्यम किसान (4 बीघा / 1.0 हे.)
              </span>
            </div>
          </div>

          <p id="machinery-desc" class="text-xs text-slate-700 leading-relaxed font-semibold">
            किराए के भारी ट्रैक्टर के अनावश्यक खर्च से बचें; अपने खेत के वास्तविक नाप के अनुसार सबसे किफायती औजार व किराया दरें।
          </p>

          <!-- 4 Plot-Scaled Machinery Tools Grid -->
          <div class="space-y-2">
            <h5 id="lbl-tools-heading" class="text-xs font-black uppercase tracking-wider text-slate-800 flex items-center gap-1.5">
              <span>🛠️</span> <span>अनुशंसित कृषि यंत्र व मानक किराया दरें (Recommended Implements)</span>
            </h5>
            <div id="machinery-tools-grid" class="grid grid-cols-1 sm:grid-cols-2 gap-3" aria-live="polite">
              <!-- Dynamically populated via renderMachineryPlan() -->
            </div>
          </div>

          <!-- 5-Stage Chronological Cultivation Lifecycle Timeline -->
          <div class="space-y-2 pt-2 border-t border-slate-200">
            <h5 id="lbl-lifecycle-heading" class="text-xs font-black uppercase tracking-wider text-emerald-950 flex items-center gap-1.5">
              <span>📅</span> <span>5-चरणीय बुवाई से कटाई समय-चक्र (Cultivation Stage Timeline)</span>
            </h5>
            <div id="lifecycle-stages-container" class="space-y-2.5" aria-live="polite">
              <!-- Dynamically populated via renderCultivationStages() -->
            </div>
          </div>
        </div>
"""

    if "id=\"machinery-lifecycle-card\"" not in html:
        target_step3_insert = '<!-- Chronological Step-by-Step Action Cards -->'
        html = html.replace(target_step3_insert, machinery_card_html + "\n        " + target_step3_insert)
        print("2. Added Machinery & Lifecycle Card in Step 3")

    # 3. Add I18N Keys to I18N.hi and I18N.en
    phase_b_hi = """        altPopupTitle: "वैकल्पिक फसल सुझाव",
        altViewMachinery: "औजार व खेती चक्र देखें",
        altApplyCrop: "यह फसल अपनाएं",
        machineryBadge: "खेत रकबा आधारित औजार योजना",
        machineryTitle: "खेत आकार अनुसार औजार व बुवाई-से-कटाई संपूर्ण चक्र",
        toolsHeading: "🛠️ अनुशंसित कृषि यंत्र व मानक किराया दरें",
        lifecycleHeading: "📅 5-चरणीय बुवाई से कटाई समय-चक्र",
"""

    phase_b_en = """        altPopupTitle: "Smart Alternate Crop Suggestion",
        altViewMachinery: "View Machinery & Timeline",
        altApplyCrop: "Switch to this Crop",
        machineryBadge: "Plot-Scaled Farm Tool Planning",
        machineryTitle: "Plot-Scaled Machinery & Sowing-to-Harvest Lifecycle",
        toolsHeading: "🛠️ Recommended Implements & Custom Hire Rates",
        lifecycleHeading: "📅 5-Stage Sowing-to-Harvest Timeline",
"""

    if "altPopupTitle" not in html:
        # In I18N.hi
        target_hi = 'mapOverlayTitle: "चयनित खेत स्थिति (Pinpoint)",'
        html = html.replace(target_hi, target_hi + "\n" + phase_b_hi)
        # In I18N.en
        target_en = 'mapOverlayTitle: "Selected Farm Position (Pinpoint)",'
        html = html.replace(target_en, target_en + "\n" + phase_b_en)
        print("3. Added Phase B dictionary keys to I18N.hi and I18N.en")

    # 4. Add setLanguage element bindings
    setlang_b_additions = """        "lbl-alt-popup-title": dict.altPopupTitle,
        "lbl-view-machinery": dict.altViewMachinery,
        "lbl-machinery-badge": dict.machineryBadge,
        "lbl-machinery-title": dict.machineryTitle,
        "lbl-tools-heading": dict.toolsHeading,
        "lbl-lifecycle-heading": dict.lifecycleHeading,"""

    if '"lbl-alt-popup-title"' not in html:
        target_setlang = '"map-overlay-title": dict.mapOverlayTitle,'
        html = html.replace(target_setlang, target_setlang + "\n" + setlang_b_additions)
        print("4. Added Phase B bindings to setLanguage")

    # 5. JavaScript Engine for Phase B
    js_phase_b = """
    // =========================================================================
    // PHASE B: DYNAMIC ALTERNATIVE CROP POP-UP & MACHINERY LIFECYCLE
    // =========================================================================
    let currentAlternativeData = null;
    let isAltPopupMinimized = false;

    async function updateAlternativeAndMachineryPlan() {
      const crop = selectedCrop || "wheat";
      const areaHa = parseFloat(getEl("plot-area")?.value) || 1.0;
      const unit = getEl("plot-unit")?.value || "bigha_pucca";
      const areaInHa = convertToHectares(areaHa, unit);
      const lat = parseFloat(getEl("coord-lat")?.value) || 25.5928;
      const lon = parseFloat(getEl("coord-lon")?.value) || 83.5770;
      const isHi = currentLang === "hi";

      try {
        const url = `/api/v1/crop/alternative-and-machinery?crop=${encodeURIComponent(crop)}&area_ha=${areaInHa.toFixed(2)}&lat=${lat}&lon=${lon}&lang=${currentLang}`;
        const resp = await fetch(url);
        if (resp.ok) {
          const data = await resp.json();
          renderAlternativePopup(data.alternative);
          renderMachineryPlan(data.machinery);
          renderCultivationStages(data.lifecycle_stages);
        }
      } catch (err) {
        console.warn("[KhetSathi Phase B] Alternative/Machinery API call error:", err);
      }
    }

    function renderAlternativePopup(alt) {
      const popup = getEl("floating-crop-advisor");
      if (!popup) return;

      currentAlternativeData = alt;
      if (!alt || !alt.has_alternative) {
        popup.classList.add("hidden");
        return;
      }

      popup.classList.remove("hidden");
      const isHi = currentLang === "hi";
      const badge = getEl("alt-popup-badge");
      if (badge) {
        badge.textContent = isHi 
          ? `+₹${Math.round(alt.total_extra_profit_inr).toLocaleString("en-IN")} लाभ · ${alt.water_saving_pct}% जल बचत`
          : `+₹${Math.round(alt.total_extra_profit_inr).toLocaleString("en-IN")} Gain · ${alt.water_saving_pct}% Water Saved`;
      }

      const reasonEl = getEl("alt-popup-reason");
      if (reasonEl) reasonEl.textContent = alt.reason;

      const btnApply = getEl("btn-apply-alt-crop");
      const lblApply = getEl("lbl-apply-alt-crop");
      if (lblApply) {
        const cropName = CROP_DB[alt.suggested_crop]?.[isHi ? "name_hi" : "name_en"] || alt.suggested_crop;
        lblApply.textContent = isHi ? `${cropName} अपनाएं` : `Switch to ${cropName}`;
      }
    }

    function renderMachineryPlan(mach) {
      if (!mach) return;
      const tag = getEl("machinery-tier-tag");
      if (tag) tag.textContent = mach.title;
      const desc = getEl("machinery-desc");
      if (desc) desc.textContent = mach.description;

      const grid = getEl("machinery-tools-grid");
      if (!grid) return;

      grid.innerHTML = mach.tools.map(tool => `
        <div class="p-3 rounded-xl bg-white border border-slate-200 shadow-2xs space-y-1 hover:border-emerald-500 transition">
          <div class="flex items-center justify-between gap-2">
            <span class="font-extrabold text-xs text-slate-900">${tool.name}</span>
            <span class="text-[11px] font-black text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">${tool.hire_cost}</span>
          </div>
          <p class="text-[11px] text-slate-600 leading-snug">${tool.role}</p>
        </div>
      `).join("");
    }

    function renderCultivationStages(stages) {
      const container = getEl("lifecycle-stages-container");
      if (!container || !stages) return;

      const isHi = currentLang === "hi";
      container.innerHTML = stages.map(st => `
        <div class="p-3 rounded-xl bg-white border-l-4 border-l-emerald-600 border border-slate-200 shadow-2xs space-y-1">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <span class="font-extrabold text-xs text-emerald-950">${st.stage_num}. ${st.title}</span>
            <span class="text-[10px] font-bold text-slate-700 bg-slate-100 px-2 py-0.5 rounded-full border border-slate-200">${st.timeline}</span>
          </div>
          <p class="text-[11px] text-slate-700 leading-relaxed">${st.activity}</p>
          <div class="text-[10px] text-emerald-800 font-semibold pt-0.5">
            <strong>${isHi ? "प्रयुक्त औजार:" : "Tools Used:"}</strong> ${st.tools}
          </div>
        </div>
      `).join("");
    }
"""

    if "PHASE B: DYNAMIC ALTERNATIVE CROP POP-UP" not in html:
        target_js_insert = "// Phase A: Farmland Map Pointer Event Listeners"
        html = html.replace(target_js_insert, js_phase_b + "\n    " + target_js_insert)
        print("5. Added Phase B JavaScript Functions")

    # 6. Add Phase B Event Listeners and Hook into runAdvisoryEngine
    listeners_b = """
      // Phase B Event Listeners
      const btnMinAlt = getEl("btn-minimize-alt-popup");
      if (btnMinAlt) {
        btnMinAlt.addEventListener("click", () => {
          isAltPopupMinimized = !isAltPopupMinimized;
          const body = getEl("alt-popup-body");
          const icon = getEl("alt-min-icon");
          if (isAltPopupMinimized) {
            body?.classList.add("hidden");
            if (icon) icon.textContent = "➕";
          } else {
            body?.classList.remove("hidden");
            if (icon) icon.textContent = "➖";
          }
        });
      }

      const btnCloseAlt = getEl("btn-close-alt-popup");
      if (btnCloseAlt) {
        btnCloseAlt.addEventListener("click", () => {
          getEl("floating-crop-advisor")?.classList.add("hidden");
        });
      }

      const btnApplyAlt = getEl("btn-apply-alt-crop");
      if (btnApplyAlt) {
        btnApplyAlt.addEventListener("click", () => {
          if (currentAlternativeData && currentAlternativeData.suggested_crop) {
            const newCrop = currentAlternativeData.suggested_crop;
            selectedCrop = newCrop;
            getEl("crop-select").value = newCrop;
            document.querySelectorAll(".crop-card").forEach(c => {
              if (c.getAttribute("data-crop") === newCrop) {
                c.className = "crop-card min-h-[44px] p-2.5 rounded-xl border-2 border-emerald-600 bg-emerald-50 text-emerald-950 font-bold text-xs flex flex-col items-center gap-1 shadow-sm transition";
              } else {
                c.className = "crop-card min-h-[44px] p-2.5 rounded-xl border-2 border-slate-200 bg-white text-slate-700 hover:border-emerald-400 font-bold text-xs flex flex-col items-center gap-1 transition";
              }
            });
            runAdvisoryEngine();
            getEl("floating-crop-advisor")?.classList.add("hidden");
            const isHi = currentLang === "hi";
            showToastNotification(isHi ? `✅ फसल बदलकर ${newCrop} कर दी गई है!` : `✅ Switched target crop to ${newCrop}!`, "emerald");
          }
        });
      }

      const btnViewMach = getEl("btn-view-machinery-plan");
      if (btnViewMach) {
        btnViewMach.addEventListener("click", () => {
          getEl("machinery-lifecycle-card")?.scrollIntoView({ behavior: "smooth" });
        });
      }
"""

    if "Phase B Event Listeners" not in html:
        target_listeners = "btnLockParcel.addEventListener(\"click\""
        idx = html.find(target_listeners)
        end_idx = html.find("});", idx) + 3
        html = html[:end_idx] + "\n" + listeners_b + html[end_idx:]
        print("6. Added Phase B Event Listeners")

    # 7. Hook updateAlternativeAndMachineryPlan() into runAdvisoryEngine()
    if "updateAlternativeAndMachineryPlan();" not in html:
        target_advisory_call = "renderFpoChart();"
        html = html.replace(target_advisory_call, target_advisory_call + "\n      updateAlternativeAndMachineryPlan();")
        print("7. Hooked updateAlternativeAndMachineryPlan into advisory engine")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("SUCCESS: Phase B fully applied to frontend/index.html")
    return True

if __name__ == "__main__":
    apply_phase_b()
