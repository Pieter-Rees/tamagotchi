import unittest
from src.tamagotchi import Tamagotchi
from src.tamagotchi.config.settings import settings

class TestTamagotchi(unittest.TestCase):
    def setUp(self):
        self.pet = Tamagotchi("TestPet")
    
    def test_initial_stats(self):
        """Test initial stats are set correctly"""
        self.assertEqual(self.pet.hunger, 100)
        self.assertEqual(self.pet.happiness, 100)
        self.assertEqual(self.pet.energy, 100)
        self.assertTrue(self.pet.is_alive)
        self.assertFalse(self.pet.is_sleeping)
    
    def test_feed(self):
        """Test feeding functionality"""
        self.pet.hunger = 50
        self.pet.feed()
        self.assertEqual(self.pet.hunger, min(100, 50 + settings.pet.FEED_HUNGER_RECOVERY))
    
    def test_play(self):
        """Test playing functionality"""
        self.pet.happiness = 50
        self.pet.energy = 50
        self.pet.play()
        self.assertEqual(self.pet.happiness, min(100, 50 + settings.pet.PLAY_HAPPINESS_RECOVERY))
        self.assertEqual(self.pet.energy, max(0, 50 - settings.pet.PLAY_ENERGY_COST))
    
    def test_sleep(self):
        """Test sleep functionality"""
        self.pet.energy = 50
        self.pet.sleep()  # Start sleeping
        self.assertTrue(self.pet.is_sleeping)
        self.assertEqual(self.pet.energy, min(100, 50 + settings.pet.SLEEP_ENERGY_RECOVERY))
        
        self.pet.sleep()  # Wake up
        self.assertFalse(self.pet.is_sleeping)
    
    def test_death_conditions(self):
        """Test death conditions"""
        self.pet.hunger = 0
        self.pet.update()
        self.assertFalse(self.pet.is_alive)
        
        # Reset for second test
        self.pet = Tamagotchi("TestPet")
        self.pet.happiness = 0
        self.pet.update()
        self.assertFalse(self.pet.is_alive)

if __name__ == '__main__':
    unittest.main() 