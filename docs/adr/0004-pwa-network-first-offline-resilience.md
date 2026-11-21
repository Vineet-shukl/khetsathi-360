# ADR-0004: Progressive Web App with Network-First Navigation Caching

**Date**: 2026-11-20  
**Status**: accepted  
**Deciders**: KhetSathi Frontend & PWA Core  

## Context

Smallholders frequently operate in deep rural agricultural fields with intermittent or zero 2G/4G network connectivity. A web platform that fails completely when offline is unusable in the field. Conversely, overly aggressive Cache-First strategies (such as caching the HTML shell in `CacheStorage` without an active network check) can trap mobile browsers on stale or broken HTML versions indefinitely.

## Decision

We adopt a **Hybrid Service Worker Caching Strategy (`khetsathi-v2.2`)**:
1. **HTML Navigation Requests (`mode === 'navigate'`)**:
   - Enforce **Network-First**: The browser always attempts a live network fetch to guarantee users receive the latest deployed build and bugfixes.
   - If network fails, it seamlessly falls back to the pre-cached offline HTML shell (`caches.match('/')`).
2. **Static Immutable Assets (CSS, JS, Fonts, Icons)**:
   - Enforce **Cache-First / Stale-While-Revalidate**: Instant sub-50ms asset loading from browser cache.
3. **API Advisory Queries (`/api/v1/`)**:
   - Network-First with offline fallback JSON returning localized agronomic baselines for the farmer's stored district.
4. **Cache Lifecycle**:
   - When a new Service Worker activates, `caches.keys()` iterates and immediately deletes all outdated cache partitions, calling `self.clients.claim()` and `skipWaiting()`.

## Alternatives Considered

### Alternative 1: Pure Native Mobile App (Flutter / React Native APK)
- **Pros**: Full access to native storage and background workers.
- **Cons**: High distribution friction (Google Play Store download required, app size 25–60 MB); many smallholders have low-tier Android devices with depleted storage.
- **Why not**: PWA provides 100% of required functionality at $< 1.5\text{ MB}$ total footprint with zero store install friction.

### Alternative 2: Pure Cache-First Shell (App Shell Model)
- **Pros**: Instant offline startup.
- **Cons**: Severe risk of serving stale or broken cached HTML indefinitely; requires complex client-side cache busting mechanisms.
- **Why not**: Caused blank screen regressions in early field testing.

## Consequences

### Positive
- **Instant Field Resilience**: The app opens and provides advisory even with zero cellular reception.
- **No Stale Trap**: Any deployment immediately reaches online users on standard page refresh.
- **Lightweight**: Zero app store friction; installable directly via Chrome "Add to Home screen" (PWA).

### Negative
- Initial cold load requires cellular connectivity to populate the offline cache bundle.

### Risks & Mitigations
- **Risk**: Upstream CDN changes breaking offline asset availability.
- **Mitigation**: Critical fonts and styles are listed in `STATIC_ASSETS` pre-caching array during worker install.
