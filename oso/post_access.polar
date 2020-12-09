## Post access rules
# Read Access
allow(_user, "read", post: Post) if
    post.pub_status = "public";  

allow(user: User, "read", post: Post) if
    (post.pub_status = "draft" and user.role = "editor") or
    post.author = user.name;

# Edit Access
allow(user: User, "edit", post: Post) if
    (post.pub_status = "draft" and user.role = "editor") or
    post.author = user.name;

# Edit Access
allow(user: User, "publish", post: Post) if
    user.role = "editor" or
    post.author = user.name;

# Delete Access
allow(user: User, "delete", post: Post) if
    (post.pub_status = "draft" and user.role = "editor") or
    post.author = user.name;