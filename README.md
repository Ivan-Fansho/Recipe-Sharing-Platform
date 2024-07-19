# Recipe-Sharing-Platform
## Description:
The Recipe Sharing Platform is a web application designed to allow users to share their culinary creations and discover new recipes. The platform enables users to create, view, and edit recipes, rate and comment on other users' recipes, and categorize recipes for easy searching. Additionally, users can save their favorite recipes for quick access. Admins will have the ability to manage users and recipe content to ensure the quality and integrity of the platform.

## Features

- **User Management:** Register, login, and manage profiles for all users, including admin functionalities for user oversight.

- **Admin Features:** Approve or block user registrations, manage user interactions, and oversee overall platform activities.

- **Profanity Check:** Automatically detect and filter inappropriate language to maintain a respectful environment.

- **Recipe Creation and Management:** Create, edit, and manage recipes with ease, including uploading and updating recipe details.

- **Commenting and Rating:** Enable users to comment on and rate recipes, facilitating community feedback and interaction.

- **Adding to Favorites:** Allow users to mark recipes as favorites for quick access and personalized recommendations.

- **Search and Pagination:** Implement search functionality to find recipes and paginate results for improved user experience.

- **Email Notification:** Send email notifications when registered successfully.

- **Custom Errors and Error Handling:** Implement custom error messages and robust error handling mechanisms. Use of logger to track, record, and manage errors effectively, ensuring comprehensive visibility into application issues.

## 1. Register User

Registers a new user with the system.

### Request

- **Method:** `POST`
- **Path:** `/users/register`

#### Request Body

- **Content Type:** `application/json`

| Field        | Type   | Description                                                                                                            |
|--------------|--------|------------------------------------------------------------------------------------------------------------------------|
| username     | string | The username of the user (unique identifier).                                                                           |
| email        | string | The email address of the user (unique identifier).                                                                      |
| password     | string | The password for the user's account. (has to be at least 8 and max 20 symbols and should contain capital letter, digit, and special symbol (+, -, *, &, ^, …) |
                                                                                            

### Response

- **Status Code:** `201 Created`
- **Body:** 
  ```json
  {
      "message": "User {username} created successfully."
  }
## 2. User Login

Logs in a user to the system and generates an authentication token.

### Request

- **Method:** `POST`
- **Path:** `/users/login`

#### Request Body

- **Content Type:** `application/x-www-form-urlencoded`

| Field    | Type   | Description                                  |
|----------|--------|----------------------------------------------|
| username | string | The username of the user.                    |
| password | string | The password for the user's account.         |

### Response

- **Status Code:** `200 OK`
- **Body:** 
  ```json
  {
      "message": "Login successful"
  }

## 3. View User Profile

Retrieves the profile information of the current user.

### Request

- **Method:** `GET`
- **Path:** `/users/me`

#### Headers

- **Authorization:** `Bearer <token>`

### Response

- **Status Code:** `200 OK`
- **Body:** 
  ```json
  {
      "id": "user_id",
      "username": "user_username",
      "email": "user_email",
      "bio": "user_bio",
      "profile_pic": "user_profile_picture"
  }
## 4. User Logout

Logs out a user and invalidates the current authentication token.

### Request

- **Method:** `POST`
- **Path:** `/users/logout`

### Response

- **Status Code:** `200 OK`
- **Body:** 
  ```json
  {
      "message": "Logout successful"
  }
## 5. Update User Profile

Updates the profile information of the current user.

### Request

- **Method:** `PUT`
- **Path:** `/users/update`

#### Request Body

- **Content Type:** `application/json`

| Field     | Type   | Description                            |
|-----------|--------|----------------------------------------|
| password  | string | The new password for the user.         |
| email     | string | The new email address of the user.     |
| photo_path| string | The path to the new profile photo.     |
| bio       | string | The new bio of the user.               |

### Response

