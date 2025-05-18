from django.shortcuts import render
from datetime import timedelta
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate as auth_authenticate 
from django.contrib.auth import  login as auth_login 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log
from django.contrib import messages
from .models import (MyCustomUser,Bakery_category,Bakery_recipe,add_cart, our_signature_banner,our_products_data,offer,review,user_comments,Prebooking)
from datetime import timedelta,datetime
from itertools import groupby
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import  make_password
from django.contrib.auth import authenticate, login as auth_login






@login_required(login_url='/admin_login')
def delete_photo(request,id):
    data = our_signature_banner.objects.get(id = id)
    data.img.delete()
    data.delete()
    return redirect('/add_our_banner')




@login_required(login_url='/admin_login')
def add_our_banner(request):
    data1 = our_signature_banner.objects.all()
    try:
        data = MyCustomUser.objects.get(username=request.user.username)
        if data.user_type == 'admin':
            if request.method == 'POST':
                img = request.FILES.get('img')
                our_signature_banner.objects.create(img = img) 
            return render(request, 'add_our_banner.html',{'data':data1})
        else:
            return redirect('/admin_login')  
    except MyCustomUser.DoesNotExist:
        return redirect('/admin_login') 



@login_required(login_url='/login')
def celebration(request):
    data = Prebooking.objects.all()
    return render(request, 'celebration.html',{'data':data})


