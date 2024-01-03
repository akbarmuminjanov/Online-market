from django.test import TestCase
from .models import User 
from django.contrib.auth import login, authenticate
# Create your tests here.


class UserModelTestCase(TestCase):
    
    def test_user_auth(self):
        user = User.objects.create(username='akbarjon', 
                                   first_name="Akbarjon", 
                                   last_name="Abdurasulov",
                                   email = "akbarjon@gmail.com",
                                   phone_number="+998345265",
                                   profile="profile_images/akbarjon.png",
                                   )
        
        user.set_password("Cr.Ronaldo")
        user.save()
        #User modeli to'g'ri yaratilganini tekshirdik
        test_user = User.objects.get(username="akbarjon")
        self.assertEqual(test_user.first_name, "Akbarjon")
        self.assertEqual(test_user.last_name, "Abdurasulov")
        self.assertEqual(test_user.email, "akbarjon@gmail.com")
        self.assertEqual(test_user.phone_number, "+998345265")
        self.assertEqual(test_user.profile, "profile_images/akbarjon.png")
        #Parolni to'g'ri kiritishni teskshirdik>
        self.assertTrue(authenticate(username="akbarjon", password="Cr.Ronaldo"))
        self.assertEqual(None, authenticate(username="akbarjon", password="passwosffgb"))
        self.assertNotEqual("Cr.Ronaldo", test_user.password)
       