- **Status Code:** `200 OK`
- **Body:** 
  ```json
  {
      "message": "Profile updated successfully"
  }
## 6. Create Recipe

Creates a new recipe in the system.

### Request

- **Method:** `POST`
- **Path:** `/recipes/create`

#### Request Body

- **Content Type:** `application/json`

| Field       | Type   | Description                                                                                                      |
|-------------|--------|------------------------------------------------------------------------------------------------------------------|
| title        | string | The title of the recipe.                                                                                          |
| ingredients  | string | A list of ingredients required for the recipe.                                                                    |
| steps        | string | The step-by-step instructions for preparing the recipe.                                                           |
| category     | string | The category of the recipe (e.g., pizzas).                                                                       |
| photo        | string | The path to a photo of the recipe.                                                                               |

### Response

- **Status Code:** `201 Created`
- **Body:** 
  ```json
  {
      "message": "New recipe created"
  }
## 7. Update Recipe

Updates an existing recipe in the system.

### Request

- **Method:** `PUT`
- **Path:** `/recipes/update`

#### Request Parameters

- **Query Parameter:**
  - **recipe_id**: `integer` (required) - The ID of the recipe to be updated.

#### Request Body

- **Content Type:** `application/json`

| Field       | Type   | Description                                                                                                      |
|-------------|--------|------------------------------------------------------------------------------------------------------------------|
| title        | string | The updated title of the recipe.                                                                                  |
| ingredients  | string | The updated list of ingredients required for the recipe.                                                          |
| steps        | string | The updated step-by-step instructions for preparing the recipe.                                                     |
| category     | string | The updated category of the recipe (e.g., pizzas).                                                               |
| photo        | string | The updated path to a photo of the recipe.                                                                       |

### Response

- **Status Code:** `201 Created`
- **Body:** 
  ```json
  {
      "message": "Recipe updated"
  }
## 8. Search Recipes

Searches for recipes based on various criteria.

### Request

- **Method:** `GET`
- **Path:** `/recipes/search`

#### Query Parameters

| Parameter  | Type   | Description                                      |
|------------|--------|--------------------------------------------------|
| title      | string | Search for recipes by title.                    |
| category   | string | Search for recipes by category.                 |
| username   | string | Search for recipes by the username of the creator. |
| sort_by    | string | Sort the results by date, either 'asc' (ascending) or 'desc' (descending). |
| page       | integer | The page number for pagination (default is 1).  |
| page_size  | integer | The number of results per page (default is 10). |

### Response

- **Status Code:** `200 OK`
- **Body:** 
  ```json
  {
      "total": 100,
      "page": 1,
      "page_size": 10,
      "results": [
          {
              "id": 1,
              "title": "Peperoni Pizza",
              "ingredients": "Dough, tomato sauce, mozzarella, peperoni",
              "steps": "1. Stretch the dough 2. Put on the tomato sauce 3. Spread the mozzarella 4. Put on the peperoni",
              "category": "Pizzas",
              "photo": "photo.jpeg/photo_path",
              "created_by": "username",
              "created_at": "2024-07-19T12:34:56Z"
          },
          ...
      ]
  }
## 9. View Recipe

Retrieves detailed information about a specific recipe, including its average rating and comments.

### Request

- **Method:** `GET`
- **Path:** `/recipes/view_recipe`

#### Query Parameters

| Parameter | Type   | Description               |
|-----------|--------|---------------------------|
| id        | integer | The ID of the recipe to view. |

### Response

