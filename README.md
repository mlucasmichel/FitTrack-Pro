# FitTrack Pro – Premium Fitness Planner

**FitTrack Pro** is a comprehensive full-stack web application designed for fitness enthusiasts who want a professional, data-driven approach to their workout and meal planning. 

***

## Table of Contents
1. [**Project Overview**](#1-project-overview)
2. [**UX & Design**](#2-ux--design)
    * [2.1 Design Process](#21-design-process)
    * [2.2 Wireframes](#22-wireframes)
3. [**Features (User Stories)**](#3-features-user-stories)
    * [3.1 New User (Visitor)](#31-new-user-visitor)
    * [3.2 Registered User (Non-Subscriber)](#32-registered-user-non-subscriber)
    * [3.3 Subscriber (Premium User)](#33-subscriber-premium-user)
4. [**Technologies Used**](#4-technologies-used)

***

## 1. Project Overview

### 1.1 Goal & Value Proposition
**FitTrack Pro** provides a premium platform for users to manage their fitness journey. By authenticating and subscribing, users unlock customized workout programs and detailed meal plans, ensuring their fitness goals are met with professional guidance.

**The application provides value by:**
* Offering structured workout and meal plans tailored to user goals.
* Providing premium content through a secure Stripe-powered subscription model.
* Enhancing the user experience with interactive tools like a calorie calculator and progress trackers.

***

## 2. UX & Design

### 2.1 Design Process
The design follows a mobile-first approach to ensure accessibility for users who may be tracking their progress while at the gym.

### 2.2 Wireframes
The following wireframes were created to map out the user flow and ensure a consistent responsive experience across mobile, tablet, and desktop devices.

| Screen | Description | Mockup Link |
| :--- | :--- | :--- |
| **Home Page** | Initial landing page highlighting the app's value. | [`home-page-desktop.png`](docs/wireframes/home-page-desktop.png) / [`home-page-tablet.png`](docs/wireframes/home-page-tablet.png) / [`home-page-mobile.png`](docs/wireframes/home-page-mobile.png) |
| **Login Page** | Simple and secure user authentication. | [`login-page-desktop.png`](docs/wireframes/login-page-desktop.png) / [`login-page-mobile.png`](docs/wireframes/login-page-mobile.png) |
| **User Profile** | Personal hub for user details and subscription status. | [`profile-page-desktop.png`](docs/wireframes/profile-page-desktop.png) / [`profile-page-mobile.png`](docs/wireframes/profile-page-mobile.png) |
| **Workout Routines** | List of available workout plans. | [`routines-page-desktop.png`](docs/wireframes/routines-page-desktop.png) / [`routines-page-mobile.png`](docs/wireframes/routines-page-mobile.png) |
| **Navigation** | Mobile-specific menu for easy access. | [`nav-menu-mobile.png`](docs/wireframes/nav-menu-mobile.png) |

***

## 3. Data Schema (Entity Relationship Diagram)

### 3.1 Core Entities & Relationships
The application is built on a relational structure designed to manage premium content access and track fitness/nutrition data over time.

| Entity | Description | Key Relationships |
| :--- | :--- | :--- |
| **CustomUser** | Extends Django's `AbstractUser`. | 1:1 with `Subscription`, 1:N with `WorkoutLog`, `MealLog`, `UserProgress` |
| **Subscription** | Tracks Stripe payment and status. | 1:1 with `CustomUser`, 1:N with `PlanTier` |
| **WorkoutPlan** | A collection of exercises. | M:N with `Exercise` (via `PlanItem`) |
| **Exercise** | Individual movement details. | M:N with `WorkoutPlan` |
| **MealPlan** | A collection of specific meals. | 1:N with `Meal` |
| **Meal** | Individual food items/recipes. | 1:N with `MealPlan`, 1:N with `MealLog` |
| **UserProgress** | Metrics for interactive charts. | 1:N with `CustomUser` |

![ERD Schema](docs/img/ERD-Schema.png)

***

## 4. Features

### 4.1 Completed Features (Sprints 1 & 2)

#### Authentication & User Management
*   **Secure Registration/Login:** Powered by `django-allauth` for industry-standard security.
*   **Custom User Profile:** Users can view their account details and current subscription status via a dedicated dashboard.
*   **Split-Screen Auth UI:** A high-conversion, professional "SaaS-style" login and registration interface that provides a premium first impression.

#### Workout Tracking & Exercise Library
*   **API-Driven Exercise Library:** The application automatically fetches and categorizes over 100+ professional exercises from the RapidAPI
ExerciseDB, complete with instructional text and animated GIFs.
*   **Search & Filter:** Users can rapidly find exercises by searching by name or filtering by target muscle group.
*   **Interactive Workout Logger:** A dynamic, JavaScript-powered interface allowing users to build custom workout sessions and log multiple sets,
weights, and reps in real-time.
*   **Visual Progress Analytics (Chart.js):** A dynamic dashboard on every exercise page that aggregates the user's `SetLog` data to display their
Volume History, Heaviest Weight, and Estimated 1RM over time.

#### Nutrition & Calorie Calculator
*   **Custom Meal Logging:** Users can log individual meals and specify portion sizes (servings).
*   **Real-time Calorie Calculator:** A JavaScript engine fetches the user's daily `MealLog` data to dynamically render a "Calories Remaining" ring
chart and macro progress bars (Protein, Carbs, Fats) against daily goals.

### 4.2 Future Features (Sprint 3 - Monetization)
*   **Stripe Checkout:** Secure payment gateway allowing users to upgrade from a Free to a Premium account.
*   **Premium Content Gating:** Specialized workout and meal plans that are locked behind the active Stripe subscription.

***

## 5. Technologies Used
* **Backend:** Python / Django
* **Frontend:** HTML, CSS, JavaScript (Vanilla JS)
* **Database:** Relational (PostgreSQL/MySQL)
* **Payments:** Stripe API
