# Projects

## Forge Fitness Project

**September 2023 – Present** (Part-time side project)

### Overview

Forge Fitness is a mobile application designed to enhance users' fitness journey in a gamified way. It includes:

- Personalized workout plans
- Real-time progress tracking
- An engaging ranking system to encourage consistency

Built around a **Forge/Anvil theme**, the app provides an immersive experience where users can:

- Craft or auto-generate workouts
- Track performance
- Complete challenges
- Unlock achievements

### Key Features

#### Personalized Workout Generator

- Users create workout routines based on goals (strength, toning, weight loss)
- Dynamic generator customizes workouts based on selected focus areas (e.g., biceps, triceps, shoulders)
- **Challenge System** rewards users with points and achievements

#### Rank System with Battle Pass Theme

- Users earn points for workouts and exercises
- **Rank tiers:** Bronze, Silver, Gold, Platinum, Diamond
- **Battle Pass progression system** unlocks rewards over time

#### Exercise Templates & Custom Workouts

- Access a database of hundreds of exercises
- Covers compound (squats, deadlifts) & isolation exercises
- Users can build custom workouts from scratch

#### Performance Tracking & Analytics

- Logs workouts, sets, reps, and weights
- **Visual dashboards** for progress insights
- Tracks improvements in strength, endurance, and growth

#### AI-Powered Smart Recommendations

- Learns from user workout data
- Suggests improvements, variations, and new challenges
- Helps break plateaus with adaptive feedback

### Future Development Plans

- **Enhanced AI** for smarter workout recommendations
- **Wearable integration** for real-time tracking
- **Community features** (challenges, competition with friends)
- **More complex ranking system** for exclusive unlocks

### Join the Forge Fitness Journey

Whether you're a beginner or an experienced athlete, Forge Fitness provides:

- **Tools** for structured training
- **Motivation** through gamification
- **A community** to stay accountable

### Tech Stack Overview

#### Frontend (Mobile App)

- **Expo:** Cross-platform development for iOS & Android
- **React Native:** UI built with TypeScript & React

#### Backend (API)

- **Node.js & Express.js:** RESTful API for handling logic
- **JWT (JSON Web Tokens):** Secure authentication
- **MongoDB:** NoSQL database for workouts & user data

#### Machine Learning & AI

- **OpenAI API (GPT-4):** Chatbot for fitness guidance

#### Infrastructure & Deployment

- **Render:** Cloud hosting with CI/CD and scaling

### Development Processs

- **Lead Developer:** Oversees project vision & execution
- **Team of 3 developers:** Experienced colleagues working part-time
- **Agile workflow:** Bug reporting, prioritization, and communication
- **Documentation:** API details, consistent styling, code-typing

---

## Paper Stonks Project

### Overview

Paper Stonks is a web application designed for paper trading, allowing users to buy and sell stocks without real money while testing portfolio strategies. The platform enables users to simulate real-world trading experiences, track portfolio performance, and analyze stock price history with interactive charts. Built over just 1.5 months as a small team during a coding bootcamp, Paper Stonks was designed to provide an intuitive and educational environment for users to practice trading without financial risk.

### Features

- **Fake Funds Management:** Users start with a predefined amount of virtual money and can add more to test different trading strategies. This allows them to experiment with riskier trades, diversification, and portfolio management techniques.

- **Paper Trading:** Users can buy and sell stocks using virtual funds, simulating real market transactions. The app tracks purchase prices, trade history, and profit/loss over time to give users a realistic investing experience.

- **Stock Price History:** Users can access historical stock price data visualized through **Chart.js**. This feature helps traders analyze trends, spot patterns, and make more informed buying or selling decisions. The app fetches real-time and past market data from **Alpha Vantage**, ensuring accurate information.

- **Portfolio Tracking:** The application continuously updates the user’s portfolio, displaying overall account value, individual stock holdings, percentage gains/losses, and past trade performance. This helps users refine their strategies over time based on simulated returns.

### Tech Stack

- **Frontend:** Built with **React.js**, providing a dynamic and responsive user interface for seamless trading interactions.

- **Backend:** Powered by **FastAPI (Python)**, ensuring fast, asynchronous API responses for stock queries and trade executions.
-
- **Authentication:** Secure user access is managed with **JWT-based authentication (JSON Web Token)**, ensuring safe login sessions and account security.

- **Microservices Architecture:** The application is designed with dedicated services for authentication and trading, enabling scalability and better system organization.

- **Stock Data API:** Real-time and historical stock market data is retrieved from **Alpha Vantage**, giving users up-to-date insights into stock performance.

- **Charts & Visualization:** Implemented using **Chart.js** to generate interactive graphs for stock price trends, portfolio value changes, and performance analytics.

- **Deployment:** The platform is no longer but was hosted using **Heroku**, with **Docker containers** for managing microservices for authentication and trading logic.
