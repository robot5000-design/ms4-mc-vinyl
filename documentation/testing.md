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

---

As the site owner/administrator:

- I want users to be able to register, login and change password.

As a user:

- I want to be able to register and change my password.

_These requirements have been met by using Django Allauth to help with authentication providing validated forms for users to register, login and change password._

![Register][1]

[1]: ../documentation/images_for_readme/register.jpg "Register"

![Login][2]

[2]: ../documentation/images_for_readme/login.jpg "Login"

![ChangePassword][3]

[3]: ../documentation/images_for_readme/change-password.jpg "Change Password"

As the site owner/administrator:

- I want customers to be able to search and sort products.

As a user:

- I want to be able to search and sort products easily.

_These requirements have been met by allowing users to search and sort products with the easily accessible search input always at the top of a page. Products can be searched by artist, title or genre and can be sorted by price, by rating or alphabetically. They can also be separated by what's on promotion._

![SearchSort][4]

[4]: ../documentation/images_for_readme/search-sort.jpg "Search and Sort"

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

![Wishlist][5]

[5]: ../documentation/images_for_readme/wishlist.jpg "Wishlist Page"

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

_These requirements have been met by providing a user message model and messaging app. Past orders can be seen by the site admin on the All-Orders page and can be searched by user. Messages can be sent by customers and replied to by the site admin. Message threads can be marked open or closed and at a glance the admin can what messages have been replied to. New messages appear in bold font._

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

_These requirements have largly been met by Django's own inbuilt security. In addition, SESSION COOKIE SECURE, SESSION COOKIE AGE, CSRF COOKIE SECURE, SECURE HSTS and SECURE SSL REDIRECT have all been set and added to the settings.py file. A CSP policy would increase security even more as evidenced by the Mozilla Observatory Security Scan shown below. Even without, the site scored well. The @login required decorator is used on functions that require it and in other functions that should only be accessible to site admins a check is performed to see if the user is a superuser. All URL's have been checked to ensure unauthorised users cannot access functions or parts of the database that they should not have access to. Finally all requests from the front-end which would alter the database are performed as POST only requests for some added security, which means the relevant functions cannot be accessed through the url directly._

![SecurityScan][11]

[11]: ../documentation/images_for_readme/security-scan.jpg "Mozilla Observatory Security Scan"

---

## 2. Automated Testing

Although this project was developed using a test driven development approach, it was mostly manual testing of functions and apps as they were developed. Automated testing was carried out at the end with the time that was left. Coverage was used to generate reports showing the percentage of each app tested. These can be seen below. Most views, models and forms have been tested to near 100% in all the apps, with some exceptions in the checkout app.

### **Cart App:**

![CartCoverage][12]

[12]: ../documentation/images_for_readme/cart-coverage.jpg "Cart Test Coverage"

### **Messaging App:**

![MessagingCoverage][13]

[13]: ../documentation/images_for_readme/messaging-coverage.jpg "Messaging Test Coverage"

### **Profiles App:**

![ProfilesCoverage][14]

[14]: ../documentation/images_for_readme/profiles-coverage.jpg "Profiles Test Coverage"

### **Products App:**

![ProductsCoverageTop][15]

[15]: ../documentation/images_for_readme/products-coverage-top.jpg "Products Test Coverage Top"

![ProductsCoverageBottom][16]

[16]: ../documentation/images_for_readme/products-coverage-bottom.jpg "Products Test Coverage Bottom"

### **Wishlist App:**

![WishlistCoverage][17]

[17]: ../documentation/images_for_readme/wishlist-coverage.jpg "Wishlist Test Coverage"

### **Checkout App:**

![CheckoutCoverage][18]

[18]: ../documentation/images_for_readme/checkout-coverage.jpg "Checkout Test Coverage"

---

## 3. Page Responsiveness

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
- iPhone 11 Pro Safari through Browserstack (limited test)
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
- Firefox 89.0
- Google Chrome 89.0.4389.114
- Opera 77.0.4054.277
- Microsoft Edge 91.0.864.48

