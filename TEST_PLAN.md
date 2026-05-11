# Test Plan — Awesome Pizza

## 1. Overview

**Application:** Awesome Pizza — browser-based pizza ordering SPA  
**Base URL:** `http://localhost:3000`  
**Stack:** Vanilla JS frontend + REST API backend  
**Test framework:** pytest + playwright-python  

### Application Summary

| Section | Description |
|---|---|
| Menu | Loads 5 pizzas from `GET /api/daily-menu`; quantity controls per item |
| Cart | Aggregates selected items; shows running total; requires customer name |
| Order Placement | `POST /api/orders`; clears cart on success; auto-fills order ID |
| Order Management | `GET /api/orders/:id` lookup; `PUT /api/orders/:id` status transitions |
| Theme Toggle | Dark / light mode switch; preference stored in `localStorage` |

---

## 2. Scope

### In scope
- All user-facing UI interactions on the single page
- REST API contract (`/api/daily-menu`, `/api/orders`, `/api/orders/:id`)
- Order status lifecycle: `RECEIVED → DELIVERING → DELIVERED` and `RECEIVED → CANCELED`
- Client-side validation (disabled button states, empty-field guards)
- Notification banner behaviour (success / error messages)
- Theme persistence across page reloads

### Out of scope
- Backend persistence layer / database internals
- Network-level performance and load testing
- Multi-user concurrency
- Browser compatibility beyond Chromium (covered by separate matrix)
- Authentication / authorization (app has none)

---

## 3. Test Environment

| Item | Value |
|---|---|
| Browser | Chromium (default), Firefox, WebKit |
| Viewport | 1280 × 720 |
| Server | `http://localhost:3000` must be running before any test |
| Python | 3.11+ |
| Key dependencies | `playwright`, `pytest-playwright`, `pytest-xdist` |

### Run commands

```powershell
.\run.ps1 headless             # CI default
.\run.ps1 headed               # local debug
.\run.ps1 headless-parallel    # pytest -n 4
.\run.ps1 headed-parallel      # pytest --headed -n 4
```

---

## 4. Risk Areas

| Risk | Likelihood | Impact | Notes |
|---|---|---|---|
| API accepts orders for off-menu pizza names | Confirmed | Medium | Server does no menu-name validation — see TC-API-005 |
| Status transitions have no server-side state machine | Confirmed | Medium | Any status → any status allowed — see TC-API-006 |
| 3-second notification auto-hide causes test flakiness | Medium | High | Tests must `wait_for(state="visible")` before reading text |
| Menu rendered by async JS fetch; race on page load | Medium | High | Tests must wait for first `.menu-item` before asserting |
| `localStorage` theme leaks between tests | Low | Medium | Each test opens a fresh browser context |

---

## 5. Test Cases

Priority: **P1** = must pass before ship · **P2** = important · **P3** = nice-to-have / exploratory  
Automation: **A** = automated in `test_pizza_ordering.py` · **M** = manual / future

---

### 5.1 Menu

| ID | Title | Steps | Expected | Priority | Auto |
|---|---|---|---|---|---|
| TC-MENU-001 | Menu displays all items from daily-menu API | Fetch `GET /api/daily-menu`; open `/` | All item names returned by the API are visible on the page | P1 | A |
| TC-MENU-002 | Each item shows name and description | Open `/`, inspect cards | Name `<h3>` and description `<p>` present on every card | P2 | M |
| TC-MENU-003 | Each item starts with quantity 0 | Open `/` | All quantity displays show `0` | P2 | M |
| TC-MENU-004 | Menu images load or fall back gracefully | Open `/` | Images render or show SVG placeholder; no broken-image icons | P3 | M |
| TC-MENU-005 | Menu section unavailable (API down) | Kill server, open `/` | Error notification shown; no blank/broken state | P2 | M |

---

### 5.2 Cart

