from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import json
from datetime import datetime, timedelta
import random
import os

app = FastAPI(title="AI News Chatbot", description="Personalized news chatbot with tech, politics, and finance updates")

# Mount static files for assets
app.mount("/static", StaticFiles(directory="."), name="static")

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    user_preferences: Optional[List[str]] = ["tech", "politics", "finance"]

class ChatResponse(BaseModel):
    response: str
    news_articles: Optional[List[dict]] = None

class NewsArticle(BaseModel):
    id: int
    title: str
    content: str
    category: str
    author: str
    published_date: str
    url: str
    summary: str

# Mock news data (30 articles)
MOCK_NEWS_DATA = [
    # Tech News
    {
        "id": 1,
        "title": "AI Revolution: New Language Model Breaks Performance Records",
        "content": "A groundbreaking new AI model has achieved unprecedented performance across multiple benchmarks, showing remarkable improvements in reasoning and code generation.",
        "category": "tech",
        "author": "Sarah Chen",
        "published_date": "2024-01-15T10:30:00Z",
        "url": "https://technews.com/ai-revolution",
        "summary": "New AI model sets performance records in reasoning and coding tasks."
    },
    {
        "id": 2,
        "title": "Quantum Computing Breakthrough: 1000-Qubit Processor Unveiled",
        "content": "Scientists have successfully developed a 1000-qubit quantum processor, marking a significant milestone in quantum computing advancement.",
        "category": "tech",
        "author": "Dr. Michael Rodriguez",
        "published_date": "2024-01-14T14:20:00Z",
        "url": "https://quantumtech.com/breakthrough",
        "summary": "1000-qubit quantum processor represents major computing advancement."
    },
    {
        "id": 3,
        "title": "Cybersecurity Alert: New Ransomware Targets Cloud Infrastructure",
        "content": "Security experts warn of a sophisticated new ransomware strain specifically designed to target cloud-based infrastructure and services.",
        "category": "tech",
        "author": "Alex Thompson",
        "published_date": "2024-01-13T09:15:00Z",
        "url": "https://cybersec.com/ransomware-alert",
        "summary": "New ransomware strain poses threat to cloud infrastructure."
    },
    {
        "id": 4,
        "title": "Electric Vehicle Sales Surge 300% in Q4 2023",
        "content": "The electric vehicle market experienced unprecedented growth with sales increasing by 300% compared to the previous quarter.",
        "category": "tech",
        "author": "Emma Wilson",
        "published_date": "2024-01-12T16:45:00Z",
        "url": "https://evnews.com/sales-surge",
        "summary": "EV sales show massive 300% growth in latest quarter."
    },
    {
        "id": 5,
        "title": "5G Network Expansion Reaches Rural Areas",
        "content": "Major telecommunications companies announce significant expansion of 5G networks to previously underserved rural communities.",
        "category": "tech",
        "author": "James Park",
        "published_date": "2024-01-11T11:30:00Z",
        "url": "https://telecom.com/5g-expansion",
        "summary": "5G networks expand to rural areas, bridging digital divide."
    },
    {
        "id": 6,
        "title": "Blockchain Technology Revolutionizes Supply Chain Management",
        "content": "Companies are increasingly adopting blockchain solutions to enhance transparency and efficiency in global supply chains.",
        "category": "tech",
        "author": "Lisa Chang",
        "published_date": "2024-01-10T13:20:00Z",
        "url": "https://blockchain.com/supply-chain",
        "summary": "Blockchain adoption grows in supply chain management sector."
    },
    {
        "id": 7,
        "title": "Virtual Reality Gaming Market Hits $50 Billion Milestone",
        "content": "The VR gaming industry reaches a significant financial milestone, driven by improved hardware and immersive experiences.",
        "category": "tech",
        "author": "Ryan Foster",
        "published_date": "2024-01-09T15:10:00Z",
        "url": "https://vrgaming.com/milestone",
        "summary": "VR gaming market achieves $50 billion valuation milestone."
    },
    {
        "id": 8,
        "title": "Space Technology: Private Companies Launch Record Number of Satellites",
        "content": "Private space companies have launched a record-breaking number of satellites, advancing global communications infrastructure.",
        "category": "tech",
        "author": "Dr. Amanda Foster",
        "published_date": "2024-01-08T12:00:00Z",
        "url": "https://spacetech.com/satellite-record",
        "summary": "Private companies set satellite launch records in 2024."
    },
    {
        "id": 9,
        "title": "Renewable Energy Storage Solutions Show Major Improvements",
        "content": "New battery technologies demonstrate significant improvements in energy storage capacity and efficiency for renewable sources.",
        "category": "tech",
        "author": "Green Energy Team",
        "published_date": "2024-01-07T10:45:00Z",
        "url": "https://renewabletech.com/storage",
        "summary": "Battery technology advances boost renewable energy storage."
    },
    {
        "id": 10,
        "title": "Autonomous Vehicles Begin Commercial Deployment in Major Cities",
        "content": "Self-driving vehicles start commercial operations in several major metropolitan areas, marking a new era in transportation.",
        "category": "tech",
        "author": "Transport Weekly",
        "published_date": "2024-01-06T14:30:00Z",
        "url": "https://autotech.com/commercial-deployment",
        "summary": "Autonomous vehicles enter commercial service in major cities."
    },
    
    # Politics News
    {
        "id": 11,
        "title": "International Climate Summit Reaches Historic Agreement",
        "content": "World leaders at the climate summit have reached a groundbreaking agreement on carbon emission reductions and renewable energy targets.",
        "category": "politics",
        "author": "Global News Network",
        "published_date": "2024-01-15T18:00:00Z",
        "url": "https://politicsnews.com/climate-summit",
        "summary": "Historic climate agreement reached at international summit."
    },
    {
        "id": 12,
        "title": "New Trade Agreement Signed Between Major Economic Powers",
        "content": "A comprehensive trade agreement has been finalized, promising to boost economic cooperation and reduce trade barriers.",
        "category": "politics",
        "author": "Economic Affairs Reporter",
        "published_date": "2024-01-14T16:30:00Z",
        "url": "https://politicsnews.com/trade-agreement",
        "summary": "Major trade agreement signed to boost economic cooperation."
    },
    {
        "id": 13,
        "title": "Electoral Reform Bill Passes Congressional Committee",
        "content": "Significant electoral reform legislation advances through committee, addressing voting rights and election security measures.",
        "category": "politics",
        "author": "Capitol Hill Reporter",
        "published_date": "2024-01-13T13:45:00Z",
        "url": "https://politicsnews.com/electoral-reform",
        "summary": "Electoral reform bill advances through congressional committee."
    },
    {
        "id": 14,
        "title": "Infrastructure Investment Plan Receives Bipartisan Support",
        "content": "A major infrastructure investment plan gains support from both parties, focusing on roads, bridges, and digital infrastructure.",
        "category": "politics",
        "author": "Infrastructure Desk",
        "published_date": "2024-01-12T11:20:00Z",
        "url": "https://politicsnews.com/infrastructure",
        "summary": "Bipartisan infrastructure plan gains momentum in Congress."
    },
    {
        "id": 15,
        "title": "Healthcare Policy Reform Debate Intensifies",
        "content": "Lawmakers engage in heated debates over proposed healthcare policy reforms aimed at improving accessibility and reducing costs.",
        "category": "politics",
        "author": "Health Policy Team",
        "published_date": "2024-01-11T15:15:00Z",
        "url": "https://politicsnews.com/healthcare-reform",
        "summary": "Healthcare reform debate intensifies in legislative chambers."
    },
    {
        "id": 16,
        "title": "International Security Alliance Strengthens Cooperation",
        "content": "Allied nations announce enhanced security cooperation measures in response to emerging global threats.",
        "category": "politics",
        "author": "Security Affairs",
        "published_date": "2024-01-10T09:30:00Z",
        "url": "https://politicsnews.com/security-alliance",
        "summary": "Security alliance strengthens cooperation against global threats."
    },
    {
        "id": 17,
        "title": "Education Funding Bill Advances to Final Vote",
        "content": "Comprehensive education funding legislation moves closer to passage, promising increased resources for schools nationwide.",
        "category": "politics",
        "author": "Education Reporter",
        "published_date": "2024-01-09T12:45:00Z",
        "url": "https://politicsnews.com/education-funding",
        "summary": "Education funding bill nears final legislative approval."
    },
    {
        "id": 18,
        "title": "Immigration Policy Updates Announced by Administration",
        "content": "The administration announces significant updates to immigration policies, affecting visa processing and border security measures.",
        "category": "politics",
        "author": "Immigration Desk",
        "published_date": "2024-01-08T14:20:00Z",
        "url": "https://politicsnews.com/immigration-policy",
        "summary": "Administration announces major immigration policy updates."
    },
    {
        "id": 19,
        "title": "Tax Reform Proposal Sparks Legislative Debate",
        "content": "New tax reform proposals generate intense debate among lawmakers, focusing on corporate rates and individual deductions.",
        "category": "politics",
        "author": "Tax Policy Reporter",
        "published_date": "2024-01-07T16:10:00Z",
        "url": "https://politicsnews.com/tax-reform",
        "summary": "Tax reform proposals trigger heated legislative debates."
    },
    {
        "id": 20,
        "title": "Diplomatic Relations Improve Between Former Adversaries",
        "content": "Historic diplomatic breakthrough as former adversaries announce improved relations and cooperation agreements.",
        "category": "politics",
        "author": "Diplomatic Correspondent",
        "published_date": "2024-01-06T10:00:00Z",
        "url": "https://politicsnews.com/diplomatic-breakthrough",
        "summary": "Former adversaries announce improved diplomatic relations."
    },
    
    # Finance News
    {
        "id": 21,
        "title": "Stock Market Reaches All-Time High Amid Economic Optimism",
        "content": "Major stock indices hit record highs as investors show confidence in economic recovery and corporate earnings growth.",
        "category": "finance",
        "author": "Market Analysis Team",
        "published_date": "2024-01-15T09:30:00Z",
        "url": "https://financenews.com/market-high",
        "summary": "Stock markets reach record highs on economic optimism."
    },
    {
        "id": 22,
        "title": "Central Bank Announces Interest Rate Decision",
        "content": "The Federal Reserve announces its latest interest rate decision, maintaining current rates while signaling future policy direction.",
        "category": "finance",
        "author": "Fed Watch Team",
        "published_date": "2024-01-14T14:00:00Z",
        "url": "https://financenews.com/fed-rates",
        "summary": "Central bank maintains interest rates, signals future policy."
    },
    {
        "id": 23,
        "title": "Cryptocurrency Market Experiences Significant Volatility",
        "content": "Digital currencies show extreme price movements as regulatory news and institutional adoption continue to drive market sentiment.",
        "category": "finance",
        "author": "Crypto Desk",
        "published_date": "2024-01-13T11:45:00Z",
        "url": "https://financenews.com/crypto-volatility",
        "summary": "Cryptocurrency markets show high volatility amid regulatory news."
    },
    {
        "id": 24,
        "title": "Major Bank Reports Record Quarterly Profits",
        "content": "Leading financial institution announces record-breaking quarterly profits, driven by strong lending and investment banking performance.",
        "category": "finance",
        "author": "Banking Reporter",
        "published_date": "2024-01-12T13:30:00Z",
        "url": "https://financenews.com/bank-profits",
        "summary": "Major bank reports record quarterly profit performance."
    },
    {
        "id": 25,
        "title": "Real Estate Market Shows Signs of Stabilization",
        "content": "Housing market data indicates stabilization after months of volatility, with prices showing moderate growth patterns.",
        "category": "finance",
        "author": "Real Estate Team",
        "published_date": "2024-01-11T10:15:00Z",
        "url": "https://financenews.com/real-estate",
        "summary": "Real estate market shows stabilization with moderate growth."
    },
    {
        "id": 26,
        "title": "Corporate Earnings Season Exceeds Expectations",
        "content": "Q4 earnings reports surpass analyst expectations across multiple sectors, boosting investor confidence in corporate performance.",
        "category": "finance",
        "author": "Earnings Watch",
        "published_date": "2024-01-10T15:45:00Z",
        "url": "https://financenews.com/earnings-season",
        "summary": "Corporate earnings exceed expectations across sectors."
    },
    {
        "id": 27,
        "title": "Inflation Data Shows Continued Moderation",
        "content": "Latest inflation figures indicate continued moderation in price pressures, supporting economic stability expectations.",
        "category": "finance",
        "author": "Economic Data Team",
        "published_date": "2024-01-09T08:30:00Z",
        "url": "https://financenews.com/inflation-data",
        "summary": "Inflation data shows continued moderation in price pressures."
    },
    {
        "id": 28,
        "title": "Venture Capital Funding Reaches New Heights",
        "content": "Startup funding hits record levels as venture capital firms increase investments in technology and innovation sectors.",
        "category": "finance",
        "author": "VC Reporter",
        "published_date": "2024-01-08T12:20:00Z",
        "url": "https://financenews.com/vc-funding",
        "summary": "Venture capital funding reaches record investment levels."
    },
    {
        "id": 29,
        "title": "International Currency Markets Show Stability",
        "content": "Foreign exchange markets demonstrate increased stability as central bank policies align across major economies.",
        "category": "finance",
        "author": "FX Desk",
        "published_date": "2024-01-07T14:10:00Z",
        "url": "https://financenews.com/currency-stability",
        "summary": "Currency markets show stability amid aligned central bank policies."
    },
    {
        "id": 30,
        "title": "ESG Investing Trends Reshape Financial Markets",
        "content": "Environmental, Social, and Governance investing continues to gain momentum, influencing corporate strategies and market valuations.",
        "category": "finance",
        "author": "ESG Investment Team",
        "published_date": "2024-01-06T11:00:00Z",
        "url": "https://financenews.com/esg-trends",
        "summary": "ESG investing trends continue reshaping financial markets."
    }
]