@login_required(login_url='/login')
def booking(request):
    data = Prebooking.objects.filter(user = request.user)
   
    user_data = MyCustomUser.objects.get(username = request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests = request.POST.get('guests')
        requests = request.POST.get('requests')
        Prebooking.objects.create(
         user = request.user,name=name, email=email, phone=phone,
            date=date, time=time, guests=guests, requests=requests
        )
        return redirect('/booking')
    return render(request, 'booking.html',{'data':data,'user':user_data})




@login_required(login_url='/login')
def user_review(request):
    data =  review.objects.filter(user = request.user)
    data1 =  review.objects.all()
    star_range = range(1, 6)
    if request.method == 'POST':
        num_of_stars = request.POST.get('stars')
        comments = request.POST.get('comments')
        review.objects.create(user = request.user ,num_of_stars = num_of_stars, comments = comments)
        return redirect('/success_rev')
    return render(request, 'review.html',{'data':data,'data1':data1,'star_range': star_range})



def success_comment(request):
    data = 'Compaint or ideas'
    return render(request, 'success_rev.html',{'data':data})


def success_rev(request):
    data = 'Review'
    return render(request, 'success_rev.html',{'data':data})




@login_required(login_url='/admin_login')
def admin_remove_reviews(request, id):
    user = get_object_or_404(MyCustomUser, username=request.user.username)
    if user.user_type == 'admin':
        try:
            data = review.objects.get(id=id)
            data.delete()
        except review.DoesNotExist:
            pass
        return redirect('/admin_review')
    else:
        return redirect('admin_login')


@login_required(login_url='/login')
def compaint(request):
    data =  user_comments.objects.filter(user = request.user)
    if request.method == 'POST':
        com = request.POST.get('comments')
        user_comments.objects.create(user = request.user , comp = com)
        return redirect('/success_comment')
    return render(request, 'compaint.html',{'data':data})




@login_required(login_url='/login')
def remove_reviews(request, id):
    try:
        data = review.objects.get(id=id)
        data.delete()
    except review.DoesNotExist:
        pass
    return redirect('/review')




@login_required(login_url='/login')
def remove_compaint(request, id):
    try:
        data = user_comments.objects.get(id=id)
        data.delete()
    except user_comments.DoesNotExist:
        pass
    return redirect('/compaint')


@login_required(login_url='/admin_login')
def admin_remove_compaint(request, id):
    user = get_object_or_404(MyCustomUser, username=request.user.username)
    if user.user_type == 'admin':
        try:
            data = user_comments.objects.get(id=id)
            data.delete()
        except user_comments.DoesNotExist:
            pass
        return redirect('/admin_review')
    else:
        return redirect('admin_login')





@login_required(login_url='/admin_login')
def admin_review(request):
    user = get_object_or_404(MyCustomUser, username=request.user.username)
    if user.user_type == 'admin':
        data =  review.objects.all()
        data1 =  user_comments.objects.all()
        star_range = range(1, 6)
    return render(request, 'admin_review.html',{'data':data,'data1':data1,'star_range':star_range})



@login_required(login_url='/login')
def remove_cart(request, id):
    try:
        user_data = MyCustomUser.objects.get(username=request.user)
        data = add_cart.objects.get(user_id=user_data, product_id=id, order_status='In Cart')
        data.delete()
        return redirect('/cart')
    except add_cart.DoesNotExist:
        return redirect('/cart')
    except MyCustomUser.DoesNotExist:
        return redirect('/login')



@login_required(login_url='/admin_login')
def admin_history(request):
    try:
        data = MyCustomUser.objects.get(username=request.user.username)
        if data.user_type == 'admin':
            try:
                order_data = add_cart.objects.filter(order_status='completed')
                user_ids = set()  # Use a set to collect unique user_ids
                for order in order_data:
                    user_ids.add(order.user_id)
                user_details = MyCustomUser.objects.filter(id__in=user_ids)
            except:
                user_details = None
            return render(request, 'admin_history.html', {'data': user_details})
        else:
            return redirect('/admin_login')  # Redirect to admin_login if not admin
    except MyCustomUser.DoesNotExist:
        return redirect('/admin_login') 




@login_required(login_url='/admin_login')
def history_view_order(request, id):
    user = get_object_or_404(MyCustomUser, username=request.user.username)
    if user.user_type == 'admin':
        user_data = add_cart.objects.filter(user_id=id, order_status='completed')
        data = []
        total_price = 0  
        for product_id in user_data:
            try:
                bakery_recipe = Bakery_recipe.objects.get(id=product_id.product_id)
                qyt = int(product_id.qyt)
                item_price = int(bakery_recipe.price)  
                total_price += int(item_price) * int(qyt)  
                data.append({'bakery_recipe': bakery_recipe, 'qty': qyt, 'total_price': item_price * qyt})
            except Bakery_recipe.DoesNotExist:
                print(f"Bakery_recipe with id {product_id} does not exist")

        return render(request, 'history_view_order.html', {'data': data, 'total_price': total_price})
    return render(request, 'history_view_order.html')






@login_required(login_url='/admin_login')
def print(request, id):

    try:
        user_data = add_cart.objects.filter(user_id=id, order_status='Order')
        user_orders = []
        tot = 0

        for item in user_data:
            try:
                product = Bakery_recipe.objects.get(id=item.product_id)
                quantity = int(item.qyt)
                price = float(product.price)
                total_price = price * quantity
                tot += total_price

                user_orders.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': total_price,
                })
            except Bakery_recipe.DoesNotExist:
                print(f"Bakery_recipe with id {item.product_id} does not exist")
        user_dataaa = MyCustomUser.objects.get(id = id)
        current_time = datetime.now().time()
        current_date = datetime.now().strftime('%Y-%m-%d')
        return render(request, 'print.html', {'data': user_orders, 'tot': tot,'id':id,'date':current_date,'user_dataaa':user_dataaa,'time':current_time})
    except Bakery_recipe.DoesNotExist:
        pass
    return render(request, 'print.html')



@login_required(login_url='/admin_login')
def view_order(request, id):
    try:
        user_data = add_cart.objects.filter(user_id=id, order_status='Order')
        user_orders = []
        tot = 0

        for item in user_data:
            try:
                product = Bakery_recipe.objects.get(id=item.product_id)
                quantity = int(item.qyt)
                price = float(product.price)
                total_price = price * quantity
                tot += total_price

                user_orders.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': total_price,
                })
            except Bakery_recipe.DoesNotExist:
                print(f"Bakery_recipe with id {item.product_id} does not exist")

        if request.method == 'POST':
            det = request.POST.get('det')
            # Cancel            
            if det == 'Completed':
                for x in user_data:
                    x.order_status = 'completed'
                    x.save()
                return redirect('/admin_order')
            elif det == 'Accepect':
                for x in user_data:
                    x.number = 1 
                    x.save()
            else:
                for x in user_data:
                    x.order_status = 'Cancelled'
                    x.save()
                return redirect('/admin_order')

        return render(request, 'view_order.html', {'data': user_orders, 'tot': tot,'id':id})
    except Bakery_recipe.DoesNotExist:
        pass
    return render(request, 'view_order.html')




