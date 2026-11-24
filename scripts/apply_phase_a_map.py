"""
scripts/apply_phase_a_map.py
Applies Phase A (Interactive Farmland Map Pointer) into frontend/index.html with:
1. Leaflet CSS and JS in <head>
2. "🗺️ नक्शे पर खेत चुनें (Map Pointer)" button in Step 1
3. #map-pointer-container with satellite/standard layer switcher, measure tool, GPS centering, and parcel locker
4. 100% flawless bilingual parity in I18N.hi and I18N.en
5. Leaflet lazy map instantiation, draggable pin synchronization with /api/v1/district/baseline and weather
6. Polygon area calculation (Shoelace formula) in Bigha and Acres
"""

import sys
from pathlib import Path


def apply_phase_a():
    html_path = Path("frontend/index.html")
    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    # 1. Add Leaflet into <head>
    leaflet_head = """  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
"""
    if "leaflet@1.9.4" not in html:
        target_head = '  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>'
        if target_head in html:
            html = html.replace(target_head, target_head + "\n" + leaflet_head)
            print("1. Added Leaflet to <head>")
        else:
            print("ERROR: Could not find chart.js target in <head>")
            return False

    # 2. Add Map Pointer button next to GPS and coordinates buttons
    map_btn_html = """                <button id="btn-toggle-map" type="button" class="min-h-[38px] px-3.5 py-1.5 rounded-xl bg-emerald-700 hover:bg-emerald-600 text-white text-xs font-bold shadow flex items-center gap-1.5 transition">
                  <span>🗺️</span> <span id="lbl-map-toggle">नक्शे पर खेत चुनें</span>
                </button>"""

    target_btn_anchor = """                <button id="btn-detect-gps-inline" type="button" class="min-h-[38px] px-3.5 py-1.5 rounded-xl bg-emerald-800 hover:bg-emerald-700 text-white text-xs font-bold shadow flex items-center gap-1.5">
                  <span>📍</span> <span id="lbl-gps-inline">1-Click GPS</span>
                </button>"""

    if "btn-toggle-map" not in html:
        if target_btn_anchor in html:
            html = html.replace(target_btn_anchor, target_btn_anchor + "\n" + map_btn_html)
            print("2. Added #btn-toggle-map button to location bar")
        else:
            print("ERROR: Could not find target_btn_anchor")
            return False

    # 3. Add #map-pointer-container right after #coord-nudge-box
    map_container_html = """            <!-- Interactive Farmland Map Pointer Container (Phase A) -->
            <div id="map-pointer-container" class="hidden space-y-3 p-4 rounded-2xl bg-emerald-950/5 border-2 border-emerald-600/60 shadow-md transition-all mt-2">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-emerald-900/10 pb-2.5">
                <div class="flex items-center gap-2">
                  <span class="text-xl">🗺️</span>
                  <div>
                    <h4 id="lbl-map-title" class="text-sm font-extrabold text-emerald-950">खेत का नक्शा व स्थिति (Interactive Farmland Map Pointer)</h4>
                    <p id="lbl-map-sub" class="text-xs text-slate-600">नक्शे को ज़ूम करें और अपने खेत पर पिन रखें, या खेत के कोनों को छूकर रकबा नापें</p>
                  </div>
                </div>
                <div class="flex flex-wrap items-center gap-1.5">
                  <button id="btn-map-layer-sat" type="button" class="min-h-[34px] px-2.5 py-1 rounded-lg text-xs font-bold bg-emerald-800 text-white transition shadow-sm">
                    🛰️ <span id="lbl-map-sat">सैटेलाइट</span>
                  </button>
                  <button id="btn-map-layer-std" type="button" class="min-h-[34px] px-2.5 py-1 rounded-lg text-xs font-bold bg-white text-slate-700 border border-slate-300 hover:bg-slate-50 transition">
                    🗺️ <span id="lbl-map-std">मानक</span>
                  </button>
                  <button id="btn-map-measure" type="button" class="min-h-[34px] px-2.5 py-1 rounded-lg text-xs font-bold bg-amber-500 hover:bg-amber-400 text-slate-950 transition shadow-sm">
                    📐 <span id="lbl-map-measure">रकबा नापें</span>
                  </button>
                  <button id="btn-map-gps" type="button" class="min-h-[34px] px-2.5 py-1 rounded-lg text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-800 border border-slate-300 transition">
                    🎯 <span id="lbl-map-gps">खेत पर जाएं</span>
                  </button>
                  <button id="btn-map-close" type="button" class="min-h-[34px] px-2 py-1 rounded-lg text-xs font-bold text-slate-500 hover:text-slate-800 transition" aria-label="बंद करें">
                    ✖️
                  </button>
                </div>
              </div>

              <!-- Area Measurement Guidance Banner (visible when measure mode active) -->
              <div id="map-measure-banner" class="hidden p-2.5 rounded-xl bg-amber-50 border border-amber-300 flex flex-wrap items-center justify-between gap-2 text-xs">
                <div class="flex items-center gap-1.5 font-bold text-amber-950">
                  <span>📐</span>
                  <span id="map-measure-hint">खेत के 3 या 4 कोनों को नक्शे पर छूएं। रकबा स्वतः निकल जाएगा।</span>
                </div>
                <div class="flex items-center gap-2">
                  <span id="map-measured-val" class="font-extrabold text-amber-900 bg-white px-2 py-0.5 rounded border border-amber-300">0.00 बीघा</span>
                  <button id="btn-apply-measured-area" type="button" class="px-2.5 py-1 bg-emerald-800 text-white font-bold rounded-lg hover:bg-emerald-700 transition">
                    📥 <span id="lbl-apply-area">रकबा दर्ज करें</span>
                  </button>
                  <button id="btn-clear-measure" type="button" class="px-2 py-1 bg-slate-200 text-slate-700 font-bold rounded-lg hover:bg-slate-300 transition">
                    🔄 रीसेट
                  </button>
                </div>
              </div>

              <!-- Map Canvas & Offline Fallback -->
              <div class="relative w-full rounded-xl overflow-hidden border border-emerald-700/30 shadow-inner" style="height: 380px;">
                <div id="farmland-map-canvas" class="w-full h-full z-10"></div>

                <!-- Floating Pin Coordinates & Confirmation Overlay -->
                <div id="map-pin-overlay" class="absolute bottom-3 left-3 right-3 sm:left-auto sm:right-3 z-20 p-2.5 rounded-xl bg-white/95 backdrop-blur-sm border border-emerald-700/40 shadow-xl flex items-center justify-between gap-3 text-xs">
                  <div class="flex items-center gap-2">
                    <span class="text-lg">📍</span>
                    <div>
                      <div class="font-extrabold text-emerald-950" id="map-overlay-title">चयनित खेत स्थिति (Pinpoint)</div>
                      <div class="font-mono text-slate-600 text-[11px]" id="map-overlay-coords">25.5928°N, 83.5770°E</div>
                    </div>
                  </div>
                  <button id="btn-lock-parcel" type="button" class="min-h-[34px] px-3 py-1 bg-emerald-800 hover:bg-emerald-700 text-white font-extrabold rounded-lg shadow transition flex items-center gap-1">
                    ✅ <span id="lbl-lock-parcel">खेत लॉक करें</span>
                  </button>
                </div>
              </div>
            </div>"""

    target_nudge_box = """            <!-- Collapsible Precise Coordinates Nudge Box -->
            <div id="coord-nudge-box" class="hidden grid grid-cols-1 sm:grid-cols-2 gap-3 p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs mt-2">
              <div>
                <label for="coord-lat" id="lbl-coord-lat" class="block font-bold text-slate-700 mb-1">अक्षांश Latitude (°N)</label>
                <input id="coord-lat" type="number" step="0.0001" min="6.0" max="38.0" value="25.5928" class="w-full min-h-[38px] p-2 border rounded-lg bg-white font-mono font-bold text-slate-900" />
              </div>
              <div>
                <label for="coord-lon" id="lbl-coord-lon" class="block font-bold text-slate-700 mb-1">देशांतर Longitude (°E)</label>
                <input id="coord-lon" type="number" step="0.0001" min="68.0" max="98.0" value="83.5770" class="w-full min-h-[38px] p-2 border rounded-lg bg-white font-mono font-bold text-slate-900" />
              </div>
            </div>"""

    if "map-pointer-container" not in html:
        if target_nudge_box in html:
            html = html.replace(target_nudge_box, target_nudge_box + "\n" + map_container_html)
            print("3. Added #map-pointer-container to Step 1")
        else:
            print("ERROR: Could not find target_nudge_box")
            return False

    # 4. Add I18N keys to I18N.hi and I18N.en
    hi_keys = """        mapPointerBtn: "नक्शे पर खेत चुनें",
        mapTitle: "खेत का नक्शा व स्थिति (Interactive Farmland Map Pointer)",
        mapSub: "नक्शे को ज़ूम करें और अपने खेत पर पिन रखें, या खेत के कोनों को छूकर रकबा नापें",
        mapSatellite: "सैटेलाइट",
        mapStandard: "मानक",
        mapMeasureArea: "रकबा नापें",
        mapMyGps: "खेत पर जाएं",
        mapClose: "नक्शा छुपाएं",
        mapLockParcel: "खेत लॉक करें",
        mapMeasuredAreaBadge: "नापा गया रकबा",
        mapApplyArea: "रकबा दर्ज करें",
"""

    en_keys = """        mapPointerBtn: "Pinpoint on Map",
        mapTitle: "Interactive Farmland Map Pointer & Boundaries",
        mapSub: "Pan/zoom and drop pin on your field parcel, or tap corners to measure acreage",
        mapSatellite: "Satellite",
        mapStandard: "Standard",
        mapMeasureArea: "Measure Area",
        mapMyGps: "My GPS",
        mapClose: "Close Map",
        mapLockParcel: "Lock Parcel",
        mapMeasuredAreaBadge: "Measured Area",
        mapApplyArea: "Apply Measured Area",
"""

    if '"mapPointerBtn"' not in html:
        # In I18N.hi: after coordToggle
        target_hi_coord = 'coordToggle: "निर्देशांक",'
        if target_hi_coord in html:
            html = html.replace(target_hi_coord, target_hi_coord + "\n" + hi_keys)
            print("4a. Added map keys to I18N.hi")
        else:
            print("ERROR: Could not find target_hi_coord")
            return False

        # In I18N.en: after coordToggle
        target_en_coord = 'coordToggle: "Coordinates",'
        if target_en_coord in html:
            html = html.replace(target_en_coord, target_en_coord + "\n" + en_keys)
            print("4b. Added map keys to I18N.en")
        else:
            print("ERROR: Could not find target_en_coord")
            return False

    # 5. Add DOM mappings in setLanguage(lang)
    setlang_additions = """        "lbl-map-toggle": dict.mapPointerBtn,
        "lbl-map-title": dict.mapTitle,
        "lbl-map-sub": dict.mapSub,
        "lbl-map-sat": dict.mapSatellite,
        "lbl-map-std": dict.mapStandard,
        "lbl-map-measure": dict.mapMeasureArea,
        "lbl-map-gps": dict.mapMyGps,
        "lbl-lock-parcel": dict.mapLockParcel,
        "lbl-apply-area": dict.mapApplyArea,
"""
    if '"lbl-map-toggle": dict.mapPointerBtn' not in html:
        target_setlang_coord = '"lbl-coord-toggle": dict.coordToggle,'
        if target_setlang_coord in html:
            html = html.replace(target_setlang_coord, target_setlang_coord + "\n" + setlang_additions)
            print("5. Added map element text updates to setLanguage")
        else:
            print("ERROR: Could not find target_setlang_coord in setLanguage")
            return False

    # 6. Add JavaScript logic for Leaflet Map Pointer
    map_js_code = """
    // =========================================================================
    // PHASE A: INTERACTIVE FARMLAND MAP POINTER & POLYGON ACREAGE ENGINE
    // =========================================================================
    let leafletMapInstance = null;
    let mapMarker = null;
    let satTileLayer = null;
    let osmTileLayer = null;
    let isMeasureMode = false;
    let measurePolygon = null;
    let measurePoints = [];
    let measureMarkers = [];
    let calculatedPolygonHa = 0.0;

    function calculateGeodesicPolygonArea(coords) {
      if (!coords || coords.length < 3) return 0.0;
      const meanLat = coords.reduce((acc, c) => acc + c[0], 0) / coords.length;
      const latRad = (meanLat * Math.PI) / 180.0;
      const metersPerLat = 111139.0;
      const metersPerLon = 111139.0 * Math.cos(latRad);
      const xy = coords.map(c => [c[1] * metersPerLon, c[0] * metersPerLat]);
      let area = 0.0;
      const n = xy.length;
      for (let i = 0; i < n; i++) {
        const j = (i + 1) % n;
        area += xy[i][0] * xy[j][1];
        area -= xy[j][0] * xy[i][1];
      }
      return Math.abs(area) / 2.0;
    }

    function initFarmlandMap() {
      if (leafletMapInstance) {
        leafletMapInstance.invalidateSize();
        return;
      }
      if (typeof L === "undefined") {
        console.warn("[KhetSathi] Leaflet library not loaded, using tactile coordinate nudge fallback.");
        return;
      }

      const initialLat = parseFloat(getEl("coord-lat")?.value) || 25.5928;
      const initialLon = parseFloat(getEl("coord-lon")?.value) || 83.5770;

      leafletMapInstance = L.map("farmland-map-canvas", {
        center: [initialLat, initialLon],
        zoom: 16,
        zoomControl: true
      });

      satTileLayer = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
        maxZoom: 19,
        attribution: "Esri Satellite Imagery"
      });

      osmTileLayer = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "© OpenStreetMap contributors"
      });

      satTileLayer.addTo(leafletMapInstance);

      // Custom high-contrast tactile harvest marker pin
      const harvestIcon = L.divIcon({
        className: "custom-harvest-pin",
        html: `<div style="background-color:#10b981; border:3px solid #ffffff; width:34px; height:34px; border-radius:50%; box-shadow:0 0 14px rgba(16,185,129,0.9); display:flex; align-items:center; justify-content:center; font-size:18px; cursor:grab;">📍</div>`,
        iconSize: [34, 34],
        iconAnchor: [17, 34]
      });

      mapMarker = L.marker([initialLat, initialLon], {
        draggable: true,
        icon: harvestIcon
      }).addTo(leafletMapInstance);

      function onPinPositionUpdated(lat, lon) {
        getEl("coord-lat").value = lat.toFixed(4);
        getEl("coord-lon").value = lon.toFixed(4);
        const overlayCoords = getEl("map-overlay-coords");
        if (overlayCoords) overlayCoords.textContent = `${lat.toFixed(4)}°N, ${lon.toFixed(4)}°E`;
        fetchLocationAndWeather(lat, lon);
      }

      mapMarker.on("dragend", (e) => {
        const pos = e.target.getLatLng();
        onPinPositionUpdated(pos.lat, pos.lng);
      });

      leafletMapInstance.on("click", (e) => {
        if (isMeasureMode) {
          addMeasurePoint(e.latlng);
        } else {
          mapMarker.setLatLng(e.latlng);
          onPinPositionUpdated(e.latlng.lat, e.latlng.lng);
        }
      });
    }

    function addMeasurePoint(latlng) {
      measurePoints.push([latlng.lat, latlng.lng]);
      const pMarker = L.circleMarker(latlng, {
        radius: 6,
        color: "#f59e0b",
        fillColor: "#ffffff",
        fillOpacity: 1.0,
        weight: 3
      }).addTo(leafletMapInstance);
      measureMarkers.push(pMarker);

      if (measurePolygon) leafletMapInstance.removeLayer(measurePolygon);
      measurePolygon = L.polygon(measurePoints, {
        color: "#10b981",
        fillColor: "#10b981",
        fillOpacity: 0.35,
        weight: 3
      }).addTo(leafletMapInstance);

      if (measurePoints.length >= 3) {
        const sqMeters = calculateGeodesicPolygonArea(measurePoints);
        calculatedPolygonHa = sqMeters / 10000.0;
        const bigha = sqMeters / 2500.0;
        const acre = sqMeters / 4046.86;
        const isHi = currentLang === "hi";
        const valText = isHi
          ? `${bigha.toFixed(2)} बीघा (${acre.toFixed(2)} एकड़)`
          : `${bigha.toFixed(2)} Bigha (${acre.toFixed(2)} Acre)`;
        getEl("map-measured-val").textContent = valText;
      }
    }

    function clearMeasurements() {
      measurePoints = [];
      measureMarkers.forEach(m => leafletMapInstance.removeLayer(m));
      measureMarkers = [];
      if (measurePolygon) {
        leafletMapInstance.removeLayer(measurePolygon);
        measurePolygon = null;
      }
      calculatedPolygonHa = 0.0;
      getEl("map-measured-val").textContent = currentLang === "hi" ? "0.00 बीघा" : "0.00 Bigha";
    }

    function toggleFarmlandMap() {
      const container = getEl("map-pointer-container");
      if (!container) return;
      const isHidden = container.classList.contains("hidden");
      if (isHidden) {
        container.classList.remove("hidden");
        setTimeout(() => {
          initFarmlandMap();
          if (leafletMapInstance) {
            leafletMapInstance.invalidateSize();
            const lat = parseFloat(getEl("coord-lat").value) || 25.5928;
            const lon = parseFloat(getEl("coord-lon").value) || 83.5770;
            leafletMapInstance.setView([lat, lon], 16);
            if (mapMarker) mapMarker.setLatLng([lat, lon]);
          }
        }, 120);
      } else {
        container.classList.add("hidden");
      }
    }
"""

    if "PHASE A: INTERACTIVE FARMLAND MAP POINTER" not in html:
        target_js_insert = "// Initial Execution"
        if target_js_insert in html:
            html = html.replace(target_js_insert, map_js_code + "\n      " + target_js_insert)
            print("6a. Added Map Pointer JavaScript functions")
        else:
            print("ERROR: Could not find target_js_insert")
            return False

    # 7. Add DOM event listeners for map pointer buttons
    map_listeners = """
      // Phase A: Farmland Map Pointer Event Listeners
      const btnToggleMap = getEl("btn-toggle-map");
      if (btnToggleMap) btnToggleMap.addEventListener("click", toggleFarmlandMap);

      const btnMapClose = getEl("btn-map-close");
      if (btnMapClose) btnMapClose.addEventListener("click", () => {
        getEl("map-pointer-container")?.classList.add("hidden");
      });

      const btnMapSat = getEl("btn-map-layer-sat");
      const btnMapStd = getEl("btn-map-layer-std");
      if (btnMapSat && btnMapStd) {
        btnMapSat.addEventListener("click", () => {
          if (leafletMapInstance && satTileLayer && osmTileLayer) {
            leafletMapInstance.removeLayer(osmTileLayer);
            satTileLayer.addTo(leafletMapInstance);
            btnMapSat.className = "min-h-[34px] px-2.5 py-1 rounded-lg text-xs font-bold bg-emerald-800 text-white transition shadow-sm";
            btnMapStd.className = "min-h-[34px] px-2.5 py-1 rounded-lg text-xs font-bold bg-white text-slate-700 border border-slate-300 hover:bg-slate-50 transition";
          }
        });
        btnMapStd.addEventListener("click", () => {
          if (leafletMapInstance && satTileLayer && osmTileLayer) {
            leafletMapInstance.removeLayer(satTileLayer);
            osmTileLayer.addTo(leafletMapInstance);
            btnMapStd.className = "min-h-[34px] px-2.5 py-1 rounded-lg text-xs font-bold bg-emerald-800 text-white transition shadow-sm";
            btnMapSat.className = "min-h-[34px] px-2.5 py-1 rounded-lg text-xs font-bold bg-white text-slate-700 border border-slate-300 hover:bg-slate-50 transition";
          }
        });
      }

      const btnMapMeasure = getEl("btn-map-measure");
      const mapMeasureBanner = getEl("map-measure-banner");
      if (btnMapMeasure && mapMeasureBanner) {
        btnMapMeasure.addEventListener("click", () => {
          isMeasureMode = !isMeasureMode;
          if (isMeasureMode) {
            mapMeasureBanner.classList.remove("hidden");
            btnMapMeasure.classList.add("ring-2", "ring-amber-400");
          } else {
            mapMeasureBanner.classList.add("hidden");
            btnMapMeasure.classList.remove("ring-2", "ring-amber-400");
          }
        });
      }

      const btnClearMeasure = getEl("btn-clear-measure");
      if (btnClearMeasure) btnClearMeasure.addEventListener("click", clearMeasurements);

      const btnApplyMeasuredArea = getEl("btn-apply-measured-area");
      if (btnApplyMeasuredArea) {
        btnApplyMeasuredArea.addEventListener("click", () => {
          if (calculatedPolygonHa > 0) {
            const plotInput = getEl("plot-area");
            const unitSelect = getEl("plot-unit");
            if (plotInput && unitSelect) {
              unitSelect.value = "ha";
              plotInput.value = calculatedPolygonHa.toFixed(2);
              runAdvisoryEngine();
              const isHi = currentLang === "hi";
              alert(isHi ? `✅ नापा गया रकबा (${calculatedPolygonHa.toFixed(2)} हेक्टेयर) दर्ज कर दिया गया है!` : `✅ Measured area (${calculatedPolygonHa.toFixed(2)} Ha) applied!`);
            }
          }
        });
      }

      const btnMapGps = getEl("btn-map-gps");
      if (btnMapGps) {
        btnMapGps.addEventListener("click", () => {
          detectFieldGPS();
          setTimeout(() => {
            const lat = parseFloat(getEl("coord-lat").value);
            const lon = parseFloat(getEl("coord-lon").value);
            if (leafletMapInstance && !isNaN(lat) && !isNaN(lon)) {
              leafletMapInstance.flyTo([lat, lon], 17);
              if (mapMarker) mapMarker.setLatLng([lat, lon]);
            }
          }, 350);
        });
      }

      const btnLockParcel = getEl("btn-lock-parcel");
      if (btnLockParcel) {
        btnLockParcel.addEventListener("click", () => {
          const lat = parseFloat(getEl("coord-lat").value);
          const lon = parseFloat(getEl("coord-lon").value);
          const isHi = currentLang === "hi";
          getEl("map-pointer-container")?.classList.add("hidden");
          alert(isHi ? `✅ खेत स्थिति सुरक्षित: (${lat.toFixed(4)}°N, ${lon.toFixed(4)}°E)\\nमौसम व मिट्टी सलाह अद्यतन कर दी गई है।` : `✅ Farm parcel locked: (${lat.toFixed(4)}°N, ${lon.toFixed(4)}°E)\\nWeather and soil baseline updated.`);
        });
      }
"""

    if "Phase A: Farmland Map Pointer Event Listeners" not in html:
        target_listeners_anchor = 'getEl("btn-detect-gps-inline").addEventListener("click", detectFieldGPS);'
        if target_listeners_anchor in html:
            html = html.replace(target_listeners_anchor, target_listeners_anchor + "\n" + map_listeners)
            print("7. Added Map Pointer Event Listeners")
        else:
            print("ERROR: Could not find target_listeners_anchor")
            return False

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("SUCCESS: Phase A Map Pointer fully integrated into frontend/index.html")
    return True


if __name__ == "__main__":
    if apply_phase_a():
        sys.exit(0)
    else:
        sys.exit(1)