and tested on a Google Pixel 5:

- Chrome 91.0.4472.164

All HTML and CSS files have been passed through the w3c validation service here https://validator.w3.org/ with any issues corrected.

Javascript files were passed through jshint.com without any significant issues.

Python code was passed through pylint and there are no known significant outstanding issues.

The Javascript on the site does not function on Internet Explorer 11, but considering its overall low usage and the fact that it is being discontinued in 2021, it was deemed not worth spending time on.

Chrome Development Tools Lighthouse after some work, scored the site well, an example of the products page score below. Each page was worked on until the accessibility score was 100 on all and there were no contrast ratio issues. One of the few issues raised was the resolution of the no-image image but it is a free image and is perfectly adequate for the job at hand.

Products Page:

![LighthouseExample][19]

[19]: ../documentation/images_for_readme/lighthouse-products.jpg "Lighthouse Example Score"

Product Detail Page:

![LighthouseExample2][20]

[20]: ../documentation/images_for_readme/lighthouse-product-detail.jpg "Lighthouse Example Score 2"

---

## 4. Final Testing Test Cases on Live Website

The site has been tested on both mobile and desktop for responsiveness and functionality.

Any issues have been cataloged in the Issues section on Github and closed when a sufficient solution was reached. There are no known exisiting issues with the final deployed version. All tests should be started with user not logged in (anonymous user), unless otherwise stated.

- TC01

    Description:

  - Verify Register account, Login and Change Password. All controls are in the Navbar.

    Procedure:

    1. Try to register a new account with a valid email address and verify the account. __PASS__

    2. Try to login to the account. __PASS__

    3. Try changing the password. __PASS__

