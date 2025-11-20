# Rental Data

# Using AI to Pull Rental Comps & Market Leasing Data (Zillow-Based)

<aside>
⌨️

**Current Prompt: [NOT WORKING]**

*You are a rental market analyst for my residential property management company based in Cincinnati, OH. You collect market data from publicly available websites, analyze the data, and populate a spreadsheet with your analysis. My company has two purposes for this data. The lesser purpose is to have comprehensive information about the competition for our own active rental listings. The greater purpose is to generate a set of proprietary market data over time that allows us to monitor the fluctuations of supply and demand for rental housing as you are prompted to retrieve and analyze this data over time.*

*Market Data Platform:  Use all relevant active rental listings on the Zillow website. Use only the Zillow website, disregard any other rental listing platforms.*

*Geographic Area:  the Zip Code or Codes you are given in each individual prompt*

*Property Types:  0-1 bedroom apartments, 2 bedroom apartments, 3+ bedroom apartments, 1-2 bedroom single family homes and townhouses, 3 bedroom single family homes and townhouses, 4+ bedroom single family homes and townhouses*

*Data Points per property type:  exact number of active listings available, median “days ago” that the listings were posted, median listed rent amount*

*Generate a data table where each row is a property type and each column is a data point corresponding to its property type. Be sure to use every single active rental listing in your analysis. Please also indicate the time and date that your analysis was generated, and the zip code for the data in the table.*

*Please generate the table for 45223.*

</aside>

### Process with TLP Team

## 1. Purpose

This SOP defines how TLP uses AI (ChatGPT / custom GPT) to:

- Pull **rental comps** and **market-level leasing data** from Zillow.
- Track key metrics over time (days on market, rents, unit count, etc.).
- Turn that data into **clear, proactive communication** for landlord clients.

The goal is to (a) underwrite more accurately, (b) explain leasing slowdowns with data instead of vibes, and (c) build TLP’s brand as the local data-driven expert.

---

## 2. Scope

This SOP applies to:

- All residential rental listings in **Greater Cincinnati** (initial focus), later expandable to other markets.
- All TLP-managed properties, with special focus on those with **leasing challenges** (e.g., Glen Parker 1589, 99, Parker Woods Flats, etc.).
- Team members: **Eric**, **Izzy**, **Ian**, and any leasing/operations staff supporting this process.

---

## 3. Definitions

- **Rental Comp:** A currently available or recently rented unit similar to our subject property (same zip, similar beds/baths, property type, location profile).
- **Market Metrics (Zillow-based):**
    - **Avg Days on Market (DOM):** Mean days since listing went live, by zip and unit type.
    - **Unit Count:** Total number of available units meeting the filter criteria.
    - **Avg Asking Rent:** Mean asking rent for active listings by unit type.
- **Internal Metrics (TLP proprietary):**
    - Showings per week/month (by property & portfolio).
    - Applications received.
    - Lease-ups / move-ins.
    - Occupancy by property / portfolio.

---

## 4. Tools & Data Sources

- **Primary market data source:** Zillow (public site + Zillow account reporting).
- **AI tool:** ChatGPT / custom GPT configured for:
    - Reading Zillow pages (via copy/paste or assisted browsing, within Zillow’s terms of use).
    - Structuring and summarizing data into tables and time-series.
- **Storage & Reporting:**
    - Google Sheets / Excel workbook: `TLP – Market Leasing Dashboard`.
    - CRM (for client communication + newsletter).
    - Optional: Notion/Docs for narrative summaries.

> Note: All data collection must respect the terms of service of Zillow and any other websites used.
> 

---

## 5. Roles & Responsibilities

- **Eric (AI + Analysis Lead):**
    - Owns the **AI workflow** and prompt templates.
    - Runs weekly/monthly **Zillow data pulls** using ChatGPT.
    - Maintains the **Market Leasing Dashboard** spreadsheet.
    - Produces a short **market summary** (internal + client-facing).
- **Izzy (Zillow Account & Comparative Insights):**
    - Reviews **Zillow account reports** (for our listings).
    - Compares **TLP listing performance vs. market averages** by zip/unit type.
    - Flags **problem assets** (e.g., high DOM, low showing volume) for deeper review.
