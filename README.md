# FitTrack Pro – Premium Fitness Tracking Platform

**FitTrack Pro** is a comprehensive full-stack web application designed for fitness enthusiasts who want a professional, data-driven approach to their workout and meal planning.

***

## Table of Contents
1. [**Project Overview**](#1-project-overview)
2. [**UX & Design (The 5 Planes)**](#2-ux--design-the-5-planes)
3. [**Data Schema (Entity Relationship Diagram)**](#3-data-schema-entity-relationship-diagram)
4. [**Features**](#4-features)
5. [**Testing**](#5-testing)
6. [**Technologies Used**](#6-technologies-used)
7. [**Deployment**](#7-deployment)
8. [**Credits**](#8-credits)

***

## 1. Project Overview

### 1.1 Goal & Value Proposition
**FitTrack Pro** provides a premium platform for users to manage their fitness journey. By authenticating and subscribing, users unlock customized workout programs and detailed meal plans, ensuring their fitness goals are met
with professional guidance.

**The application provides value by:**
* Offering structured workout and meal plans tailored to user goals.
* Providing premium content through a secure Stripe-powered subscription model.
* Enhancing the user experience with interactive tools like a calorie calculator and progress trackers.

***

## 2. UX & Design (The 5 Planes)

### 2.1 The Strategy Plane
The primary objective of FitTrack Pro is to provide a "SaaS-style" fitness tool that bridges the gap between simple logging and professional coaching.
*   **User Needs:** High-quality exercise data, clear progress visualization, and structured plans.
*   **Business Needs:** A robust monetization model using Stripe to gate premium content.

### 2.2 The Scope Plane
The scope was defined to ensure a Minimum Viable Product (MVP) that included:
*   Full CRUD for User Routines and Meals.
*   External API integration for a comprehensive exercise library.
*   Secure payment processing.
*   Interactive JavaScript components for real-time tracking.

### 2.3 The Structure Plane
The site is divided into two distinct zones:
1.  **Public/Marketing:** High-conversion split-screen landing pages for visitors.
2.  **Private/Dashboard:** A sidebar-driven workspace for authenticated users to manage their data.

### 2.4 The Skeleton Plane (Wireframes)
The design follows a mobile-first approach to ensure accessibility for users in the gym.

| Screen | Description | Mockup Link |
| :--- | :--- | :--- |
| **Home Page** | Landing page highlighting value. | [Link](docs/wireframes/home-page-desktop.png) |
| **Routines** | Two-column builder & library. | [Link](docs/wireframes/routines-page-desktop.png) |
| **Dashboard** | Data-driven user command center. | [Link](docs/wireframes/profile-page-desktop.png) |

### 2.5 The Surface Plane (Design System)
The "Premium" feel is achieved through:
*   **Palette:** Primary Orange (`#FF5722`), Deep Grey, and Cream.
*   **Typography:** `Lexend` for headings (Modern/Bold) and `Roboto Flex` for body (Readable).
*   **Depth:** Use of custom floating shadows and glassmorphism.

***

## 3. Data Schema (Entity Relationship Diagram)

The application uses a complex relational structure to track user progress and manage subscription access.

| Entity | Description | Key Relationships |
| :--- | :--- | :--- |
| **CustomUser** | Extends `AbstractUser`. | 1:1 with `Subscription` |
| **WorkoutPlan** | Routine templates. | M:N with `Exercise` (via `PlanItem`) |
| **WorkoutLog** | A specific session. | 1:N with `SetLog` |
| **MealPlan** | Curated nutrition guides. | 1:N with `Meal` |
| **Subscription** | Tracks Stripe state. | 1:1 with `CustomUser` |

![ERD Schema](docs/img/ERD-Schema.png)

***

## 4. Features

### 4.1 Core Features
*   **Secure Authentication:** Powered by `django-allauth`.
*   **Interactive Workout Logger:** Dynamic, real-time logging of sets, weights, and reps.
*   **Routine Builder:** Drag-and-drop interface (SortableJS) for creating custom routines.
*   **API-Powered Library:** 100+ exercises fetched from RapidAPI ExerciseDB.
*   **Progress Visualization:** Interactive Chart.js graphs showing Volume, 1RM, and Weight history.
*   **Nutrition Hub:** A daily calorie calculator with custom meal creation and logging.

### 4.2 Monetization & Gating
*   **Stripe Integration:** Fully functional test-mode checkout for Monthly and Yearly Pro plans.
*   **Webhooks:** Automated account upgrading via Stripe webhook listeners.
*   **Tiered Access:** Free users are limited to 3 routines and 3 meal logs per day. Pro users enjoy unlimited access.

***

## 5. Testing

The testing documentation, including manual test cases, automated unit test results, code validation, and Lighthouse performance audits, can be found in the dedicated testing file:

[**View TESTING.md**](docs/TESTING.md)

***

## 6. Technologies Used
*   **Backend:** Python / Django (v6.0)
*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5.
*   **Database:** PostgreSQL.
*   **APIs:** Stripe API, RapidAPI (ExerciseDB).
*   **Storage:** Cloudinary (Media), Whitenoise (Static).

***

## 7. Deployment

### 7.1 Heroku Deployment
The project is live here: [FitTrack-Pro](https://fittrack-pro-48af9670b2de.herokuapp.com/)
1.  Connected GitHub repository to Heroku.
2.  Configured Config Vars (DATABASE_URL, SECRET_KEY, STRIPE_KEYS, CLOUDINARY_URL).
3.  Executed `python manage.py migrate` and `python manage.py collectstatic`.

### 7.2 Local Development
1.  Clone repo.
2.  Install requirements: `pip install -r requirements.txt`.
3.  Set variables in `env.py`.
4.  Run `python manage.py runserver`.

***

## 8. Credits

### 8.1 Content & Data
*   **Exercise Library:** Data/GIFs provided by [ExerciseDB via RapidAPI](https://rapidapi.com/justin-m-pk-m-p-m-nwovszks/api/exercisedb/).
*   **Imagery:** Photos from [Unsplash](https://unsplash.com/).

### 8.2 Code & Technology
*   **Libraries:** SortableJS, Chart.js, Canvas Confetti.
*   **Django Packages:** django-allauth, django-cloudinary-storage, whitenoise.

### 8.3 Acknowledgements
*   **Stripe Webhooks:** Logic adapted from official [Stripe Documentation](https://stripe.com/docs/webhooks).
*   **Code Institute:** For curriculum and technical support.