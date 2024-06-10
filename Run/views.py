from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm,ProfileForm,AchievementForm, AchievementSearchForm
from .models import Profile
from .models import Achievement
from django.db.models import Sum, F,Q
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle




def registerUser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')  # Assuming your form uses password1 field
            user.set_password(password)  # Save the hashed password
            user.save()

            # Authenticate the user with the cleaned data
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('loginpage')
    else:
        form = CustomUserCreationForm()


    context = {'form': form}  
    return render(request, 'Run/register.html', context)

def loginUser(request):

    if request.method == 'POST':
        username= request.POST['username']
        password =request.POST['password']

        user = authenticate(request,username=username,password=password) 
    
        if user is not None:
            login(request,user)
            return redirect('dashboard')


    return render(request, 'Run/login.html' )

def logoutUser(request):
    logout(request)
    return redirect('loginpage')


@login_required(login_url='loginpage')
def Dashboard(request):
    achievements = Achievement.objects.filter(user=request.user).order_by('-achievement_date')
    search_form = AchievementSearchForm(request.GET)
    if search_form.is_valid():
        search_query = search_form.cleaned_data['search_query']
        if search_query:
            achievements = achievements.filter(
                Q(achievement_date__icontains=search_query) |
                Q(distance_covered__icontains=search_query) |
                Q(calories_burned__icontains=search_query)
            )

    total_distance = achievements.aggregate(Sum('distance_covered'))['distance_covered__sum'] or 0
    total_runs = achievements.count()
    total_distance = round(total_distance, 2)
    total_calories = achievements.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0

    total_time_seconds = achievements.aggregate(
        total_time_seconds=Sum(
            F('time_hours') * 3600 + F('time_minutes') * 60 + F('time_seconds')
        )
    )['total_time_seconds'] or 0

    # Ensure total_time_seconds is not None
    if total_time_seconds is None:
        total_time_seconds = 0

    total_time_hours = total_time_seconds // 3600
    total_time_minutes = (total_time_seconds % 3600) // 60
    total_time_seconds %= 60

    context = {
        'achievements': achievements,
        'total_distance': total_distance,
        'total_calories': total_calories,
        'total_time_hours': total_time_hours,
        'total_time_minutes': total_time_minutes,
        'total_time_seconds': total_time_seconds,
        'total_runs': total_runs,
        'search_form': search_form,
    }
    return render(request, 'Run/index.html', context)


def create_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'Run/create_profile.html', {'form': form})



@login_required(login_url='loginpage')
def add_achievement(request):
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES)
        if form.is_valid():
            achievement = form.save(commit=False)
            achievement.user = request.user
            achievement.save()
            messages.success(request, 'Achievement  added Successfully.')
            return redirect('dashboard')  # Redirect to dashboard or another page
    else:
        form = AchievementForm()
    return render(request, 'Run/addAchievement.html', {'form': form})



@login_required(login_url='loginpage')
def edit_achievement(request, slug):
    achievement = get_object_or_404(Achievement, slug=slug, user=request.user)
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES, instance=achievement)
        if form.is_valid():
            achievement = form.save(commit=False)
            achievement.slug = slugify(achievement.achievement_date)
            achievement.save()
            return redirect('dashboard')
    else:
        form = AchievementForm(instance=achievement)
    return render(request, 'Run/editAchievement.html', {'form': form})

@login_required(login_url='loginpage')
def all_data(request):
    achievements = Achievement.objects.all()
    achievements = Achievement.objects.filter(user=request.user).order_by('-achievement_date')
    return render(request,'Run/all_data.html',{'achievements':achievements})



def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="achievements.pdf"'

    # Get achievements data
    achievements = Achievement.objects.all()
    achievements = Achievement.objects.filter(user=request.user)

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)
    data = [['Date', 'Distance Covered (km)', 'Time Taken', 'Calories Burned', 'Average Speed (km/hr)']]
    for achievement in achievements:
        data.append([
            achievement.achievement_date,
            achievement.distance_covered,
            f"{achievement.time_hours}h {achievement.time_minutes}m {achievement.time_seconds}s",
            achievement.calories_burned,
            achievement.average_speed
        ])

    # Create table and style
    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Build PDF document
    elements = []
    elements.append(table)
    pdf.build(elements)

    return response