- **Ian (Client Communication & Strategy):**
    - Turns data into **plain-English messaging** for landlords.
    - Oversees **newsletter / CRM-driven updates**.
    - Ensures early, even anecdotal, communication goes out **before** a problem feels like a crisis.

---

## 6. Process Overview

**Cadence:**

- **Weekly:** Quick pull for core metrics (DOM, unit count, avg rents) for priority zips.
- **Monthly:** Deeper analysis, trend charts, and client-facing commentary.
- **Ad hoc:** Subject-property rental comps when pricing or re-pricing a specific unit.

**Core Steps:**

1. Define zips & unit types to track.
2. Use AI to help pull and structure Zillow data.
3. Clean and store data in the dashboard.
4. Compare **market vs. TLP internal metrics**.
5. Draft **insights + client messaging**.
6. Publish via CRM/newsletter and specific landlord updates.

---

## 7. Detailed Procedure

### 7.1. Set Up Tracking Framework (One-Time + Occasional Updates)

**Owner:** Eric

1. **Define geographies:**
    - Create a list of **priority zip codes** (e.g., 45211, 45238, etc.).
    - Note any **school districts / submarkets** that matter (for future segmentation).
2. **Define unit categories:**
    - Unit types: `0–1 BR`, `2 BR`, `3+ BR`.
    - Property type flags: `Apartment`, `Single-Family`, `Duplex/Small Multi`.
3. **Create the dashboard:**
    - Google Sheet tabs:
        - `Raw_Zillow_YYYY` – weekly snapshots.
        - `Trends_DOM` – pivot tables/charts (DOM over time).
        - `Trends_Rents` – avg rents over time.
        - `Unit_Counts` – supply over time.
        - `TLP_Internal` – showing counts, applications, occupancies.
        - `Client_Reports` – formatted tables for copy/paste into newsletters.

---

### 7.2. Weekly Zillow Data Pull (AI-Assisted)

**Owner:** Eric

**Timing:** Once per week (e.g., every Monday)

### 7.2.1. Prepare Inputs

1. List the **zip codes** to pull this week.
2. For each zip, decide if you’re running:
    - **All units**, or
    - Separate runs by **unit type** (0–1 BR, 2 BR, 3+ BR).

### 7.2.2. Use ChatGPT to Structure Data

You or a VA can:

1. Navigate to Zillow search results for each zip and unit type.
2. Copy the **listing results section** (addresses, rents, beds/baths, DOM if visible, or listing dates).
3. Paste into ChatGPT with a structured prompt like:

> Prompt Template – Market Snapshot
> 
> 
> “You are helping a property management company analyze the current rental market in Greater Cincinnati.
> 
> I will paste Zillow search results for [ZIP CODE], filtered to [UNIT TYPE description: e.g., ‘1 bedroom apartments’].
> 
> From this text, extract and return a **clean table** with the following columns:
> 
> - Address
> - Zip Code
> - Property Type (if you can infer)
> - Beds
> - Baths
> - Asking Rent
> - Days on Market (or calculated days based on listing date and [TODAY’S DATE])
> - Link (if available in the text)
>     
>     Then calculate and summarize:
>     
> - Average Days on Market
> - Median Days on Market
> - Total Number of Active Listings
> - Average Asking Rent
>     
>     Please ignore obvious outliers (e.g., listings with absurdly high days on market) in a separate ‘Outliers’ section, but still include them in the raw table. Return the result as a markdown table followed by a short written summary in plain English.”
>     
1. Copy the resulting table into the `Raw_Zillow_YYYY` tab:
    - Add columns for `Date Pulled`, `Zip`, `Unit Category`.

### 7.2.3. Quality Check

- Spot-check a few listings to ensure:
    - Bed/bath counts and rents look right.
    - DOM calculations are reasonable (no negative/insane values).
- Ensure outliers (e.g., 154 DOM listing) are **flagged** but not removed from raw data.

---

### 7.3. Monthly Trend Analysis

**Owner:** Eric

**Support:** Izzy

1. In Google Sheets:
    - Create/update pivot tables:
        - **Avg DOM by Zip & Unit Type over time.**
        - **Avg Rent by Zip & Unit Type over time.**
        - **Unit Count by Zip & Unit Type over time.**
