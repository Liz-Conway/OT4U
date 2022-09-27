from django.views.generic.base import TemplateView
from django.urls.base import reverse
from django.contrib import messages
from django.shortcuts import redirect, render
from home.forms import ContactForm


class HomePage(TemplateView):
    """A class for rendering the home page"""

    template_name = "home/index.html"

    # TemplateView does not need to define get() method


class AboutPage(TemplateView):
    """A class for rendering the home page"""

    template_name = "home/about.html"

    # TemplateView does not need to define get() method


class ContactView(TemplateView):
    """
    Display the Get in Touch page
    """

    template_name = "home/contact.html"

    def get_context_data(self, **kwargs):
        print("In get_context_data()")

        form = ContactForm()
        print(f"form :\n {form}")

        context = {
            "form": form,
        }

        print(f"Context :\n{context}")

        return context

    # def post(self, request, *args, **kwargs):
    #
    #     # Create a new instance of the ContactForm using the POST data.
    #     form = ContactForm(request.POST)
    #
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "Contact enquiry sent successfully")
    #
    #         return redirect(reverse('getInTouch'))
    #     else:
    #         # Attach a generic error message telling the user to check their form
    #         # which will display the errors.
    #         messages.error(
    #             request,
    #             "Failed to log your enquiry.  Please ensure the form is valid.",
    #         )
    #
    #         return render(request, self.template_name, {"form": form})
