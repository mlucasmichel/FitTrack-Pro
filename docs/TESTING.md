# Testing Documentation | FitTrack Pro

This document details the testing procedures and results for the FitTrack Pro application. Testing was conducted to ensure that all user stories are met, data integrity is maintained, and the code adheres to professional standards.

---

## 1. Code Validation
All code was passed through the relevant validators to ensure syntax correctness and best practices.

*   **HTML:** W3C Markup Validator - [Result: Pending]
*   **CSS:** W3C CSS Validator (Jigsaw) - [Result: Pending]
*   **JavaScript:** JSHint - [Result: Pending]
*   **Python:** PEP8 (CI Python Linter) - [Result: Pending]

---

## 2. Manual Testing (User Stories)

The following tests were performed manually on both the local development environment and the deployed Heroku application.

### 2.1 New User (Visitor)
| ID | User Story | Action | Expected Result | Pass/Fail |
| :--- | :--- | :--- | :--- | :--- |
| **1.1** | Understand value proposition | Navigate to the root URL (`/`). | The Home page displays a clear split-screen layout highlighting features and value. | [Pass] |
| **1.2** | Navigate to registration | Click "Get Started Now" on the Home page. | Redirects to `/accounts/signup/`. | [Pass] |
| **1.3** | View subscription tiers | Click the locked content prompt or navigate to the pricing page. | Displays the pricing comparison table (Free vs Pro). | [Pass] |

### 2.2 Registered User (Non-Subscriber / Free Tier)
| ID | User Story | Action | Expected Result | Pass/Fail |
| :--- | :--- | :--- | :--- | :--- |
| **2.1** | Log in/out securely | Log in via `/accounts/login/`, then click "Logout" in sidebar. | Success toasts appear. Sidebar state updates correctly. | [Pass] |
| **2.2** | View/update profile | Click "Profile" in the sidebar. | Profile page loads, showing username, email, and custom meals. | [Pass] |
| **2.3** | Browse free content | Navigate to "Routines" and "Nutrition". | Free plans are fully accessible and clickable. | [Pass] |
| **2.4** | Prompted to subscribe | Attempt to click a "Pro" routine or meal plan. | Plan appears dimmed/locked. Clicking "Upgrade to Access" redirects to Pricing page. | [Pass] |
| **2.5** | Calorie calculator limits | Navigate to Nutrition Hub. Attempt to log 4 meals. | After 3 meals, the log modal shows a "Daily Limit Reached" lock screen. | [Pass] |
| **2.6** | Routine limits | Navigate to Routines. Attempt to create a 4th routine. | After 3 routines, the "Create Routine" button is disabled and shows a lock icon. | [Pass] |

### 2.3 Subscriber (Premium User)
| ID | User Story | Action | Expected Result | Pass/Fail |
| :--- | :--- | :--- | :--- | :--- |
| **3.1** | Secure upgrade via Stripe | Click "Upgrade to Pro", enter test card details, and submit. | Redirects to Success page. Status updates to "Active" via webhook. | [Pass] |
| **3.2** | Unrestricted access | Navigate to Routines and Nutrition as an Active subscriber. | Previously locked "Pro" plans are now fully accessible and clickable. | [Pass] |
| **3.3** | Unlimited custom plans | Navigate to Routines and Nutrition. | The 3-routine and 3-meal/day limits are removed. Buttons remain active. | [Pass] |
| **3.4** | Interactive charts | Log a workout, then view the Exercise Detail page. | Chart.js renders a line chart of volume history. Toggle buttons change metrics. | [Pass] |
| **3.5** | Manage subscription | *Future implementation (e.g., Stripe Customer Portal).* | - | N/A |

### 2.4 Site Administrator
| ID | User Story | Action | Expected Result | Pass/Fail |
| :--- | :--- | :--- | :--- | :--- |
| **4.1** | Access Admin dashboard | Navigate to `/admin/` and log in as superuser. | Django administration panel loads. | [Pass] |
| **4.2** | Manage plans/content | Create, edit, and delete `WorkoutPlan` and `MealPlan` objects. | Changes reflect immediately on the frontend. | [Pass] |
| **4.3** | View user status | Navigate to `Subscriptions` in the admin panel. | Can view a list of all users, their Stripe IDs, and their active/canceled status. | [Pass] |

---

## 3. Data Integrity & Validation Testing
Specific tests conducted to address previous assessor feedback regarding negative values.

| Test | Action | Expected Result | Pass/Fail |
| :--- | :--- | :--- | :--- |
| **Negative Workout Weight** | Try logging a workout with `-10` kg. | Form validation prevents submission. | [Pass] |
| **Negative Workout Reps** | Try logging a workout with `0` or `-5` reps. | Form validation prevents submission. | [Pass] |
| **Negative Meal Calories** | Try creating a custom meal with `-500` calories. | Form validation prevents submission. | [Pass] |
| **Negative Meal Macros** | Try creating a custom meal with `-10`g protein. | Form validation prevents submission. | [Pass] |

---

## 4. Lighthouse Audits
*To be completed. Goal: 90+ across all metrics.*

| Page | Performance | Accessibility | Best Practices | SEO |
| :--- | :--- | :--- | :--- | :--- |
| Home | Pending | Pending | Pending | Pending |
| Dashboard | Pending | Pending | Pending | Pending |
| Routines | Pending | Pending | Pending | Pending |

---

## 5. Automated Testing
*(Optional but recommended for Distinction: Document the results of your `tests.py` runs here).*