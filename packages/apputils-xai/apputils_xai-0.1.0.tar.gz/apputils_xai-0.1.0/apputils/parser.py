"""
Text parser module for converting natural language app requests into structured data.
"""
import re
import json
from typing import Dict, List, Any, Optional

class TextParser:
    """
    Parses natural language input for app creation requests.
    """
    
    # Expanded app types and their synonyms
    APP_TYPES = {
        "task": ["todo", "task", "to-do", "to do", "checklist", "planner", "reminder", "productivity", "organization"],
        "shopping": ["shop", "shopping", "ecommerce", "e-commerce", "store", "marketplace", "retail", "online store", "commerce", "buy", "sell", "product"],
        "social": ["social", "social media", "community", "network", "messaging", "chat", "friends", "connection", "sharing", "profile", "social network"],
        "fitness": ["fitness", "gym", "workout", "exercise", "health", "training", "wellness", "sport", "activity tracker", "workout log"],
        "education": ["education", "learning", "course", "study", "school", "teaching", "educational", "training", "knowledge", "tutorial", "quiz", "learning management"],
        "finance": ["finance", "financial", "money", "banking", "budget", "accounting", "expense", "payment", "transaction", "invoice", "billing"],
        "blog": ["blog", "blogging", "content", "article", "writing", "post", "publish", "newsletter", "journal"],
        "dating": ["dating", "date", "matchmaking", "relationship", "romantic", "match", "couple"],
        "food": ["food", "restaurant", "dining", "recipe", "cooking", "menu", "order", "delivery", "reservation", "cafe", "bakery", "coffee", "pizzeria", "kitchen"],
        "travel": ["travel", "trip", "journey", "tourism", "booking", "flight", "hotel", "vacation", "adventure", "explore", "destination"],
        "real_estate": ["real estate", "property", "home", "house", "apartment", "rent", "buy", "listing", "realty"],
        "medical": ["medical", "healthcare", "health", "doctor", "patient", "clinic", "hospital", "appointment", "medicine", "therapy", "telehealth"],
        "event": ["event", "calendar", "scheduling", "booking", "reservation", "ticket", "concert", "conference", "meeting", "appointment", "organize"],
        "portfolio": ["portfolio", "showcase", "gallery", "exhibition", "display", "artwork", "photography", "design", "creative"],
        "job": ["job", "career", "employment", "hiring", "recruitment", "resume", "cv", "job board", "applicant", "talent", "hr", "human resources"],
        "news": ["news", "media", "journalism", "article", "magazine", "publication", "press", "report", "headline"],
        "music": ["music", "audio", "song", "playlist", "album", "artist", "player", "streaming", "radio"],
        "video": ["video", "streaming", "movie", "film", "tv", "television", "series", "show", "watch", "broadcast", "channel"],
        "game": ["game", "gaming", "play", "entertainment", "fun", "interactive", "competition", "challenge", "quiz"],
        "ai": ["ai", "artificial intelligence", "bot", "chatbot", "assistant", "ml", "machine learning", "intelligent", "smart", "automated"],
        "iot": ["iot", "internet of things", "smart home", "connected", "device", "sensor", "automation", "smart device"],
        "crm": ["crm", "customer", "client", "lead", "contact", "relationship", "sales", "customer management"],
        "project": ["project", "management", "task", "team", "collaboration", "workflow", "kanban", "agile", "sprint", "track"],
        "inventory": ["inventory", "stock", "warehouse", "supply", "product", "item", "asset", "tracking", "management"],
        "booking": ["booking", "reservation", "appointment", "schedule", "calendar", "time slot", "availability"]
    }
    
    # Expanded features and their synonyms
    FEATURES = {
        "auth": ["authentication", "login", "signup", "register", "user accounts", "users", "profile", "account"],
        "crud": ["crud", "create", "read", "update", "delete", "data management", "edit", "add", "remove", "modify"],
        "payment": ["payment", "subscription", "billing", "checkout", "purchase", "transaction", "money", "financial", "pricing", "pay", "credit card", "stripe", "paypal"],
        "social": ["social", "share", "like", "comment", "follow", "friends", "network", "connection", "community", "post", "reaction"],
        "messaging": ["message", "chat", "communication", "notification", "alert", "inbox", "conversation", "email", "contact", "sms", "text", "direct message"],
        "ai": ["ai", "bot", "chatbot", "assistant", "recommendation", "prediction", "machine learning", "intelligent", "smart", "automated", "analysis"],
        "file": ["file", "upload", "download", "document", "image", "photo", "video", "attachment", "storage", "share", "gallery", "media"],
        "location": ["location", "map", "gps", "tracking", "geolocation", "address", "direction", "navigation", "route", "distance", "place", "proximity"],
        "search": ["search", "filter", "find", "discovery", "browse", "lookup", "query", "explore", "sort", "categorize", "taxonomy"],
        "analytics": ["analytics", "stats", "statistics", "dashboard", "chart", "tracking", "metrics", "insight", "report", "visualization", "graph", "data", "performance"],
        "calendar": ["calendar", "scheduling", "date", "time", "event", "reminder", "appointment", "booking", "planner", "timetable"],
        "notification": ["notification", "alert", "reminder", "push", "email", "sms", "message", "update", "inform", "announce"],
        "rating": ["rating", "review", "feedback", "stars", "testimonial", "opinion", "score", "evaluation", "assessment"],
        "subscription": ["subscription", "membership", "plan", "recurring", "period", "term", "service", "monthly", "annual", "tier"],
        "inventory": ["inventory", "stock", "product", "item", "quantity", "availability", "warehouse", "supply", "manage"],
        "booking": ["booking", "reservation", "appointment", "schedule", "slot", "availability", "calendar"],
        "export": ["export", "download", "csv", "excel", "pdf", "report", "data", "backup", "extract"],
        "import": ["import", "upload", "csv", "excel", "data", "bulk", "batch", "migration"],
        "multi_language": ["multilanguage", "language", "translation", "localization", "international", "global", "i18n"],
        "theme": ["theme", "appearance", "design", "style", "color", "customize", "layout", "ui", "ux", "brand", "look"],
        "admin": ["admin", "administration", "dashboard", "control panel", "manage", "moderate", "back office", "backoffice"],
        "api": ["api", "integration", "connect", "webhook", "third-party", "external", "service", "endpoint"],
        "offline": ["offline", "local", "cache", "no internet", "disconnected", "sync"],
        "security": ["security", "privacy", "protection", "encryption", "secure", "permission", "role", "access control"],
        "marketplace": ["marketplace", "vendor", "multi-vendor", "seller", "shop", "store", "merchant"],
        "loyalty": ["loyalty", "reward", "points", "discount", "coupon", "promotion", "benefit", "vip", "membership"]
    }
    
    def __init__(self):
        pass
    
    def parse_text_input(self, text: str) -> Dict[str, Any]:
        """
        Parse natural language input to extract app type and features.
        
        Args:
            text: The natural language input describing the desired app
            
        Returns:
            A dictionary containing app_type and features
        """
        # Convert to lowercase for easier matching
        text = text.lower()
        
        # Extract app type
        app_type = self._extract_app_type(text)
        
        # Extract features
        features = self._extract_features(text)
        
        # Add domain-specific default features based on app type
        features = self._add_domain_specific_features(app_type, features)
        
        # Create app structure
        app_structure = {
            "app_type": app_type,
            "features": features,
            "raw_input": text
        }
        
        return app_structure
    
    def _extract_app_type(self, text: str) -> str:
        """
        Extract the app type from the text.
        
        Args:
            text: The input text
            
        Returns:
            The extracted app type or 'generic' if none found
        """
        for app_type, synonyms in self.APP_TYPES.items():
            for synonym in synonyms:
                # Use word boundary to prevent partial matching
                if re.search(r'\b' + synonym + r'\b', text):
                    return app_type
        
        # Look for specific industry keywords that might indicate app type
        if any(word in text for word in ["coffee", "restaurant", "cafe", "bakery", "pizzeria"]):
            return "food"
        
        if any(word in text for word in ["doctor", "clinic", "patient", "healthcare"]):
            return "medical"
            
        if any(word in text for word in ["teacher", "student", "course", "class", "learn"]):
            return "education"
        
        # Default to generic if no specific type found
        return "generic"
    
    def _extract_features(self, text: str) -> List[str]:
        """
        Extract features from the text.
        
        Args:
            text: The input text
            
        Returns:
            A list of extracted features
        """
        features = []
        
        for feature, synonyms in self.FEATURES.items():
            for synonym in synonyms:
                if re.search(r'\b' + synonym + r'\b', text) and feature not in features:
                    features.append(feature)
        
        # Always include basic CRUD functionality
        if "crud" not in features:
            features.append("crud")
        
        return features
    
    def _add_domain_specific_features(self, app_type: str, features: List[str]) -> List[str]:
        """
        Add default features based on the app type.
        
        Args:
            app_type: The type of app
            features: Current list of features
            
        Returns:
            Updated list of features with domain-specific defaults
        """
        # Add authentication for most app types
        auth_required_apps = ["social", "finance", "shopping", "medical", "education", "booking", "crm", "project"]
        if app_type in auth_required_apps and "auth" not in features:
            features.append("auth")
        
        # Add app-specific default features
        if app_type == "shopping" and "payment" not in features:
            features.append("payment")
            
        if app_type == "social" and "messaging" not in features:
            features.append("messaging")
            
        if app_type == "food" and "booking" not in features:
            features.append("booking")
            
        if app_type == "fitness" and "calendar" not in features:
            features.append("calendar")
            
        if app_type in ["event", "booking"] and "calendar" not in features:
            features.append("calendar")
            
        if app_type == "medical" and "booking" not in features:
            features.append("booking")
            
        if app_type == "travel" and "location" not in features:
            features.append("location")
            
        if app_type == "inventory" and "search" not in features:
            features.append("search")
            
        if app_type == "crm" and "analytics" not in features:
            features.append("analytics")
            
        return features