- **Status Code:** `200 OK`
- **Body:** 
  ```json
  {
      "title": "Peperoni Pizza",
      "username": "john_doe",
      "category": "Pizzas",
      "ingredients": "Dough, tomato sauce, mozzarella, peperoni",
      "steps": "1. Stretch the dough 2. Put on the tomato sauce 3. Spread the mozzarella 4. Put on the peperoni",
      "photo": "photo.jpeg/photo_path",
      "avg_rating": "4.50",
      "created_at": "2024-07-19T12:34:56Z",
      "comments": [
          {
              "username": "jane_doe",
              "created_at": "2024-07-19T13:00:00Z",
              "comment": "Delicious pizza! Would definitely make again."
          },
          {
              "username": "chef_mike",
              "created_at": "2024-07-19T14:20:00Z",
              "comment": "Good recipe, but could use more spices."
          }
      ]
  }
## 10. Give Rating

Allows a user to give a rating to a specific recipe.

### Request

- **Method:** `POST`
- **Path:** `/ratings/give`

#### Request Body

- **Content Type:** `application/json`

| Field      | Type   | Description                              |
|------------|--------|------------------------------------------|
| recipe_id  | integer | The ID of the recipe being rated.        |
| rating     | integer | The rating given by the user (1 to 5).   |

#### Example Request Body

```json
{
    "recipe_id": 1,
    "rating": 5
}
```
### Response

- **Status Code:** `201 Created`
- **Body:** 
```json
{
    "message": "Successfully given rating of 5 stars to recipe 1"
}
```
## 11. Add Favorite

Adds a recipe to the user's list of favorites.

### Request

- **Method:** `POST`
- **Path:** `/favorites/add_favorite`

#### Query Parameters

| Parameter  | Type   | Description                      |
|------------|--------|----------------------------------|
| recipe_id  | integer | The ID of the recipe to be added to favorites. Must be greater than 0. |

### Response

- **Status Code:** `201 Created`
- **Body:** 
```json
{
    "message": "Added <recipe_id> to your favorites"
}
```
## 12. Remove Favorite

Removes a recipe from the user's list of favorites.

### Request

- **Method:** `DELETE`
- **Path:** `/favorites/remove_favorite`

#### Query Parameters

| Parameter  | Type   | Description                      |
|------------|--------|----------------------------------|
| recipe_id  | integer | The ID of the recipe to be removed from favorites. Must be greater than 0. |

### Response

- **Status Code:** `200 OK`
- **Body:** 
```json
{
    "message": "Removed <recipe_id> from your favorites"
}
```
## 13. View Favorites

Retrieves a list of recipes that the user has marked as favorites. You can filter and sort the results based on various criteria.

### Request

- **Method:** `GET`
- **Path:** `/favorites/view_favorites`

#### Query Parameters

| Parameter  | Type   | Description                                      |
|------------|--------|--------------------------------------------------|
| title      | string | Search for recipes by title.                    |
| category   | string | Search for recipes by category.                 |
| username   | string | Search for recipes by the username of the creator. |
| sort_by    | string | Sort the results by date, either 'asc' (ascending) or 'desc' (descending). |
| page       | integer | The page number for pagination (default is 1).  |
| page_size  | integer | The number of results per page (default is 10). |

### Response

- **Status Code:** `200 OK`
- **Body:** 
```json
{
    "total": 25,
    "page": 1,
    "page_size": 10,
    "results": [
        {
            "id": 1,
            "title": "Peperoni Pizza",
            "ingredients": "Dough, tomato sauce, mozzarella, peperoni",
            "steps": "1. Stretch the dough 2. Put on the tomato sauce 3. Spread the mozzarella 4. Put on the peperoni",
            "category": "Pizzas",
            "photo": "photo.jpeg/photo_path",
            "created_by": "username",
            "created_at": "2024-07-19T12:34:56Z"
        },
        ...
    ]
}
```
## 14. Create Comment

Allows a user to add a comment to a specific recipe.

### Request

- **Method:** `POST`
- **Path:** `/comments/create`

#### Request Body

- **Content Type:** `application/json`

| Field      | Type   | Description                                   |
|------------|--------|-----------------------------------------------|
| recipe_id  | integer | The ID of the recipe being commented on.      |
| comment    | string  | The text of the comment.                     |

#### Example Request Body

```json
{
    "recipe_id": 1,
    "comment": "This was a very helpful recipe, it turned out very delicious."
}
```
### Response

- **Status Code:** `201 Created`
- **Body:** 
```json
{
    "message": "Comment created"
}
```
## 15. Delete Comment

Allows a user to delete a specific comment they have made on a recipe.

### Request

- **Method:** `DELETE`
- **Path:** `/comments/delete`

#### Query Parameters

| Parameter   | Type   | Description                      |
|-------------|--------|----------------------------------|
| comment_id  | integer | The ID of the comment to be deleted. |

### Response

- **Status Code:** `200 OK`
- **Body:**
```json
{
    "message": "Comment deleted"
}
```
## 16. Admin Get Users

Retrieves a list of users based on various search criteria.

### Request

- **Method:** `GET`
- **Path:** `/admin/users`

#### Query Parameters

| Parameter      | Type    | Description                                               |
|----------------|---------|-----------------------------------------------------------|
| username       | string  | Search for users by username.                            |
| email          | string  | Search for users by email address.                       |
| is_restricted  | string  | Search for users by restriction status ('yes' or 'no').   |
| page           | integer | The page number for pagination (default is 1).           |
| page_size      | integer | The number of results per page (default is 10).          |

### Response

- **Status Code:** `200 OK`
- **Body:** 
```json
{
    "total": 100,
    "page": 1,
    "page_size": 10,
    "results": [
        {
            "id": 1,
            "username": "john_doe",
            "email": "john_doe@example.com",
            "profile_picture": "profile_pic.jpeg",
            "bio": "A short bio about John.",
            "is_restricted": false
        },
        {
            "id": 2,
            "username": "jane_doe",
            "email": "jane_doe@example.com",
            "profile_picture": null,
            "bio": "A short bio about Jane.",
            "is_restricted": true
        },
        ...
    ]
}
```
## 17. Restrict User

Allows an admin to restrict or unrestrict a user.

### Request

- **Method:** `PUT`
- **Path:** `/admin/restrict`

#### Query Parameters

| Parameter    | Type    | Description                                  |
|--------------|---------|----------------------------------------------|
| user_id      | integer | The ID of the user to restrict or unrestrict. |
| restriction  | string  | The restriction action ('block' or 'unblock'). |

### Response

- **Status Code:** `200 OK`
- **Body:**
```json
{
    "message": "User: 1 was blocked"
}
```
## 18. Get Comments

Retrieves comments based on user ID, recipe ID, and pagination.

### Request

- **Method:** `GET`
- **Path:** `/admin/comments`

#### Query Parameters

| Parameter   | Type    | Description                                   |
|-------------|---------|-----------------------------------------------|
| user_id     | integer | Filter comments by user ID (optional).        |
| recipe_id   | integer | Filter comments by recipe ID (optional).      |
| page        | integer | The page number for pagination (default is 1). |
| page_size   | integer | The number of results per page (default is 10). |

### Response

- **Status Code:** `200 OK`
- **Body:**
```json
{
     "total_results": 50,
    "page": 1,
    "page_size": 10,
    "results": [
        {
            "id": 1,
            "recipe_id": 1,
            "username": "john_doe",
            "comment": "Delicious recipe!",
            "created_at": "2024-07-19T12:34:56Z"
        },
        {
            "id": 2,
            "recipe_id": 1,
            "username": "jane_doe",
            "comment": "I loved it!",
            "created_at": "2024-07-19T13:45:00Z"
        }
    ]
}
```
## 19. Delete Comment

Deletes a specific comment by its ID.

### Request

- **Method:** `DELETE`
- **Path:** `/admin/comments`

#### Query Parameters

| Parameter  | Type    | Description                 |
|------------|---------|-----------------------------|
| comment_id | integer | The ID of the comment to delete. |

### Response

- **Status Code:** `200 OK`
- **Body:**
```json
{
"message": "Comment: 1 was deleted"
}
```