from django.db import models
import uuid
from accounts.models import *
from product.models import *

# Create your models here.

# ------------------ORDER MODEL ------------------------------
OrderStateT = (
    ("Dispatch", "Dispatch"),
    ("Shipment", "Shipment"),
    ("Arrives at", "Arrives at"),
    ("Complete", "Complete"),
)

StateT = (("Pending", "Pending"), ("Accept", "Accept"), ("Decline", "Decline"))


# ORDER BASE CLASS
class BaseOrder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField(default=100)

    # ! this method add ammount value is
    def save(self, *args, **kwargs):
        if not self.pk:  # Check for create
            self.amount = self.product.discount_price * self.quantity
        else:

            self.amount = self.product.discount_price * self.quantity
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True


class AllOrder(BaseOrder):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    status = models.CharField(max_length=100, choices=StateT)


# ! CURRENT ORDER
class CurrentOrder(BaseOrder):
    id = models.UUIDField(
        primary_key=True,
    )
    orderSeller = models.ForeignKey(AllOrder, on_delete=models.CASCADE)
    orderStatus = models.CharField(
        max_length=100,
        choices=OrderStateT,
        default="OrderConfirm",
        null=True,
        blank=True,
    )


# Success ORDER
class SuccessOrder(BaseOrder):
    id = models.UUIDField(
        primary_key=True,
    )
    orderSeller = models.ForeignKey(CurrentOrder, on_delete=models.CASCADE)


# CANCEL ORDER
class CancelOrder(BaseOrder):
    id = models.UUIDField(
        primary_key=True,
    )
    orderSeller = models.ForeignKey(
        AllOrder, on_delete=models.CASCADE, null=True, blank=True
    )
    orderUser = models.ForeignKey(
        CurrentOrder, on_delete=models.CASCADE, null=True, blank=True
    )


# -------------- NOTIFICATIONS -----------------------------


# class NotificationOrder(BaseOrder):
#     sender = models.ForeignKey(
#         to=CustomUser, on_delete=models.CASCADE, related_name="sendernotifororder"
#     )
#     user = models.ForeignKey(
#         to=CustomUser, on_delete=models.CASCADE, related_name="receviernotifororder"
#     )
#     txt = models.CharField(max_length=100, null=True, blank=True)
#     is_seen = models.BooleanField(default=False)


# # ONE NOIFICATION FOR ALL DATA OF USER
# class AllDataNotification(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(
#         to=CustomUser, on_delete=models.CASCADE, related_name="usersnotications"
#     )
#     orderkey = models.ForeignKey(
#         to=AllOrder, on_delete=models.CASCADE, related_name="orderbox"
#     )
#     addresskey = models.ForeignKey(
#         to=Address, on_delete=models.CASCADE, related_name="address"
#     )
