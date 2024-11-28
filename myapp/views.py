import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import OrderedItems, CartItem, Product, register ,ProductImage  # Add register here
import razorpay
import logging
from django.urls import reverse

# Create your views here.


def index(request):
    return render(request,'index.html')

def Payment(request,amount):
    try:
        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Convert amount to paise (Razorpay expects amount in paise)
        amount_in_paise = int(float(amount) * 100)
        
        # Create Razorpay order
        payment_data = {
            'amount': amount_in_paise,
            'currency': 'INR',
            'payment_capture': '1'
        }
        
        # Create order
        order = client.order.create(payment_data)
        
        # Prepare context for template
        context = {
            'amount': amount,
            'amount_in_paise': amount_in_paise,
            'order_id': order['id'],
            'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
            'callback_url': 'payment_success'  # URL name for success callback
        }
        
        logger.info(f"Payment initiated for amount: {amount}")
        return render(request, 'Payment.html', context)
        
    except Exception as e:
        logger.error(f"Payment initialization failed: {str(e)}")
        messages.error(request, "Payment initialization failed. Please try again.")
        return redirect('show-cart')

def cart(request):
    return render(request,'cart.html')

def orders(request):
    return render(request,'Orders.html')

def ProductDetail(request,pk):
    try:
        item=Product.objects.get(id=pk)
        images=ProductImage.objects.filter(p_id=item)
    except:
        pass

    return render(request,'ProductDetail.html',locals())

def add_cart(request):
        proid = request.GET.get('proid')
        quan = request.GET.get('quan')
        tprice = request.GET.get('tprice')
        user = None
        try:
            unknown = request.session['log_id']
            user = register.objects.get(id=unknown)
            if user is not None:
                product = Product.objects.get(id=proid)
                t_price = tprice
                quantity = quan
                cartitem = CartItem(p_id=product,user=user,tprice=t_price,quantity=quantity)
                cartitem.save()
                return redirect('ProductDetail', pk=product.id)
            else:
                return redirect('login')

        except:
            return redirect('ProductDetail', pk=product.id)

def Products(request):
    Products = Product.objects.all()
    print(Products)
    return render(request,'Product.html',locals())

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def services(request):
    return render(request,'services.html')

def login(request):
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')


def login(request):
    if request.method == 'POST':
        u_name = request.POST.get('u_name')
        u_pass = request.POST.get('u_pass')
        try:
            user = register.objects.get(username=u_name, password=u_pass)
            if user is not None:
                request.session['log_id'] = user.id
                request.session['log_name'] = user.username
                messages.success(request, "Login successful!")
                return redirect('index')
        except register.DoesNotExist:
            messages.error(request, "Incorrect Username or Password")
            return redirect('login')
    return render(request, 'login.html')

def adduser(request):
    if request.method == 'POST':
      username = request.POST.get('username')
      emailaddress = request.POST.get('email')
      password = request.POST.get('password')
      repassword = request.POST.get('repassword')
      Mobileno= request.POST.get('Mobileno')
      if password != repassword:
          messages.error(request, "Both Password doesn't Match")
          return redirect(signup)
      else:
          query = register(username=username, emailaddress=emailaddress, password=password,Mobileno=Mobileno)
          query.save()
          return redirect(login)

    return render(request, 'login.html')

def show_cart(request):
    userid = request.session.get('log_id')
    cuser = None
    if userid:
        try:
            cuser = register.objects.get(id=userid)
        except register.DoesNotExist:
            cuser = None

    if cuser is not None:
        cart_items = CartItem.objects.filter(user=cuser, status=True)
        total = sum(item.tprice * item.quantity for item in cart_items)  # Calculate total price

        if not cart_items:
            return render(request, "cart.html", {'message': 'Cart is Empty'})

        return render(request, "cart.html", {'cart_items': cart_items, 'total': total})
    else:
        return render(request, 'login.html')

def logout(request):
    del request.session['log_id']
    del request.session['log_name']
    #messages.info(request, "Logout Success fully")
    #return render(request, 'index.html')
    return redirect(index)

def removeitem(request,pk):
    try:
        getcartitem = CartItem.objects.get(id=pk)
        getcartitem.delete()
        messages.success(request, "Item removed from cart successfully")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in cart")
    return redirect('show-cart')

