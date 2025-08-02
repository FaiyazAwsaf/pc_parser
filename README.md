# PC Parser

**PC Parser** is a full-stack web app that helps users compare PC component prices, see detailed specs, and find the best deals from Bangladesh’s top tech retailers (Startech, Ryans, Techland). Features also include a second-hand component marketplace and an AI PC build assistant.

## Features

- **User Authentication:** Secure register/login, JWT-based auth, email verification, profile management.
- **Component Catalog:** Standardized global database 'PC parts picker' using [docyx/pc-part-dataset](https://github.com/docyx/pc-part-dataset).
- **Price Comparison:** Scrapes and matches prices, URLs, images, and availability from Startech, Ryans, and Techland.
- **Marketplace:** View and compare new/second-hand listings, trusted sellers highlighted.
- **AI Build Assistant:** (Planned) Recommends PC builds based on your needs.
- **Modern UI:** Built with Vue 3 and Tailwind CSS.

## Tech Stack

- **Frontend:** Vue 3, Vite, Pinia, Vue Router, Tailwind CSS
- **Backend:** Django REST Framework, PostgreSQL
- **Scraping/Matching:** Python scripts (BeautifulSoup, fuzzywuzzy/rapidfuzz)

## Project Structure