2. Compare **this month vs. prior months**:
    - Is DOM increasing or decreasing?
    - Are rents softening, holding, or increasing?
    - Is supply (unit count) rising in problem zips?
3. Document key **headline insights** in `Client_Reports` tab, e.g.:
    - “In 45211, avg DOM for 1BRs increased from 18 days in June to 29 days in October.”
    - “Available 2BR units in 45238 increased by 40% since July.”

---

### 7.4. Internal Metrics & Benchmarking

**Owner:** Izzy (with ops support)

1. Pull internal stats from your leasing system:
    - Showings per week, by property.
    - Applications per week, by property.
    - Current occupancy for each building.
2. For priority properties (e.g., Glen Parker 1589 & 99, Parker Woods Flats):
    - Compare **property-level performance** vs. market:
        - DOM vs. market average DOM.
        - Current occupancy vs. “normal” for that asset class/submarket.
3. Summarize performance:
    - Example:
        - “45211 1BR avg DOM: 25–30 days. Glen Parker 1589 1BR units: 32 DOM on average — slightly slower than market but within the current range.”

---

### 7.5. Subject-Property Rental Comps (Ad Hoc Use Case)

**Owner:** Any leasing/asset manager; AI support by Eric

When pricing a specific unit (new listing or re-pricing):

1. Gather **basic property info:**
    - Address, zip.
    - Beds/baths, sq ft.
    - Property type (apartment vs SFR).
    - Special features (parking, new reno, etc.).
2. Use a targeted ChatGPT prompt:

> Prompt Template – Rental Comps for a Specific Unit
> 
> 
> “You are supporting a property management company in pricing a rental unit.
> 
> Subject property: [Address, City, Zip, Beds/Baths, Property Type, features].
> 
> Below is copied text from Zillow search results for similar rentals in [ZIP + nearby zips if relevant].
> 
> Please:
> 
> 1. Identify the 5–10 best comps (most similar in location, unit type, rent level).
> 2. Create a table with: Address, Beds, Baths, Asking Rent, Days on Market, Notes (e.g., newer, parking, upgraded).
> 3. Recommend a target asking rent and a **positioning strategy** (e.g., ‘price slightly below market to reduce DOM’ or ‘match market and emphasize upgrades’).
> 4. Add a short explanation we can share with a landlord in plain English.”
1. Copy results into the property’s asset file / leasing notes.

---

## 8. Client Communication Workflow

### 8.1. Early, Anecdotal Outreach (Even Before Data Is Robust)

**Owner:** Ian (with CRM support)

1. When leasing feels slow (e.g., showings noticeably down):
    - Send a brief **“market pulse” email** to affected landlords:
        - “We’re seeing a slower leasing season this quarter than prior years. We’re monitoring both our internal showings and Zillow data and will share detailed updates as we gather more.”
2. Purpose:
    - Set expectations early.
    - Build trust that TLP is **paying attention**, not reacting late.

### 8.2. Monthly Market Update / Newsletter

**Owner:** Ian & Eric

1. Use the `Client_Reports` tab to build:
    - 2–4 simple charts (DOM trend, avg rent, unit count).
    - 3–5 bullet point takeaways.
2. Draft a **newsletter-style summary**, e.g.:
- “Leasing activity slowed in July–August but picked up in October and November.”
- “In the 45211 zip code, avg DOM for 1BRs increased ~10 days versus last year.”
- “Our portfolio is performing slightly **better than the market** on DOM, suggesting pricing and product are in line, but demand is softer overall.”
1. Push via CRM to:
    - All landlord clients.
    - Prospective clients (marketing angle: ‘TLP Market Intelligence’).

### 8.3. Property-Specific Reporting

**Owner:** PM/Asset Manager, with data from Eric/Izzy

For a landlord of a particular building (e.g., 99 or Glen Parker 1589):

1. Prepare a short, focused note:
- 1 paragraph: What’s happening in the **broader market** (based on Zillow data).
- 1 paragraph: How **their property** compares (DOM, showings, rent vs comps).
- 1–2 bullets: Recommended actions (price adjust, marketing tweak, incentive, or “hold steady”).
1. Example structure:

