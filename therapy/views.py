from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from therapy.models import Therapy, Style
from django.contrib import messages
from django.urls.base import resolve
from django.db.models.query_utils import Q
from django.db.models.functions.text import Lower


# Create your views here.
class AllTherapies(TemplateView):
    """A class for rendering a page containing all available therapies"""

    template_name = "therapy/therapies.html"

    # TemplateView does not need to define get() method
    # But here we need to tell the page what Therapies to show so we will
    def get(self, request, *args, **kwargs):
        all_therapies = Therapy.objects.all()
        total_therapies = all_therapies.count()

        # Start as None to ensure we don't get an error
        # when loading the Therapies page without a search term.
        style = None
        sort = None
        direction = None
        sorted_therapies = None
        filter_therapies = None
        query = None

        # Access URL parameters by checking whether request.GET exists
        if request.GET:
            if "sort" in request.GET:
                sortkey = request.GET["sort"]
                sort = sortkey
                if sortkey == "name":
                    # annotate() allows us to add another field to the
                    # dataset returned from the database.
                    # Using the Lower() function on the original "name" field
                    all_therapies = all_therapies.annotate(
                        lower_name=Lower("name")
                    )
                    # The reason for copying the sort parameter
                    # into a new variable called sortkey,
                    # Is because now we've preserved the original field
                    # we want to sort on ("name").
                    # But we have the actual field we're going to sort on,
                    # ("lower_name") in the sort key variable.
                    # If we had just renamed sort itself to "lower_name"
                    # we would have lost the original field ("name")

                    # set the sortKey to lower_name
                    sortkey = "lower_name"

                if sortkey == "category":
                    sortkey = "category__name"

                if "direction" in request.GET:
                    direction = request.GET["direction"]
                    if direction == "desc":
                        # Add a minus in front of the sort key
                        # using string formatting, which reverses the order
                        sortkey = f"-{sortkey}"

                sorted_therapies = all_therapies.order_by(sortkey)
                therapies = sorted_therapies

            # Filter the therapies by the style chosen by the client
            if "style" in request.GET:
                # If the therapies have been sorted already,
                # use the sorted therapies
                if sorted_therapies:
                    filter_on = sorted_therapies
                else:
                    filter_on = all_therapies

                # Retrieve the style from the GET parameter
                selected_style = request.GET["style"]
                # Space not allowed in HTML
                # So replaced with dash
                # Now set it back
                if selected_style == "Self-Care":
                    selected_style = "Self Care"

                # Use the requested style to
                # filter the current query set of all therapies
                # down to only therapies with that style
                filter_therapies = filter_on.filter(style__name=selected_style)
                # Filter a Style objects
                # to that passed in the URL parameter
                style = Style.objects.filter(name=selected_style)

                therapies = filter_therapies

            # Search
            # Since we named the text input in the form "q".
            # We can just check if "q" is in request.get
            if "q" in request.GET:
                # If "q" is a URL parameter
                # set it equal to a variable called query.
                query = request.GET["q"]
                # If the query is blank it's not going to return any results
                if not query:
                    # Use the Django messages framework
                    # to attach an error message to the request
                    messages.warning(
                        self.request,
                        "You didn't enter any search criteria.\
                          Showing all therapies.",
                    )
                    # Redirect back to the therapies URL
                    current_url = resolve(request.path_info).url_name
                    return redirect(current_url)

                # Django can't handle basic database OR logic
                # We want to return results where the query was matched
                # in either the therapy name OR the description
                # In order to accomplish this OR logic, we need to use Q
                # Set a variable equal to a Q object
                #  - Where the "name" contains the query
                #  - OR the "description" contains the query.
                # The pipe generates the OR statement.
                # The "i" in front of "contains"
                # makes the queries case insensitive.
                queries = Q(name__icontains=query) | Q(
                    description__icontains=query
                )

                if filter_therapies:
                    query_on = filter_therapies
                else:
                    query_on = all_therapies

                therapies = query_on.filter(queries)

        else:
            # If there are no GET parameters, return ALL therapies
            therapies = all_therapies

        all_styles = Style.objects.all()

        # If there is no sorting
        # The value of this variable will be the string "None_None".
        current_sorting = f"{sort}_{direction}"

        context = {
            "therapies": therapies,
            "current_sorting": current_sorting,
            "chosen_styles": style,
            "all_styles": all_styles,
            "search_term": query,
            "total": total_therapies,
        }

        return render(request, self.template_name, context)


class SingleTherapy(TemplateView):
    """
    A view to show all details for an individual therapy
    """

    template_name = "therapy/therapy-details.html"

    def get_context_data(self, *args, **kwargs):
        therapy_id = kwargs.get("therapy_id")
        single_therapy = get_object_or_404(Therapy, pk=therapy_id)

        # Call the base implementation first to get a context
        context = super().get_context_data(*args, **kwargs)
        context["therapy"] = single_therapy

        return context
