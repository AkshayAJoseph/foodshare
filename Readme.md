# FoodShare

## 🚀 Project Description
A sustainability-driven platform that **reduces food waste** by enabling users to **list, buy, and donate near-expiry food items**. The app integrates **AI-powered expiry detection (Gemini Vision)**, **real-time updates (WebSockets)**, and **automated meal planning** to promote responsible consumption.

## 🎯 Link to Project
[live link of project](live_link)

## 🛠 Tech Stack
| **Component**          | **Technology**                                                     |
|------------------------|-------------------------------------------------------------------|
| **Frontend**           | SvelteKit (Bundled with Capacitor for mobile)                     |
| **Backend**            | Go (Cloud Server)                                                 |
| **AI (Vision & Text)** | Gemini Vision API (Food Recognition, Expiry Extraction, Recipe Generation) |
| **Database**           | PostgreSQL (NeonDB / Supabase)                                    |
| **Real-Time Updates**  | WebSockets (Go + SvelteKit)                                      |
| **Cloud Hosting**      | Backend (Cloud Server) + Frontend (Cloudflare)                   |
| **Payment Gateway**    | Razorpay                                                         |

## 📦 Prerequisites
- List all required software and versions
- Include installation instructions
  ```
  - Node.js (v14+)
  - npm (v6+)
  - Python (v3.8+)
  ```

## 🔧 Installation & Setup

1. Install dependencies
   ```bash
   # Frontend
   cd frontend
   npm install

   # Backend
   cd ../backend
   pip install -r requirements.txt
   ```

2. Configure Environment Variables
   
   - Create a `.env` file
   - Add necessary configuration details
     
   ```
   API_KEY=your_api_key
   DATABASE_URL=your_database_connection_string
   ```

4. Run the Application
   ```bash
   # Start frontend
   npm start

   # Start backend
   python app.py
   ```

## 👥 Team Members
  [1. Akshay Joseph](enter_github_id_here)   
  [2. Harinarayan M R](enter_github_id_here)   
  [3. Sebastian Abraham](enter_github_id_here)   
  [4. John K. Titus](enter_github_id_here)  

**Made with ❤️ at Beachhack 6**