@login_required(login_url='/admin_login')
def admin_order(request):
    try:
        data = MyCustomUser.objects.get(username=request.user.username)
        if data.user_type == 'admin':
            try:
                order_data = add_cart.objects.filter(order_status='Order')
                user_ids = set()  # Use a set to collect unique user_ids
                for order in order_data:
                    user_ids.add(order.user_id)

                user_details = MyCustomUser.objects.filter(id__in=user_ids)
            except:
                user_details: None
            return render(request, 'admin_order.html', {'data': user_details})
        else:
            return redirect('/admin_login')  # Redirect to admin_login if not admin
    except MyCustomUser.DoesNotExist:
        return redirect('/admin_login') 

@login_required(login_url='/login')
def user_history(request):
    product_data = add_cart.objects.filter(user_id=request.user.id, order_status='completed')
    data = []
    
    for item in product_data:
        try:
            bakery_recipe = Bakery_recipe.objects.get(id=item.product_id)
            quantity = int(item.qyt)
            price = float(bakery_recipe.price)
            total_price = price * quantity
            data.append({
                'product': bakery_recipe,
                'quantity': int(item.qyt),
                'total_price': total_price
            })
        except Bakery_recipe.DoesNotExist:
            print(f"Bakery_recipe with id {item.product_id} does not exist")
            
    return render(request, 'user_history.html', {'data': data})


@login_required(login_url='/login')
def order(request):
    try:
        user = request.user
        order_data = add_cart.objects.filter(user_id=user.id, order_status='Order')
        order_data_det = order_data.first()  # Get the first item, if exists

        user_orders = []
        tot = 0
        for item in order_data:
            try:
                product = Bakery_recipe.objects.get(id=item.product_id)
                quantity = int(item.qyt)
                price = float(product.price)
                total_price = price * quantity
                tot += total_price
                user_orders.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': total_price,
                })
            except Bakery_recipe.DoesNotExist:
                print(f"Bakery_recipe with id {item.product_id} does not exist")

        if request.method == 'POST':
            for x in order_data:
                x.order_status = 'canceled'
                x.save()
            return redirect('/order')

        return render(request, 'order.html', {'data': user_orders, 'tot': tot, 'data1': order_data_det})

    except Exception as e:
        print(e)
        return render(request, 'order.html', {'data': [], 'tot': 0, 'data1': None})

@login_required(login_url='/login')
def order_success(request):
    try:
        user = request.user
        order_data = add_cart.objects.filter(user_id=user.id, order_status='Order')
        order_data_det = order_data.first()  # Get the first item, if exists

        user_orders = []
        tot = 0
        
        for item in order_data:
            try:
                product = Bakery_recipe.objects.get(id=item.product_id)
                quantity = int(item.qyt)
                price = float(product.price)
                total_price = price * quantity
                tot += total_price
                user_orders.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': total_price,
                })
            except Bakery_recipe.DoesNotExist:
                print(f"Bakery_recipe with id {item.product_id} does not exist")
        advance = tot/2
        return render(request, 'order_sucess.html', {'tot': tot,'advance':advance})

    except Exception as e:
        print(e)
        return render(request, 'order_sucess.html', {'tot': 0})
    


@login_required(login_url='/login')
def cart(request):
    user = request.user
    order_data = add_cart.objects.filter(user_id=user.id, order_status='In Cart')
    user_orders = []
    tot = 0
    for item in order_data:
        product = Bakery_recipe.objects.get(id=item.product_id)
        quantity = int(item.qyt)
        price = float(product.price)
        total_price = price * quantity
        tot += total_price
        user_orders.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price
        })
    if request.method == 'POST':
        for x in order_data:
            x.order_status = 'Order'
            x.save()
        return redirect('/order_success')
    return render(request, 'cart.html', {'data': user_orders,'tot':tot})