> “We’re seeing avg days on market for comparable 1BR units in 45211 at around 28–30 days. Your units at [Property] are averaging 32 days, which is slightly slower but still in line with the current softening demand.
> 
> 
> Our recommendation is to [adjust rent / hold price / add promotion], and we’ll continue to monitor DOM and inquiry volume weekly.”
> 

---

## 9. Strategic & Marketing Use

**Owner:** Ian & Marketing

- Use this dataset to position TLP like **RL Property Management / Peter Lohman**:
    - Share **simple charts** on LinkedIn, blog posts, and in decks.
    - Reference “According to our weekly Zillow-based leasing tracker…” to establish authority.
- Over time (12+ months), use **year-over-year** Zillow data plus **internal TLP data** to:
    - Show how TLP performs vs. market during good and bad leasing seasons.
    - Support case studies and investor presentations.

---

## 10. Implementation Checklist

**This Week (Kickoff):**

- [ ]  Finalize list of **priority zip codes & unit types**.
- [ ]  Create `TLP – Market Leasing Dashboard` Google Sheet.
- [ ]  Eric builds & tests **ChatGPT prompt templates** (market snapshot + subject comps).
- [ ]  Izzy logs into Zillow account and identifies available reporting exports.

**This Month:**

- [ ]  Run **weekly** Zillow pulls for at least 3–4 weeks.
- [ ]  Start logging **internal showings & occupancy** into the dashboard.
- [ ]  Produce first **monthly market summary** (even if light).
- [ ]  Send first **client market pulse email** / newsletter.

**Next 12 Months:**

- [ ]  Maintain consistent weekly/monthly pulls to build **year-over-year** data.
- [ ]  Refine prompts and charts as needed.
- [ ]  Integrate data snapshots into **pitch decks, owner calls, and quarterly reviews**.

### Process with N8n

## 1. High-Level Automation Architecture

**Goal:**

Every week/month, automatically:

1. Pull Zillow market data by zip & unit type
2. Store metrics (DOM, rent, unit count) in a database
3. Compare to your internal leasing data
4. Have AI generate:
    - Market summary
    - Per-property owner updates (if needed)
5. Push straight to your CRM/email provider – no human.

**Core pieces:**

- **n8n Workflows**
    - `WF1 – Market Data Ingestion (Zillow)`
    - `WF2 – Internal Data Sync (Showings/Occupancy)`
    - `WF3 – Market Analysis & Trend Builder`
    - `WF4 – Client Communications (Newsletter & Owner Alerts)`
    - `WF5 – Property-Specific Rental Comp Generator (event-based)`
- **AI Agents (via OpenAI/ChatGPT API)**
    - **Parser Agent** – turns raw Zillow data/HTML/CSV into structured rows + metrics.
    - **Analyst Agent** – finds trends, compares TLP vs market, flags issues.
    - **Copywriter Agent** – writes landlord-safe, plain-English explanations & newsletters.
- **Storage**
    - Database (Postgres/MySQL/Airtable) OR a Google Sheet (quick & dirty).
    - Key tables: `zillow_snapshots`, `market_metrics`, `internal_metrics`, `owner_messages`.

---

## 2. WF1 – Zillow Market Data Ingestion (Automated)

**Trigger:** n8n **Cron** node

- Weekly (e.g., Monday 6 AM) + Monthly (e.g., 1st day of month) runs.

**Config storage:**

- Use a table or Google Sheet: `market_config`
    - Columns: `zip_code`, `unit_type_group` (0–1 BR / 2 BR / 3+ BR), `active=true/false`

### Steps

1. **Cron → Read Config**
    - `Cron` → `Google Sheets / DB Read` node to pull list of zips & unit types.
2. **Loop Over Zips & Unit Types**
    - `Split In Batches` node over rows.
3. **Fetch Zillow Data (Machine Only)**
    - Preferred: use **official API or export/reporting** if Zillow provides it for your account.
    - If not, use:
        - A headless browser / scraping service (e.g., Browserless, Apify, your own Playwright service) behind an **HTTP Request** node.
    - Output: **raw HTML/JSON/CSV** for “rentals in ZIP X with beds=Y” as text.
