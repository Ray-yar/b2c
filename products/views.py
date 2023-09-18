from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.contrib import messages
from .models import Product


class ProductsView(generic.ListView):
    template_name = "index.html"

    model = Product
    object = Product.objects.order_by('created_at')
    paginate_by = 8


class ProductDetail(View):

    def get(self, request, id, *args, **keyargs):
        queryset = Product.objects
        product = get_object_or_404(queryset, id=id)

        return render(
            request, 
            'product_details.html', 
            {
                'product' : product,
            },
        )

    # def post(self, request, id, *args, **keyargs):
    #     queryset = Vehicle.objects.filter(status=1)
    #     vehicle = get_object_or_404(queryset, id=id)

    #     # Check if the review ID is present in the form data
    #     review_id = request.POST.get('id')
    #     if review_id:
    #         # Editing an existing review
    #         review = get_object_or_404(Review, id=review_id)
    #         review_form = ReviewForm(request.POST, instance=review)
    #         messages.success(request, "Review updated successfully.")
    #     else:
    #         # Inserting a new review
    #         review_form = ReviewForm(request.POST)
    #         messages.success(request, "Review inserted successfully, please wait we will publish it after a quick review.")

    #     if review_form.is_valid():
    #         review = review_form.save(commit=False)
    #         review.vcl = vehicle
    #         review.user = request.user
    #         review.save()

    #         # Clear the form after successful submission
    #         review_form = ReviewForm()
    #     else:
    #         # If the form is not valid, display errors and keep the form data
    #         review = None

    #     reviews = vehicle.reviews.filter(approved=True)
    #     return redirect('/'+id +'/')


    # def delete(self, request, id, *args, **kwargs):

    #     review = get_object_or_404(Review, id=id)
    #     if not request.user.is_authenticated or review.user != request.user:
    #         messages.error(request, "You don't have permission to delete this review.")
    #         return HttpResponseBadRequest("You don't have permission to delete this review.")

    #     review.delete()
    #     messages.success(request, "Review deleted successfully.")
    #     return HttpResponse("Review deleted successfully.", status=200)