@login_required(login_url='/login')  
@require_POST
def add_to_cart(request):
    try:
        user = request.user
    except:
        return redirect('/login')
    recipe_id = request.POST.get('recipe_id')
    action = request.POST.get('action')
    quantity = request.POST.get('quantity')
 
    data = get_object_or_404(MyCustomUser, username=request.user)
    
    if recipe_id and action:
        try:
            recipe = get_object_or_404(Bakery_recipe, id=recipe_id)
            cart_item = add_cart.objects.filter(user=request.user, product_id=recipe_id, order_status='In Cart').first()
            
            if action == 'add':
                if cart_item:
                    return JsonResponse({'status': 'error', 'message': 'Item already in cart'}, status=400)
                else:
                    cart_item = add_cart.objects.create(
                        user=request.user,
                        product_id=recipe_id,
                        order_status='In Cart',
                        number=data.number_pare,
                        qyt = int(quantity)
                    )
                    return JsonResponse({'status': 'added'})
                
            elif action == 'remove':
                if cart_item:
                    cart_item.delete()  # Delete the cart item
                    return JsonResponse({'status': 'removed'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Item not found in cart'}, status=400)
        
        except Bakery_recipe.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Bakery recipe does not exist'}, status=404)
        except MyCustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=404)
        except add_cart.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cart item does not exist'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)







def list_recipe(request,category):
    data = Bakery_recipe.objects.all()
    product_det = Bakery_recipe.objects.filter(category=category)
    return render(request, 'list_recipe.html', {'data': product_det, 'x': category})






def recipe(request):
    data = Bakery_category.objects.all()
    return render(request, 'recipe.html', {'data': data})


@login_required(login_url='/admin_login')
def user(request):
    try:
        data = MyCustomUser.objects.get(username=request.user.username)
        if data.user_type == 'admin':
            data = MyCustomUser.objects.all()
            return render(request, 'users.html', {'data': data})
        else:
            return redirect('/admin_login')  
    except MyCustomUser.DoesNotExist:
        return redirect('/admin_login')  

@login_required(login_url='/admin_login')
def delete_recipe(request, id):
    try:
        data = Bakery_recipe.objects.get(id=id)
        data.img1.delete()
        data.delete()
    except Bakery_recipe.DoesNotExist:
        pass
    return redirect('/our_products')



@login_required(login_url='/login')
def product_edit(request, id):
    dis = Bakery_recipe.objects.values('category').distinct()
    data_all = Bakery_recipe.objects.all()
    data = get_object_or_404(Bakery_recipe, id=id)
    
    if request.method == 'POST':
        category = request.POST.get('category')
        img1 = request.FILES.get('img1')
        name = request.POST.get('name')
        price = request.POST.get('price')
        price_in_market = request.POST.get('price_in_market')
        weight = request.POST.get('weight')
        inches = request.POST.get('inches')

        data.category = category
        if img1:
            data.img1.delete()  # Delete the old image file
            data.img1 = img1
        else:
            pass
        data.name = name
        data.price = price
        data.weight = weight
        data.inches = inches
        data.price_in_market = price_in_market

        data.save()
        return redirect('/our_products')

    return render(request, 'product_edit.html', {'data': data_all,'dis':dis, 'x': data})



@login_required(login_url='/admin_login')
def our_products(request):
    try:
        data = MyCustomUser.objects.get(username=request.user.username)
        if data.user_type == 'admin':
            data = Bakery_recipe.objects.all()
            return render(request, 'our_product.html', {'data': data})
        else:
            return redirect('/admin_login')  # Redirect to user login if not admin
    except MyCustomUser.DoesNotExist:
        return redirect('/admin_login')  # Redirect to login if user does not exist


@login_required(login_url='/admin_login')
def add_recipe(request):
    try:
        dis = Bakery_category.objects.values('category').distinct()
        data = MyCustomUser.objects.get(username=request.user.username)
        if data.user_type == 'admin':
            data = Bakery_category.objects.all()
            if request.method == 'POST':
                category = request.POST.get('category')
                img1 = request.FILES.get('img1')
                name = request.POST.get('name')
                price = request.POST.get('price')
                price_in_market = request.POST.get('price_in_market')
                weight = request.POST.get('weight')
                inches = request.POST.get('inches')
                Bakery_recipe.objects.create(category = category,price_in_market = price_in_market, img1 = img1, name = name, price = price, weight = weight, inches = inches) 
            return render(request, 'add_recipe.html',{'data':data,'dis':dis})
        else:
            return redirect('/login')  
    except MyCustomUser.DoesNotExist:
        return redirect('/login') 


@login_required(login_url='/admin_login')
def del_category(request, id):
    try:
        data = Bakery_category.objects.get(id=id)
        data.img.delete()
        data.delete()
    except Bakery_category.DoesNotExist:
        pass
    return redirect('/add_category')

@login_required(login_url='/admin_login')
def add_category(request):
    try:
        data = MyCustomUser.objects.get(username=request.user.username)
        if data.user_type == 'admin':
            data = Bakery_category.objects.all()
            if request.method == 'POST':
                img = request.FILES.get('img')
                category = request.POST.get('category')
                Bakery_category.objects.create(category=category,img = img)
                return redirect('/add_category')
            return render(request, 'add_category.html', {'data': data})
        else:
            return redirect('/login')  # Redirect to user login if not admin
    except MyCustomUser.DoesNotExist:
        return redirect('/login')  # Redirect to login if user does not exist







@login_required(login_url='/admin_login')
def dashboard(request):
    try:
        data = MyCustomUser.objects.get(username=request.user.username)
        if data.user_type == 'admin':
            off = offer.objects.all().first()
            print(off)
            try:
                order_data = add_cart.objects.filter(order_status='Order')
                user_ids = set()  # Use a set to collect unique user_ids
                for order in order_data:
                    user_ids.add(order.user_id)
                    
                user_details = MyCustomUser.objects.filter(id__in=user_ids).count()
                print(user_details)
            except:
                user_details: None
            if request.method == 'POST':
                if off != None:
                    if (off.of or len(off.of) == 0):
                        offf =  request.POST.get('offer') 
                        off.of = offf 
                        off.save()
                        return redirect('/dashboard')
                else:
                    off = request.POST.get('offer')
                    offer.objects.create(of = off)
                    return redirect('/dashboard')
            return render(request, 'dashboard.html',{'off':off,'dataaaa': user_details})
        else:
            return redirect('/admin_login')  # Redirect to user login if not admin
    except MyCustomUser.DoesNotExist:
        return redirect('/admin_login')  # Redirect to login if user does not exist







@login_required(login_url='/admin_login')
def off_delete(request,id):
    try:
        data = MyCustomUser.objects.get(username=request.user.username)
        if data.user_type == 'admin':
            off = offer.objects.get(id = id) 
            off.delete()
            return redirect('/dashboard')
    except MyCustomUser.DoesNotExist:
        return redirect('/admin_login')  # Redirect to login if user does not exist




def admin_login(request):
    if request.user.is_authenticated:
        try:
            data = MyCustomUser.objects.get(username=request.user.username)
        except MyCustomUser.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist'})
        if data.user_type == 'user':

            return redirect('/')
        else:
            return redirect('/dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me') == 'on'
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                data = MyCustomUser.objects.get(username=user.username)
            except MyCustomUser.DoesNotExist:
                return render(request, 'login.html', {'error': 'User does not exist'})
            
            if data.user_type == 'admin':
                auth_login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)  # Session will expire when the user closes the browser
                else:
                    request.session.set_expiry(timedelta(days=30))  # Session will expire in 30 days
                return redirect('/dashboard')
            else:
                return render(request, 'login.html', {'error': 'Access denied for non-admin users'})
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'login.html')


