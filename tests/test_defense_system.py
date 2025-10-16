"""
Tests for the defense system module
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath.abspath(__file__))))

from defense_system import DefenseSystem

class TestDefenseSystem(unittest.TestCase):
    def setUp(self):
        self.mock_bot = Mock()
        self.defense_system = DefenseSystem(self.mock_bot)
    
    def test_protected_user_by_username(self):
        """Test that user 'by_bytes' is automatically protected"""
        # Mock guild and member
        mock_guild = Mock()
        mock_member = Mock()
        mock_member.name = "by_bytes"
        mock_member.display_name = "by_bytes"
        mock_guild.get_member.return_value = mock_member
        
        # Test protection
        result = self.defense_system.is_protected_user(12345, mock_guild)
        self.assertTrue(result)
    
    def test_protected_user_by_display_name(self):
        """Test that user with display name 'by_bytes' is protected"""
        # Mock guild and member
        mock_guild = Mock()
        mock_member = Mock()
        mock_member.name = "different_name"
        mock_member.display_name = "by_bytes"
        mock_guild.get_member.return_value = mock_member
        
        # Test protection
        result = self.defense_system.is_protected_user(12345, mock_guild)
        self.assertTrue(result)
    
    def test_non_protected_user(self):
        """Test that regular users are not protected"""
        # Mock guild and member
        mock_guild = Mock()
        mock_member = Mock()
        mock_member.name = "regular_user"
        mock_member.display_name = "Regular User"
        mock_guild.get_member.return_value = mock_member
        
        # Test protection
        result = self.defense_system.is_protected_user(12345, mock_guild)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
