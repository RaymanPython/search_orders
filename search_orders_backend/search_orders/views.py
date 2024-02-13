from search_orders.models import Profile, Order
from search_orders.serializers import ProfileSerializer, OrderSerializer
from ninja import Router

router = Router()

@router.get("profiles/{user_id}")
def get_profile(request, user_id: int):
    profile = Profile.objects.get(user_id=user_id)
    return ProfileSerializer(profile)

@router.post("profiles")
def create_profile(request, profile: ProfileSerializer):
    profile_instance = Profile.objects.create(user=request.user, category=profile.category)
    return ProfileSerializer(profile_instance)

@router.post("orders")
def create_order(request, order: OrderSerializer):
    order_instance = Order.objects.create(title=order.title, description=order.description, category=order.category)
    return OrderSerializer(order_instance)
    
@router.get("orders")
def get_relevant_orders(request):
    user_category = request.user.profile.category
    relevant_orders = Order.objects.filter(category=user_category)
    return OrderSerializer(relevant_orders, many=True)

@router.post("register")
def register_user(request, user: UserCreateRequest):
    user_instance = User.objects.create_user(user.username, user.email, user.password)
    user_instance.profile.category = user.category
    user_instance.save()
    return UserResponse(user_instance).dict()

@router.post("login")
def user_login(request, username: str, password: str):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return UserResponse(user).dict()