@login_required(login_url='/admin_login')
def dashboard(request):
    try:
        data = MyCustomUser.objects.get(username=request.user.username)
        if data.user_type == 'admin':
            off = offer.objects.all().first()
            
            try:
                order_data = add_cart.objects.filter(order_status='Order')
                user_ids = set()  # Use a set to collect unique user_ids
                for order in order_data:
                    user_ids.add(order.user_id)
                    
                user_details = MyCustomUser.objects.filter(id__in=user_ids).count()
                print(user_details)
            except:
                user_details: None
            if request.method == 'POST':
                if off != None:
                    if (off.of or len(off.of) == 0):
                        offf =  request.POST.get('offer') 
                        off.of = offf 
                        off.save()
                        return redirect('/dashboard')
                else:
                    off = request.POST.get('offer')
                    offer.objects.create(of = off)
                    return redirect('/dashboard')
            return render(request, 'dashboard.html',{'off':off,'dataaaa': user_details})
        else:
            return redirect('/admin_login')  # Redirect to user login if not admin
    except MyCustomUser.DoesNotExist:
        return redirect('/admin_login')  # Redirect to login if user does not exist



def pass_change(request, id):
    user = MyCustomUser.objects.get(id=id)

    if request.method == 'POST':
        
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if len(new_password) < 7:
            messages.error(request, 'New password must be at least 7 characters long.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        else:
            # Update password
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/login')

    return render(request, 'pass_change.html', {'user': user})





def check_username(request):
    if request.method == 'GET':
        username = request.GET.get('username', None)
        print(username)
        response = {
            'exists': False
        }

        if username:
            try:
                user = MyCustomUser.objects.get(username=username)
                response['exists'] = True
                response['phone_number'] = user.phone_number 
            except MyCustomUser.DoesNotExist:
                response['message'] = 'Username does not exist'

        return JsonResponse(response)


def forgot_verifiy(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        number = request.POST.get('number')
        if MyCustomUser.objects.filter(username = username, phone_number = number).exists():
            dd = MyCustomUser.objects.get(username = username)
            return redirect('/pass_change/'+ str(dd.id) +'/')
        else:
            messages.success(request,'Phone number does not match the username.') 
            return redirect('/forgot_verifiy')
    return render(request,'forgot_verifiy.html')


def logout(request):
    log(request)
    return redirect('/')


@login_required(login_url='/login')  
def profile_edit(request,id):
    username = request.user
    data = MyCustomUser.objects.get(username=username)
    if request.method == 'POST':
        phone_number = request.POST.get('number')
        postcode = request.POST.get('postcode')
        address = request.POST.get('address')
        near_by = request.POST.get('near_by')
        data.phone_number = phone_number        
        data.postcode = postcode
        data.address = address
        data.near_by = near_by
        data.save()
        return redirect('/profile')
    return render(request,'profile_edit.html',{'data': data})



@login_required(login_url='/login')  
def profile(request):
    username = request.user
    data = MyCustomUser.objects.get(username=username)
    return render(request,'profile.html',{'data': data})




# Create your views here.
def index(request):
    star_range = range(1, 6)
    data1 =  review.objects.all()
    data = our_signature_banner.objects.all()
    #data1 = our_products_data.objects.all()
    off = offer.objects.all().first()
    return render(request,'index.html',{'star_range': star_range,'data':data,'off':off,'user_rev':data1})


@login_required(login_url='/admin_login')
def off_delete(request,id):
    try:
        data = MyCustomUser.objects.get(username=request.user.username)
        if data.user_type == 'admin':
            off = offer.objects.get(id = id) 
            off.delete()
            return redirect('/dashboard')
    except MyCustomUser.DoesNotExist:
        return redirect('/admin_login') 


def login(request):
    if request.user.is_authenticated:
        try:
            data = MyCustomUser.objects.get(username=request.user.username)
        except MyCustomUser.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist'})
        if data.user_type == 'user':
            if not request.POST.get('remember_me'):
                request.session.set_expiry(0) 
            return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me') == 'on'
        user = auth_authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                data = MyCustomUser.objects.get(username=user.username)
            except MyCustomUser.DoesNotExist:
                return render(request, 'login.html', {'error': 'User does not exist'})
            
            if data.user_type == 'user':
                auth_login(request, user)
                request.session.set_expiry(30 * 24 * 60 * 60)
                return redirect('/')
            elif data.user_type == 'admin':
                request.session.set_expiry(30 * 24 * 60 * 60)
                return redirect('/dashboard')
            else:
                return render(request, 'login.html', {'error': 'Access denied for admin users'})
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')




# ------------------------------------------------------------------------------------------------------------------------------------------------



def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('e_mail')
        password1 = request.POST.get('password')
        password2 = request.POST.get('repassword')
        phone_number = request.POST.get('number')
        postcode = request.POST.get('post_code')
        address = request.POST.get('address')
        near_by = request.POST.get('near_by')
        if MyCustomUser.objects.filter(username=username).exists():
            error_message = 'Username is already taken. Please choose another one.'
            messages.error(request, error_message)
            return render(request, 'signup.html', {'error_message': error_message})
        
        if MyCustomUser.objects.filter(phone_number=phone_number).exists():
            error_message = 'Phone number is already taken. Please choose another one.'
            messages.error(request, error_message)
            return render(request, 'signup.html', {'error_message': error_message})
       
        if password1 != password2:
            error_message = 'Passwords do not match.'
            messages.error(request, error_message)
            return render(request, 'signup.html', {'error_message': error_message})
        
        if len(password1)<=6:
            error_message = 'Passwords should be a minimum of 6 letters or more.'
            messages.error(request, 'Passwords should be a minimum of 6 letters or more.')
            return render(request, 'signup.html', {'error_message': error_message})
            
        user = MyCustomUser.objects.create_user(number_pare = 0,username=username,address=address,postcode = postcode,user_type = 'user', near_by = near_by, email=email, password=password1, phone_number=phone_number)
        return redirect('/login')
    return render(request,'signup.html')
