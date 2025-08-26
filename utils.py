# Utility functions for Telegram Bot Cloudflare Pro
# Created by @bukanaol

import re
import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """Rate limiter for API calls and user actions."""
    
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, user_id: int, action: str, limit: int, window: int) -> bool:
        """Check if user is allowed to perform action based on rate limits."""
        current_time = time.time()
        key = f"{user_id}_{action}"
        
        if key not in self.requests:
            self.requests[key] = []
        
        # Remove old requests outside the window
        self.requests[key] = [req_time for req_time in self.requests[key] 
                            if current_time - req_time < window]
        
        # Check if limit exceeded
        if len(self.requests[key]) >= limit:
            return False
        
        # Add current request
        self.requests[key].append(current_time)
        return True
    
    def get_remaining_requests(self, user_id: int, action: str, limit: int, window: int) -> int:
        """Get remaining requests for user action."""
        current_time = time.time()
        key = f"{user_id}_{action}"
        
        if key not in self.requests:
            return limit
        
        # Remove old requests outside the window
        self.requests[key] = [req_time for req_time in self.requests[key] 
                            if current_time - req_time < window]
        
        return max(0, limit - len(self.requests[key]))

class DomainValidator:
    """Domain and subdomain validation utilities."""
    
    @staticmethod
    def validate_ip(ip: str) -> bool:
        """Validate IPv4 address."""
        pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        return bool(re.match(pattern, ip))
    
    @staticmethod
    def validate_domain(domain: str) -> bool:
        """Validate domain name."""
        pattern = r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
        return bool(re.match(pattern, domain))
    
    @staticmethod
    def validate_subdomain(subdomain: str) -> bool:
        """Validate subdomain name."""
        if len(subdomain) < 3 or len(subdomain) > 63:
            return False
        
        pattern = r"^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]$"
        return bool(re.match(pattern, subdomain))
    
    @staticmethod
    def is_private_ip(ip: str) -> bool:
        """Check if IP is private/internal."""
        private_ranges = [
            ("10.0.0.0", "10.255.255.255"),
            ("172.16.0.0", "172.31.255.255"),
            ("192.168.0.0", "192.168.255.255"),
            ("127.0.0.0", "127.255.255.255")
        ]
        
        ip_parts = [int(part) for part in ip.split('.')]
        ip_num = (ip_parts[0] << 24) + (ip_parts[1] << 16) + (ip_parts[2] << 8) + ip_parts[3]
        
        for start, end in private_ranges:
            start_parts = [int(part) for part in start.split('.')]
            end_parts = [int(part) for part in end.split('.')]
            
            start_num = (start_parts[0] << 24) + (start_parts[1] << 16) + (start_parts[2] << 8) + start_parts[3]
            end_num = (end_parts[0] << 24) + (end_parts[1] << 16) + (end_parts[2] << 8) + end_parts[3]
            
            if start_num <= ip_num <= end_num:
                return True
        
        return False

class SubdomainGenerator:
    """Generate unique and meaningful subdomain names."""
    
    ADJECTIVES = [
        "fast", "secure", "reliable", "swift", "powerful", 
        "efficient", "smart", "dynamic", "rapid", "stable",
        "quick", "safe", "trusted", "agile", "robust",
        "flexible", "scalable", "optimized", "enhanced", "premium"
    ]
    
    NOUNS = [
        "server", "node", "host", "instance", "service", 
        "app", "api", "gateway", "proxy", "cdn",
        "cluster", "endpoint", "router", "bridge", "tunnel",
        "cache", "storage", "database", "queue", "stream"
    ]
    
    @classmethod
    def generate_name(cls, length: int = 3) -> str:
        """Generate a random subdomain name."""
        import random
        import string
        
        adj = random.choice(cls.ADJECTIVES)
        noun = random.choice(cls.NOUNS)
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        
        return f"{adj}-{noun}-{suffix}"
    
    @classmethod
    def generate_custom_name(cls, prefix: str, length: int = 3) -> str:
        """Generate custom subdomain name with specific prefix."""
        import random
        import string
        
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        return f"{prefix}-{suffix}"

