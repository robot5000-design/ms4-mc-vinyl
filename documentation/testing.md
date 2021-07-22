# Testing Report

_* Note all testing was carried out on the deployed version of the site._

## 1. Compare User Test Cases

The first part of testing was to confirm that all user stories requirements have been met. There is large crossover between both sets of user stories.

As the site owner/administrator:

- I want the site layout to be a typical e-commerce with the expected features and smooth navigation between sections.

As a user:

- I want the site to be appealing and easy to use.
- I want the site navigation between sections to be easy.

_These requirements have been met by keeping the site similar to other e-comerce store layouts and not straying beyond convention in terms of layout._

![EasyNavigation][1]

[1]: ../documentation/images_for_readme/easy-nav.jpg "Easy Navigation"

As the site owner/administrator:

- I want users to be able to register, login and change password.

As a user:

- I want to be able to register and change my password.

_These requirements have been met by using Django Allauth to help with authentication providing validated forms for users to register, login and change password._

![Register][2]

[2]: ../documentation/images_for_readme/register.jpg "Register"

![Login][3]

[3]: ../documentation/images_for_readme/login.jpg "Login"

![ChangePassword][4]

[4]: ../documentation/images_for_readme/change-password.jpg "Change Password"

As the site owner/administrator:

- I want customers to be able to search and sort products.

As a user:

- I want to be able to search and sort products easily.

_These requirements have been met by allowing users to search and sort products with the easily accessible search input always at the top of a page. Products can be searched by artist, title or genre and can be sorted by price, by rating or alphabetically. They can also be separated by what's on promotion._

![SearchSort][5]

[5]: ../documentation/images_for_readme/search-sort.jpg "Search and Sort"

As the site owner/administrator:

- I want customers to be able to purchase and pay for products.

As a user:

- I want to be able to purchase products and pay securely.

_These requirements have been met by providing a Stripe payments function enhanced by using Stripe Webhooks for added reliability. Customers can pay for products by credit card. Feedback is provided if a payment fails or succeeds. Orders are saved to the database._

---

As the site owner/administrator:

- I want customers to be able to save favourite items to a wishlist for later which is saved to their account.

As a user:

- I want to be able to save products to a wishlist, which I may purchase at a later date.

_These requirements have been met by providing a Wishlist page where users can save up to 10 of their favourite products referenced to their user account._

![Wishlist][6]

[6]: ../documentation/images_for_readme/wishlist.jpg "Wishlist Page"

As the site owner/administrator:

- I want customers to be able to save profile information to their account.

As a user:

- I want to be able to save profile information so i don't have to type the same information every time I order.

_These requirements have been met by providing a user profile model where users save their payment/shipping information._

---

As the site owner/administrator:

- I want users to be able to make new reviews and edit or delete old reviews.
- I want users to be able to rate products and i want the rating to be updated if reviews are adjusted or deleted.
- I want users to be able to sort reviews.
- I want users to be able to upvote/like other reviews.

As a user:

- I want be able to be able to read and sort reviews by other customers.
- I want to be able to upvote other most useful reviews for other customers.
- I want to be able to leave reviews myself and be able to edit, or delete those reviews.
- I want to be able to rate products.

_These requirements have been met by providing a user review model where users can make reviews and ratings of products and upvote other users reviews. Ratings adjust as reviews are added, changed or deleted. Reviews can be sorted by popularity, date or rating._

![Reviews][6]

[6]: ../documentation/images_for_readme/review.jpg "Reviews Page"

As the site owner/administrator:

- I want any text inputs by users to be validated.

_This requirement has been met because every input form that requires it, has some type of validation. For instance, the search input or review text input cannot be empty. When entering new genre or promotion tags, the programmatic name can only be in a certain format without spaces._

---

As the site owner/administrator:

- I want customers to be able to message staff and vice versa with a record kept of all conversations.

As a user:

- I want to be able to see past orders and be easily able to contact the site owner in the event of a problem with an order.

_These requirements have been met by providing a user message model and messaging app. Past orders can be seen by the site admin on the All Orders page and can be searched by user. Messages can sent by customers and replied to by the site admin. Message threads can be marked open or closed and at a glance the admin can what messages have been replied to. New messages appear in bold font._

![Messaging][7]

