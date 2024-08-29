from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm ,AppForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import App
from myapp.utils import launch_emulator, start_appium_session, capture_initial_state, click_first_button, capture_new_state, assess_screen_change, save_test_results,record_video, stop_video
from django.shortcuts import redirect
from time import sleep
from django.http import HttpResponseServerError


def home(request):
    return render(request, 'myapp/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('app_list')
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

def app_list(request):
    apps = App.objects.all()
    return render(request, 'myapp/app_list.html', {'apps': apps})

def app_add(request):
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.uploaded_by = request.user
            app.save()
            return redirect('app_list')
    else:
        form = AppForm()
    return render(request, 'myapp/app_form.html', {'form': form})

def app_update(request, pk):
    app = get_object_or_404(App, pk=pk)
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES, instance=app)
        if form.is_valid():
            form.save()
            return redirect('app_list')
    else:
        form = AppForm(instance=app)
    return render(request, 'myapp/app_form.html', {'form': form})


def app_delete(request, pk):
    app = get_object_or_404(App, pk=pk)
    if request.method == 'POST':
        app.delete()
        return redirect('app_list')
    return render(request, 'myapp/app_confirm_delete.html', {'app': app})



def app_run(request, app_id):
    app = get_object_or_404(App, id=app_id)
    
    try:
        # Start the Android Emulator
        launch_emulator("Pixel_8_API_35")
        print("Emulator launching...")

        # Wait for emulator to fully boot
        sleep(20)  # Adjust sleep time as necessary

        # Start the Appium Session
        driver = start_appium_session(app.apk_file.path)
        print("Appium session started successfully")

        # Capture Initial State
        initial_hierarchy = capture_initial_state(driver)
        print("Initial UI state captured")

        # Record Video
        record_video()
        print("Video recording started")

        # Click the First Button and Capture New State
        click_first_button(driver)
        new_hierarchy = capture_new_state(driver)
        print("New UI state captured after button click")

        # Stop Video Recording
        stop_video()
        print("Video recording stopped")

        # Assess Screen Change
        screen_changed = assess_screen_change(initial_hierarchy, new_hierarchy)
        print(f"Screen change detected: {screen_changed}")

        # Save the Test Results
        save_test_results(app, screen_changed, new_hierarchy)
        print("Test results saved successfully")

    except Exception as e:
        print(f"Error occurred during app test run: {str(e)}")
        return HttpResponseServerError("An error occurred during the app test run.")

    finally:
        if 'driver' in locals():
            driver.quit()
            print("Appium driver closed")

    return render(request, 'myapp/app_list.html')
