# MC Vinyl - Vinyl Records E-Commerce Site

## 4th Milestone Project

## Full Stack Frameworks with Django

## Code Institute 2021

---

The brief for this project was to build a full-stack website using the Django framework and which utilised a relational database such as MySQL or Postgres and provided some e-commerce functionality by using Stripe payments. MC Vinyl is a vinyl records store where users; staff or customers can interact with the site giving them full CRUD functionality over a Postgres database.

In the case of staff they can add, edit or delete products. They have a messaging app where they can converse with customers regarding problems with orders.

For customers they can purchase products. If they register to the site they can leave, edit, delete or upvote product reviews. They also have a wishlist which saves to their profile for convenient ordering of favourites. They can view past orders and contact the site owner regarding an order via the messaging function. User authentication is provided. 

The design is based on user experience principles. Clean coding and a responsive mobile first method were employed. Bootstrap 4 was used to aid the responsiveness and front-end design. 

---

### See the image below for an example of the responsiveness of the site.

Click the image to be taken to a live demo of the site:

[![homepage][1]][2]

[1]: ./documentation/images_for_readme/am-i-responsive.jpg
[2]: https://mc-vinyl.herokuapp.com "Live Site" ###############################

---

### **Contents:**

[1. UX Design](#1-ux-design)

[2. Features and Functionality](#2-features-and-functionality)

[3. Technologies Used](#3-technologies-used)

[4. Testing](#4-testing)

[5. Deployment](#5-deployment)

[6. Credits and Notes](#6-credits-and-notes)

---

### **1. UX Design**

#### Strategy

_User Stories:_

There are 2 types of users of the site: the site staff (including owner/administrator) or a customer user.

As the site owner/administrator:

- I want the site layout to be a typical e-commerce with the expected features and smooth navigation between sections.
- I want users to be able to register, login and change password.
- I want the site to be relatively secure for users.
- I want customers to be able to purchase and pay for products.
- I want customers to be able to save favourite items to a wishlist for later which is saved to their account.
- I want customers to be able to save profile information to their account.
- I want staff to be able to add, edit and delete products.
- I want customers to be able to message staff and vice versa with a record kept of all conversations.
- I want customers to be able to search and sort products.
- I want users to be able to make new reviews and edit or delete old reviews.
- I want users to be able to rate products and i want the rating to be updated if reviews are adjusted or deleted.
- I want users to be able to sort reviews.
- I want users to be able to upvote/like other reviews.
- I want the site to have a staff account with exclusive features, such as, crud of products, messaging, adding genres, view all orders.
- I want any text inputs by users to be validated.
- I want users to be able to see updates or news on the site through social media links.
- I want a site that is not crashing with bugs and if there is an error, that it is managed in a good way for the user.

As a customer:

- I want the site to be appealing and easy to use.
- I want the site navigation between sections to be easy.
- I want to be able to search and sort products easily.
- I want to be able to purchase products and pay securely.
- I want to be able to save profile information so i don't have to type the same information every time I order.
- I want to be able to save products to a wishlist, which I may purchase at a later date.
- I want to be able to see past orders and be easily able to contact the site owner in the event of a problem with an order.
- I want be able to be able to read and sort reviews by other customers.
- I want to be able to upvote other most useful reviews for other customers.
- I want to be able to leave reviews myself and be able to edit, or delete those reviews.
- I want to be able to rate products.
- I want to be able to register and change my password.
- I want to know that the site is secure and safe to use.
- I want to be aware of updates or new features through social links.
- I want a site that is not slow to use and full of bugs, or if there is an error it is managed properly.

#### Scope


---

Trash Can icon used under Font Awesome Licence https://fontawesome.com/license

star rating css https://github.com/chrislingxiao/starrating