def update_cart(request):
    if request.method == "POST":
        # Assuming you are sending item ID and new quantity from the form
        item_id = request.POST.get('item_id')
        new_quantity = request.POST.get('quantity')

        if item_id and new_quantity:
            try:
                cart_item = CartItem.objects.get(id=item_id)
                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(request, "Cart updated successfully!")
            except CartItem.DoesNotExist:
                messages.error(request, "Item not found in cart.")
        else:
            return HttpResponseBadRequest("Invalid item ID or quantity.")

    return redirect('show-cart')  # Redirect back to the cart page

def Orders(request):
    if request.method == 'POST':
        userid = request.session['log_id']
        try:
            customer = register.objects.get(id=userid)
            getcartitem = CartItem.objects.values('product').filter(user=customer)
            print(getcartitem)
            for item in getcartitem:
                print("Ghooooooooooom")
                pro = Products.objects.get(id=item['product'])
                print(pro)
                ordered = OrderedItems(user=customer,product=pro)
                ordered.save()
            CartItem.objects.filter(user=customer).delete()

        except:
            print("error Occured")
        return redirect(Orders)
    else:
        userid = request.session['log_id']
        order_items = OrderedItems.objects.values('product').filter(user=userid).order_by('-id')
        products = Products.objects.filter(id__in=order_items).values().order_by('-id')
        areProducts = len(products)
        return render(request, "orders.html", locals())


def ConfirmOrder(request):
    try:
        unknown = request.session['log_id']
        user = register.objects.get(id=unknown)
    except:
        user = None
        return redirect(login)
    if request.method == 'POST':
        amount = request.POST.get('money')
        print(amount)
        if user is not None:
            cartitems = CartItem.objects.filter(user=user,status=True)
            orderedItem = OrderedItems(user=user,totalPrice=int(amount))
            orderedItem.save()
            for items in cartitems:
                orderedItem.cart.add(items)
                items.status = False
                items.save()
            orderedItem.save()
            return redirect(ConfirmOrder)
        else:
            return redirect(login)
    else:
        orders = OrderedItems.objects.filter(user=user)
        return redirect(getorders)

def getorders(request):
    userid = request.session.get('log_id')  # Use .get() to avoid KeyError
    if userid is not None:
        order_id = OrderedItems.objects.filter(user=userid)  # Fetch orders for the user
        if order_id.exists():  # Check if any orders exist
            return render(request, 'Orders.html', {'order_id': order_id})
        else:
            return HttpResponse('<h1>No orders found</h1>')
    else:
        return render(request, 'login.html')
    


logger = logging.getLogger(__name__)


def initiate_payment(request, amount):
    try:
        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Create Razorpay order
        payment = client.order.create({
            'amount': amount * 100,  # Amount in paise
            'currency': 'INR',
            'payment_capture': '1'
        })
        
        context = {
            'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
            'order_id': payment['id'],
            'amount_in_paise': amount * 100,
        }
        
        return render(request, 'Payment.html', context)
    except Exception as e:
        messages.error(request, f"Payment initiation failed: {str(e)}")
        return redirect('show-cart')

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            payment_id = data.get('razorpay_payment_id')
            order_id = data.get('razorpay_order_id')
            signature = data.get('razorpay_signature')

            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # Verify payment signature
            params_dict = {
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': order_id,
                'razorpay_signature': signature
            }
            
            try:
                client.utility.verify_payment_signature(params_dict)
                
                # Get current user and process order
                user_id = request.session.get('log_id')
                if not user_id:
                    return JsonResponse({'error': 'User not logged in'}, status=400)
                
                user = register.objects.get(id=user_id)
                cart_items = CartItem.objects.filter(user=user, status=True)
                
                if not cart_items.exists():
                    return JsonResponse({'error': 'No items in cart'}, status=400)
                
                # Create order and process cart items
                total_amount = sum(item.tprice for item in cart_items)
                order = OrderedItems.objects.create(
                    user=user,
                    totalPrice=total_amount,
                    payment_id=payment_id,
                    order_id=order_id
                )
                
                for cart_item in cart_items:
                    order.cart.add(cart_item)
                    cart_item.status = False
                    cart_item.save()
                
                messages.success(request, "Payment successful!")
                return redirect('Getorder')
                
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def payment_failed(request):
    messages.error(request, "Payment failed. Please try again.")
    return redirect('show-cart')