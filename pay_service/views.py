import json
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


from .models import Product, Order


stripe.api_key = settings.STRIPE_SECRET_KEY

order = ""
total_sum = 0

class ProductLandingPageView(TemplateView):
    template_name = "pay_service/landing.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Order.objects.filter(title="1a").select_related("product_to_pay")
        order_lst = []
        for i in qs:
            order_lst.append({"title": i.title, "prod": i.product_to_pay.name, "amount": i.amount, "total": i.amount * i.product_to_pay.price})
        global order
        global total_sum
        order = order_lst[0]["title"]
        total_sum = sum([i["total"] for i in order_lst])
        context.update(
            {"order": order, "total": total_sum, "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY}
        )
        return context


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded":

        query = Order.objects.filter(title="1a")
        for i in query:
            i.state = True

        Order.objects.bulk_update(query, ['state'])

        print(f"Thanks for your purchase. Order paid")

    # Passed signature verification
    return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])

            intent = stripe.PaymentIntent.create(
                amount=total_sum,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "order": order
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({ 'error': str(e) })