[7]: ../documentation/images_for_readme/messaging.jpg "Messaging Page"

![AllOrders][8]

[8]: ../documentation/images_for_readme/all-orders.jpg "All Orders Page"

As the site owner/administrator:

- I want staff to be able to add, edit and delete products.
- I want the site to have a staff account with exclusive features, such as, crud of products, messaging, adding genres, view all orders.

_These requirements have been met by providing views and templates for site admin to add/edit/delete products and add product tags. Admin can leave a comment on a review or delete/edit any review on the site._

![AddEditProduct][9]

[9]: ../documentation/images_for_readme/edit-product.jpg "Add/Edit Product Page"

![AddProductTag][10]

[10]: ../documentation/images_for_readme/add-tags.jpg "Add Product Tag Page"

As the site owner/administrator:

- I want users to be able to see updates or news on the site through social media links.

As a user:

- I want to be aware of updates or new features through social links.

_These requirements have been met by having social media links in the footer._

---

As the site owner/administrator:

- I want a site that is not crashing with bugs and if there is an error, that it is managed in a good way for the user.

As a user:

- I want a site that is not slow or full of bugs and if there is an error it is managed properly.

_These requirements have been met by employing defensive programming, by trying to predict where errors may occur in the code and taking appropriate action. For instance, if there is the possibility of an index error occurring a try/except block is used. Custom http error pages are in use in the templates folder. Depending on the situation, sometimes feedback is provided to the user in the form of a toast error or in the case of a not found error, they may be sent to the custom 404 error page._

---

As the site owner/administrator:

- I want the site to be relatively secure for users.

As a user:

- I want to know that the site is secure and safe to use.

_These requirements have largly been met by Django's own inbuilt security. In addition, SESSION COOKIE SECURE, SESSION COOKIE AGE, CSRF COOKIE SECURE, SECURE HSTS and SECURE SSL REDIRECT have all been set and added to the settings.py file. A CSP policy would increase security even more. The @login required decorator is used on functions that require it and in other functions that should only be accessible to site admins a check is performed to see if the user is a superuser. All URL's have been checked to ensure unauthorised users cannot access functions or parts of the database that they should not have access to. Finally all requests from the front-end which would alter the database are performed as POST only requests for some added security, which means the relevant functions cannot be accessed through the url directly._

---

## 2. Page Responsiveness

### Testing responsiveness of each html page

Using Chrome and Chrome Dev Tools.

Breakpoints | index | products | product detail | register| login | change password | add product | edit product | edit review | add tags | all orders | order detail | profile | past order | messaging | message thread | wishlist | cart | checkout | error
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
W280px | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y
W400px | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y
W576px | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y
W768px | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y
W992px | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y
W1200px | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y | y

- In addition, each page is checked for responsiveness using Chrome Dev Tools infinitely adjustable sliding re-sizer tool. From 280px (Samsung Galaxy Fold) up to full width 1536px on a 4k laptop. Although not optimised for 280px, it is perfectly useable.
- All tests passed.

### __Summary:__

- No problems found.

---

## 3. List of devices tested

- Google Pixel 5
- Samsung Galaxy S7
- Samsung A21s
- Samsung Galaxy S10
- Huawei P30 Pro
- iPhone 11 Safari through Browserstack (limited test)
- Asus k501u 4k laptop
- Chrome Dev Tools Device Emulator:
  - Samsung Galaxy Fold
  - Samsung S5
  - Google Pixel 2
  - iPhone 5
  - iPhone X
  - iPad
  - iPad Pro

The site has been tested on the following browsers on Windows 10:

- Internet Explorer 11
- Firefox 87.0
- Google Chrome 89.0.4389.114
- Opera 75.0.3969.149
- Microsoft Edge 89.0.774.68
- Safari 10.1 on Mac using www.browserstack.com (limited test)

and tested on a Google Pixel 5:

- Chrome 91.0.4472.101

All HTML and CSS files have been passed through the w3c validation service here https://validator.w3.org/ with any issues corrected.

Javascript files were passed through jshint.com without any significant issues.

Python code was passed through pylint and there are no outstanding issues.

The Javascript on the site does not function on Internet Explorer 11, but considering its overall low usage and the fact that it is being discontinued in 2021, it was deemed not worth spending time on.

---







