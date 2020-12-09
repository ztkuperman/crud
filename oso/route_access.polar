## Route access rules
# URLs accessible to the public
allow(_user, _action, path: String) if
    public_urls := ["/","/static","/signup","/login","/logout", "/static/favicon.ico"] and
    path in public_urls;

# Needed to allow public access to static/* routes.
allow(_user, _action, path: String) if
    path.startswith("/static/");

# Needed to allow access to read/* routes.
allow(_user, _action, path: String) if
    path.startswith("/read/");

# URLs acessible to editors
allow(user: User, _action, path: String) if
    editor_urls := ["/drafts","/update","/publish"] and
    path in editor_urls and
    user.role = "editor";

# URLs accessible to authors only
allow(user: User, _action, path: String) if
    author_urls := ["/create","/tinymce","/trix","/myposts",
        "/publish","/delete","/drafts"] 
    and path in author_urls 
    and user.role = "author";

# URLs acessible to admins
allow(user: User, _action, path: String) if
    admin_urls := ["/admin"] and
    path in admin_urls and
    user.role = "admin";

# Needed to allow access to and update/* routes.
allow(user: User, _action, path: String) if
    user.role = "author"
    and path.startswith("/update/");