| ID | Title | Steps | Expected | Priority | Auto |
|---|---|---|---|---|---|
| TC-CART-001 | Add one item → cart total = 1 | Open `/`, click `+` on any pizza | Cart total shows `1`; item appears in cart panel | P1 | A |
| TC-CART-002 | Add same item 3×, decrement 1× → quantity = 2 | Click `+` three times, then `−` once | Menu quantity display shows `2`; cart total shows `2` | P1 | A |
| TC-CART-003 | Add two different items → both in cart | Add Margherita ×1 and Pepperoni ×1 | Cart shows two entries; total = 2 | P2 | M |
| TC-CART-004 | Remove item via cart Remove button → empty cart | Add item, click Remove | Cart shows "Your cart is empty" | P1 | A |
| TC-CART-005 | Remove one of two cart items | Add two items, remove one | Removed item gone; other still present with correct quantity | P2 | M |
| TC-CART-006 | Decrement to 0 removes item from cart | Add item ×1, click `−` | Cart becomes empty; menu quantity back to `0` | P2 | M |
| TC-CART-007 | Place Order button disabled with empty cart and no name | Open fresh page | Button `disabled` attribute present | P1 | A |
| TC-CART-008 | Place Order disabled with items but no name | Add item, leave name blank | Button remains disabled | P2 | M |
| TC-CART-009 | Place Order disabled with name but empty cart | Enter name, add nothing | Button remains disabled | P2 | M |
| TC-CART-010 | Place Order enabled when name + at least one item present | Enter name + add item | Button becomes enabled | P2 | M |
| TC-CART-011 | Whitespace-only name does not enable Place Order | Type `   ` in name field | Button remains disabled (`.trim()` guard in JS) | P2 | M |

---

### 5.3 Order Placement

| ID | Title | Steps | Expected | Priority | Auto |
|---|---|---|---|---|---|
| TC-ORDER-001 | Successful order shows notification with Order ID | Enter name, add item, click Place Order | Success notification: `"Order placed successfully! Order ID: order-…"` | P1 | A |
| TC-ORDER-002 | Cart clears after successful order | Place order, inspect cart | Cart shows empty state; total = 0 | P2 | M |
| TC-ORDER-003 | Customer name field clears after order | Place order | Name input is empty | P2 | M |
| TC-ORDER-004 | Order ID auto-fills in the lookup field | Place order | `#order-id` input shows the new order ID | P2 | M |
| TC-ORDER-005 | Order details panel appears after placement | Place order | Order details section becomes visible with status `RECEIVED` | P2 | M |
| TC-ORDER-006 | Placing a second order replaces previous order ID in lookup | Place two orders sequentially | Lookup field holds the ID of the most-recent order | P3 | M |

---

### 5.4 Order Lookup

| ID | Title | Steps | Expected | Priority | Auto |
|---|---|---|---|---|---|
| TC-LOOK-001 | Look up valid order ID → details shown | Place order; use auto-filled ID to look up | Order details visible; customer name and `RECEIVED` status correct | P1 | A |
| TC-LOOK-002 | Invalid order ID → error notification | Enter `INVALID-ORDER-999`, click Look Up | Error notification contains "not found" or "error" | P1 | A |
| TC-LOOK-003 | Empty order ID field → validation notification | Click Look Up with empty field | Notification: `"Please enter an order ID"` | P2 | M |
| TC-LOOK-004 | Press Enter key to submit lookup | Enter valid ID, press Enter | Same result as clicking Look Up | P2 | M |
| TC-LOOK-005 | Details panel hidden before first lookup | Open fresh page | `#order-details` has `display: none` | P3 | M |
| TC-LOOK-006 | Details panel hides after failed lookup | Show valid order, then look up invalid ID | Details panel hidden; error notification shown | P2 | M |

---

### 5.5 Order Status Transitions

| ID | Title | Steps | Expected | Priority | Auto |
|---|---|---|---|---|---|
| TC-STAT-001 | RECEIVED → DELIVERING | Place order, look up, click "Mark as Delivering" | Status badge changes to `DELIVERING` | P1 | A (part of TC-STAT-003) |
| TC-STAT-002 | DELIVERING → DELIVERED | After DELIVERING, click "Mark as Delivered" | Status badge changes to `DELIVERED` | P1 | A (part of TC-STAT-003) |
| TC-STAT-003 | Full chain: RECEIVED → DELIVERING → DELIVERED | Place order, walk through both transitions | Each badge update reflects the new status | P1 | A |
| TC-STAT-004 | RECEIVED → CANCELED | Place order, look up, click "Cancel Order" | Status badge changes to `CANCELED` | P2 | M |
| TC-STAT-005 | DELIVERED order shows no action buttons | Reach DELIVERED state | No "Mark as…" buttons rendered | P2 | M |
| TC-STAT-006 | CANCELED order shows no action buttons | Reach CANCELED state | No "Mark as…" buttons rendered | P2 | M |
| TC-STAT-007 | DELIVERING state shows only "Mark as Delivered" | Reach DELIVERING state | No Cancel button; only "Mark as Delivered" visible | P2 | M |
| TC-STAT-008 | Status change shows confirmation notification | Transition any status | Notification: `"Order status updated to <STATUS>"` | P2 | M |

---

### 5.6 Theme Toggle