# Chatbot responses and logic
class NewsBot:
    def __init__(self):
        self.news_data = MOCK_NEWS_DATA
        self.greetings = {
            "hello": ["Hello! 👋", "Hi there! 👋", "Hey! How can I help you today? 👋"],
            "how are you": ["I'm doing great, thanks for asking! How can I assist you with news today?", 
                          "I'm wonderful! Ready to share the latest news with you. What interests you?"],
            "good morning": ["Good morning! ☀️ Ready to catch up on the latest news?", 
                           "Morning! What news would you like to explore today?"],
            "good afternoon": ["Good afternoon! 🌤️ How can I help you stay informed today?", 
                             "Afternoon! What's on your mind?"],
            "good evening": ["Good evening! 🌙 Let's catch up on today's news.", 
                           "Evening! What would you like to know about?"]
        }
        
    def get_personalized_news(self, categories: List[str], limit: int = 5) -> List[dict]:
        """Get personalized news based on user preferences"""
        filtered_news = [
            article for article in self.news_data 
            if article["category"] in categories
        ]
        sorted_news = sorted(filtered_news, key=lambda x: x["published_date"], reverse=True)
        return sorted_news[:limit]
    
    def get_greeting_response(self, message: str) -> Optional[str]:
        """Get a contextual greeting response"""
        message_lower = message.lower()
        for greeting, responses in self.greetings.items():
            if greeting in message_lower:
                return random.choice(responses)
        return None
    
    def generate_response(self, message: str, preferences: List[str]) -> ChatResponse:
        """Generate chatbot response based on user message"""
        message_lower = message.lower()
        
        # Check for greetings first
        greeting_response = self.get_greeting_response(message_lower)
        if greeting_response:
            return ChatResponse(
                response=greeting_response,
                news_articles=self.get_personalized_news(preferences, 2)
            )
        
        # News request patterns
        news_patterns = {
            "latest": "Here are the latest updates based on your interests:",
            "what's new": "Here's what's new in your preferred categories:",
            "what's happening": "Here's what's happening in the world:",
            "any news": "Here are some recent news updates:",
            "tell me about": "Here's what I found about that:",
            "show me": "Here are some relevant updates:"
        }
        
        for pattern, response in news_patterns.items():
            if pattern in message_lower:
                return ChatResponse(
                    response=response,
                    news_articles=self.get_personalized_news(preferences, 4)
                )
        
        # Category-specific requests
        category_responses = {
            "tech": ("Here are the latest technology updates:", ["tech"]),
            "technology": ("Here are the latest technology updates:", ["tech"]),
            "politics": ("Here are the latest political updates:", ["politics"]),
            "political": ("Here are the latest political updates:", ["politics"]),
            "finance": ("Here are the latest financial updates:", ["finance"]),
            "financial": ("Here are the latest financial updates:", ["finance"]),
            "market": ("Here are the latest market updates:", ["finance"])
        }
        
        for keyword, (response, categories) in category_responses.items():
            if keyword in message_lower:
                return ChatResponse(
                    response=response,
                    news_articles=self.get_personalized_news(categories, 4)
                )
        
        # Help request
        if "help" in message_lower or "what can you do" in message_lower:
            return ChatResponse(
                response="I can help you with:\n• Latest news in tech, politics, and finance\n• Personalized news based on your preferences\n• Specific category updates\n• Just ask me about any topic you're interested in!\n\nTry asking me about the latest tech news, political updates, or financial market trends!"
            )
        
        # Default response with contextual news
        return ChatResponse(
            response="I understand you're interested in news. Here are some relevant updates that might interest you:",
            news_articles=self.get_personalized_news(preferences, 3)
        )