class DataManager:
    """Manage bot data storage and backup."""
    
    def __init__(self, backup_dir: str = "backups"):
        self.backup_dir = backup_dir
        self.data_file = "user_data.json"
        self.backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    def save_data(self, data: Dict, filename: str = None) -> bool:
        """Save data to JSON file."""
        try:
            if filename is None:
                filename = self.data_file
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            return False
    
    def load_data(self, filename: str = None) -> Dict:
        """Load data from JSON file."""
        try:
            if filename is None:
                filename = self.data_file
            
            if not os.path.exists(filename):
                return {}
            
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return {}
    
    def create_backup(self) -> bool:
        """Create backup of current data."""
        try:
            import os
            
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir)
            
            current_data = self.load_data()
            backup_path = os.path.join(self.backup_dir, self.backup_file)
            
            return self.save_data(current_data, backup_path)
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return False
    
    def cleanup_old_backups(self, max_backups: int = 7) -> bool:
        """Remove old backup files."""
        try:
            import os
            import glob
            
            if not os.path.exists(self.backup_dir):
                return True
            
            backup_files = glob.glob(os.path.join(self.backup_dir, "backup_*.json"))
            backup_files.sort(key=os.path.getmtime, reverse=True)
            
            # Remove old backups
            for old_backup in backup_files[max_backups:]:
                os.remove(old_backup)
                logger.info(f"Removed old backup: {old_backup}")
            
            return True
        except Exception as e:
            logger.error(f"Error cleaning up backups: {e}")
            return False

class MessageFormatter:
    """Format messages with consistent styling."""
    
    @staticmethod
    def format_success(title: str, message: str, details: Dict = None) -> str:
        """Format success message."""
        formatted = f"✅ **{title}** 🎉\n\n{message}"
        
        if details:
            formatted += "\n\n**Detail:**\n"
            for key, value in details.items():
                formatted += f"• **{key}:** {value}\n"
        
        return formatted
    
    @staticmethod
    def format_error(title: str, message: str, solutions: List[str] = None) -> str:
        """Format error message."""
        formatted = f"❌ **{title}**\n\n{message}"
        
        if solutions:
            formatted += "\n\n**Solusi yang bisa dicoba:**\n"
            for i, solution in enumerate(solutions, 1):
                formatted += f"{i}. {solution}\n"
        
        return formatted
    
    @staticmethod
    def format_info(title: str, message: str, items: List[str] = None) -> str:
        """Format information message."""
        formatted = f"ℹ️ **{title}**\n\n{message}"
        
        if items:
            formatted += "\n\n"
            for item in items:
                formatted += f"• {item}\n"
        
        return formatted
    
    @staticmethod
    def format_table(headers: List[str], rows: List[List[str]]) -> str:
        """Format data as table."""
        if not headers or not rows:
            return "Tidak ada data"
        
        # Calculate column widths
        col_widths = [len(header) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Create separator line
        separator = "+" + "+".join("-" * (width + 2) for width in col_widths) + "+"
        
        # Format table
        table = separator + "\n"
        
        # Headers
        header_row = "| " + " | ".join(f"{header:<{width}}" for header, width in zip(headers, col_widths)) + " |"
        table += header_row + "\n"
        table += separator + "\n"
        
        # Data rows
        for row in rows:
            data_row = "| " + " | ".join(f"{str(cell):<{width}}" for cell, width in zip(row, col_widths)) + " |"
            table += data_row + "\n"
        
        table += separator
        return table

class SecurityUtils:
    """Security and encryption utilities."""
    
    @staticmethod
    def hash_string(text: str) -> str:
        """Hash string using SHA-256."""
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def validate_token(token: str, min_length: int = 32) -> bool:
        """Validate API token format."""
        if len(token) < min_length:
            return False
        
        # Check if token contains only valid characters
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
        return all(char in valid_chars for char in token)
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input to prevent injection attacks."""
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '|', '`', '$', '(', ')', '{', '}']
        sanitized = text
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized.strip()

class TimeUtils:
    """Time and date utilities."""
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%d %B %Y, %H:%M:%S") -> str:
        """Format datetime object to string."""
        return dt.strftime(format_str)
    
    @staticmethod
    def parse_datetime(date_string: str) -> Optional[datetime]:
        """Parse datetime string to datetime object."""
        try:
            # Try common formats
            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%d/%m/%Y %H:%M:%S",
                "%d-%m-%Y %H:%M:%S"
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_string, fmt)
                except ValueError:
                    continue
            
            return None
        except Exception:
            return None
    
    @staticmethod
    def time_ago(dt: datetime) -> str:
        """Get human-readable time ago string."""
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            return f"{diff.days} hari yang lalu"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} jam yang lalu"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} menit yang lalu"
        else:
            return "Baru saja"
    
    @staticmethod
    def is_recent(dt: datetime, hours: int = 24) -> bool:
        """Check if datetime is within recent hours."""
        now = datetime.now()
        return (now - dt).total_seconds() < (hours * 3600)