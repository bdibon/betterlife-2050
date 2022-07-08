# Betterlike 2050

A REST api built to support a project managemet platform for NGO's.

## Current State

### Models

The main models of the app have been setup: `User`, `Organization`, `Project`.

The `Comment` model should be implemented next, it is a bit trickier because a comment might be a response to a specific project or to another comment, users can indefinitely respond to comments.
The problem is that relational database are not natively good at supporting hierachichal data structures, however there are well known tricks that make it possible and relatively efficient such as the Modified Preorder Tree Traversal (MPTT).

So the main challenge left would be to implement the `Comment` model using a library such as [treebeard](https://github.com/django-treebeard/django-treebeard).

### Permissions

Permissions have been handled at the model level with [dry_rest_pemrissions](https://github.com/dbkaplan/dry-rest-permissions) package, this allows us to control what actions any user is able to perform based on the relations between our different models.

At the moment this has only been implemented for the `Project` model, we should then implement it for the other models.

What field a user can modify is determined by its role on the target ressource, which will determine what serializer to use, thus serializer also serve as permission layers (i.e the `ProjectSerializerAllRights` allows to modify any field, when `ProjectSerializerReadOnly` only allow read operations). This solution has been retained to not clutter our permissions on the model level with field details, `Project` serializers are written, it now has to be done on other resources.

### Authentication

User have to be added by a superuser that will assign them an organization, beside this registration step they are allowed to perform any of the standard account operations (such as password reset).
Then user can retrieve their access and refresh tokens from the API, the access token will be required as a bearer token in any following requests or the server will respond with a `401` code.

We leverage the [dj_rest_auth](https://django-rest-auth.readthedocs.io/en/latest/) that provides endpoints to deal with authentication tasks and [rest_framework_simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) for the JWT authentication backend.

### Bunch of todos

- set up environment variable to check if we are dev/prod
- set up production configuration
- double check how pagination is handled
- finish implementing the permissions on all models
- implement the `Comment` model
