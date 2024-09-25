# Self-Service Order System

## Overview

This project is a self-service order system designed for restaurants and cafes. It allows customers to place their orders independently without the need for authentication. The system includes a guest checkout feature where customers can add items to their cart, proceed to checkout, and place their order.

Admins can manage menus, orders, bills, and transactions through Django's built-in admin interface. Payment is currently handled manually with cash.

## Features

- **Guest-Based Ordering**: Customers can place orders without needing to log in or register.
- **Menu Display**: Customers can view the available menu items on the main page and add them to their cart.
- **Cart Management**: Customers can add items to their cart and adjust quantities as needed.
- **Checkout Process**: A straightforward checkout page to finalize an order.
- **Billing**: A generated bill for the customer's order.

## Pages

### Main Page (Menu)
Displays the list of available menu items with an option to add items to the cart.

![Main Page](https://github.com/user-attachments/assets/8c07ea2b-5de5-4b71-a00c-1e5e76b10f87)

### Cart Page
Allows customers to review the items they have added to their cart and reduce item quantities.

![Cart Page](https://github.com/user-attachments/assets/02cd5050-8acc-4fca-8f5b-2f6e73a59dfd)

### Checkout Page
Customers can review their order, provide necessary details, and confirm the checkout.

![Checkout Page](https://github.com/user-attachments/assets/22a55fd6-fa92-4b05-a825-a7eb1949cf89)

### Bill Page
Displays the bill for the customer's order after the checkout is complete.

![Bill Page](https://github.com/user-attachments/assets/b6046795-7d87-419d-bea0-7294c147ae01)


## To Do
- [ ] **Payment Handling**: Implement payment or transaction handling.
- [ ] **Receipt Generation**: Generate a receipt for the order.