- TC02

    Description:

  - Verify all navbar and footer links on Index page function as expected which will also confirm that the base template links work.

    Procedure:

    1. Navigate to [Index](https://ms4-mc-vinyl-record-store.herokuapp.com/). Check the navbar logo. It should link to index. __PASS__

    2. Check the navbar menu item links all work as expected. All links in the dropdowns, All Products, Genre, Special Offers. Check the links work in the My Account sub-menu which should show Login and Register only. Check Cart link goes to Cart. Check the Wishlist link goes to Login page. __PASS__

    3. Login and check the user sub-menu in the navbar. My Profile, Change Password and Logout should all link to their relevant pages. Wishlist should now link to the Wishlist page. __PASS__

    4. Login as a Superuser and check the user sub-menu in the navbar. Messaging, All Orders, Add a New Product and Product Tags Admin should all link to their relevant pages. __PASS__

    5. Check the footer links work as expected. Social links should open in a new tab. __PASS__

    6. Test the search input. Try 'rock' which should show albums of the rock genre. Try 'queen' and then try 'deaf', which should result in albums with the word queen and then deaf in the artist name or album title. __PASS__

    7. Click Enter Shop which should link to the products page. __PASS__

- TC03

    Description:

  - Verify links on Products page.

    Procedure:

    1. Navigate to [Products Page](https://ms4-mc-vinyl-record-store.herokuapp.com/products/). Product images should link to Product Detail page. __PASS__

    2. Login as a Superuser. Edit and Delete buttons should now be visible above each product image. Edit should link to the Edit Product page. Delete should call up a modal to confirm delete of the product. __PASS__

    3. Test all options of the sorting dropdown, which sorts by price, rating or artist alphabetically, in either direction. __PASS__

    4. Clicking on a genre tag under any product should show all products of that genre. __PASS__

- TC04

    Description:

  - Verify links on Products Details page.

    Procedure:

    1. Click on any product on the Products page. Test Back button on Product Detail page. Should return to Products page. __PASS__

    2. Clicking on the heart icon as an anonymous user should redirect to the login page. __PASS__

    3. Login as standard user. Clicking on the heart icon should add the product to, or remove the product from, the Wishlist. __PASS__

    4. Clicking on the genre tag should show all products of that genre. __PASS__

    5. The Keep Shopping button should link to the Products page. __PASS__

    6. Trying to add zero quantity to the cart should not work. __PASS__

    7. Try to add any non-zero quantity to the cart to confirm it adds to the cart correctly. A success toast should confirm this as well as the correct cart total under the cart icon. __PASS__

    8. Logout. An anonymous user should be displayed a message to login to make a review. __PASS__

    9. Login as standard user. The review form should now be visible. Make a review. The review should appear at the top. There should be a Edit/Delete button under this review only. __PASS__

    10. Try to edit the review. Confirm the changes. __PASS__

    11. Test all options of the review sort dropdown. __PASS__

    12. Login as Superuser. Edit any review but add an Admin comment to the review to check functionality. __PASS__

    13. Navigate back to a Product Detail page. There should be Edit and Delete product buttons at the top of the page. Edit should link to the Edit Product page. Delete should call up a modal to confirm delete of the product. __PASS__

    14. Scroll down and every review should have a Edit/Delete button under it. __PASS__

    15. Like a review and confirm it counts up by 1 and should no longer be clickable. __PASS__

- TC05

    Description:

  - Verify Cart functionality. Stripe test card credentials: 4242 4242 4242 4242 #242.

    Procedure:

    1. Add a product to the cart. Check that a delivery price is applicable if below the free delivery threshold and vice versa if not. __PASS__

    2. Checkout as an anonymous user using test card credentials. Confirm redirect to checkout success page, success toast and email delivered. __PASS__

    3. Add a product and checkout as a standard logged in user using test card credentials. Do not tick the Save Profile field. Confirm redirect to checkout success page, success toast and email delivered. __PASS__

    4. Confirm the Profile information from step 3 was not saved to the user profile by checking the My Profile page. All fields should be blank. __PASS__

    5. Repeat step 3 but this time tick the Save Profile field. The profile information should be available on the My Profile page after chaeckout. __PASS__

- TC06

    Description:

  - Verify Wishlist functionality.

    Procedure:

    1. Login as a standard user. Add a product to the wishlist. Transfer the product to the cart. __PASS__

    2. Add another product to the wishlist. Use the Add All To Cart button to transfer all of the products to the cart. __PASS__

    3. Logout and login to confirm that the cart details are saved to the user. __PASS__

    4. Login and use the delete button to remove products from the cart. __PASS__

    5. The Keep Shopping button should direct back to the products page. __PASS__

- TC07

    Description:

  - Verify Cart functionality.

    Procedure:

    1. Add products to the cart and navigate to the Cart page. Clicking on any product image should link to the Product Detail page for that product. __PASS__

    2. Confirm Update button updates the product quantity. __PASS__

    3. Confirm Remove button removes the product from the cart. __PASS__

    4. The Keep Shopping button should direct back to the products page. __PASS__

    5. The Secure Checkout button should redirect to the Checkout page. __PASS__

- TC08

    Description:

  - Verify My Profile functionality. TC07 must be completed beforehand.

    Procedure:

    1. Login as standard user and navigate to My Profile page. Click on any order to view detail of the order. Write a test message. Message should now be visible below the order detail. __PASS__
    
    2. Try updating the profile information and confirm the change. __PASS__

    3. The back button should direct back to the last page. __PASS__

- TC09

    Description:

  - Verify Messaging App functionality. TC08 must be completed beforehand.

    Procedure:

    1. Login as a Superuser and navigate to the Messaging page. The message written in TC07 should appear in bold as unread and unreplied. __PASS__

    2. Clicking on Open Threads or Closed Threads should show one or the other. Clicking Refresh should show all messages again. __PASS__

    3. Clicking on the message should direct to the message thread page. The message from TC08 should be visible below the order detail. Write a test reply and the new message should appear and confirm a notification email is sent to the customer eamil address. __PASS__

    4. Clicking Back to Messages button should return to the messaging page where the message should now not be in bold text and should be indicated as replied. __PASS__

    5. Click into the message thread again and mark as Thread Closed. Clicking back to messages should now show the message in the closed thread table. __PASS__

    6. Confirm the admin message also appears in the relevant My Profile/Past Order page. __PASS__

    7. Back on the Messaging page try to delete the message thread. A modal for confirmation should pop up. __PASS__

- TC10

    Description:

  - Verify All Orders page functionality.

    Procedure:

    1. Login as a Superuser and navigate to the All Orders page. All order should appear sorted by most recent. Click on any order and details of that order should be shown. __PASS__

    2. A blank search input should not be accepted. Search for any username or a partial username and results that match the query should be shown. __PASS__

    3. Search for 'no account' and anonymous user orders only should be shown. __PASS__

    4. Reset should show all orders again. __PASS__

- TC11

    Description:

  - Verify Add Product and Edit Product page functionality.

    Procedure:

    1. Login as a Superuser and navigate to the Add Product page. Fill out the details. Confirm Artist, Title, SKU and Price are required. Confirm SKU cannot match another product. __PASS__

    2. Add a product. __PASS__
    
    3. Edit that product. __PASS__

    4. Confirm an invalid image file brings up a toast error showing the error text. __PASS__

    5. Delete that product. __PASS__

    6. Confirm Cancel button returns to the previous page. __PASS__

- TC12

    Description:

  - Verify Product Tags Admin page functionality.

    Procedure:

    1. Login as a Superuser and navigate to the Product Tags Admin page. Confirm spaces not allowed in genre programmatic name by trying to add a new genre. __PASS__

    2. Confirm add a new genre tag. __PASS__

    3. Confirm spaces not allowed in promotion programmatic name by trying to add a new promotion. __PASS__

    4. Confirm add a new promotion tag. __PASS__

    5. Confirm Cancel button returns to last page. __PASS__

- TC13

    Description:

  - Verify 404 error page functionality.

    Procedure:

    1. Type an invalid extension to the site address in the address bar and the 404.html page is shown. __PASS__

- TC14

    Description:

  - Verify 500 error page functionality.

    Procedure:

    1. Raise an unhandled exception in the code and the 500.html page is shown. __PASS__

- TC15

    Description:

  - Verify CSRF error page functionality.

    Procedure:

    1. Insert the following javascript to make the CSRF token invalid. The CSRF error page 403_csrf.html is shown. __PASS__

            $(document).ready(function() {
                csrfInputElement = $( "input[name='csrfmiddlewaretoken']" );
                $(csrfInputElement).val('invalidToken');
            });

---

## 5. Debugging

Although there are no known outstanding bugs, the main problematic bugs were reported in the issues section of Github and are copied below.

1. Overall rating not updating after adding, deleting or updating a review #1.

    _Solved for adding and deleting by implementing signals and solved for updating by calling the save() method rather than using update()._

2. Deleting an item from wishlist not reloading the current page #2.

    _Use JS to send an AJAX request to the backend and JS to reload page whether deleted from wishlist or product detail page._

3. User message not closing as requested after automatically reopening due to new message #3.

    _Solved by ordering messages by date before closing the last message._

4. Wishlist remove in the url address bar gives a front end error as it directs to nowhere #4.

    _Solved by adding an extra variable to the url path which indicates which page the remove from wishlist button was pressed. This removed the need for the javascript ajax post request._

5. Review sort by most likes not working #7.

    _Solved by modifying the model to have a default of zero rather than null._

6. Problem with some order confirmation emails not being sent #8.

    _From Stripe seems to be a problem during the checkout process. Check errors in console on dev server. Solve by removing code that was setting empty optional shipping address details to None. Psycopg2 does not seem to allow null values._

7. Randomising the product order causing duplicates to appear in a search #9.

    _Solved by only randomising the queryset if not a search or sort get request._

8. Messaging page not showing and giving 500 error on deployed site only #10

    _Solved by adding a conditional statement checking if the user profile exists on an order before using it. On the deployed site there are probably messages from orders that have been tampered with or users changed or removed. So this makes the site more robust._

---
