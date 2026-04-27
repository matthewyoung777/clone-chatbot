# About Me

## Background

I'm a full-stack software engineer with a background in economics. I got into coding a bit later than most — I worked for a few years after college before deciding to make the switch and join a bootcamp. Since then I've been building things on my own time, picking up new tools as I go, and trying to get better at both the frontend and backend sides of things. I like building stuff that actually gets used, not just toy projects.

## Education

I went to the University of Washington in Seattle for undergrad, where I majored in Economics with a focus on statistics and data analysis. After a few years in the working world I realized I wanted to go deeper into tech, so I joined HackReactor — a pretty intense 5-month, 10-hour-a-day bootcamp where I learned to build full applications from scratch in Python and JavaScript. It was brutal but worth it.

## Hobbies

### NBA Basketball (Golden State Warriors)

I've been a Warriors fan since 2006 — the "We Believe" era with Baron Davis. Been through the highs and lows. Watching Steph Curry develop from a somewhat overlooked draft pick into arguably the best shooter ever has been the highlight of being a fan.

### Premier League Soccer (Tottenham Hotspur)

I support Spurs, which means I spend a lot of time hoping and not a lot of time celebrating. Son Heung-min is my favorite player on the squad. It can be painful supporting them but I'm not going anywhere.

### Video Games

I consider them sports, genuinely.

- **Overwatch** – Hit Grandmaster rank, so I'm pretty comfortable saying I'm decent. I main Genji and Ana, which is kind of a weird combo but it works for me.
- **The Witcher 3** – One of the best RPGs ever made. The world-building and side quests are better than most games' main stories.
- **Subnautica** – Survival/exploration game set entirely underwater. Genuinely unsettling in the best way — nothing like the feeling of descending into deep water not knowing what's down there.

### Tennis

Played a lot growing up, junior high and high school. My best shot was ironically my two-handed backhand. Still pick up a racket occasionally.

### Music (Piano & Trumpet)

I played both piano and trumpet when I was younger. Don't really play anymore but I still listen to a lot of classical and jazz.

## Favorite Foods

- **Ramen** – Good broth, firm noodles, solid toppings. Hard to beat.
- **Dumplings** – Any style. Steamed, pan-fried, soup dumplings — all of it.
- **Pizza** – Sausage and pepperoni, no notes.

## Favorite TV Shows

I gravitate toward dramas, dystopian stuff, and sci-fi.

- **Breaking Bad** – Probably the best-written show I've seen. The character arc is just unreal.
- **Black Mirror** – Not always easy to watch but it makes you think. Love the anthology format.
- **Dark** – German time travel show on Netflix. Incredibly dense and well-constructed — the way they tie everything together across three seasons is genuinely impressive. Subtitles required but absolutely worth it.
- **Demon Slayer** – My favorite anime. The animation is stunning and the fights are some of the best I've seen in any medium.

## Favorite Movies

- **Interstellar** – The score, the visuals, the time stuff. Gets me every time.
- **Ocean's 11** – Just a fun, well-made heist movie. Great cast, great pacing.
- **Tron Legacy** – The Daft Punk soundtrack alone puts this in my top list.
- **RV** – Look, it's not a prestige film. It's just a good time.

# Projects

## Forge Fitness

**September 2023 – Present** (part-time side project)

Forge Fitness is a workout app I'm building with a couple of friends. The idea is to make working out feel more like a game — you earn points, rank up, unlock stuff. We thought most fitness apps were either too clinical or too fluffy, so we wanted something that actually felt engaging to use.

It's built around a forge/anvil theme. You can build custom workouts or auto-generate them based on your goals and what muscle groups you want to hit. There's a ranking system with tiers (Bronze through Diamond) and a battle pass-style progression that unlocks rewards over time. The app also tracks your sets, reps, and weights over time so you can see actual progress, and we're working in some AI-powered suggestions that adapt based on your workout history.

**Tech:** React Native + Expo (TypeScript), Node.js + Express backend, MongoDB, OpenAI API (GPT-4), deployed on Render. Team of 3 working part-time.

---

## Tea Run

Tea Run is an app I built solo for coordinating group tea and coffee runs — the kind where someone's heading to a café and wants to grab drinks for the whole team. You create a group, start a run, set a deadline, and your teammates drop their orders in before you leave. The runner gets one clean screen with everyone's orders and Venmo links for payment.

It's live on the App Store. Landing page at [tea-run.com](https://tea-run.com/).

The interesting technical parts were getting realtime order syncing to work smoothly (Supabase Realtime subscriptions on the orders table), and dealing with Supabase's Row Level Security policies for group membership without causing infinite recursion — ended up using a `SECURITY DEFINER` helper function to handle that cleanly.

**Tech:** React Native + Expo SDK 54 (TypeScript), React Navigation, Supabase (Postgres + Realtime + Auth), passwordless magic link login via Resend, expo-secure-store for session persistence.

---

## Paper Stonks

Paper Stonks was a paper trading web app I built with a small team during my bootcamp — we had about 1.5 months to put it together. The idea was to let people practice buying and selling stocks with fake money, so they could experiment with strategies without any real risk.

Users start with a set amount of virtual funds, can look up stock price history, make trades, and track how their portfolio is doing over time. We pulled real market data from Alpha Vantage and visualized it with Chart.js. It's not live anymore but it was a solid project for the time frame we had.

**Tech:** React.js frontend, FastAPI (Python) backend, JWT auth, Alpha Vantage API, Chart.js, previously hosted on Heroku with Docker for the microservices.

---

## RAG Clone Chatbot

This one is pretty meta — it's a chatbot that's supposed to answer questions as if it were me. I feed it information about my background, projects, work history, and interests, and it uses RAG (Retrieval-Augmented Generation) to pull the relevant context and respond in first person.

When someone asks a question, it embeds the query, finds the closest matching chunks from my knowledge base via cosine similarity, and passes that context to GPT-4o-mini which responds as me. It works better than I expected honestly.

**Tech:** FastAPI (Python), PostgreSQL with pgvector, OpenAI gpt-4o-mini, text-embedding-ada-002 for embeddings, deployed on Render.

# Work Experience

## Test Engineer – Quanta Manufacturing Fremont

_Apr 2025 – Present_

- Defined and supported test processes for production hardware — servers, switches, storage devices, fully configured racks
- Developed test scripts and test plans covering functional and system-level validation
- Worked closely with R&D, Test Development, and Manufacturing to analyze test data, troubleshoot defects, and document results
- Built automated test processes to improve reliability and consistency across new and existing hardware

## Software Engineer Intern – MiniMe AI

_Apr 2024 – Dec 2024 · 9 months_

- Built a RAG system in Python using LangChain and pgvector to enhance the product's AI features
- Built a data preprocessing pipeline for crawling, cleaning, and transcribing content to improve RAG data quality
- Improved development efficiency by ~50% by packaging reusable Python modules across the team

## Software Engineer Intern – Networky.ai

_Oct 2023 – Apr 2024 · 7 months_

- Built and optimized a mobile-friendly site for on-the-go networking
- Built a product metrics dashboard using SQL queries that helped surface marketing insights and contributed to a 15% increase in user acquisition
- Documented the development lifecycle, architecture, and deployment processes for the team
- Worked primarily in Python and JavaScript

## Autonomous Vehicle Test Specialist – Cruise

_Nov 2019 – Jul 2022 · 2 years 9 months_

- Expanded drivable testing zones by 50% through lane and route mapping
- Identified and reported problematic vehicle behavior to engineers, helping reduce errors by 30%
- Trained fleet operators on new testing techniques, which increased driverless mileage accumulation by 100%
