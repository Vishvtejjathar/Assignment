from django.shortcuts import render
from core.models import Users, Products, Orders
import threading

def insert_data(request):
    users_data = [
        (1, "Alice", "alice@example.com"),
        (2, "Bob", "bob@example.com"),
        (3, "Charlie", "charlie@example.com"),
        (4, "David", "david@example.com"),
        (5, "Eve", "eve@example.com"),
        (6, "Frank", "frank@example.com"),
        (7, "Grace", "grace@example.com"),
        (8, "Alice", "alice@example.com"),
        (9, "Henry", "henry@example.com"),
        (10, "", "jane@example.com"),
    ]

    products_data = [
        (1, "Laptop", 1000.00),
        (2, "Smartphone", 700.00),
        (3, "Headphones", 150.00),
        (4, "Monitor", 300.00),
        (5, "Keyboard", 50.00),
        (6, "Mouse", 30.00),
        (7, "Laptop", 1000.00),
        (8, "Smartwatch", 250.00),
        (9, "Gaming Chair", 500.00),
        (10, "Earbuds", -50.00),
    ]

    orders_data = [
        (1, 1, 1, 2),
        (2, 2, 2, 1),
        (3, 3, 3, 5),
        (4, 4, 4, 1),
        (5, 5, 5, 3),
        (6, 6, 6, 4),
        (7, 7, 7, 2),
        (8, 8, 8, 0),
        (9, 9, 1, -1),
        (10, 10, 11, 2),
    ]

    def insert_users():
        Users.objects.all().delete()  # Clear previous data
        for user in users_data:
            if user[1] and user[2]:  # Ensure name and email are not empty
                Users.objects.create(id=user[0], name=user[1], email=user[2])

    def insert_products():
        Products.objects.all().delete()
        for product in products_data:
            if product[2] > 0:  # Ensure the price is positive
                if product[1]:  # Ensure product name is not empty
                    Products.objects.create(id=product[0], name=product[1], price=product[2])

    def insert_orders():
        Orders.objects.all().delete()
        for order in orders_data:
            # Check if user exists and product exists
            user_exists = Users.objects.filter(id=order[1]).exists()
            product_exists = Products.objects.filter(id=order[2]).exists()

            # Ensure quantity is valid and the product and user exist
            if user_exists and product_exists and order[3] > 0:
                Orders.objects.create(id=order[0], user_id=order[1], product_id=order[2], quantity=order[3])

    # Create threads for each insertion task
    threads = []
    
    # Create and start the threads for each insertion task
    thread_users = threading.Thread(target=insert_users)
    thread_products = threading.Thread(target=insert_products)
    
    # Start user and product insert threads
    thread_users.start()
    thread_products.start()
    
    # Wait for user and product threads to complete before starting orders insertion
    thread_users.join()
    thread_products.join()

    # Now insert orders after ensuring the users and products have been inserted
    thread_orders = threading.Thread(target=insert_orders)
    thread_orders.start()
    thread_orders.join()  # Ensure orders are inserted after users and products

    # Context for the template
    context = {
        'users_count': Users.objects.count(),
        'products_count': Products.objects.count(),
        'orders_count': Orders.objects.count(),
    }

    return render(request, 'index.html', context)
