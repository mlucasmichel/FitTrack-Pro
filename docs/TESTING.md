# Testing Documentation | FitTrack Pro

This document details the testing procedures and results for the FitTrack Pro application. Testing was conducted to ensure that all user stories are met, data integrity is maintained, and the code adheres to professional standards.

---

## 1. Code Validation
All code was passed through the relevant validators to ensure syntax correctness and best practices.

*   **HTML:** W3C Markup Validator - [Result: Pass]
*   **CSS:** W3C CSS Validator (Jigsaw) - [Result: Pass]
*   **JavaScript:** JSHint - [Result: Pass]
*   **Python:** PEP8 (CI Python Linter) - [Result: Pass]

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

| Page | Performance | Accessibility | Best Practices | SEO |
| :--- | :--- | :--- | :--- | :--- |
| Home | 100 | 90 | 100 | 90 |
| Dashboard | 90 | 92 | 100 | 90 |
| Routines | 97 | 93 | 100 | 90 |

---

## 5. Automated Testing

A total of **12 automated unit tests** were implemented using Django's built-in `TestCase` framework. These tests ensure that the core business logic, data integrity, and security models are functioning correctly and will not
regress during future updates.

*   **Result:** OK
*   **Total Tests:** 12
*   **Execution Time:** 20.387s

### 5.1 Test Coverage Areas:
*   **Workouts:** Verified `Exercise` creation, `WorkoutLog` session recording, and strict `PlanItem` validation (ensuring negative reps/sets are rejected).
*   **Nutrition:** Verified meal calorie/macro math correctly accounts for portion sizes (servings) and that custom meals are correctly associated with their creators.
*   **Subscriptions:** Verified that the `is_premium` status logic correctly reflects the user's active/inactive payment state and that Euro formatting is applied to plan tiers.

> **Note:** These tests can be run locally using the command `python manage.py test`.