| ID | Title | Steps | Expected | Priority | Auto |
|---|---|---|---|---|---|
| TC-THEME-001 | Toggle to dark mode | Open `/`, click 🌙 | `<html data-theme="dark">` set; button shows ☀️ | P1 | A |
| TC-THEME-002 | Toggle back to light mode | While in dark mode, click ☀️ | `data-theme` attribute removed; button shows 🌙 | P1 | A |
| TC-THEME-003 | Dark mode preference persists on reload | Enable dark mode, reload page | Page loads in dark mode | P2 | M |
| TC-THEME-004 | Light mode preference persists on reload | Ensure light mode, reload page | Page loads in light mode | P3 | M |

---

### 5.7 API Contract

Direct API tests (no UI). Run with a REST client or dedicated API test suite.

| ID | Endpoint | Payload / Condition | Expected Response | Priority |
|---|---|---|---|---|
| TC-API-001 | `GET /api/daily-menu` | — | `success: true`, array of 5 items with `name`, `description`, `imageUrl` | P1 |
| TC-API-002 | `POST /api/orders` | Valid `{sender, contents}` | `success: true`, order with `id`, `status: "RECEIVED"` | P1 |
| TC-API-003 | `POST /api/orders` | `sender: ""` | `success: false`, 400, message about sender | P1 |
| TC-API-004 | `POST /api/orders` | `contents: []` | `success: false`, 400, message about contents | P1 |
| TC-API-005 | `POST /api/orders` | `sender: "X"`, `contents: [{name: "Nonexistent Pizza", quantity: 1}]` | **Currently returns 200** — no menu-name validation ⚠️ | P2 |
| TC-API-006 | `PUT /api/orders/:id` | `status: "INVALID_STATUS"` | `success: false`, 400, lists valid statuses | P1 |
| TC-API-007 | `PUT /api/orders/:id` | Skip DELIVERING, go RECEIVED → DELIVERED | **Currently returns 200** — no state machine enforced ⚠️ | P2 |
| TC-API-008 | `PUT /api/orders/:id` | Revert CANCELED → RECEIVED | **Currently returns 200** — allows reverting terminal state ⚠️ | P2 |
| TC-API-009 | `GET /api/orders/:id` | Nonexistent ID | `success: false`, message about order not found | P1 |

---

### 5.8 Notification Behaviour

| ID | Title | Condition | Expected | Priority | Auto |
|---|---|---|---|---|---|
| TC-NOTIF-001 | Success notification shows green styling | Place order | Notification has `success` CSS class | P2 | M |
| TC-NOTIF-002 | Error notification shows error styling | Invalid lookup | Notification has `error` CSS class | P2 | M |
| TC-NOTIF-003 | Notification auto-hides after ~3 seconds | Trigger any notification | Banner disappears without user action | P2 | M |
| TC-NOTIF-004 | New notification replaces existing one | Trigger two actions quickly | Only latest message shown | P3 | M |

---

## 6. Known Issues / Observations

| # | Observation | Severity |
|---|---|---|
| 1 | API accepts orders containing pizza names not on the daily menu | Medium — data integrity risk |
| 2 | API allows arbitrary status transitions (no state machine) — e.g. `RECEIVED → DELIVERED`, or reverting `CANCELED → RECEIVED` | Medium — business logic gap |
| 3 | Cancelling a `DELIVERING` order is not supported via UI buttons, but is possible directly via API | Low |
| 4 | No server-side quantity validation (0 or negative quantities not tested) | Low |

---

## 7. Entry / Exit Criteria

### Entry criteria
- `http://localhost:3000` is reachable and `GET /api/daily-menu` returns 5 items
- `venv` is activated and `playwright install chromium` has been run
- All P1 test cases have been reviewed and approved

### Exit criteria
- All **P1** automated tests pass with 0 failures
- All **P2** manual tests executed with results documented
- Known issues logged and triaged
- No regressions in previously passing tests

---

## 8. Automated Test Coverage Summary

The 10 automated tests in `tests/test_pizza_ordering.py` cover:

| Test | IDs covered |
|---|---|
| `test_menu_displays_all_items` | TC-MENU-001 |
| `test_place_order_button_disabled_by_default` | TC-CART-007 |
| `test_add_item_increments_cart_total` | TC-CART-001 |
| `test_remove_item_shows_empty_cart` | TC-CART-004 |
| `test_quantity_increment_and_decrement` | TC-CART-002 |
| `test_place_order_shows_success_notification` | TC-ORDER-001 |
| `test_lookup_order_after_placing` | TC-LOOK-001 |
| `test_lookup_invalid_order_id_shows_error` | TC-LOOK-002 |
| `test_order_progresses_received_to_delivered` | TC-STAT-001, TC-STAT-002, TC-STAT-003 |
| `test_theme_toggle_switches_between_dark_and_light` | TC-THEME-001, TC-THEME-002 |
