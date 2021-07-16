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
- I want a site that is not slow or full of bugs and if there is an error it is managed properly.

#### Scope

From researching other similar vinyl e-commerce sites it should be possible to provide a broadly similar experience.

Based on the results of the Strategy research the features to be included are:

- Home: Landing page with large obvious CTA and the purpose of the site should be obvious.
- Users can register, login and change password.
- Passwords are validated and hashed.
- Products can be searched by artist, title and genre.
- Products can be sorted by price, rating or alphabetically.
- A wishlist which saves to a user profile.
- A payment system to purchase products using Stripe.
- A user profile where customer shipping information and past orders and associated communication can be saved.
- Sortable product reviews and ratings can be added, edited and deleted.
- Staff can leave a comment underneath a review.
- Reviews can be upvoted.
- Staff messaging app for communicating with customers regarding orders.
- Staff can view all orders and search by customer.
- Staff can add, edit and delete products.
- Staff can add new genre or promotion fields.
- Footer: Links to social media.


From the strategy table all the above features appear viable. Some basic features such as pagination and a contact form may be left out for now due to time constraints. A wishlist and the messaging app for use between staff and customers are more relevant to the project requirements and interesting features to have instead. A CSP strategy would be useful to boost security but may also be left aside for now due to time constraints.

#### Structure

- A pretty typical e-commerce structure with all important pages accessible from any page from the Navbar at the top of the page, including the shopping cart.
- Customer Wishlist link is in the Navbar.
- User account features are accessible through a dropdown sub-menu in the Navbar along with staff features such as the messaging app.
- Custom error page, for 404, 500 and CSRF errors so in the case of a broken internal link or where a CSRF form token has expired, a button is provided for the user to return to safety.

#### Skeleton

Wireframes made in Balsamiq Wireframes were used for basic layout. These can be viewed here:

[Landing Page All Sizes](./documentation/wireframes/landing_page.png)

[Admin Controls Page All Sizes](./documentation/wireframes/admin_controls.png)

[Browse Reviews Page All Sizes](./documentation/wireframes/browse_my_reviews.png)

[New Review Search Page All Sizes](./documentation/wireframes/new_review_search.png)

[New/Edit Review Page All Sizes](./documentation/wireframes/new_edit_review.png)

[Review Detail Page All Sizes](./documentation/wireframes/review_detail.png)

[Register Page All Sizes](./documentation/wireframes/register.png)

[Change Password Page All Sizes](./documentation/wireframes/change_password.png)

[Contact Page All Sizes](./documentation/wireframes/contact_page.png)

#### Surface

[Pixabay](https://pixabay.com/) provided the free background image and the logo icon. The main font is a Google font called Monoton which conveniently matches the vinyl theme, with the secondary font being Montserrat.
The main colors used were #F9F6F6 for the background contrasting with #451D1D for much of the text and the footer. #A20B0B is used for the banner announcing free delivery.

![ColourChoices][3]

[3]: ./documentation/images_for_readme/palette.png "Colour Choices"

---

### **2. Features and Functionality**

The site was designed with a mobile first approach. Customised Bootstrap was used to help with the responsiveness and layout of the site. In addition targeted media queries were used to assist with this. The site borrows much of the functionality of Stripe payments from the Boutique Ado project however modified to suit this application. Superuser staff do not have access to the admin backend of the site. There is a specific Staff setting to allow that. 

The Crispy Forms add-on is used throughout the site to aid form formatting. Each form has a CSRF tag for added security.

Bootstrap toasts are used to provide feedback to the user regarding an action by utilising the Django message system levels and displaying the messages within the toasts.

_Landing Page:_

The landing page features a simple layout with a background image which assists in directing the user as to the purpose of the site and a large CTA to enter the shop. The navbar alternatively gives access to search the site directly or to log-in.

_Authentication Pages:_

Including Log-in, log-out, register, verification and change password are all handled using the Django-Allauth add-on which integrates seamlessly.

_Products Page:_

User can see all products. They can search and sort. The search input will search by artist or title or genre. Genres can be clicked directly or the dropdown sort allows sorting by price, rating or alphabetically. Product ratings are shown and additional edit and delete product buttons are shown to superusers.

_Product Details Page:_

Here users can see details of the product. The track listing makes use of the add-on Django-Better-Admin-Arrayfield. A Postgres relational database was used both locally and when deployed, as the sqlite3 or mysql versions will not handle the arrayfield.

If a user is logged in they can; add the product to their wishlist, add it to their cart, leave a review and rating. They can also sort reviews by most popular review, by latest review or highest/lowest rating. There is also a button to edit or delete their own review. Superusers can again see the additional edit and delete buttons.

_Product Review Page:_

Here there's a form where users can edit or delete a past review and superusers can leave a comment beneath a review, which can be useful if it is a complaint. A modal is used to confirm a delete action.

_Wishlist Page:_

The wishlist allows users to make a list of up to 10 favourite products which they might like to purchase at some point in the future. For convenience there's are buttons to add each individual product to the cart or all items at once. This is one of the big advantages for a customer to sign up to the site as you cannot access or use the wishlist otherwise.

_Cart Page:_

As with any e-commerce site the cart shows the products added for purchase and a total to be paid including delivery.

_Checkout Page:_

The checkout page shows details of the intended purchases including a delivery cost if total is less than the free delivery threshold. Stripe credit card payments input are integrated into the template.

_My Profile Page:_

From here customers can save address details to make checkout quicker and easier. The can also view past orders and start a conversation with the site owners regarding a particular order. When they receive a message back they will also get an email notification to let them know they have a new message. A users username and email address are fixed and are the ones they signed up with.




---

Trash Can icon used under Font Awesome Licence https://fontawesome.com/license

star rating css https://github.com/chrislingxiao/starrating
