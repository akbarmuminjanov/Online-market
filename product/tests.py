from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import login
from django.conf import settings
from .models import Category, Product, ArrivedCargo, ArrivedProduct, SelledProduct, Customer
from users.models import User
from finance.models import DebtCustomer
import random
# Create your tests here.


@override_settings(MEDIA_ROOT=settings.BASE_DIR.joinpath("test_media"))
class ProductTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="akbarjon", email="aa@aaa.aa", password="my_pass")
        self.category = Category.objects.create(name="O'yinchoqlar")
        
    def test_model_creation(self):
        
        
        Product.objects.create(
            name="Pepsi",
            category = self.category,
            user=self.user,
            image="pepsi.jpg",
            actual_price=9000,
            wholesale_price=9000,
            selling_price=9000,
            type_of_measurement="pc",
            quantity=5
        )
        
        product = Product.objects.get(id=1)
        
        self.assertEqual(product.name, "Pepsi")
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.user, self.user)
        self.assertEqual(product.image, "pepsi.jpg")
        self.assertEqual(product.actual_price, 9000)
        self.assertEqual(product.type_of_measurement, "pc")
        
    def test_product_create_view(self):
        
        
        self.client.login(username="akbarjon", password="my_pass")
        
        url = reverse("create") 
        image = open(f"{settings.BASE_DIR}\\media\\default_user.jpg", "rb")
        
        response = self.client.post(url, {
            "name": "Non",
            'category': self.category.id, 
            "image": image,
            "selling_price": 9000,
            "actual_price": 9000,
            "wholesale_price": 9000,
            "type_of_measurement": "pc",
        })
        self.assertEqual(response.status_code, 302)  
        product = Product.objects.get(name="Non")
        self.assertEqual(self.user, product.user)
        
    def test_product_update_view(self):
        product = Product.objects.create(
            name="Pepsi",
            category = self.category,
            user=self.user,
            image="pepsi.jpg",
            actual_price=9000,
            wholesale_price=9000,
            selling_price=9000,
            type_of_measurement="pc",
            quantity=5
        )
        url = reverse("update", args={product.id})
        self.client.login(username="akbarjon", password="my_pass")
        image = open(f"{settings.BASE_DIR}\\media\\default_user.jpg", "rb")
        
        context = {
            "name": "Pepsi 1.5l",
            'category': self.category.id, 
            "image": image,
            "selling_price": 12000,
            "actual_price": 9000,
            "wholesale_price": 9000,
            "type_of_measurement": "kg",
            "quantity": 50,
        }
        
        response = self.client.post(url, context )
        product = Product.objects.get(name="Pepsi 1.5l")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(product.selling_price, 12000)
        self.assertEqual(product.id, 1)
        self.assertNotEqual(product.quantity, 50)
        
        User.objects.create_user(username="elon", email="elon@gs.com", password="my_pass")
        self.client.login(username="elon", password="my_pass")
        response2 = self.client.post(url, context)
        self.assertEqual(response2.status_code, 404)
        
    def test_product_detail_view(self):
        product = Product.objects.create(
            name="Pepsi",
            category = self.category,
            user=self.user,
            image="pepsi.jpg",
            actual_price=9000,
            wholesale_price=9000,
            selling_price=9000,
            type_of_measurement="pc",
            quantity=5
        )
        self.client.login(username="akbarjon", password="my_pass")
        url = reverse("detail", args={product.id})
        response = self.client.get(url)
        
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Pepsi")
        
    def test_product_delete_view(self):
        product = Product.objects.create(
            name="Pepsi",
            category = self.category,
            user=self.user,
            image="pepsi.jpg",
            actual_price=9000,
            wholesale_price=9000,
            selling_price=9000,
            type_of_measurement="pc",
            quantity=5
        )
        
        self.client.login(username="akbarjon", password="my_pass")
        
        url = reverse("delete", args={product.id})
        
        response = self.client.post(url, {"product_name":"fghfjg"})
        self.assertEqual(Product.objects.all().count(), 1)
        self.assertContains(response, "Error")
        
        response2 = self.client.post(url, {'product_name':"Pepsi"})
        self.assertEqual(Product.objects.all().count(), 0)
        self.assertEqual(response2.url, "/list/")
        
  
class ArrivedProductTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="akbarjon", password="my_pass", email="aa@aaa.aa")   
        self.category = Category.objects.create(name="Mevalar")
        
        products = ['Olma', "Anor", "Behi", "Olcha"]
        for i in products:
            Product.objects.create(
                name=i,
                category = self.category,
                user=self.user,
                image="meva.jpg",
                actual_price=random.randint(10000, 30000),
                wholesale_price=random.randint(10000, 30000),
                selling_price=random.randint(10000, 30000),
                type_of_measurement="kg",
                quantity=5
            )  
            
    def test_arrivedproduct_creation(self):
        self.client.login(username="akbarjon", password="my_pass")
        url = reverse("arrived_cargo")
        
        context = {
            "supplier":"AliBaba",
            "type_of_trade":"cash",
            "arrivedproduct_set-TOTAL_FORMS":'7',
            "arrivedproduct_set-INITIAL_FORMS":'0',
            "arrivedproduct_set-MIN_NUM_FORMS":'0',
            "arrivedproduct_set-MAX_NUM_FORMS":'1000',
            "arrivedproduct_set-0-product":1,
            "arrivedproduct_set-0-quantity":'150',
            "arrivedproduct_set-0-type_of_price":'actual',
            "arrivedproduct_set-1-product":2,
            "arrivedproduct_set-1-quantity":10,
            "arrivedproduct_set-2-product":3,
            "arrivedproduct_set-2-quantity":5,
        }
        
        response = self.client.post(url, context)
        self.assertEqual(response.status_code, 302)
        arrivedCardo = ArrivedCargo.objects.get(supplier="AliBaba")
        product1 = Product.objects.get(id=1)
        product2 = Product.objects.get(id=2)
        product3 = Product.objects.get(id=3)
        
        self.assertEqual(product1.quantity, 155)
        self.assertEqual(product2.quantity, 15)
        self.assertEqual(product3.quantity, 10)
        
        self.assertEqual(arrivedCardo.user, self.user)
        
class CustomerhammasiTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="my_pass", email="aa@aaa.aa", is_superuser=True)   
        self.category = Category.objects.create(name="Mevalar")
        
        products = ['Olma', "Anor", "Behi", "Olcha"]
        for i in products:
            Product.objects.create(
                name=i,
                category = self.category,
                user=self.user,
                image="meva.jpg",
                actual_price=random.randint(10000, 30000),
                wholesale_price=random.randint(10000, 30000),
                selling_price=random.randint(10000, 30000),
                type_of_measurement="kg",
                quantity=10,
            )  
  
    def test_sell_product(self):
        self.client.login(username="test_user", password="my_pass",)
        url = reverse("sell_product")
        
        context = {
            "name":"dip",
            "type_of_trade":"debt",
            "selledproduct_set-TOTAL_FORMS":'7',
            "selledproduct_set-INITIAL_FORMS":'0',
            "selledproduct_set-MIN_NUM_FORMS":'0',
            "selledproduct_set-MAX_NUM_FORMS":'1000',
            "selledproduct_set-0-product":1,
            "selledproduct_set-0-quantity":5,
            "selledproduct_set-0-type_of_price":"selling",
            "selledproduct_set-1-product":2,
            "selledproduct_set-1-quantity":4,
            "selledproduct_set-1-type_of_price":"selling",
            "selledproduct_set-2-product":3,
            "selledproduct_set-2-quantity":6,
            "selledproduct_set-2-type_of_price":"selling",
        }
        
        # Sell Productga request jo'natish
        response = self.client.post(url, context)
        print(response.content)
        # Status kodini tekshirish
        self.assertEqual(response.status_code, 302)

        customer = Customer.objects.get(name="dip")
        self.assertEqual(customer.type_of_trade, "debt")
        self.assertEqual(SelledProduct.objects.filter(customer=customer).count(), 3)

        product1 = Product.objects.get(id=1)
        product2 = Product.objects.get(id=2)
        product3 = Product.objects.get(id=3)
        product4 = Product.objects.get(id=4)
        
        
        self.assertEqual(product1.quantity, 5)
        self.assertEqual(product2.quantity, 6)
        self.assertEqual(product3.quantity, 4)
        self.assertEqual(product4.quantity, 10)

        if customer.type_of_trade == "debt":
            print("ishladi")
            debtcustomer = DebtCustomer.objects.get(customer=customer)
            self.assertEqual(debtcustomer.amount, customer.amount)
            self.assertEqual(debtcustomer.is_payed, False)

            debt_url = reverse("debt_customer_list")

            context = {
                "debt_id":debtcustomer.id,
                "amount":customer.amount
            }

            response2 = self.client.post(debt_url, context)

            self.assertEqual(response2.status_code, 302)
            debtcustomer.refresh_from_db()
            print(debtcustomer.amount)
            self.assertEqual(debtcustomer.is_payed, True)


class IndexPageTextCase(TestCase):
    def test_page_working(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    

