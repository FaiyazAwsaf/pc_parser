# PC Parser – The Ultimate PC Components Marketplace & Build Assistant

## Overview

**PC Parser** is a web application designed to be the definitive platform for PC builders and buyers in Bangladesh. It combines a standardized global database of component specifications with real-time price and availability data from the country’s top tech retailers. Users can compare, research, and build their dream PC—all on a modern, mobile-friendly platform.

---

## Key Features

- **Standardized Global Specs:** All component specs (CPU, GPU, RAM, etc.) are normalized in a central PostgreSQL database, making search and comparison reliable and meaningful.
- **Bangladesh Price Comparison:** Instantly compare prices and stock for every component across Startech, Techland, and Ryans.
- **AI Build Assistant:** Chat with an LLM-powered assistant for PC building advice, budget builds, and personalized recommendations.
- **User Marketplace (Planned):** List, buy, and sell used PC parts with a peer-to-peer marketplace experience.
- **Modern UI:** Responsive, fast frontend built with Vue 3, Vite, and Tailwind CSS. All data fetched via Django REST APIs.

---

## Technical Approach

- **Backend:** Django & Django REST Framework (DRF) power the APIs; PostgreSQL handles relational data; Celery scheduled tasks keep prices and availability up to date.
- **Frontend:** Built with Vue 3 + Tailwind CSS for a smooth, modern, and mobile-friendly user experience.
- **Data Pipeline:** Python scraping scripts regularly fetch data from each retailer, with fuzzy matching and normalization logic to reconcile different product names and specs.
- **LLM Integration:** An API endpoint connects to a hosted LLM (Groq, OpenAI, etc.) for AI-powered chat and build recommendations.

---

## Why Is It Unique?

- **Bangladesh-first:** The only platform with real-time, cross-store PC part comparison for the Bangladesh market.
- **Universal Specs:** No more confusing or inconsistent specs—users always see apples-to-apples product info.
- **AI Support:** From part picking to troubleshooting, the AI chat assistant helps everyone build better PCs, faster.

---