# Initialize the bot
news_bot = NewsBot()

# API Routes
@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    """Serve the main HTML page"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI News Chatbot</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', sans-serif;
                background: #0A0F1C;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
                color: #E2E8F0;
            }
            
            .container {
                background: rgba(17, 24, 39, 0.8);
                backdrop-filter: blur(10px);
                border-radius: 24px;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
                width: 100%;
                max-width: 1000px;
                height: 800px;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .header {
                background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
                padding: 30px;
                text-align: center;
                position: relative;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 20px;
            }
            
            .header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    radial-gradient(circle at 20% 20%, rgba(255,255,255,0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(255,255,255,0.1) 0%, transparent 50%);
                opacity: 0.5;
            }
            
            .logo {
                width: 60px;
                height: 60px;
                filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
            }
            
            .header-content {
                position: relative;
                z-index: 1;
            }
            
            .header h1 {
                font-size: 32px;
                font-weight: 600;
                margin-bottom: 8px;
                letter-spacing: -0.5px;
                background: linear-gradient(to right, #fff, #E2E8F0);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            .header p {
                opacity: 0.9;
                font-size: 16px;
                font-weight: 400;
            }
            
            .preferences {
                padding: 20px 30px;
                background: rgba(31, 41, 55, 0.5);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                align-items: center;
            }
            
            .preferences label {
                font-weight: 500;
                color: #E2E8F0;
                display: flex;
                align-items: center;
                cursor: pointer;
                padding: 8px 16px;
                background: rgba(55, 65, 81, 0.5);
                border-radius: 12px;
                transition: all 0.2s ease;
            }
            
            .preferences label:hover {
                background: rgba(55, 65, 81, 0.8);
            }
            
            .preferences input[type="checkbox"] {
                appearance: none;
                width: 18px;
                height: 18px;
                border: 2px solid #4F46E5;
                border-radius: 4px;
                margin-right: 8px;
                position: relative;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            
            .preferences input[type="checkbox"]:checked {
                background: #4F46E5;
            }
            
            .preferences input[type="checkbox"]:checked::after {
                content: '✓';
                position: absolute;
                color: white;
                font-size: 12px;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
            }
            
            .chat-container {
                flex: 1;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                background: rgba(17, 24, 39, 0.5);
                position: relative;
            }
            
            .chat-container::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    radial-gradient(circle at 0% 0%, rgba(79, 70, 229, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 100% 100%, rgba(124, 58, 237, 0.1) 0%, transparent 50%);
                pointer-events: none;
            }
            
            .messages {
                flex: 1;
                overflow-y: auto;
                padding: 30px;
                display: flex;
                flex-direction: column;
                gap: 24px;
            }
            
            .message {
                max-width: 85%;
                animation: fadeIn 0.4s ease-out;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .message.user {
                align-self: flex-end;
            }
            
            .message.bot {
                align-self: flex-start;
            }
            
            .message-content {
                padding: 16px 20px;
                border-radius: 20px;
                font-size: 15px;
                line-height: 1.6;
                position: relative;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .message.user .message-content {
                background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
                color: white;
                border-bottom-right-radius: 4px;
            }
            
            .message.bot .message-content {
                background: rgba(31, 41, 55, 0.8);
                color: #E2E8F0;
                border-bottom-left-radius: 4px;
            }
            
            .news-articles {
                margin-top: 20px;
                display: flex;
                flex-direction: column;
                gap: 16px;
            }
            
            .news-article {
                background: rgba(31, 41, 55, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 20px;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .news-article:hover {
                transform: translateY(-2px);
                background: rgba(31, 41, 55, 0.9);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            }
            
            .news-article h4 {
                color: #E2E8F0;
                font-size: 16px;
                font-weight: 500;
                margin-bottom: 10px;
            }
            
            .news-article p {
                color: #94A3B8;
                font-size: 14px;
                line-height: 1.6;
            }
            
            .news-meta {
                font-size: 12px;
                color: #64748B;
                margin-top: 12px;
                display: flex;
                gap: 16px;
                align-items: center;
            }
            
            .news-meta span {
                display: flex;
                align-items: center;
                gap: 4px;
            }
            
            .input-container {
                padding: 24px 30px;
                background: rgba(17, 24, 39, 0.8);
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                display: flex;
                gap: 16px;
            }
            
            .input-container input {
                flex: 1;
                padding: 16px 24px;
                background: rgba(31, 41, 55, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                outline: none;
                font-size: 15px;
                color: #E2E8F0;
                transition: all 0.2s ease;
            }
            
            .input-container input::placeholder {
                color: #64748B;
            }
            
            .input-container input:focus {
                border-color: #4F46E5;
                box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
            }
            
            .input-container button {
                padding: 16px 32px;
                background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
                color: white;
                border: none;
                border-radius: 16px;
                cursor: pointer;
                font-weight: 500;
                font-size: 15px;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .input-container button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
            }
            
            .input-container button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
            
            .typing-indicator {
                display: none;
                padding: 12px 20px;
                background: rgba(31, 41, 55, 0.8);
                border-radius: 16px;
                margin-bottom: 15px;
                align-self: flex-start;
            }
            
            .typing-indicator span {
                display: inline-block;
                width: 8px;
                height: 8px;
                background: #4F46E5;
                border-radius: 50%;
                margin: 0 2px;
                animation: typing 1s infinite;
            }
            
            .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
            .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
            
            @keyframes typing {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-5px); }
            }
            
            /* Custom Scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(31, 41, 55, 0.3);
            }
            
            ::-webkit-scrollbar-thumb {
                background: rgba(79, 70, 229, 0.5);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: rgba(79, 70, 229, 0.7);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="/static/logo.svg" alt="AI News Bot Logo" class="logo">
                <div class="header-content">
                    <h1>AI News Chatbot</h1>
                    <p>Your personalized news companion</p>
                </div>
            </div>
            <div class="preferences">
                <label><input type="checkbox" name="preference" value="tech" checked> Technology</label>
                <label><input type="checkbox" name="preference" value="politics" checked> Politics</label>
                <label><input type="checkbox" name="preference" value="finance" checked> Finance</label>
            </div>
            <div class="chat-container">
                <div class="messages" id="messages"></div>
                <div class="typing-indicator" id="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                <div class="input-container">
                    <input type="text" id="user-input" placeholder="Ask me about the latest news..." autocomplete="off">
                    <button id="send-button">Send</button>
                </div>
            </div>
        </div>
        <script>
            const messagesContainer = document.getElementById('messages');
            const messageInput = document.getElementById('user-input');
            const sendButton = document.getElementById('send-button');
            const typingIndicator = document.getElementById('typing-indicator');
            
            function getSelectedPreferences() {
                const preferences = [];
                const checkboxes = document.querySelectorAll('.preferences input[type="checkbox"]:checked');
                checkboxes.forEach(checkbox => {
                    preferences.push(checkbox.value);
                });
                return preferences;
            }
            
            function addMessage(content, isUser = false, newsArticles = null) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
                
                let messageHTML = `<div class="message-content">${content}</div>`;
                
                if (newsArticles && newsArticles.length > 0) {
                    messageHTML += '<div class="news-articles">';
                    newsArticles.forEach(article => {
                        const date = new Date(article.published_date).toLocaleDateString();
                        messageHTML += `
                            <div class="news-article">
                                <h4>${article.title}</h4>
                                <p>${article.summary}</p>
                                <div class="news-meta">
                                    ${article.category.toUpperCase()} • ${article.author} • ${date}
                                </div>
                            </div>
                        `;
                    });
                    messageHTML += '</div>';
                }
                
                messageDiv.innerHTML = messageHTML;
                messagesContainer.appendChild(messageDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
            
            function showTyping() {
                typingIndicator.style.display = 'block';
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
            
            function hideTyping() {
                typingIndicator.style.display = 'none';
            }
            
            async function sendMessage() {
                const message = messageInput.value.trim();
                if (!message) return;
                
                const preferences = getSelectedPreferences();
                if (preferences.length === 0) {
                    alert('Please select at least one interest category!');
                    return;
                }
                
                // Add user message
                addMessage(message, true);
                messageInput.value = '';
                sendButton.disabled = true;
                showTyping();
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            message: message,
                            user_preferences: preferences
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    
                    const data = await response.json();
                    
                    // Simulate typing delay
                    setTimeout(() => {
                        hideTyping();
                        addMessage(data.response, false, data.news_articles);
                        sendButton.disabled = false;
                        messageInput.focus();
                    }, 1000);
                    
                } catch (error) {
                    hideTyping();
                    addMessage('Sorry, I encountered an error. Please try again.', false);
                    sendButton.disabled = false;
                    console.error('Error:', error);
                }
            }
            
            // Enter key to send message
            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !sendButton.disabled) {
                    sendMessage();
                }
            });
            
            // Focus on input when page loads
            messageInput.focus();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    """Main chat endpoint"""
    try:
        response = news_bot.generate_response(message.message, message.user_preferences)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/news", response_model=List[NewsArticle])
async def get_all_news():
    """Get all news articles"""
    return MOCK_NEWS_DATA

@app.get("/news/{category}", response_model=List[NewsArticle])
async def get_news_by_category(category: str):
    """Get news articles by category"""
    if category not in ["tech", "politics", "finance"]:
        raise HTTPException(status_code=400, detail="Invalid category. Use: tech, politics, or finance")
    
    filtered_news = [article for article in MOCK_NEWS_DATA if article["category"] == category]
    return filtered_news

@app.get("/news/article/{article_id}", response_model=NewsArticle)
async def get_news_article(article_id: int):
    """Get a specific news article by ID"""
    article = next((article for article in MOCK_NEWS_DATA if article["id"] == article_id), None)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "AI News Chatbot is running!"}

# Run the application
if __name__ == "__main__":
    print("🚀 Starting AI News Chatbot...")
    print("📱 Features:")
    print("   • Interactive chat interface")
    print("   • Personalized news recommendations")
    print("   • 30 mock articles across tech, politics, and finance")
    print("   • REST API endpoints")
    print("   • Elegant and responsive UI")
    print("\n🌐 Available endpoints:")
    print("   • GET  /          - Main chat interface")
    print("   • POST /chat      - Chat with the bot")
    print("   • GET  /news      - Get all news articles")
    print("   • GET  /news/{category} - Get news by category")
    print("   • GET  /news/article/{id} - Get specific article")
    print("   • GET  /health    - Health check")
    print("\n💡 Try asking:")
    print("   • 'What's the latest tech news?'")
    print("   • 'Show me finance updates'")
    print("   • 'Any political news today?'")
    print("   • 'Hello' or 'Help'")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)