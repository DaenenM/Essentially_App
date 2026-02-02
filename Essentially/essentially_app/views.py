from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClassSessionForm
from .models import ClassSession
from django.db.models import Sum, Count, Max, Min

def home(request):
    if request.method == "POST":
        form = ClassSessionForm(request.POST)
        
        if form.is_valid():
            # Do not save immediately
            session = form.save(commit=False)

            # Make sure time is an integer (posted from JS hidden input)
            session.time = int(form.cleaned_data.get("time", 0))

            # No need to set average here — use the model property
            session.save()

            return redirect("home")
    else:
        form = ClassSessionForm()

    return render(request, "essentially_app/home.html", {"form": form})


def stats(request):
    sessions = ClassSession.objects.all().order_by("-date")

    totals = sessions.aggregate(
        total_sessions=Count("id"),
        total_time=Sum("time"),
        total_count=Sum("count"),
        max_count=Max("count"),
        min_count=Min("count")
    )

    total_sessions = totals["total_sessions"] or 0
    total_time = totals["total_time"] or 0
    total_count = totals["total_count"] or 0
    total_most = totals["max_count"] or 0
    total_least = totals["min_count"] or 0

    overall_average = total_count / total_time if total_time > 0 else 0

    context = {
        "sessions": sessions,
        "total_sessions": total_sessions,
        "total_time": total_time,
        "total_count": total_count,
        "overall_average": overall_average,
        "total_most": total_most,
        "total_least": total_least,
    }

    return render(request, "essentially_app/stats.html", context)