4. **AI Parser Agent**
    - `HTTP Request` → `OpenAI/LLM` node (Parser Agent).
    - Prompt example:
        
        > “You are a data parser for a property management company.
        > 
        > 
        > I’ll give you raw Zillow page content or CSV for rentals in ZIP [ZIP] for [UNIT TYPE].
        > 
        > 1. Extract each listing as JSON with fields:
        >     - address, zip, property_type, beds, baths, asking_rent, listing_date (if present), days_on_market (calculate relative to [TODAY]), listing_url
        > 2. Return JSON: `{ "listings": [...], "metrics": { "avg_dom": X, "median_dom": Y, "unit_count": Z, "avg_rent": R } }`
        > 3. If some fields are missing, leave them null but keep the listing.”
    - n8n parses LLM response with a `JSON Parse` node.
5. **Store Raw & Metrics**
    - `Database` node(s) to insert:
        - Raw listings into `zillow_snapshots`:
            - `pull_date`, `zip`, `unit_type`, `address`, `beds`, `baths`, `rent`, `dom`, `url`, `source="zillow"`
        - Summary metrics into `market_metrics`:
            - `pull_date`, `zip`, `unit_type`, `avg_dom`, `median_dom`, `unit_count`, `avg_rent`
6. **Error Handling & Logging**
    - Use `Error Workflow` and `IF` nodes in n8n:
        - If LLM error or 0 listings returned, log row to `failed_runs` table and continue with next zip/unit.
    - No human intervention; errors are just logged.

> Outcome: every week you have fresh, structured Zillow data in your DB, captured entirely by bots.
> 

---

## 3. WF2 – Internal Data Sync (Showings & Occupancy)

**Trigger:** Another **Cron** (daily or weekly).

### Steps

1. **Pull from Your PM/CRM System**
    - `HTTP Request` / `Database` node to:
        - Get **showings per property**, **applications**, **leases signed**, **current occupancy**.
2. **Transform**
    - `Function` node to normalize:
        - `property_id`, `date`, `showings`, `applications`, `leases`, `occupancy`.
3. **Store**
    - Insert into `internal_metrics` table.

> This gives the bots a benchmark for “how TLP is doing vs the market” automatically.
> 

---

## 4. WF3 – Market Analysis & Trend Builder (AI Analyst)

**Trigger:** **Cron monthly** (e.g., 2nd of each month).

### Steps

1. **Query Aggregated Metrics**
    - `Database` node:
        - Pull last 3–6 months of `market_metrics` (by zip/unit).
        - Pull last 3–6 months of `internal_metrics`.
2. **Preprocessing in n8n (Optional)**
    - `Function` node to compute:
        - Month-over-month changes (% change DOM, rent, unit count).
        - Portfolio vs Market comparisons (e.g., `TLP_avg_dom` vs `market_avg_dom` by zip/unit_type).
3. **Send to Analyst Agent**
    - `OpenAI/LLM` node:
        
        > “You are the Market Analyst Bot for a property management company in Cincinnati.
        > 
        > 
        > I will give you JSON with:
        > 
        > - `market_metrics`: [dom, rent, unit_count by zip/unit_type for the last N months]
        > - `internal_metrics`: [showings, leases, occupancy by property and zip]
        >     
        >     Tasks:
        >     
        > 1. Identify key trends (up/down in DOM, rents, supply) by zip and unit type.
        > 2. Identify whether our portfolio is performing better/worse than the market (DOM, occupancy).
        > 3. Produce:
        >     - A bullet-point summary for internal use (technical).
        >     - A simplified bullet list for landlord clients (plain English).
        >     - A few specific talking points explaining current leasing conditions (e.g., ‘summer was unusually slow, picked up in Oct–Nov’).
        >         
        >         Return strict JSON: `{ "internal_summary": "...", "client_summary": "...", "key_stats": [...], "alerts": [...] }`”
        >         
4. **Store Analysis**
    - `Database` node: write to `monthly_analysis` table:
        - `month`, `internal_summary`, `client_summary`, `key_stats`, `alerts_json`.

> Now your “what’s going on out there?” analysis is entirely bot-driven.
> 

---

## 5. WF4 – Automated Client Communications (Newsletter + Alerts)

### 5.1 Monthly Newsletter

**Trigger:** Upon completion of `WF3` (or separate monthly Cron).

1. **Fetch Latest Client-Facing Summary**
    - `Database` node: get latest row from `monthly_analysis`.
