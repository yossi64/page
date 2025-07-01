"""
Core Functionality Tests for Google Ads Automation System
"""
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import SystemConfig
from core.master_orchestrator import MasterOrchestrator

class TestCoreFunctionality(unittest.TestCase):
    """Test core system functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.config = SystemConfig()
        self.orchestrator = MasterOrchestrator(self.config)
    
    def test_config_loading(self):
        """Test configuration loading"""
        self.assertIsNotNone(self.config.google_ads.customer_id)
        self.assertIsNotNone(self.config.openai.api_key)
        self.assertEqual(self.config.google_ads.customer_id, "8246122588")
    
    def test_orchestrator_initialization(self):
        """Test master orchestrator initialization"""
        self.assertIsNotNone(self.orchestrator)
        self.assertIsNotNone(self.orchestrator.config)
    
    def test_config_validation(self):
        """Test configuration validation"""
        missing = self.config.validate()
        self.assertIsInstance(missing, list)
    
    def test_production_readiness(self):
        """Test production readiness check"""
        ready = self.config.is_production_ready()
        self.assertIsInstance(ready, bool)

if __name__ == '__main__':
    unittest.main()
