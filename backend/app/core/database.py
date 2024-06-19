"""

Users Table:

    id (Primary Key)
    username
    email
    password
    profile_picture
    bio
    is_admin

Recipes Table:

    id (Primary Key)
    user_id (Foreign Key)
    title
    ingredients
    steps
    category
    photo
    created_at
    updated_at

Ratings Table:

    id (Primary Key)
    recipe_id (Foreign Key)
    user_id (Foreign Key)
    rating

Comments Table:

    id (Primary Key)
    recipe_id (Foreign Key)
    user_id (Foreign Key)
    comment
    created_at

Favorites Table:

    id (Primary Key)
    user_id (Foreign Key)
    recipe_id (Foreign Key)

"""