2. **Copywriter Agent (Format & Tone)**
    - `OpenAI/LLM` node:
        
        > “You are the Communications Bot for TLP.
        > 
        > 
        > Here is this month’s client_summary and key_stats JSON.
        > 
        > Write an email newsletter to landlord clients:
        > 
        > - Subject line options (3)
        > - Email body in HTML with headings and bullet points
        > - Tone: calm, data-driven, reassuring, transparent.
        >     
        >     Avoid jargon, explain DOM and market trends in simple language.”
        >     
3. **Send via Email/CRM**
    - Use n8n’s **Mailchimp / SendGrid / HubSpot / ActiveCampaign** node (whatever you use):
        - `Create Campaign` or `Send Email` using the generated HTML.
    - Fully automated sending; no approval step if you truly want **no human intervention**.

### 5.2 Property-Specific Alerts

**Trigger:** **Cron daily/weekly**, or event-based.

1. **Identify Problem Properties**
    - `Database` node query:
        - For each property: compare internal DOM vs market DOM for its zip/unit.
        - Flag if:
            - `property_dom > market_dom * 1.3` OR occupancy below target, etc.
2. **AI Generates Owner Message**
    - For each flagged property, `OpenAI/LLM` node:
        
        > “You are Owner Messaging Bot for TLP.
        > 
        > 
        > Input:
        > 
        > - Property name and address
        > - Market stats: avg_dom, avg_rent, unit_count for the property’s zip/unit_type
        > - Property stats: current asking rent, dom, showings, occupancy
        >     
        >     Task: Write a concise email to the owner explaining:
        >     
        > 1. What we’re seeing in the broader market (DOM, demand).
        > 2. How their property compares.
        > 3. Our recommended next step (price adjustment / promo / hold steady).
        >     
        >     Tone: calm, data-backed, proactive, not defensive.
        >     
        >     Return JSON with `subject`, `body_html`.”
        >     
3. **Auto-Send**
    - `Email` / CRM node:
        - To: the owner’s email from your owner table.
        - Subject/body from LLM output.
    - Log sent messages in `owner_messages` table.

> This is the “notifications just show up in the owner’s inbox” piece—no human drafting.
> 

---

## 6. WF5 – Rental Comp Reports on Events (e.g., New Listing)

**Trigger:** **Webhook** or **Polling** to your PM software.

1. **Event Source**
    - PM system calls an n8n **Webhook** when:
        - A unit status is set to “Coming Soon” or “Vacant – To Be Listed”.
2. **Get Subject Property Data**
    - `HTTP Request` / `Database` node: pull property fields (address, beds, baths, sq ft, etc.).
3. **Fetch Zillow Data for Comps (Automated)**
    - Same mechanism as WF1 but narrower:
        - Only relevant zip + maybe a custom radius.
4. **Comp-Selection AI Agent**
    - `OpenAI/LLM` node:
        
        > “You are the Rental Comp Bot.
        > 
        > 
        > Subject property: [JSON with details].
        > 
        > Here are candidate listings from Zillow [JSON].
        > 
        > 1. Choose the 5–10 best comps (similar beds, baths, condition, location).
        > 2. Return a JSON report with:
        >     - `comps` table
        >     - `suggested_rent`
        >     - `pricing_rationale` paragraph we can send to the owner.”
5. **Send Owner Report Automatically**
    - `Email` node:
        - Subject: “Pricing Recommendation for [Property Name]”
        - Body: AI-written explanation + comps table (HTML).
6. **Store**
    - Save comp report JSON to `comp_reports` table for audit/history.

---

## 7. Guardrails & Practical Tips

- **Terms & Legality:**
    
    Make sure your data collection method respects **Zillow’s Terms of Use**. Prefer:
    
    - Official data exports / reports from your Zillow account.
    - Partner APIs, if available.
    - If you use scraping, do it responsibly and legally (rate limiting, no abuse).
- **Idempotency:**
    
    Include `pull_date + zip + unit_type` as a unique key so you don’t double-insert if a job runs twice.
    
- **Versioned Prompts:**
    
    Store prompt templates in a DB or file so you can tweak them without editing every n8n node.
    
- **Testing Mode First:**
    
    Before going fully “no human,” add:
    
    - A `test_mode` flag that sends outputs only to internal emails.
    - Once stable, flip to full automation.