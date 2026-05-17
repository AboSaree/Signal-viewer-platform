# Medical Signal Viewer — Angular

This is the original **Medical Signal Viewer** (vanilla JS single-file app) ported to **Angular 17** (standalone components, no NgModule).

## Project Structure

```
medical-signal-viewer-angular/
├── src/
│   ├── index.html                      # Angular entry HTML
│   ├── main.ts                         # Bootstrap entry point
│   ├── styles.css                      # Global styles (all CSS from original)
│   └── app/
│       ├── app.component.ts            # Main AppComponent (all logic)
│       ├── app.component.html          # Angular template
│       └── canvas-views.ts            # All canvas classes + services
├── angular.json
├── package.json
├── tsconfig.json
└── tsconfig.app.json
```

## Architecture

### What Changed (Vanilla → Angular)

| Vanilla JS | Angular |
|---|---|
| `class App { _buildDOM() }` | `AppComponent` with HTML template |
| `document.getElementById(...)` | `@ViewChild()` refs + Angular bindings |
| `el.classList.toggle(...)` | `[class.name]="condition"` |
| `el.style.display = 'block'` | `*ngIf="condition"` |
| `el.textContent = v` | `{{ variable }}` interpolation |
| `el.addEventListener(...)` | `(click)="handler()"` |
| `new App(document.getElementById('app'))` | `bootstrapApplication(AppComponent)` |

### What Stayed the Same

All canvas drawing logic is **100% preserved** in `canvas-views.ts`:
- `ChannelView` — individual lead canvas with drag/scroll/zoom
- `SingleView` — all leads overlaid in one canvas
- `PolarView` — polar coordinate visualization
- `PolarRatioView` — dual-lead polar ratio
- `ScatterView` — lead cross-analysis scatter plot
- `XorView` — XOR anomaly stack graph
- `DigitalXorView` — per-chunk deviation waveform
- `SignalService` — reactive key-value state store
- `AnimationService` — RAF-based animation loop
- `Draw` utilities — grid, signal, axes, miniSubAxis

## Setup & Run

```bash
# 1. Install dependencies
npm install

# 2. Start dev server (opens at http://localhost:4200)
npm start

# 3. Build for production
npm run build
```

## Requirements

- Node.js 18+
- npm 9+

## Backend

The app connects to a Django backend at `http://127.0.0.1:8000/api`. The `API_BASE` constant is defined in `app.component.ts`. The Django server handles WFDB file parsing and AI diagnosis. CSV files are processed client-side without a server.

## Key Angular Patterns Used

- **Standalone component** (`standalone: true`) — no NgModule needed
- **ChangeDetectorRef** — manually trigger detection after imperative DOM changes from canvas classes
- **@ViewChild** — access `<canvas>` and container elements for imperative canvas setup
- **ngModel** — two-way binding for selects and range inputs
- **ngClass / ngStyle** — dynamic class and style bindings
- **CommonModule + FormsModule** — for `*ngIf`, `*ngFor`, `[(ngModel)]`
