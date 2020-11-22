from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
from .models import Thammart, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
import os

# Create your tests here.
class TestView(TestCase):
    def setUp(self):

        # create profile
        self.s1 = Profile.objects.create(p_user="6010610001",p_name="student",p_sname="one",p_mail="6010610001@thammahakin.com")
        self.s2 = Profile.objects.create(p_user="6010610002",p_name="student",p_sname="two",p_mail="6010610002@thammahakin.com")

        # create user
        self.user1 = User.objects.create_user(username='6010610001', password='123456', email='6010610001@thammahakin.com')
        self.user2 = User.objects.create_user(username='6010610002', password='123456', email='6010610002@thammahakin.com')
        self.user3 = User.objects.create_superuser(username='admin', password='1234', email='admin@reg.com')

        # create product
        self.p1 = Thammart.objects.create(t_user=self.user1,t_name="one",t_detail="one",t_cat="food",t_price="100",t_image="",t_count=0,t_channel="['1','1','1','1']")
        self.p2 = Thammart.objects.create(t_user=self.user1,t_name="one",t_detail="two",t_cat="closet",t_price="100",t_image="",t_count=0,t_channel="['1','1','1','1']")
        self.p3 = Thammart.objects.create(t_user=self.user1,t_name="one",t_detail="three",t_cat="accessary",t_price="100",t_image="[]",t_count=0,t_channel="['1','1','1','1']")
        self.p4 = Thammart.objects.create(t_user=self.user1,t_name="one",t_detail="four",t_cat="beauty",t_price="100",t_image="",t_count=0,t_channel="['1','1','1','1']")
        self.p5 = Thammart.objects.create(t_user=self.user1,t_name="one",t_detail="five",t_cat="electronic",t_price="100",t_image="",t_count=0,t_channel="['1','1','1','1']")
        self.p6 = Thammart.objects.create(t_user=self.user1,t_name="one",t_detail="six",t_cat="others",t_price="100",t_image="",t_count=0,t_channel="['1','1','1','1']")
        self.p7 = Thammart.objects.create(t_user=self.user2,t_name="two",t_detail="one",t_cat="food",t_price="100",t_image="",t_count=0,t_channel="['1','1','1','1']")
        self.p8 = Thammart.objects.create(t_user=self.user2,t_name="two",t_detail="two",t_cat="closet",t_price="100",t_image="",t_count=0,t_channel="['1','1','1','1']")
        self.p9 = Thammart.objects.create(t_user=self.user2,t_name="two",t_detail="three",t_cat="accessary",t_price="100",t_image="",t_count=0,t_channel="['1','1','1','1']")
        self.p10 = Thammart.objects.create(t_user=self.user2,t_name="two",t_detail="four",t_cat="beauty",t_price="100",t_image="",t_count=0,t_channel="['1','1','1','1']")
        self.p11 = Thammart.objects.create(t_user=self.user2,t_name="two",t_detail="five",t_cat="electronic",t_price="100",t_image="",t_count=0,t_channel="['1','1','1','1']")
        self.p12 = Thammart.objects.create(t_user=self.user2,t_name="two",t_detail="six",t_cat="others",t_price="100",t_image="",t_count=0,t_channel="['1','1','1','1']")

        # path url
        self.index_url = reverse('index')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        # self.detail_url = (f"/detail/1")
        self.about_url = reverse('about_view')
        self.register_url = reverse('register')
        self.add_user_url = reverse('add_user')
        self.add_view_url = reverse('add_view')
        self.thammart_url = reverse('thammart')
        self.add_product_url = reverse('add_product')
        self.remove_product_url = reverse('remove_product')
        self.favorite_url = reverse('favo')
        self.add_favo_url = reverse('favorite')
        self.remove_favo_url = reverse('remove_favorite')
        self.search_url = reverse('search')
        self.edit_url = reverse('edit')
        self.edit_product_url = reverse('edit_product')
        self.reset_view_url = reverse('reset_view')
        self.reset_url = reverse('reset')
        self.forgot_view_url = reverse('forgot_view')
        self.forgot_url = reverse('forgot')

        # Client
        self.client = Client()

    def redirect(self , res):
        return dict(res.items())['Location']

    # กรณีที่ล็อคอิน ผิดพลาด ต้องไม่สามารถเข้าสู่ระบบได้
    def test_login_1(self):
        """ check in test_login_1!! """
        response = self.client.post(self.login_url,{'username':'5555','password':'5555'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/login.html')
        self.assertEqual(response.context["message"],"Invalid Credential.")

    # กรณีที่สมัครเป็นสมาชิกแล้ว ต้องสามารถเข้าสู่ระบบได้
    def test_login_2(self):
        """ check in test_login_2!! """
        user = User.objects.filter(email=self.user2.email).first()
        user.is_active=True
        user.save()
        response = self.client.post(self.login_url,{'username':user,'password':'123456'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/")

    # กรณีที่ล็อคอินเป็น แอดมิน ต้องไม่สามารถเข้าสู่ระบบได้
    def test_login_3(self):
        """ check in test_login_3!! """
        user = User.objects.filter(email=self.user3.email).first()
        user.is_active=True
        user.save()
        response = self.client.post(self.login_url,{'username':user,'password':'1234'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินถูกต้องและต้องการล็อคเอ้าท์ ต้องสามารถออกจากระบบได้
    def test_logout(self):
        """ check in test_logout!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเป็น admin ไม่สามารถเข้าถึงหน้า index ได้
    def test_index_0(self):
        """ check in test_index_0!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.index_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ไม่ได้ล็อคอิน ไม่สามารถเข้าถึงหน้า index ได้
    def test_index_1(self):
        """ check in test_index_1!! """
        response = self.client.post(self.index_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินถูกต้อง สามารถเข้าถึงหน้า  index ได้
    def test_index_2(self):
        """ check in test_index_2!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/index.html')
        self.assertEqual(len(response.context["products"]),12)

    # กรณีที่ล็อคอินถูกต้องต้องสามารถเข้าถึงหน้า index และ เลือก ดูหมวดหมู่ของสินค้าชนิด อาหาร (food) ได้
    def test_index_3(self):
        """ check in test_index_3!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.index_url,{'food':'food',})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/index.html')
        # print(response.context["products"])
        self.assertEqual(len(response.context["products"]),2)

    # กรณีที่ล็อคอินถูกต้องต้องสามารถเข้าถึงหน้า index และ เลือก ดูหมวดหมู่ของสินค้าชนิด เสื้อผ้า (closet) ได้
    def test_index_4(self):
        """ check in test_index_4!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.index_url,{'closet':'closet',})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/index.html')
        # print(response.context["products"])
        self.assertEqual(len(response.context["products"]),2)

    # กรณีที่ล็อคอินถูกต้องต้องสามารถเข้าถึงหน้า index และ เลือก ดูหมวดหมู่ของสินค้าชนิด เครื่องประดับ (accessary) ได้
    def test_index_5(self):
        """ check in test_index_5!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.index_url,{'accessary':'accessary',})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/index.html')
        # print(response.context["products"])
        self.assertEqual(len(response.context["products"]),2)

    # กรณีที่ล็อคอินถูกต้องต้องสามารถเข้าถึงหน้า index และ เลือก ดูหมวดหมู่ของสินค้าชนิด เครื่องสำอาง (beauty) ได้
    def test_index_6(self):
        """ check in test_index_6!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.index_url,{'beauty':'beauty',})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/index.html')
        # print(response.context["products"])
        self.assertEqual(len(response.context["products"]),2)

    # กรณีที่ล็อคอินถูกต้องต้องสามารถเข้าถึงหน้า index และ เลือก ดูหมวดหมู่ของสินค้าชนิด อุปกรณ์ไฟฟ้า (electronic) ได้
    def test_index_7(self):
        """ check in test_index_7!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.index_url,{'electronic':'electronic',})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/index.html')
        # print(response.context["products"])
        self.assertEqual(len(response.context["products"]),2)

    # กรณีที่ล็อคอินถูกต้องต้องสามารถเข้าถึงหน้า index และ เลือก ดูหมวดหมู่ของสินค้าชนิด อื่นๆ (others) ได้
    def test_index_8(self):
        """ check in test_index_8!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.index_url,{'others':'others',})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/index.html')
        # print(response.context["products"])
        self.assertEqual(len(response.context["products"]),2)

    # กรณีที่ล็อคอินแล้วจะไม่สามารถเข้าสู่หน้า register ได้
    def test_register_1(self):
        """ check in test_register_1!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/")

    # กรณีที่กรอกข้อมูลไม่ครบถ้วน
    def test_register_2(self):
        """ check in test_register_2!! """
        response = self.client.post(self.add_user_url,{'username':'6010610003','name':'student','sname':'student','password':'','cpassword':'', 'mail':'test@thammahakin.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/register.html')
        self.assertEqual(response.context["message"],"Please complete this registration form.")

    # กรณีที่มี user อยู่แล้ว
    def test_register_3(self):
        """ check in test_register_3!! """
        response = self.client.post(self.add_user_url,{'username':'6010610001','name':'student','sname':'one','password':'123456','cpassword':'123456', 'mail':'test@thammahakin.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/login.html')
        self.assertEqual(response.context["message"],"you are already in website!")

    # กรณีที่กรอก password ผิดพลาด
    def test_register_4(self):
        """ check in test_register_4!! """
        response = self.client.post(self.add_user_url,{'username':'6010610003','name':'student','sname':'three','password':'123455','cpassword':'123456', 'mail':'test@thammahakin.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/register.html')
        self.assertEqual(response.context["message"],"fail to register!")

    # กรณีที่กรอก username เป็นอักขระ
    def test_register_5(self):
        """ check in test_register_5!! """
        response = self.client.post(self.add_user_url,{'username':'student','name':'student','sname':'three','password':'123455','cpassword':'123456', 'mail':'test@thammahakin.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/register.html')
        self.assertEqual(response.context["message"],"fail to register!")

    # กรณีที่ register สมบูรณ์
    def test_register_6(self):
        """ check in test_register_6!! """
        response = self.client.post(self.add_user_url,{'username':'6010610003','name':'student','sname':'three','password':'123456','cpassword':'123456', 'mail':'test@thammahakin.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/login.html')
        self.assertEqual(response.context["message"],"register success!")

    # กรณีไม่ได้ล็อคอินเข้าสู่ระบบจะไม่สามารถเข้าถึงหน้า about ได้
    def test_about_1(self):
        """ check in test_about_1!! """
        response = self.client.post(self.about_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin ไม่สามารถเข้าถึงหน้า about ได้
    def test_about_2(self):
        """ check in test_about_2!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.about_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้สามารถเข้าถึงหน้า about ได้
    def test_about_3(self):
        """ check in test_about_3!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/about.html')

    # #กรณีที่ไม่ได้ล้อคอินเข้าสู่ระบบจะไม่สามารถเข้าถคงหน้ารายละเอียดสินค้าได้
    def test_detail_1(self) :
        """ check in test_detail_1!! """
        product = Thammart.objects.get(pk=1)
        response = self.client.get(f"/detail/{product.id}")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin จะไม่สามารถเข้าถึงหน้ารายละเอียดสินค้าได้
    def test_detail_2(self) :
        """ check in test_detail_2!! """
        self.client.force_login(self.user3)
        product = Thammart.objects.get(pk=1)
        response = self.client.get(f"/detail/{product.id}")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้ สามารถเข้าถึงหน้ารายละเอียดสินค้านั้น ๆ ได้
    def test_detail_3(self) :
        """ check in test_detail_3!! """
        self.client.force_login(self.user1)
        product = Thammart.objects.get(pk=1)
        response = self.client.get(f"/detail/{product.id}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'Thamahakinview/detail.html')
        self.assertEqual(response.context["product"],product)
        self.assertEqual(len(response.context["images"]),0)
        self.assertEqual(len(response.context["channels"]),4)

    # กรณีไม่ได้ล็อคอินเข้าสู่ระบบจะไม่สามารถเข้าถึงหน้าเพิ่มสินค้าได้
    def test_add_view_1(self):
        """ check in test_add_view_1!! """
        response = self.client.post(self.add_view_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin ไม่สามารถเข้าถึงหน้าเพิ่มสินค้าได้
    def test_add_view_2(self):
        """ check in test_add_view_2!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.add_view_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้สามารถเข้าถึงหน้าเพิ่มสินค้าได้
    def test_add_view_3(self):
        """ check in test_add_view_3!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.add_view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'Thamahakinview/add.html')

    # กรณีไม่ได้ล็อคอินเข้าสู่ระบบจะไม่สามารถเข้าถึงหน้า thammart ได้
    def test_thammart_1(self):
        """ check in test_thammart_1!! """
        response = self.client.post(self.thammart_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin ไม่สามารถเข้าถึงหน้า thammart ได้
    def test_thammart_2(self):
        """ check in test_thammart_2!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.thammart_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้สามารถเข้าถึงหน้า thammart ได้
    def test_thammart_3(self):
        """ check in test_thammart_3!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.thammart_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'Thamahakinview/thammart.html')
        self.assertEqual(len(response.context["mymart"]),6)

    # กรณีไม่ได้ล็อคอินเข้าสู่ระบบจะไม่สามารถเข้าถึงหน้า favorite ได้
    def test_favorite_1(self):
        """ check in test_favorite_1!! """
        response = self.client.post(self.favorite_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin ไม่สามารถเข้าถึงหน้า favorite ได้
    def test_favorite_2(self):
        """ check in test_favorite_2!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.favorite_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้สามารถเข้าถึงหน้า favorite ได้
    def test_favorite_3(self):
        """ check in test_favorite_3!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.favorite_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'Thamahakinview/favo.html')
        self.assertEqual(len(response.context["favos"]),0)

    # กรณีไม่ได้ล็อคอินเข้าสู่ระบบจะไม่สามารถเข้าถึงการค้นหาสินค้าได้
    def test_search_1(self):
        """ check in test_search_1!! """
        response = self.client.post(self.search_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin ไม่สามารถเข้าถึงการค้นหาสินค้าได้
    def test_search_2(self):
        """ check in test_search_2!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.search_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้ถูกต้อง และต้องการค้นหาสินค้าที่มีอยู่ในระบบ
    def test_search_3(self):
        """ check in test_search_3!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.search_url,{'product':'one',})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/index.html')
        self.assertEqual(len(response.context["products"]),6)

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้ถูกต้อง และต้องการค้นหาสินค้าที่ไม่มีอยู่ในระบบ
    def test_search_4(self):
        """ check in test_search_4!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.search_url,{'product':'zero',})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/index.html')
        self.assertEqual(len(response.context["products"]),0)

    # กรณีไม่ได้ล็อคอินเข้าสู่ระบบจะไม่สามารถเข้าถึงการเพิ่มสินค้าใน favorite ได้
    def test_add_favo_1(self):
        """ check in test_add_favo_1!! """
        response = self.client.post(self.add_favo_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin ไม่สามารถเข้าถึงการเพิ่มสินค้าใน favorite ได้
    def test_add_favo_2(self):
        """ check in test_add_favo_2!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.add_favo_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้สามารถเข้าถึงการค้นหาเพิ่มสินค้าใน favorite ได้ซึ่งสินค้าชนิดนั้นจะต้องไม่อยู่ใน favorite ของผู้ใช้
    def test_add_favo_3(self):
        """ check in test_add_favo_3!! """
        self.client.force_login(self.user1)
        product = Thammart.objects.get(t_user=self.user2,t_name="two",t_detail="one",t_cat="food")
        response = self.client.post(self.add_favo_url,{'fav':product.id,})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/index.html')
        self.assertEqual(len(response.context["products"]),12)
        self.assertEqual(response.context["messages"],"Successful Add Favorite Product.")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้สามารถเข้าถึงการค้นหาเพิ่มสินค้าใน favorite ได้ และสินค้าอยู่ใน favorite ของผู้ใช้แล้วจะไม่สามารถเพิ่มสินค้าได้
    def test_add_favo_4(self):
        """ check in test_add_favo_4 """
        self.client.force_login(self.user1)
        product = Thammart.objects.get(t_user=self.user2,t_name="two",t_detail="one",t_cat="food")
        response1 = self.client.post(self.add_favo_url,{'fav':product.id,})
        self.assertEqual(response1.status_code, 200)
        self.assertTemplateUsed(response1 , 'users/index.html')
        self.assertEqual(len(response1.context["products"]),12)
        self.assertEqual(response1.context["messages"],"Successful Add Favorite Product.")
        response2 = self.client.post(self.add_favo_url,{'fav':product.id,})
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2 , 'users/index.html')
        self.assertEqual(len(response2.context["products"]),12)
        self.assertEqual(response2.context["messages"],"Product has already in Your Favorite.")

    # กรณีไม่ได้ล็อคอินเข้าสู่ระบบจะไม่สามารถเข้าถึงการลบสินค้าใน favorite ได้
    def test_remove_favo_1(self):
        """ check in test_remove_favo_1!! """
        response = self.client.post(self.remove_favo_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin ไม่สามารถเข้าถึงการลบสินค้าใน favorite ได้
    def test_remove_favo_2(self):
        """ check in test_remove_favo_2!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.remove_favo_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้สามารถเข้าถึงการลบสินค้าใน favorite ได้ ซึ่งสินค้านั้นจะต้องอยู่ใน favorite ของผู้ใช้ก่อนแล้ว
    def test_remove_favo_3(self):
        """ check in test_remove_favo_3!! """
        self.client.force_login(self.user1)
        product = Thammart.objects.get(t_user=self.user2,t_name="two",t_detail="one",t_cat="food")
        response1 = self.client.post(self.add_favo_url,{'fav':product.id,})
        self.assertEqual(response1.status_code, 200)
        self.assertTemplateUsed(response1 , 'users/index.html')
        self.assertEqual(len(response1.context["products"]),12)
        self.assertEqual(response1.context["messages"],"Successful Add Favorite Product.")
        response2 = self.client.post(self.remove_favo_url,{'remove_favo':product.id,})
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2 , 'Thamahakinview/favo.html')
        self.assertEqual(len(response2.context["favos"]),0)
        self.assertEqual(response2.context["messages"],"Successful Remove Favorite Product.")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้สามารถเข้าถึงการลบสินค้าใน favorite ได้ แต่สินค้านั้นไม่อยู่ใน favorite ของผู้ใช้
    def test_remove_favo_4(self):
        """ check in test_remove_favo_4!! """
        self.client.force_login(self.user1)
        product = Thammart.objects.get(t_user=self.user2,t_name="two",t_detail="one",t_cat="food")
        response = self.client.post(self.remove_favo_url,{'remove_favo':product.id,})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'Thamahakinview/favo.html')
        self.assertEqual(len(response.context["favos"]),0)
        self.assertEqual(response.context["messages"],"Product has not already in Your Favorite.")

    # กรณีไม่ได้ล็อคอินเข้าสู่ระบบจะไม่สามารถเข้าถึงการลบสินค้าได้
    def test_remove_product_1(self):
        """ check in test_remove_product_1!! """
        response = self.client.post(self.remove_product_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin ไม่สามารถเข้าถึงการลบสินค้าได้
    def test_remove_product_2(self):
        """ check in test_remove_product_2!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.remove_product_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้สามารถเข้าถึงการลบสินค้าได้ ซึ่งต้องเป็นสินค้าที่ผู้ใช้โพสต์ขายเอง
    def test_remove_product_3(self):
        """ check in test_remove_product_3!! """
        self.client.force_login(self.user2)
        product = Thammart.objects.get(t_user=self.user2,t_name="two",t_detail="one",t_cat="food")
        PATH_IMAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/temporaryfile')
        PATH = os.path.join(PATH_IMAGE, 'grape.jpg')
        with open(PATH,'rb') as image:
            self.client.post(self.edit_product_url,{'edit':product.id,'name':product.t_name,'detail':product.t_detail,'type':product.t_cat,'price':product.t_price,'fileToUpload':image})
        response = self.client.post(self.remove_product_url,{'remove':product.id,})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'Thamahakinview/thammart.html')
        self.assertEqual(len(response.context["mymart"]),5)
        self.assertEqual(response.context["messages"],"Successful Remove Product.")

    # กรณีไม่ได้ล็อคอินเข้าสู่ระบบจะไม่สามารถเข้าถึงหน้าแก้ไขสินค้าได้
    def test_edit_1(self):
        """ check in test_edit_1!! """
        response = self.client.post(self.edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin ไม่สามารถเข้าถึงหน้าแก้ไขสินค้าได้
    def test_edit_2(self):
        """ check in test_edit_2!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้สามารถเข้าถึงหน้าแก้ไขสินค้าได้
    def test_edit_3(self):
        """ check in test_edit_3!! """
        self.client.force_login(self.user1)
        product = Thammart.objects.get(t_user=self.user1,t_name="one",t_detail="two",)
        response = self.client.post(self.edit_url,{'edit':product.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'Thamahakinview/edit.html')
        self.assertEqual(response.context["product"],product)
        self.assertEqual(len(response.context["images"]),0)
        self.assertEqual(len(response.context["channels"]),4)

    # กรณีไม่ได้ล็อคอินเข้าสู่ระบบจะไม่สามารถเข้าถึงหน้าเพิ่มสินค้าได้
    def test_add_product_1(self):
        """ check in test_add_product_1!! """
        response = self.client.post(self.add_product_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin ไม่สามารถเข้าถึงหน้าเพิ่มสินค้าได้
    def test_add_product_2(self):
        """ check in test_add_product_2!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.add_product_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้ถูกต้องสามารถเพิ่มสินค้าได้
    def test_add_product_3(self):
        """ check in test_add_product_3!! """
        self.client.force_login(self.user1)
        PATH_IMAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/temporaryfile')
        PATH = os.path.join(PATH_IMAGE, 'grape.jpg')
        with open(PATH,'rb') as image:
            response = self.client.post(self.add_product_url,{'product':'test','price':120,'type':'food','detail':'test','tel':'0811001000','line':'test','instagram':'test','facebook':'test','fileToUpload':image})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/thammart")
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'users/index.html')
        # self.assertEqual(len(response.context["products"]), 13)
        product = Thammart.objects.get(t_name='test')
        self.client.post(self.remove_product_url,{'remove':product.id,})

    # กรณีไม่ได้ล็อคอินเข้าสู่ระบบจะไม่สามารถเข้าถึงการแก้ไขสินค้าได้
    def test_edit_product_1(self):
        """ check in test_edit_product_1!! """
        response = self.client.post(self.edit_product_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin ไม่สามารถเข้าถึงการแก้ไขสินค้าได้
    def test_edit_product_2(self):
        """ check in test_edit_product_2!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.edit_product_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้ถูกต้อง สามารถแก้ไขรูปภาพของสินค้าได้
    def test_edit_product_3(self):
        """ check in test_edit_product_3!! """
        self.client.force_login(self.user1)
        product = Thammart.objects.get(t_user=self.user1,t_name="one",t_detail="two",)
        PATH_IMAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/temporaryfile')
        PATH = os.path.join(PATH_IMAGE, 'grape.jpg')
        with open(PATH,'rb') as image:
            response = self.client.post(self.edit_product_url,{'edit':product.id,'name':product.t_name,'detail':product.t_detail,'type':product.t_cat,'price':product.t_price,'fileToUpload':image})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Thamahakinview/detail.html')
        product_check = Thammart.objects.get(id=product.id)
        self.assertEqual(product,product_check)
        self.assertEqual(response.context["messages"],"Edit SuccessFul.")
        self.client.post(self.remove_product_url,{'remove':product.id,})

    # กรณีไม่ได้ล็อคอินเข้าสู่ระบบจะไม่สามารถเข้าถึงหน้าแก้ไขรหัสผ่านได้
    def test_reset_view_1(self):
        """ check in test_reset_view_1!! """
        response = self.client.post(self.reset_view_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin ไม่สามารถเข้าถึงหน้าแก้ไขรหัสผ่านได้
    def test_reset_view_2(self):
        """ check in test_reset_view_2!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.reset_view_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้ไม่สามารถเข้าถึงหน้าแก้ไขรหัสผ่านได้
    def test_reset_view_3(self):
        """ check in test_reset_view_3!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.reset_view_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/")

        # กรณีไม่ได้ล็อคอินเข้าสู่ระบบจะสามารถเข้าถึงหน้าลืมรหัสผ่านได้
    def test_forgot_view_1(self):
        """ check in test_forgot_view_1!! """
        response = self.client.post(self.forgot_view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/forgot_password.html')

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin ไม่สามารถเข้าถึงหน้าลืมรหัสผ่านได้
    def test_forgot_view_2(self):
        """ check in test_forgot_view_2!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.forgot_view_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้ไม่สามารถเข้าถึงหน้าลืมรหัสผ่านได้
    def test_forgot_view_3(self):
        """ check in test_forgot_view_3!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.forgot_view_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin ไม่สามารถเข้าถึงการลืมรหัสผ่านได้
    def test_forgot_1(self):
        """ check in test_forgot_1!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.forgot_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้ไม่สามารถเข้าถึงการลืมรหัสผ่านได้
    def test_forgot_2(self):
        """ check in test_forgot_2!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.forgot_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/")

    # กรณีที่ไม่ได้ล็อคอินเข้าสู่ระบบ และกรอก email เพื่อเปลี่ยนรหัสผิด
    def test_forgot_3(self):
        """ check in test_forgot_3!! """
        response = self.client.post(self.forgot_url,{'email' : '6010610003@thammahakin.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/forgot_password.html')
        self.assertEqual(response.context["messages"],"Wrong E-mail")

    # กรณีที่ไม่ได้ล็อคอินเข้าสู่ระบบ และกรอก email เพื่อเปลี่ยนรหัสถูกต้อง
    def test_forgot_4(self):
        """ check in test_forgot_4!! """
        response = self.client.post(self.forgot_url,{'email' : '6010610002@thammahakin.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/reset_password.html')
        self.assertEqual(response.context["user"],self.s2.p_mail)

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะ admin ไม่สามารถเข้าถึงการลืมรหัสผ่านได้
    def test_reset_1(self):
        """ check in test_reset_1!! """
        self.client.force_login(self.user3)
        response = self.client.post(self.reset_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/logout")

    # กรณีที่ล็อคอินเข้าสู่ระบบในฐานะผู้ใช้ไม่สามารถเข้าถึงการลืมรหัสผ่านได้
    def test_reset_2(self):
        """ check in test_reset_2!! """
        self.client.force_login(self.user1)
        response = self.client.post(self.reset_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/")

    # กรณีที่ไม่ได้ล็อคอินเข้าสู่ระบบ และกรอกรหัสผ่านใหม่ไม่ตรงกัน
    def test_reset_3(self):
        """ check in test_reset_3!! """
        response = self.client.post(self.reset_url,{'user' : '6010610002@thammahakin.com','n_password':'01234','nc_password':'12345'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/reset_password.html')
        self.assertEqual(response.context["message"],"Change Password fail!")
        self.assertEqual(response.context["user"],self.s2.p_mail)

    # กรณีที่ไม่ได้ล็อคอินเข้าสู่ระบบ และกรอกรหัสผ่านถูกต้อง
    def test_forgot_4(self):
        """ check in test_forgot_4!! """
        response = self.client.post(self.reset_url,{'user' : '6010610002@thammahakin.com','n_password':'01234','nc_password':'01234'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'users/login.html')
        self.assertEqual(response.context["message"],"Change Password Success!")
